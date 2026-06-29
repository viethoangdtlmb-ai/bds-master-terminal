      // ── Portfolio-Level Alerts ────────────────────────────────────────────

      // Tính toán tổng danh mục
      const totalDebt   = calcs.reduce((s, {c}) => s + (c.autoDebt > 0 ? c.autoDebt / 1000 : 0), 0);
      const totalMarket = calcs.reduce((s, {a}) => s + (a.market || 0), 0);
      const totalCF     = calcs.reduce((s, {c}) => s + (c.cashflow || 0), 0);
      const avgHealth   = calcs.length > 0 ? calcs.reduce((s, {c}) => s + c.health, 0) / calcs.length : 100;

      // 1. LTV Danh Mục
      if (totalMarket > 0) {
        const ltvPct = totalDebt / totalMarket * 100;
        if (ltvPct > 60)
          alerts.push({ type: 'danger', icon: '🏦', msg: `<strong>LTV Danh Mục: ${ltvPct.toFixed(0)}%</strong> — Tổng dư nợ ${totalDebt.toFixed(1)} Tỷ / Tổng giá trị ${totalMarket.toFixed(1)} Tỷ. Rủi ro đòn bẩy cao.` });
        else if (ltvPct > 45)
          alerts.push({ type: 'warn', icon: '🏦', msg: `LTV Danh Mục: ${ltvPct.toFixed(0)}% — Đòn bẩy mức trung bình (${totalDebt.toFixed(1)}T/${totalMarket.toFixed(1)}T). Theo dõi khi lãi thả nổi.` });
      }

      // 2. Dòng Tiền Ròng Tổng
      if (totalCF < -50)
        alerts.push({ type: 'danger', icon: '🩸', msg: `<strong>Dòng tiền ròng: ${totalCF.toFixed(0)} Tr/tháng</strong> — Danh mục đang đốt tiền nặng. Cần tái cơ cấu ngay.` });
      else if (totalCF < 0)
        alerts.push({ type: 'warn', icon: '🩸', msg: `Dòng tiền ròng: ${totalCF.toFixed(0)} Tr/tháng — Portfolio Âm nhẹ. Tối ưu bằng cách bổ sung tài sản Pha 3.` });

      // 3. Tỷ lệ tài sản không sinh tiền
      const nonIncome = calcs.filter(({a}) => a.rentstatus === 'trong' || a.rentstatus === 'chua-ban-giao');
      if (calcs.length > 0 && nonIncome.length / calcs.length > 0.5)
        alerts.push({ type: 'warn', icon: '🏚️', msg: `<strong>${nonIncome.length}/${calcs.length} tài sản không sinh tiền</strong> (${(nonIncome.length/calcs.length*100).toFixed(0)}%) — Gánh nặng chi phí cơ hội cao.` });

      // 4. Concentration Risk (1 tài sản > 50% giá trị)
      if (totalMarket > 0) {
        calcs.forEach(({a}) => {
          const pct = a.market / totalMarket * 100;
          if (pct > 50)
            alerts.push({ type: 'warn', icon: '⚠️', msg: `<strong>Concentration Risk:</strong> "${a.name}" chiếm <strong>${pct.toFixed(0)}%</strong> giá trị danh mục — Đa dạng hóa để giảm rủi ro.` });
        });
      }

      // 5. Tập trung địa lý (>= 2 tài sản cùng quận)
      const distCount = {};
      calcs.forEach(({a}) => { if (a.district) distCount[a.district] = (distCount[a.district] || 0) + 1; });
      Object.entries(distCount).forEach(([dist, cnt]) => {
        if (cnt >= 2)
          alerts.push({ type: 'warn', icon: '🗺️', msg: `Tập trung địa lý: <strong>${cnt} tài sản</strong> ở <strong>${dist}</strong> — Rủi ro nếu thị trường khu vực này điều chỉnh.` });
      });

      // 6. Thiếu tài sản Pha 3 (dòng tiền)
      if (calcs.length > 0 && calcs.filter(({c}) => c.phase === 3).length === 0)
        alerts.push({ type: 'warn', icon: '💧', msg: `<strong>Thiếu Pha 3:</strong> Không có tài sản dòng tiền. Danh mục phụ thuộc hoàn toàn vào tăng giá — cần ít nhất 1 tài sản cho thuê ổn định.` });

      // 7. Cluster ân hạn (>= 2 tài sản hết ân hạn trong 3 tháng)
      const graceCluster = calcs.filter(({a}) => (a.grace || 0) > 0 && (a.grace || 0) <= 3);
      if (graceCluster.length >= 2)
        alerts.push({ type: 'danger', icon: '💥', msg: `<strong>Cú sốc ân hạn đồng loạt:</strong> ${graceCluster.length} tài sản (${graceCluster.map(({a}) => a.name).join(', ')}) cùng hết ân hạn trong ≤3 tháng — Dòng tiền ra tăng đột biến.` });

      // 8. Health Score trung bình danh mục
      if (avgHealth < 45)
        alerts.push({ type: 'danger', icon: '💊', msg: `<strong>Health Score TB: ${avgHealth.toFixed(0)}/100</strong> — Danh mục ở trạng thái yếu toàn diện. Ưu tiên can thiệp.` });
      else if (avgHealth < 60)
        alerts.push({ type: 'warn', icon: '💊', msg: `Health Score TB: ${avgHealth.toFixed(0)}/100 — Danh mục cần theo dõi và tối ưu dần.` });

