// ── Tab Switcher ──────────────────────────────────────────────



    function switchTab(id) {



      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));



      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));



      document.getElementById('tab-' + id).classList.add('active');



      document.querySelector('[data-tab="' + id + '"]').classList.add('active');



      // Auto-render hooks



      const _p = window.SESSION_PORTFOLIO || PORTFOLIO;



      if (id === 'diagnosis' && _p && _p.length > 0) {



        setTimeout(() => { if (typeof renderDiagnosis === 'function') renderDiagnosis(_p); }, 10);



      }



      if (id === 'surgery' && _p) {



        setTimeout(() => { if (typeof openSimulator === 'function') openSimulator(_p); }, 10);



      }



    }







    // ── Session Reset ─────────────────────────────────────────────



    function newSession() {



      if (confirm('Bắt đầu buổi khám mới? Dữ liệu hiện tại sẽ được xóa.')) {



        localStorage.removeItem('aa_session');



        clearForm();



        switchTab('triage');



      }



    }







    // ── Market Data ───────────────────────────────────────────────



    async function loadMarketData() {



      try {



        const res = await fetch('data.json');



        if (!res.ok) throw new Error();



        const fetched = await res.json();



        // Only overwrite if fetched is newer



        if (!window.MARKET_DATA || fetched.updated !== window.MARKET_DATA.updated)



          window.MARKET_DATA = fetched;



      } catch {



        // fallback: use embedded MARKET_DATA (already set above)



      }



      const md = window.MARKET_DATA;



      const stamp = document.getElementById('stamp-text');



      if (md) {



        stamp.textContent = `📡 Cập nhật: ${md.updated} · ${md.districts.length} khu vực`;



        populateDistrictDropdowns();



      } else {



        stamp.textContent = '⚠️ Chưa có data — chạy auto_crawl_daily.bat';



        stamp.style.color = '#F59E0B';



      }



    }







    // ── Districts Dropdown ────────────────────────────────────────



    function populateDistrictDropdowns() {



      const md = window.MARKET_DATA;



      if (!md) return;



      const sorted = [...md.districts].sort((a, b) => a.name.localeCompare(b.name, 'vi'));



      ['f-district', 'qs-district'].forEach(id => {



        const sel = document.getElementById(id);



        if (!sel) return;



        sorted.forEach(d => {



          const opt = document.createElement('option');



          opt.value = d.name;



          opt.textContent = `${d.name} — Cycle ${d.cycle} | Nhà: ${d.gia} tr/m²${d.gia_cc != null ? ' | CC: ' + d.gia_cc + ' tr/m²' : ' | CC: N/A'}`;



          sel.appendChild(opt);



        });



      });



    }







    // ── Quick Scan ────────────────────────────────────────────────



    function toggleQuickScan() {



      const form = document.getElementById('qs-form');



      const btn = document.getElementById('qs-toggle');



      const open = form.style.display === 'none';



      form.style.display = open ? 'block' : 'none';



      btn.textContent = open ? '▲ Đóng' : '▼ Mở Quick Scan';



    }







    function runQuickScan() {



      const district = document.getElementById('qs-district').value;



      const buyPrice = parseFloat(document.getElementById('qs-buy').value) || 0;



      const nowPrice = parseFloat(document.getElementById('qs-now').value) || 0;



      const loanPct = parseFloat(document.getElementById('qs-loan').value) || 0;



      const buyYear = parseInt(document.getElementById('qs-year').value) || (new Date().getFullYear() - 2);







      if (!buyPrice || !nowPrice) { alert('Vui lòng nhập giá mua và giá hiện tại.'); return; }







      const years = Math.max(0.5, new Date().getFullYear() - buyYear);



      const gainPct = (nowPrice - buyPrice) / buyPrice * 100;



      const equity = buyPrice * (1 - loanPct / 100);



      const roeAnn = equity > 0 ? (gainPct / years) * (buyPrice / equity) : 0;



      const md = window.MARKET_DATA;



      const distData = md ? md.districts.find(d => d.name === district) : null;



      const cycle = distData ? distData.cycle : null;



      const viewsTin = distData ? distData.views_tin : null;







      let health = 50;



      if (gainPct > 30) health += 20;



      else if (gainPct > 15) health += 10;



      else if (gainPct < 0) health -= 20;



      if (roeAnn > 18) health += 10;



      else if (roeAnn < 4 && loanPct > 0) health -= 10;



      if (cycle && cycle > 70) health += 10;



      if (cycle && cycle < 35) health -= 15;



      if (viewsTin && viewsTin < 3) health -= 10;



      health = Math.max(10, Math.min(95, health));







      const color = health >= 70 ? 'var(--emerald)' : health >= 45 ? 'var(--yellow)' : 'var(--red)';



      const icon = health >= 70 ? '🟢' : health >= 45 ? '🟡' : '🔴';







      const res = document.getElementById('qs-result');



      res.style.display = 'flex';



      res.style.gap = '12px';



      res.style.alignItems = 'center';



      res.style.flexWrap = 'wrap';



      const qsResetBtn = document.getElementById('qs-reset-btn');



      if (qsResetBtn) qsResetBtn.style.display = 'inline-flex';



      res.innerHTML = `



    <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:${color}">${icon} ${health}/100</div>



    <div style="font-size:12px;color:var(--text-2)">



      Lãi vốn: <strong style="color:${gainPct >= 0 ? 'var(--emerald)' : 'var(--red)'}">${gainPct >= 0 ? '+' : ''}${gainPct.toFixed(1)}%</strong>



      &nbsp;|&nbsp; ROE/vốn: <strong style="color:${roeAnn >= 18 ? 'var(--emerald)' : roeAnn >= 8 ? 'var(--yellow)' : 'var(--red)'}">${roeAnn.toFixed(1)}%/năm</strong>



      ${cycle ? `&nbsp;|&nbsp; Cycle: <strong>${cycle}/100</strong>` : ''}



      ${viewsTin ? `&nbsp;|&nbsp; Views/Tin: <strong>${viewsTin}</strong>` : ''}



    </div>



    <button class="btn btn-secondary btn-sm" onclick="switchTab('triage');toggleQuickScan()">→ Khám đầy đủ</button>



  `;



    }



    function showToast(msg, duration) {



      const t = document.getElementById('toast-notify');



      if (!t) return;



      t.textContent = msg;



      t.classList.add('show');



      clearTimeout(t._timer);



      t._timer = setTimeout(() => t.classList.remove('show'), duration || 2000);



    }







    function resetQuickScan() {



      ['qs-district', 'qs-buy', 'qs-now', 'qs-loan', 'qs-year'].forEach(id => {



        const el = document.getElementById(id);



        if (el) el.value = '';



      });



      const res = document.getElementById('qs-result');



      if (res) { res.innerHTML = ''; res.style.display = 'none'; }



      const btn = document.getElementById('qs-reset-btn');



      if (btn) btn.style.display = 'none';



    }







    // ── Loan Branch ───────────────────────────────────────────────



    function onLoanPctChange(val) {



      const bank = document.getElementById('group-bank');



      const notice = document.getElementById('no-loan-notice');



      const v = parseFloat(val) || 0;



      // We keep bank form visible always; just show/hide no-loan notice



      notice.style.display = (v === 0) ? 'block' : 'none';



    }







    // ── Rent Status Branch ────────────────────────────────────────



    function onRentStatusChange(val) {



      const row = document.getElementById('rent-income-row');



      row.style.display = (val === 'trong' || val === 'tu-dung' || val === 'chua-ban-giao') ? 'none' : '';



      if (val !== 'dang-thue') document.getElementById('f-rent').value = '';



      const note = document.getElementById('chua-ban-giao-note');



      if (note) note.style.display = val === 'chua-ban-giao' ? 'block' : 'none';



    }







    // ── Templates ─────────────────────────────────────────────────



    const TEMPLATES = {
      chungcu: { name: 'Chung Cư Tiết Kiệm', type: 'chung-cu', district: 'Hà Đông', area: 68, year: 2020, cost: 3.2, market: 3.8, goal: 'cho-thue', loanpct: 70, debt: 1.8, rate: 7.5, prefmonths: 2, floatrate: 12.5, grace: 0, loanterm: 20, rentstatus: 'dang-thue', rent: 12, mgmt: 2, maint: 8, delivery: 0, rentExpected: 0 },
      shophouse: { name: 'Shophouse Làng Vân', type: 'shophouse', district: 'Hoài Đức', area: 80, year: 2022, cost: 9, market: 8.5, goal: 'cho-thue', loanpct: 60, debt: 4.8, rate: 8.5, prefmonths: 6, floatrate: 13, grace: 8, loanterm: 18, rentstatus: 'dang-thue', rent: 20, mgmt: 3.5, maint: 15, delivery: 0, rentExpected: 0 },
      bietthu: { name: 'Biệt Thự Vườn', type: 'biet-thu', district: 'Nam Từ Liêm', area: 200, year: 2019, cost: 15, market: 22, goal: 'tu-o', loanpct: 50, debt: 5, rate: 8.0, prefmonths: 0, floatrate: 13, grace: 0, loanterm: 15, rentstatus: 'trong', rent: 0, mgmt: 5, maint: 20, delivery: 0, rentExpected: 0 },
      datnen: { name: 'Đất Nền Bắc Quốc Oai', type: 'dat-nen', district: 'Thạch Thất', area: 120, year: 2021, cost: 3.5, market: 3.2, goal: 'tang-gia', loanpct: 50, debt: 1.5, rate: 9, prefmonths: 3, floatrate: 13.5, grace: 0, loanterm: 15, rentstatus: 'trong', rent: 0, mgmt: 0, maint: 5, delivery: 0, rentExpected: 0 },
      nghiduong: { name: 'Villa Biển Nghỉ Dưỡng', type: 'biet-thu', district: '', area: 250, year: 2018, cost: 12, market: 11, goal: 'cho-thue', loanpct: 60, debt: 6, rate: 8.5, prefmonths: 0, floatrate: 14, grace: 0, loanterm: 10, rentstatus: 'dang-thue', rent: 35, mgmt: 12, maint: 30, delivery: 0, rentExpected: 0 },
      vanphong: { name: 'Sàn Văn Phòng HH', type: 'nha-rieng', district: 'Cầu Giấy', area: 150, year: 2016, cost: 8, market: 10, goal: 'cho-thue', loanpct: 40, debt: 1.5, rate: 9, prefmonths: 0, floatrate: 12.5, grace: 0, loanterm: 10, rentstatus: 'dang-thue', rent: 45, mgmt: 8, maint: 15, delivery: 0, rentExpected: 0 }
    };







    function loadTemplate(key, ev) {



      const t = TEMPLATES[key];



      if (!t) return;



      const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };



      set('f-name', t.name); set('f-type', t.type);



      set('f-district', t.district); set('f-area', t.area);



      set('f-year', t.year); set('f-cost', t.cost);



      set('f-market', t.market); set('f-goal', t.goal);



      set('f-loanpct', t.loanpct); set('f-debt', t.debt);



      set('f-rate', t.rate); set('f-prefmonths', t.prefmonths);



      set('f-floatrate', t.floatrate); set('f-grace', t.grace);



      set('f-loanterm', t.loanterm); set('f-rentstatus', t.rentstatus);



      set('f-rent', t.rent); set('f-mgmt', t.mgmt); set('f-maint', t.maint);



      set('f-delivery', t.delivery || ''); set('f-rent-expected', t.rentExpected || '');



      onLoanPctChange(t.loanpct);



      onRentStatusChange(t.rentstatus);



      // Flash feedback



      document.querySelectorAll('#templates-row .btn').forEach(b => b.classList.remove('btn-primary'));



      if (ev && ev.target) { ev.target.classList.add('btn-primary'); setTimeout(() => ev.target.classList.remove('btn-primary'), 1500); }



      showToast('✅ Đã tải mẫu: ' + t.name, 2000);



    }







    // ── Asset Portfolio Management ────────────────────────────────



    let PORTFOLIO = [];







    const TYPE_LABEL = { 'nha-rieng': 'Nhà riêng', 'shophouse': 'Shophouse', 'chung-cu': 'Chung cư', 'dat-nen': 'Đất nền', 'biet-thu': 'Biệt thự' };



    const GOAL_LABEL = { 'cho-thue': 'Cho thuê', 'tang-gia': 'Tăng giá', 'tu-o': 'Tự ở', 'tich-san': 'Tích sản (Pha 4)' };







    function addToPortfolio() {



      const d = getFormData();



      if (!d.cost || !d.market) {



        alert('Vui lòng nhập ít nhất Giá Vốn và Giá Hiện Tại.');



        return;



      }



      if (!d.name) d.name = `Tài sản ${PORTFOLIO.length + 1}`;



      d._id = Date.now();



      PORTFOLIO.push(d);



      savePortfolio();



      renderAssetList();



      showToast('\u2705 \u0110\u00e3 th\u00eam: ' + d.name, 2500);



      clearForm();



    }







    function removeAsset(id) {



      PORTFOLIO = PORTFOLIO.filter(a => a._id !== id);



      savePortfolio();



      renderAssetList();



    }







    function editAsset(id) {



      const idx = PORTFOLIO.findIndex(a => a._id === id);



      if (idx < 0) return;



      const d = PORTFOLIO[idx];



      // Fill form with asset data



      const set = (fid, val) => { const el = document.getElementById(fid); if (el) el.value = val ?? ''; };



      ['name', 'type', 'district', 'area', 'year', 'cost', 'market', 'goal',



        'loanpct', 'debt', 'rate', 'prefmonths', 'floatrate', 'grace', 'loanterm',



        'rentstatus', 'rent', 'mgmt', 'maint'].forEach(k => set('f-' + k, d[k]));



      onLoanPctChange(d.loanpct || 0);



      onRentStatusChange(d.rentstatus || 'dang-thue');



      // Remove from list (re-add after edit)



      PORTFOLIO.splice(idx, 1);



      savePortfolio();



      renderAssetList();



      document.getElementById('main-form').scrollIntoView({ behavior: 'smooth' });



    }








    // === GLOBAL: generateAssetCardHTML ===
    // Dung chung cho Triage va Chan Doan
    function generateAssetCardHTML(a, i, isReadOnly = false) {

      const PHASE_META = {
        1: { label: 'Pha 1 — Chính Sách', color: '#3B82F6', bg: 'rgba(59,130,246,.12)' },
        2: { label: 'Pha 2 — Di Dân', color: '#EAB308', bg: 'rgba(234,179,8,.12)' },
        3: { label: 'Pha 3 — Dòng Tiền', color: '#10B981', bg: 'rgba(16,185,129,.12)' },
        4: { label: 'Pha 4 — Tích Sản', color: '#A855F7', bg: 'rgba(168,85,247,.12)' },
      };

      const gain = a.market && a.cost ? ((a.market - a.cost) / a.cost * 100) : 0;



      const gainColor = gain >= 0 ? 'var(--emerald)' : 'var(--red)';



      const gainSign = gain >= 0 ? '+' : '';



      const c_q = calcAsset(a);



      const phMeta = PHASE_META[c_q.phase] || PHASE_META[2];



      const phaseBadge = `<span style="display:inline-flex;align-items:center;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700;background:${phMeta.bg};color:${phMeta.color};border:1px solid ${phMeta.color}33;white-space:nowrap">${phMeta.label}</span>`;



      const dscr = c_q.dscr !== null ? c_q.dscr.toFixed(2) : 'N/A';



      const dscrColor = dscr === 'N/A' ? 'var(--text-2)' : (parseFloat(dscr) < 0.3 ? 'var(--red)' : parseFloat(dscr) < 0.8 ? 'var(--yellow)' : 'var(--emerald)');



      const distData = window.MARKET_DATA?.districts.find(d => d.name === a.district);



      const cycle = distData ? distData.cycle : '?';



      const cycleColor = cycle === '?' ? 'var(--text-2)' : (cycle > 70 ? 'var(--red)' : cycle > 50 ? 'var(--yellow)' : 'var(--emerald)');







      return `



    <div class="card card-sm" style="margin-bottom:10px;display:flex;align-items:center;gap:16px;flex-wrap:wrap">



      <div style="min-width:28px;width:28px;height:28px;background:var(--gold-dim);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--gold);flex-shrink:0">${i + 1}</div>



      <div style="flex:1;min-width:180px">



        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px">



          <span style="font-weight:600;font-size:13px">${a.name}</span>



          ${phaseBadge}



        </div>



        <div style="font-size:11px;color:var(--text-2)">${TYPE_LABEL[a.type] || a.type} · ${a.district || 'Chưa chọn'} · Mua: T${a.month || 1}/${a.year || new Date().getFullYear()} · ${GOAL_LABEL[a.goal] || a.goal}</div>

      </div>



      ${isReadOnly ? `
      <!-- isReadOnly: [Row1+Row2 LEFT] | [HEALTH RIGHT] + Row3 full-width -->
      <div style="width:100%;margin-top:10px;padding-top:10px;border-top:1px solid var(--bg-border);display:flex;gap:12px;align-items:stretch">

        <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:8px">

          <!-- Row 1: Kế Toán -->
          <div style="display:flex;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px">
            <div>
              <div style="color:var(--text-3);font-size:10px">GIÁ VỐN</div>
              <div>${a.cost} Tỷ</div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="Vốn thực bỏ ra lúc mua">VỐN TỰ CÓ</div>
              <div><strong style="color:var(--text-1)">${(a.cost * (1 - (a.loanpct || 0) / 100)).toFixed(2)}</strong> <span style="font-size:10px;color:var(--text-3)">Tỷ</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="Gốc NH đã trả được">GỐC ĐÃ TRẢ</div>
              <div><strong style="color:var(--emerald)">${Math.max(0, a.cost * (a.loanpct || 0) / 100 - (c_q.autoDebt / 1000)).toFixed(2)}</strong> <span style="font-size:10px;color:var(--text-3)">Tỷ</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="Dư nợ gốc còn lại">DƯ NỢ</div>
              <div><strong style="color:${c_q.autoDebt > 0 ? 'var(--yellow)' : 'var(--text-1)'}">${c_q.autoDebt > 0 ? (c_q.autoDebt / 1000).toFixed(2) : '0'}</strong> <span style="font-size:10px;color:var(--text-3)">Tỷ</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="Lãi NH luỹ kế đã đóng">LÃI ĐÃ ĐÓNG</div>
              <div><strong style="color:var(--red)">${(c_q.interestPaid || 0).toFixed(2)}</strong> <span style="font-size:10px;color:var(--text-3)">Tỷ</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="Giá bán tối thiểu để hòa vốn">GIÁ SÀN</div>
              <div style="color:${a.market >= c_q.floorPrice ? 'var(--emerald)' : 'var(--red)'}">${c_q.floorPrice.toFixed(2)} Tỷ${a.market >= c_q.floorPrice ? ' ✅' : ' 🔴'}</div>
            </div>
          </div>

          <!-- Row 2: Phân Tích -->
          <div style="display:flex;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;padding-top:8px;border-top:1px solid var(--bg-border)">
            <div>
              <div style="color:var(--text-3);font-size:10px">GIÁ HIỆN TẠI</div>
              <div style="color:var(--text-1);font-weight:600">${a.market} Tỷ</div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">ĐƠN GIÁ</div>
              <div><strong style="color:var(--text-1)">${c_q.unitPrice > 0 ? c_q.unitPrice.toFixed(1) : '?'}</strong> <span style="font-size:10px;color:var(--text-3)">Tr/m²</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">LÃI VỐN</div>
              <div style="color:${gainColor}">${gainSign}${gain.toFixed(1)}%</div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="ROE Toàn Khóa">ROE NGẦM</div>
              <div><strong style="color:${c_q.roeTotal >= 0 ? 'var(--emerald)' : 'var(--red)'}">${c_q.roeTotal.toFixed(1)}%</strong></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="ROE trung bình mỗi năm">ROE/NĂM</div>
              <div><strong style="color:${c_q.roeAnnual >= 15 ? 'var(--emerald)' : c_q.roeAnnual >= 8 ? 'var(--yellow)' : 'var(--red)'}">${c_q.roeAnnual.toFixed(1)}%</strong></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">DÒNG TIỀN</div>
              <div><strong style="color:${c_q.cashflow >= 0 ? 'var(--emerald)' : 'var(--red)'}">${c_q.cashflow > 0 ? '+' : ''}${c_q.cashflow.toFixed(1)}</strong> <span style="font-size:10px;color:var(--text-3)">Tr</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">DSCR</div>
              <div style="color:${dscrColor}">${dscr}</div>
            </div>
          </div>

        </div>

        <!-- HEALTH column — spans Row 1 + Row 2 -->
        <div style="min-width:70px;width:70px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:${c_q.health >= 65 ? 'rgba(16,185,129,.08)' : c_q.health >= 40 ? 'rgba(234,179,8,.08)' : 'rgba(239,68,68,.08)'};border:1px solid ${c_q.health >= 65 ? 'rgba(16,185,129,.25)' : c_q.health >= 40 ? 'rgba(234,179,8,.25)' : 'rgba(239,68,68,.25)'};border-radius:8px;padding:10px 6px;text-align:center">
          <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px">Health</div>
          <div style="font-size:26px;font-weight:800;font-family:var(--mono);color:${c_q.health >= 65 ? 'var(--emerald)' : c_q.health >= 40 ? 'var(--yellow)' : 'var(--red)'};line-height:1">${c_q.health}</div>
          <div style="font-size:9px;color:var(--text-3)">/100</div>
          <div style="font-size:13px;margin-top:4px">${c_q.health >= 70 ? '🟢' : c_q.health >= 45 ? '🟡' : '🔴'}</div>
        </div>

      </div>

      <!-- Row 3: Verdict — full width -->
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:8px;padding-top:7px;border-top:1px solid var(--bg-border)">
        <span class="badge ${assetVerdict(a, c_q).cls}" style="font-size:10px;padding:3px 10px">${assetVerdict(a, c_q).label}</span>
        ${c_q.deliveryNote ? `<span style="font-size:11px;color:var(--gold);background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);padding:2px 8px;border-radius:4px">⏳ ${c_q.deliveryNote}</span>` : ''}
        ${(a.grace || 0) > 0 ? `<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">💣 Ân hạn gốc còn <strong>${a.grace} tháng</strong></span>` : ''}
        ${(a.prefmonths || 0) > 0 && (a.prefmonths || 0) <= 6 ? `<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">⚡ Ưu đãi hết trong <strong>${a.prefmonths} tháng</strong></span>` : ''}
        ${c_q.phaseWarning ? `<span style="font-size:11px;color:var(--text-2);background:rgba(100,116,139,0.08);border:1px solid rgba(100,116,139,0.25);padding:2px 8px;border-radius:4px">⚠️ ${c_q.phaseWarning}</span>` : ''}
        ${parseFloat(dscr) < 0.3 && dscr !== 'N/A' ? `<span style="font-size:11px;color:var(--red);background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);padding:2px 8px;border-radius:4px">🚨 DSCR=${dscr} — Dòng tiền sắp đứt gãy</span>` : ''}
      </div>
      ` : `
      <div style="display:flex;gap:20px;flex-wrap:wrap;font-family:var(--mono);font-size:12px">
        <div>
          <div style="color:var(--text-3);font-size:10px">GIÁ VỐN</div>
          <div>${a.cost} Tỷ</div>
        </div>
        <div>
          <div style="color:var(--text-3);font-size:10px">GIÁ HIỆN TẠI</div>
          <div style="color:var(--text-1);font-weight:600">${a.market} Tỷ</div>
        </div>
      </div>
      `}


      ${!isReadOnly ? `
      <!-- Row 2: Chỉ số gốc (raw inputs) — chỉ hiện ở Triage -->
      <div style="width:100%;margin-top:10px;padding-top:10px;border-top:1px solid var(--bg-border);display:flex;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:11px">

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Diện Tích</div>
          <div><strong>${a.area || '?'}</strong> <span style="color:var(--text-3)">m²</span></div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Tỷ Lệ Vay</div>
          <div style="color:${(a.loanpct || 0) >= 70 ? 'var(--red)' : (a.loanpct || 0) >= 50 ? 'var(--yellow)' : 'var(--text-1)'}">
            <strong>${a.loanpct || 0}%</strong>
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Kỳ Hạn</div>
          <div><strong>${a.loanterm || 0}</strong> <span style="color:var(--text-3)">năm</span></div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Ưu đãi</div>
          <div style="color:${(a.prefmonths || 0) <= 3 && (a.prefmonths || 0) > 0 ? 'var(--yellow)' : 'var(--text-1)'}">
            <strong>${a.prefmonths || 0}</strong> <span style="color:var(--text-3)">tháng</span>
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Lãi Ưu Đãi</div>
          <div style="color:${(a.rate || 0) >= 12 ? 'var(--red)' : (a.rate || 0) >= 9 ? 'var(--yellow)' : 'var(--emerald)'}">
            <strong>${a.rate || 0}%</strong>/năm
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em;cursor:help" title="Tháng còn được ân hạn nợ gốc — chưa trả gốc">Ân Hạn Gốc</div>
          <div style="color:${(a.grace || 0) > 0 && (a.grace || 0) <= 3 ? 'var(--yellow)' : 'var(--text-1)'}">
            <strong>${a.grace || 0}</strong> <span style="color:var(--text-3)">tháng</span>
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Lãi Thả Nổi</div>
          <div style="color:${(a.floatrate || 0) >= 14 ? 'var(--red)' : (a.floatrate || 0) >= 12 ? 'var(--yellow)' : 'var(--text-1)'}">
            <strong>${a.floatrate || 0}%</strong>/năm
          </div>
        </div>

        ${(a.extrapaid || 0) > 0 ? `<div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Trả Thêm Gốc</div>
          <div style="color:var(--emerald)"><strong>${a.extrapaid}</strong> <span style="color:var(--text-3)">Tỷ/kỳ</span></div>
        </div>` : ''}

        <div style="border-left:1px solid var(--bg-border);padding-left:16px">
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Tình Trạng</div>
          <div style="color:${{
            'dang-thue': 'var(--emerald)',
            'trong': 'var(--text-2)',
            'tu-dung': 'var(--text-2)',
            'chua-ban-giao': 'var(--yellow)'
          }[a.rentstatus] || 'var(--text-2)'}">
            <strong>${{
            'dang-thue': 'Đang thuê ✅',
            'trong': 'Bỏ trống',
            'tu-dung': 'Tự dùng',
            'chua-ban-giao': 'Chưa bàn giao 🔑'
          }[a.rentstatus] || a.rentstatus}</strong>
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Thu Thuê</div>
          <div style="color:${(a.rent || 0) > 0 ? 'var(--emerald)' : 'var(--text-3)'}">
            <strong>${a.rent || 0}</strong> <span style="color:var(--text-3)">Tr/th</span>
          </div>
        </div>

        <div>
          <div style="color:var(--text-3);font-size:9px;text-transform:uppercase;letter-spacing:.05em">Phí Quản lý/ bảo trì</div>
          <div style="color:${(a.mgmt || 0) > 0 ? 'var(--red)' : 'var(--text-3)'}">
            <strong>${a.mgmt || 0}</strong> <span style="color:var(--text-3)">Tr/th</span>
          </div>
        </div>

      </div>
      <!-- End Row 2 -->
      ` : ''}

      ${!isReadOnly ? `
      <div style="display:flex;gap:6px;flex-shrink:0">



        <button class="btn btn-secondary btn-sm" onclick="editAsset(${a._id})">✏️ Sửa</button>



        <button class="btn btn-danger btn-sm" onclick="removeAsset(${a._id})">🗑️</button>



      </div>
      ` : ''}



    </div>`;



    }

    function renderAssetList() {



      const panel = document.getElementById('portfolio-panel');



      const list = document.getElementById('asset-list');



      const badge = document.getElementById('asset-count-badge');



      const btnD = document.getElementById('btn-diagnose-all');







      badge.textContent = `${PORTFOLIO.length} tài sản`;

      // Portfolio panel luôn hiển thị
      panel.style.display = 'block';

      btnD.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';

      const btnExp = document.getElementById('btn-export');
      if (btnExp) btnExp.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';

      const btnQP = document.getElementById('btn-print-quick');
      if (btnQP) btnQP.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';

      // Ẩn onboarding-guide (không cần nữa vì panel luôn hiện)
      const guide = document.getElementById('onboarding-guide');
      if (guide) guide.style.display = 'none';







      // Portfolio Summary Strip



      const sumDiv = document.getElementById('portfolio-summary');



      if (sumDiv) {



        if (PORTFOLIO.length === 0) { sumDiv.style.display = 'none'; }



        else {



          const tMkt = PORTFOLIO.reduce((s, a) => s + (a.market || 0), 0);



          const tCost = PORTFOLIO.reduce((s, a) => s + (a.cost || 0), 0);



          const tEq = PORTFOLIO.reduce((s, a) => s + (a.cost || 0) * (1 - (a.loanpct || 0) / 100), 0);



          const tDebt = PORTFOLIO.reduce((s, a) => s + (calcAsset(a).autoDebt || 0) / 1000, 0);



          const tCF = PORTFOLIO.reduce((s, a) => s + calcAsset(a).cashflow, 0);



          const gain = tMkt - tCost;



          const mkStat = (label, val, sub, color) =>



            `<div style="text-align:center"><div style="font-size:10px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${label}</div><div style="font-family:var(--mono);font-size:18px;font-weight:700;color:${color}">${val}</div><div style="font-size:11px;color:var(--text-2);margin-top:2px">${sub}</div></div>`;



          sumDiv.style.display = 'grid';



          sumDiv.innerHTML =



            mkStat('Tổng Giá Trị', tMkt.toFixed(1) + ' Tỷ',



              (gain >= 0 ? '+' : '') + gain.toFixed(1) + ' Tỷ so vốn gốc',



              'var(--gold)') +



            mkStat('Vốn Tự Có', tEq.toFixed(1) + ' Tỷ',



              PORTFOLIO.length + ' tài sản',



              'var(--text-1)') +



            mkStat('Tổng Dư Nợ', tDebt.toFixed(1) + ' Tỷ',



              'Nợ NH hiện tại',



              tDebt > 0 ? 'var(--yellow)' : 'var(--text-1)') +



            mkStat('Dòng Tiền/Tháng', (tCF >= 0 ? '+' : '') + tCF.toFixed(1) + ' Tr',



              'Ước tính lãi vay cơ bản',



              tCF >= 0 ? 'var(--emerald)' : 'var(--red)');



        }



      }















      // PHASE_META is now inside generateAssetCardHTML (self-contained global function)



      // Empty state: hiện bảng rỗng với hướng dẫn khi chưa có tài sản
      if (PORTFOLIO.length === 0) {
        list.innerHTML = `
      <div style="
        border: 1px dashed var(--bg-border);
        border-radius: var(--r-md);
        padding: 32px 24px;
        text-align: center;
        background: rgba(14,20,34,0.5);
        margin-top: 4px;
      ">
        <div style="font-size: 36px; margin-bottom: 12px; opacity: 0.4;">🏠</div>
        <div style="font-size: 13px; font-weight: 600; color: var(--text-2); margin-bottom: 6px;">Chưa có tài sản nào trong danh mục</div>
        <div style="font-size: 12px; color: var(--text-3); line-height: 1.6;">
          Điền thông tin tài sản vào form phía dưới<br>
          rồi nhấn <strong style="color:var(--gold)">＋ Thêm Vào Danh Mục</strong> để bắt đầu chẩn đoán.
        </div>
        <div style="display:flex;justify-content:center;gap:12px;margin-top:16px;flex-wrap:wrap">
          <div style="font-size:11px;color:var(--text-3);padding:4px 10px;border:1px solid var(--bg-border);border-radius:20px">📌 Nhà riêng</div>
          <div style="font-size:11px;color:var(--text-3);padding:4px 10px;border:1px solid var(--bg-border);border-radius:20px">🏢 Shophouse</div>
          <div style="font-size:11px;color:var(--text-3);padding:4px 10px;border:1px solid var(--bg-border);border-radius:20px">🏙️ Chung cư</div>
          <div style="font-size:11px;color:var(--text-3);padding:4px 10px;border:1px solid var(--bg-border);border-radius:20px">🌿 Đất nền</div>
        </div>
      </div>`;
        return;
      }



      // generateAssetCardHTML is now a global function (see below)



      list.innerHTML = PORTFOLIO.map((a, i) => generateAssetCardHTML(a, i, false)).join('');



    }







    function diagnoseAll() {



      if (PORTFOLIO.length === 0) return;



      window.SESSION_PORTFOLIO = PORTFOLIO;



      localStorage.setItem('aa_session', JSON.stringify(PORTFOLIO));



      switchTab('diagnosis');



      if (typeof renderDiagnosis === 'function') renderDiagnosis(PORTFOLIO);



    }







    function quickPrintSummary() {



      if (!PORTFOLIO.length) return;



      const now = new Date().toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });



      const tMkt = PORTFOLIO.reduce((s, a) => s + (a.market || 0), 0);



      const tEq = PORTFOLIO.reduce((s, a) => s + (a.cost || 0) * (1 - (a.loanpct || 0) / 100), 0);



      const tCF = PORTFOLIO.reduce((s, a) => s + calcAsset(a).cashflow, 0);



      const rows = PORTFOLIO.map((a, i) => {



        const c = calcAsset(a);



        const phLabel = { 1: 'Pha 1', 2: 'Pha 2', 3: 'Pha 3', 4: 'Pha 4' }[c.phase] || '?';



        const dscrTxt = c.dscr !== null ? c.dscr.toFixed(2) : 'N/A';



        return `<tr style="border-bottom:1px solid #eee">



      <td style="padding:6px 8px">${i + 1}. ${a.name}</td>



      <td style="padding:6px 8px;text-align:center">${phLabel}</td>



      <td style="padding:6px 8px;text-align:right">${a.market} Tỷ</td>



      <td style="padding:6px 8px;text-align:center;color:${dscrTxt === 'N/A' ? '#888' : parseFloat(dscrTxt) >= 1 ? '#059669' : '#DC2626'}">${dscrTxt}</td>



      <td style="padding:6px 8px;text-align:center;color:${c.health >= 65 ? '#059669' : c.health >= 40 ? '#D97706' : '#DC2626'}">${c.health}/100</td>



    </tr>`;



      }).join('');



      const win = window.open('', '_blank', 'width=800,height=600');



      win.document.write(`<!DOCTYPE html><html><head><title>Tóm Tắt Danh Mục — ${now}</title>



  <style>body{font-family:Arial,sans-serif;padding:24px;font-size:13px}h2{color:#1C1C2E}table{width:100%;border-collapse:collapse}th{background:#F1F5F9;padding:8px;text-align:left;font-size:11px;color:#6B7280;text-transform:uppercase}@media print{button{display:none}}</style>



  </head><body>



  <h2>📋 Tóm Tắt Danh Mục BĐS — ${now}</h2>



  <div style="display:flex;gap:24px;margin-bottom:16px;padding:12px;background:#F8FAFC;border-radius:8px">



    <div><div style="font-size:11px;color:#6B7280">Tổng Giá Trị</div><div style="font-size:20px;font-weight:700;color:#D4AF37">${tMkt.toFixed(1)} Tỷ</div></div>



    <div><div style="font-size:11px;color:#6B7280">Vốn Tự Có</div><div style="font-size:20px;font-weight:700">${tEq.toFixed(1)} Tỷ</div></div>



    <div><div style="font-size:11px;color:#6B7280">CF/Tháng</div><div style="font-size:20px;font-weight:700;color:${tCF >= 0 ? '#059669' : '#DC2626'}">${tCF >= 0 ? '+' : ''}${tCF.toFixed(1)} Tr</div></div>



  </div>



  <table><thead><tr><th>Tài Sản</th><th>Pha</th><th>Giá TT</th><th>DSCR</th><th>Health</th></tr></thead>



  <tbody>${rows}</tbody></table>



  <div style="margin-top:16px;font-size:11px;color:#9CA3AF">Asset Architect OS — In nhanh từ Triage · ${now}</div>



  <button onclick="window.print()" style="margin-top:12px;padding:8px 16px;background:#D4AF37;border:none;cursor:pointer;border-radius:4px;font-weight:700">🖨️ In / Xuất PDF</button>



  <div id="toast-notify"></div>



</body></html>`);



      win.document.close();



    }







    function exportPortfolio() {



      if (!PORTFOLIO.length) { alert('Danh mục rỗng, không có gì để xuất!'); return; }



      const data = JSON.stringify(PORTFOLIO, null, 2);



      const blob = new Blob([data], { type: 'application/json' });



      const url = URL.createObjectURL(blob);



      const a = document.createElement('a');



      a.href = url;



      a.download = `danh-muc-bds-${new Date().toISOString().slice(0, 10)}.json`;



      document.body.appendChild(a);



      a.click();



      document.body.removeChild(a);



      URL.revokeObjectURL(url);



    }







    function importPortfolio() {



      document.getElementById('import-file').click();



    }







    function handleImport(e) {



      const file = e.target.files[0];



      if (!file) return;



      const reader = new FileReader();



      reader.onload = (ev) => {



        try {



          const data = JSON.parse(ev.target.result);



          if (!Array.isArray(data)) { alert('File không hợp lệ — phải là JSON danh mục!'); return; }



          if (!confirm('Import ' + data.length + ' tài sản?\nDữ liệu hiện tại sẽ bị thay thế.')) return;



          PORTFOLIO = data;



          savePortfolio();



          renderAssetList();



          alert('✅ Import thành công ' + data.length + ' tài sản!');



        } catch (err) {



          alert('Lỗi đọc file JSON: ' + err.message);



        }



      };



      reader.readAsText(file);



      e.target.value = ''; // reset để import lại cùng file



    }







    function savePortfolio() {



      localStorage.setItem('aa_portfolio', JSON.stringify(PORTFOLIO));



      // AutoSave badge



      const sb = document.getElementById('save-badge');



      const st = document.getElementById('save-time');



      if (sb && st) {



        st.textContent = new Date().toLocaleTimeString('vi', { hour: '2-digit', minute: '2-digit' });



        sb.style.display = 'flex';



        sb.style.opacity = '1';



        clearTimeout(sb._fadeTimer);



        sb._fadeTimer = setTimeout(() => { sb.style.opacity = '0.5'; }, 3000);



      }



    }







    function loadPortfolio() {



      try {



        const saved = localStorage.getItem('aa_portfolio');



        if (saved) PORTFOLIO = JSON.parse(saved);



      } catch { PORTFOLIO = []; }



      renderAssetList();



    }











    // ── Investor Profile System ─────────────────────────────────────────



    const PROFILES = {



      ruler: {



        icon: '👑', name: 'NGƯỜI CAI TRỊ', eng: 'The Ruler', color: 'var(--gold)',



        desc: 'Tài sản đa dạng, đòn bẩy kiểm soát tốt. Pha 3 — Dòng tiền đang nuôi cả hệ thống.',



        weakness: 'Sự trì trệ thế hệ kế cận, cấu trúc quản trị cũ lỗi thời.',



        rx: 'Tiếp tục thâu tóm Pha 1 — Chính sách, Hạ Tầng để không ai thay thế đế chế. Consolidate & Expand.',



      },



      guardian: {



        icon: '🛡️', name: 'NGƯỜI BẢO VỆ', eng: 'The Guardian', color: 'var(--emerald)',



        desc: 'Bảo toàn vốn tốt, ít rủi ro. Tiền đang "ngủ yên" — tăng trưởng chậm hơn tiềm năng.',



        weakness: 'Lạm phát âm thầm ăn mòn sức mua. Thiếu tài sản tăng trưởng.',



        rx: 'Chuyển 20–30% danh mục sang Pha 1 để tăng hệ số nhân vốn. Giữ Pha 3 làm lõi phòng thủ.',



      },



      predator: {



        icon: '🐺', name: 'KẺ SĂN MỒI', eng: 'The Predator', color: 'var(--blue,#3B82F6)',



        desc: 'Cấu trúc tấn công. Đặt cược vào tăng trưởng Pha 1/2. Dòng tiền chưa phải ưu tiên.',



        weakness: 'FOMO ngược — sợ bỏ lỡ kèo thập kỷ. Dễ vỡ nếu thị trường đứng yên > 18 tháng.',



        rx: 'Cần ít nhất 1 tài sản Pha 3 tạo "máu" nuôi đòn bẩy. Cân bằng offense với defense.',



      },



      prey: {



        icon: '🩸', name: 'CON MỒI', eng: 'The Prey', color: 'var(--red)',



        desc: 'Cảnh báo nguy hiểm. Dòng tiền âm nặng, đòn bẩy cao — đang là "nhiên liệu" cho ngân hàng.',



        weakness: 'Sự ngoan cố và hối tiếc quá khứ. Nguy cơ vỡ nợ kỹ thuật.',



        rx: 'CẤP CỨU: Cắt ngay tài sản gánh lãi nặng nhất. Giải phóng dòng tiền — thoát khỏi bẫy trước khi quá muộn.',



      },



    };







    function classifyProfile(portfolio, calcs) {



      const n = portfolio.length;



      if (!n) return 'prey';



      const totalMarket = calcs.reduce((s, { a }) => s + (a.market || 0), 0);



      const totalDebt = calcs.reduce((s, { a }) => s + (a.debt || 0), 0);



      const totalCF = calcs.reduce((s, { c }) => s + c.cashflow, 0);



      const avgLoan = calcs.reduce((s, { a }) => s + (a.loanpct || 0), 0) / n;



      const ph1 = calcs.filter(({ c }) => c.phase === 1).length / n;



      const ph2 = calcs.filter(({ c }) => c.phase === 2).length / n;



      const ph3 = calcs.filter(({ c }) => c.phase === 3).length / n;



      const debtR = totalMarket > 0 ? totalDebt / totalMarket : 0;



      // Edge case: không vay / tiền mặt — tối thiểu là Người Bảo Vệ (không bao giờ là Con Mồi)



      if (totalDebt < 0.1 && avgLoan < 5) return ph3 >= 0.3 ? 'ruler' : 'guardian';



      // Con Mồi: CF rất âm, đòn bẩy cao, không có Pha3



      if (totalCF < -15 && avgLoan > 55 && ph3 < 0.2) return 'prey';



      // Kẻ Săn Mồi: Pha1+Pha2 nhiều, đòn bẩy cao



      if ((ph1 + ph2) >= 0.6 && avgLoan > 40) return 'predator';



      // Người Cai Trị: cân bằng, nợ thấp, CF ổn



      if (ph3 >= 0.3 && debtR < 0.4 && totalCF > -10) return 'ruler';



      // Người Bảo Vệ: Pha3 nhiều, vay ít



      if (ph3 >= 0.35 || (ph3 > 0 && avgLoan < 35)) return 'guardian';



      if ((ph1 + ph2) >= 0.5) return 'predator';



      return 'prey';



    }







    function assetVerdict(a, c) {



      if (c.health < 38 || (c.cashflow < -20 && (a.grace || 0) <= 3))



        return { label: '🚨 NÊN BÁN', cls: 'badge-danger' };



      if (a.market < c.floorPrice && c.viewsTin < 3)



        return { label: '⚠️ XEM XÉT BÁN', cls: 'badge-warn' };



      if (c.health >= 65 && c.cashflow > 0)



        return { label: '✅ GIỮ VỮNG', cls: 'badge-ok' };



      if (c.phase === 3 && (c.dscr || 0) > 0.8)



        return { label: '✅ GIỮ VỮNG', cls: 'badge-ok' };



      if (a.market < c.floorPrice && c.cycle < 60)



        return { label: '⏳ GIỮ 6–12T', cls: 'badge-gold' };



      return { label: '👁️ THEO DÕI', cls: 'badge-muted' };



    }











    // ── Radar Chart Engine ──────────────────────────────────────────────────



    function renderRadarChart(portfolio, calcs) {



      const box = document.getElementById('diag-radar');



      const legend = document.getElementById('diag-radar-legend');



      const section = document.getElementById('diag-radar-section');



      if (!box || !legend || !section || !calcs.length) return;



      section.style.display = 'block';







      const n = calcs.length;



      const _totalMkt1 = calcs.reduce((s, { a }) => s + (a.market || 0), 0);
      const avgHealth = _totalMkt1 > 0
        ? calcs.reduce((s, { a, c }) => s + (a.market || 0) * c.health, 0) / _totalMkt1
        : calcs.reduce((s, { c }) => s + c.health, 0) / n;



      const totalCF = calcs.reduce((s, { c }) => s + c.cashflow, 0);



      const avgLoan = portfolio.reduce((s, a) => s + (a.loanpct || 0), 0) / n;



      const avgGainPct = calcs.reduce((s, { c }) => s + (c.gainPct || 0), 0) / n;



      const phases = new Set(calcs.map(({ c }) => c.phase));







      // Each metric normalized 0→1



      const scores = [



        { label: 'Sức Khỏe', val: Math.max(0, Math.min(1, avgHealth / 100)), color: '#10B981', desc: `TB ${avgHealth.toFixed(0)}/100` },



        { label: 'Dòng Tiền', val: Math.max(0, Math.min(1, (totalCF + 50 * n) / (100 * n))), color: '#3B82F6', desc: `${totalCF >= 0 ? '+' : ''}${totalCF.toFixed(0)} Tr/tháng` },



        { label: 'An Toàn Nợ', val: Math.max(0, Math.min(1, 1 - avgLoan / 100)), color: '#EAB308', desc: `Vay TB ${avgLoan.toFixed(0)}%` },



        { label: 'Tăng Vốn', val: Math.max(0, Math.min(1, (avgGainPct + 10) / 60)), color: '#F97316', desc: `Lãi vốn TB ${avgGainPct.toFixed(1)}%` },



        { label: 'Đa Dạng', val: phases.size / 4, color: '#A855F7', desc: `${phases.size}/4 Pha` },



      ];







      // SVG geometry



      const CX = 130, CY = 130, R = 90, N = 5;



      const W = 260;



      function ptAt(val, i) {



        const ang = (i * 2 * Math.PI / N) - Math.PI / 2;



        return { x: CX + R * val * Math.cos(ang), y: CY + R * val * Math.sin(ang) };



      }



      function polyPath(val) {



        return Array.from({ length: N }, (_, i) => ptAt(val, i))



          .map((p, i) => (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ' ' + p.y.toFixed(1)).join(' ') + 'Z';



      }







      // Background grid (4 levels)



      const gridSVG = [0.25, 0.5, 0.75, 1].map((lv, gi) =>



        `<path d="${polyPath(lv)}" fill="none" stroke="rgba(255,255,255,${0.04 + gi * 0.02})" stroke-width="${gi === 3 ? 1.5 : 0.7}"/>`



      ).join('');







      // Axis lines + labels



      const axesSVG = scores.map((sc, i) => {



        const tip = ptAt(1, i);



        const lbl = ptAt(1.28, i);



        return `<line x1="${CX}" y1="${CY}" x2="${tip.x.toFixed(1)}" y2="${tip.y.toFixed(1)}" stroke="rgba(255,255,255,.1)" stroke-width="1"/>



      <text x="${lbl.x.toFixed(1)}" y="${(lbl.y + 4).toFixed(1)}" text-anchor="middle" fill="${sc.color}" font-size="9.5" font-family="monospace" font-weight="600">${sc.label}</text>`;



      }).join('');







      // Data polygon



      const dataPath = scores.map((sc, i) => ptAt(sc.val, i))



        .map((p, i) => (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ' ' + p.y.toFixed(1)).join(' ') + 'Z';







      // Dots + value labels



      const dotsSVG = scores.map((sc, i) => {



        const p = ptAt(sc.val, i);



        const vStr = (sc.val * 100).toFixed(0);



        return `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="5" fill="${sc.color}" stroke="#0d0d1a" stroke-width="1.5"/>`;



      }).join('');







      // Aura ring at center showing overall score



      const overallScore = scores.reduce((s, sc) => s + sc.val, 0) / N;



      const overallColor = overallScore >= 0.65 ? '#10B981' : overallScore >= 0.4 ? '#EAB308' : '#EF4444';







      const svg = `<svg width="${W}" height="${W}" viewBox="0 0 ${W} ${W}" style="max-width:100%">



    <circle cx="${CX}" cy="${CY}" r="${R * 1.1}" fill="rgba(255,255,255,.01)" stroke="rgba(255,255,255,.03)" stroke-width="1"/>



    ${gridSVG}



    ${axesSVG}



    <path d="${dataPath}" fill="${overallColor}22" stroke="${overallColor}" stroke-width="2" stroke-linejoin="round"/>



    ${dotsSVG}



    <text x="${CX}" y="${CY - 6}" text-anchor="middle" fill="${overallColor}" font-size="22" font-weight="700" font-family="monospace">${(overallScore * 100).toFixed(0)}</text>



    <text x="${CX}" y="${CY + 12}" text-anchor="middle" fill="#9CA3AF" font-size="9" font-family="monospace">/100 Tổng Điểm</text>



  </svg>`;







      box.innerHTML = svg;







      // Legend



      const grade = overallScore >= 0.7 ? { g: 'A', c: '#10B981', t: 'Danh mục MẠNH' } : overallScore >= 0.5 ? { g: 'B', c: '#EAB308', t: 'Cần Tối Ưu' } : overallScore >= 0.35 ? { g: 'C', c: '#F97316', t: 'Nguy Cơ Trung Bình' } : { g: 'D', c: '#EF4444', t: 'NGUY HIỂM — Cần Cấp Cứu' };



      const singleAssetNote = n < 2 ? '<div style="font-size:10px;color:var(--text-3);margin-bottom:10px;padding:6px 8px;background:rgba(168,85,247,.06);border-radius:4px;border:1px solid rgba(168,85,247,.15)">💡 Cần ≥ 2 tài sản để Radar phản ánh đầy đủ sức khỏe danh mục</div>' : '';



      legend.innerHTML = singleAssetNote + `



    <div style="margin-bottom:16px;padding:12px;background:${grade.c}11;border-radius:8px;border:1px solid ${grade.c}33;text-align:center">



      <div style="font-size:32px;font-weight:900;color:${grade.c};font-family:monospace">${grade.g}</div>



      <div style="font-size:12px;color:${grade.c};font-weight:600;margin-top:2px">${grade.t}</div>



    </div>



    ${scores.map(sc => {



        const bar = Math.round(sc.val * 10);



        return `<div style="margin-bottom:10px">



        <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">



          <span style="color:${sc.color};font-weight:600">${sc.label}</span>



          <span style="color:var(--text-2)">${sc.desc}</span>



        </div>



        <div style="height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden">



          <div style="height:100%;width:${(sc.val * 100).toFixed(0)}%;background:${sc.color};border-radius:3px;transition:width 0.5s"></div>



        </div>



      </div>`;



      }).join('')}



  `;



    }











    // ── Giả Lập Tổ Hợp ─────────────────────────────────────────────────────



    let COMBO_SELL_IDS = new Set();







    function renderComboSim(portfolio) {



      // Populate sell list



      const sellList = document.getElementById('combo-sell-list');



      if (!sellList) return;



      COMBO_SELL_IDS.clear();



      sellList.innerHTML = portfolio.map((a, i) => {



        const c = calcAsset(a);



        const cfSign = c.cashflow >= 0 ? '+' : '';



        const cfColor = c.cashflow >= 0 ? '#10B981' : '#EF4444';



        return `<button class="btn btn-secondary btn-sm combo-sell-btn" data-id="${a._id}"



        onclick="toggleComboSell('${a._id}', this)"



        style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-width:130px">



        <span style="font-weight:600">${i + 1}. ${a.name}</span>



        <span style="font-size:10px;font-family:monospace;color:${cfColor}">${cfSign}${c.cashflow.toFixed(0)} Tr/th &nbsp;|&nbsp; H:${c.health}</span>



      </button>`;



      }).join('');







      // Populate cb-district dropdown



      const cbDist = document.getElementById('cb-district');



      if (cbDist && window.MARKET_DATA) {



        const existing = [...cbDist.options].map(o => o.value);



        window.MARKET_DATA.districts.forEach(d => {



          if (!existing.includes(d.name)) {



            const opt = document.createElement('option');



            opt.value = d.name;



            opt.textContent = `${d.name} — Cycle ${d.cycle}`;



            cbDist.appendChild(opt);



          }



        });



      }



    }







    function toggleComboSell(id, btn) {



      const numId = parseInt(id);



      if (COMBO_SELL_IDS.has(numId)) {



        COMBO_SELL_IDS.delete(numId);



        btn.classList.remove('btn-primary');



        btn.classList.add('btn-secondary');



      } else {



        COMBO_SELL_IDS.add(numId);



        btn.classList.remove('btn-secondary');



        btn.classList.add('btn-primary');



      }



    }







    function runComboSim() {



      const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;



      if (!portfolio.length) { alert('Chưa có danh mục!'); return; }







      // Get new asset from form



      const g = id => document.getElementById(id);



      const n = id => parseFloat(g(id)?.value) || 0;



      const s = id => g(id)?.value || '';







      const newAsset = {



        _id: 'combo-new',



        name: s('cb-name') || 'Tài sản mới B',



        type: s('cb-type') || 'nha-rieng',



        district: s('cb-district'),



        area: n('cb-area') || 80,



        year: n('cb-year') || new Date().getFullYear(),



        cost: n('cb-cost'),



        market: n('cb-market') || n('cb-cost'),



        goal: s('cb-goal') || 'cho-thue',



        loanpct: n('cb-loanpct'),



        debt: n('cb-debt'),



        rate: n('cb-rate') || 8.5,



        prefmonths: 6,



        floatrate: 13,



        grace: n('cb-grace'),



        loanterm: 20,



        rentstatus: n('cb-rent') > 0 ? 'dang-thue' : 'trong',



        rent: n('cb-rent'),



        mgmt: n('cb-rent') > 0 ? 1.5 : 0,



        maint: 8,



      };







      if (!newAsset.cost && COMBO_SELL_IDS.size === 0) {



        alert('Vui lòng chọn ít nhất 1 tài sản BÁN hoặc nhập tài sản MUA mới.');



        return;



      }







      // Before



      const beforePortfolio = portfolio;



      const beforeCalcs = beforePortfolio.map(a => ({ a, c: calcAsset(a) }));







      // After: remove sold + add new (if cost filled)



      let afterPortfolio = portfolio.filter(a => !COMBO_SELL_IDS.has(a._id));



      if (newAsset.cost > 0) afterPortfolio = [...afterPortfolio, newAsset];



      if (!afterPortfolio.length) { alert('Danh mục sau giả lập sẽ trống rỗng!'); return; }



      const afterCalcs = afterPortfolio.map(a => ({ a, c: calcAsset(a) }));







      // Metrics



      function metrics(calcs, port) {



        const n = calcs.length;



        return {



          n,



          mkt: port.reduce((s, a) => s + (a.market || 0), 0),



          debt: port.reduce((s, a) => s + (a.debt || 0), 0),



          cf: calcs.reduce((s, { c }) => s + c.cashflow, 0),



          health: Math.round(calcs.reduce((s, { c }) => s + c.health, 0) / n),



          equity: calcs.reduce((s, { c }) => s + c.equity, 0),



          ph3: calcs.filter(({ c }) => c.phase === 3).length,



          profile: classifyProfile(port, calcs),



        };



      }



      const B = metrics(beforeCalcs, beforePortfolio);



      const A = metrics(afterCalcs, afterPortfolio);







      function delta(before, after, fmt, higherBetter = true) {



        const diff = after - before;



        const sign = diff >= 0 ? '+' : '';



        const isGood = higherBetter ? diff > 0 : diff < 0;



        const color = Math.abs(diff) < 0.01 ? '#9CA3AF' : (isGood ? '#10B981' : '#EF4444');



        const arrow = Math.abs(diff) < 0.01 ? '→' : (diff > 0 ? '↑' : '↓');



        return { sign, diff, color, arrow, str: fmt(diff) };



      }







      const rows = [



        {
          label: 'Số tài sản', b: B.n + '', a: A.n + '',



          d: delta(B.n, A.n, v => (v > 0 ? '+' : '') + v, true)
        },



        {
          label: 'Tổng Giá Trị', b: B.mkt.toFixed(1) + ' Tỷ', a: A.mkt.toFixed(1) + ' Tỷ',



          d: delta(B.mkt, A.mkt, v => (v >= 0 ? '+' : '') + v.toFixed(2) + ' Tỷ', true)
        },



        {
          label: 'Tổng Dư Nợ', b: B.debt.toFixed(1) + ' Tỷ', a: A.debt.toFixed(1) + ' Tỷ',



          d: delta(B.debt, A.debt, v => (v >= 0 ? '+' : '') + v.toFixed(2) + ' Tỷ', false)
        },



        {
          label: 'Vốn Tự Có', b: B.equity.toFixed(1) + ' Tỷ', a: A.equity.toFixed(1) + ' Tỷ',



          d: delta(B.equity, A.equity, v => (v >= 0 ? '+' : '') + v.toFixed(2) + ' Tỷ', true)
        },



        {
          label: 'CF / Tháng', b: (B.cf >= 0 ? '+' : '') + B.cf.toFixed(0) + ' Tr', a: (A.cf >= 0 ? '+' : '') + A.cf.toFixed(0) + ' Tr',



          d: delta(B.cf, A.cf, v => (v >= 0 ? '+' : '') + v.toFixed(0) + ' Tr', true)
        },



        {
          label: 'Health Score TB', b: B.health + '/100', a: A.health + '/100',



          d: delta(B.health, A.health, v => (v >= 0 ? '+' : '') + v, true)
        },



        {
          label: 'Tài Sản Pha 3', b: B.ph3 + ' / ' + B.n, a: A.ph3 + ' / ' + A.n,



          d: delta(B.ph3, A.ph3, v => (v >= 0 ? '+' : '') + v, true)
        },



        {
          label: 'Profile NĐT', b: PROFILES[B.profile].icon + ' ' + PROFILES[B.profile].name,



          a: PROFILES[A.profile].icon + ' ' + PROFILES[A.profile].name,



          d: { color: B.profile === A.profile ? '#9CA3AF' : '#A855F7', arrow: '→', str: '' }
        },



      ];







      const soldNames = portfolio.filter(a => COMBO_SELL_IDS.has(a._id)).map(a => a.name);



      const summary = [



        soldNames.length ? `🔴 Đã bán: ${soldNames.join(', ')}` : null,



        newAsset.cost > 0 ? `🟢 Mua thêm: ${newAsset.name} (${newAsset.cost} Tỷ, ${(newAsset.rent || 0)} Tr/tháng)` : null



      ].filter(Boolean).join('&nbsp;&nbsp;|&nbsp;&nbsp;');







      const resultEl = document.getElementById('combo-result');



      resultEl.style.display = 'block';



      resultEl.innerHTML = `



    <div style="background:rgba(168,85,247,.06);border:1px solid rgba(168,85,247,.2);border-radius:10px;padding:16px">



      <div style="font-size:11px;color:#A855F7;font-weight:700;letter-spacing:.07em;text-transform:uppercase;margin-bottom:14px">



        📊 Kết Quả Giả Lập Tổ Hợp



      </div>



      <div style="font-size:11px;color:var(--text-2);margin-bottom:16px;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:6px">${summary}</div>



      <div style="overflow-x:auto">



        <table style="width:100%;border-collapse:collapse;font-size:12px">



          <thead>



            <tr style="border-bottom:1px solid rgba(255,255,255,.1)">



              <th style="text-align:left;padding:8px 10px;color:var(--text-3);font-size:10px;text-transform:uppercase">Chỉ Số</th>



              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">TRƯỚC</th>



              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">SAU</th>



              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">THAY ĐỔI</th>



            </tr>



          </thead>



          <tbody>



            ${rows.map(r => `<tr style="border-bottom:1px solid rgba(255,255,255,.04)">



              <td style="padding:8px 10px;color:var(--text-2);font-weight:500">${r.label}</td>



              <td style="padding:8px 10px;text-align:center;color:var(--text-1);font-family:monospace">${r.b}</td>



              <td style="padding:8px 10px;text-align:center;color:var(--text-1);font-family:monospace;font-weight:700">${r.a}</td>



              <td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:${r.d.color}">${r.d.arrow} ${r.d.str}</td>



            </tr>`).join('')}



          </tbody>



        </table>



      </div>



      <div style="margin-top:14px;padding:10px 14px;background:rgba(168,85,247,.06);border-radius:8px;font-size:12px">



        <strong style="color:#A855F7">💬 Nhận Định:</strong>



        <span style="color:var(--text-2)">



          ${A.cf > B.cf && A.health > B.health ? ' Tổ hợp này CẢI THIỆN cả dòng tiền và sức khỏe danh mục. Khuyến nghị THỰC HIỆN.' :



          A.cf > B.cf && A.health <= B.health ? ' Dòng tiền tốt hơn nhưng Health Score giảm. Chấp nhận nếu ưu tiên thanh khoản tháng gần.' :



            A.cf <= B.cf && A.health > B.health ? ' Health Score cải thiện nhưng dòng tiền kém hơn. Phù hợp chiến lược dài hạn.' :



              ' Tổ hợp này chưa tối ưu. Cân nhắc lại khu vực / giá mua hoặc chọn tài sản khác để bán.'}



        </span>



      </div>



    </div>



  `;



    }











    // ══ PRESCRIPTION ENGINE ════════════════════════════════════════════════



    function buildPrescription() {



      const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;



      if (!portfolio || !portfolio.length) {



        alert('Chưa có danh mục! Quay lại Triage thêm tài sản trước.');



        return;



      }







      const calcs = portfolio.map(a => ({ a, c: calcAsset(a) }));



      const n = portfolio.length;



      const totalCF = calcs.reduce((s, { c }) => s + c.cashflow, 0);



      const totalMkt = portfolio.reduce((s, a) => s + (a.market || 0), 0);



      const totalDebt = calcs.reduce((s, { c }) => s + (c.autoDebt || 0) / 1000, 0);



      const totalEq = calcs.reduce((s, { c }) => s + c.equity, 0);



      const _totalMkt2 = calcs.reduce((s, { a }) => s + (a.market || 0), 0);
      const avgHealth = Math.round(_totalMkt2 > 0
        ? calcs.reduce((s, { a, c }) => s + (a.market || 0) * c.health, 0) / _totalMkt2
        : calcs.reduce((s, { c }) => s + c.health, 0) / n);



      const profKey = classifyProfile(portfolio, calcs);



      const pCfg = PROFILES[profKey];



      const dateStr = new Date().toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });



      const timeStr = new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });







      // Client info



      const clientName = document.getElementById('rx-client-name')?.value || '_______________';



      const clientPhone = document.getElementById('rx-client-phone')?.value || '_______________';



      const consultant = document.getElementById('rx-consultant')?.value || 'Hoàng Việt';



      const rxNote = document.getElementById('rx-note')?.value || '';







      // Alerts



      const alerts = [];



      calcs.forEach(({ a, c }) => {



        if (c.dscr !== null && c.dscr < 0.3)



          alerts.push({ type: 'danger', msg: `${a.name}: DSCR = ${c.dscr.toFixed(2)} — nguy hiểm cao` });



        if ((a.grace || 0) > 0 && (a.grace || 0) <= 3)



          alerts.push({ type: 'warn', msg: `${a.name}: Ân hạn còn ${a.grace} tháng — chuẩn bị tăng dòng tiền ra` });



        if ((a.prefmonths || 0) > 0 && (a.prefmonths || 0) <= 3)



          alerts.push({ type: 'warn', msg: `${a.name}: Ưu đãi lãi suất hết trong ${a.prefmonths} tháng` });



        if (a.market < c.floorPrice)



          alerts.push({ type: 'danger', msg: `${a.name}: Giá thị trường thấp hơn giá sàn hòa vốn ${c.floorPrice.toFixed(2)} Tỷ` });



      });







      // Recommendations



      const sorted = [...calcs].sort((a, b) => a.c.cashflow - b.c.cashflow);



      const recos = [];



      if (sorted[0] && sorted[0].c.cashflow < -10)



        recos.push(`CẮT HOẠI TỬ: "${sorted[0].a.name}" — đang đốt ${Math.abs(sorted[0].c.cashflow).toFixed(0)} Tr/tháng. Thoát trong 0–3 tháng.`);



      if (!calcs.find(({ c }) => c.phase === 3))



        recos.push('BƠM MÁU: Chưa có tài sản Pha 3 dòng tiền. Ưu tiên mua 1 tài sản cho thuê ổn định trong 6 tháng tới.');



      recos.push(pCfg.rx);







      // Radar SVG (copy from existing)



      // Ensure radar is always freshly rendered (write to diag-radar div, even hidden)



      renderRadarChart(portfolio, calcs);



      const radarSVG = (document.getElementById('diag-radar')?.innerHTML || '').trim();



      const radarDisplay = radarSVG



        ? radarSVG.replace(/width="[^"]*"/, 'width="240"').replace(/height="[^"]*"/, 'height="240"')



        : '<div style="color:#9CA3AF;font-size:12px;padding:20px;text-align:center">⚠️ Chưa có dữ liệu Radar — vui lòng chẩn đoán ít nhất 1 tài sản.</div>';







      // Phase labels



      const PHASE_LABEL = ['', 'Pha 1 — Chính sách, Hạ Tầng', 'Pha 2 — Di Dân Cơ Học', 'Pha 3 — Dòng tiền', 'Pha 4 — Tích Sản Dài Hạn'];



      const PHASE_COLOR = ['', '#3B82F6', '#EAB308', '#10B981', '#9CA3AF'];







      // Pre-compute complex HTML blocks to avoid nested template literal issues



      const PHASE_COL_ARR = ['', '#3B82F6', '#EAB308', '#10B981', '#9CA3AF'];



      const detailRowsHTML = calcs.map(({ a, c }, i) => {



        const rowBg = i % 2 === 1 ? 'background:#FAFAFA' : '';



        const dscrColor = c.dscr === null ? '#6B7280' : c.dscr >= 1 ? '#059669' : c.dscr >= 0.5 ? '#D97706' : '#DC2626';



        const dscrTxt = c.dscr === null ? 'N/A' : (c.dscr.toFixed(2) + (c.dscr < 0.5 ? ' 🚨' : c.dscr < 1 ? ' ⚠️' : ' ✅'));



        const roeColor = c.roeAnnual >= 18 ? '#059669' : c.roeAnnual >= 8 ? '#D97706' : '#DC2626';



        const floorColor = a.market >= (c.floorPrice || 0) ? '#059669' : '#DC2626';



        const noteArr = [];



        if (c.phaseWarning) noteArr.push(c.phaseWarning);



        if (c.deliveryNote) noteArr.push('🔑 ' + c.deliveryNote);



        if ((a.grace || 0) > 0) noteArr.push('💣 Ân hạn còn ' + a.grace + 'T');



        if ((a.prefmonths || 0) > 0 && (a.prefmonths || 0) <= 3) noteArr.push('⚡ Ưu đãi còn ' + a.prefmonths + 'T');



        return '<tr style="border-bottom:1px solid #F1F5F9;' + rowBg + '">'



          + '<td style="padding:8px 10px;font-weight:600;color:#1C1C2E">' + a.name + '</td>'



          + '<td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:' + dscrColor + '">' + dscrTxt + '</td>'



          + '<td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:' + roeColor + '">' + c.roeAnnual.toFixed(1) + '%</td>'



          + '<td style="padding:8px 10px;text-align:center;font-family:monospace;color:' + floorColor + '">' + (c.floorPrice || 0).toFixed(2) + ' Tỷ</td>'



          + '<td style="padding:8px 10px;text-align:center;font-family:monospace;color:#6B7280">' + (c.cycle ? c.cycle + '/100' : 'N/A') + (c.yoy ? ' | YoY ' + c.yoy + '%' : '') + '</td>'



          + '<td style="padding:8px 10px;font-size:10px;color:#374151">' + (noteArr.join(' • ') || '—') + '</td>'



          + '</tr>';



      }).join('');







      const _avgHr = calcs.reduce((s, { c }) => s + c.health, 0) / calcs.length;



      const _cfr = calcs.reduce((s, { c }) => s + c.cashflow, 0);



      const _avgLr = portfolio.reduce((s, a) => s + (a.loanpct || 0), 0) / portfolio.length;



      const _avgGr = calcs.reduce((s, { c }) => s + (c.gainPct || 0), 0) / calcs.length;



      const _phsR = new Set(calcs.map(({ c }) => c.phase));



      const _v1r = Math.max(0, Math.min(1, _avgHr / 100));



      const _v2r = Math.max(0, Math.min(1, (_cfr + 50 * calcs.length) / (100 * calcs.length)));



      const _v3r = Math.max(0, Math.min(1, 1 - _avgLr / 100));



      const _v4r = Math.max(0, Math.min(1, (_avgGr + 10) / 60));



      const _v5r = _phsR.size / 4;



      const _overall = (_v1r + _v2r + _v3r + _v4r + _v5r) / 5;



      const _grd = _overall >= 0.7 ? { g: 'A', c: '#059669', t: 'MẠNH' } : _overall >= 0.5 ? { g: 'B', c: '#D97706', t: 'CẦN TỐI ƯU' } : _overall >= 0.35 ? { g: 'C', c: '#F97316', t: 'RỦI RO TRUNG BÌNH' } : { g: 'D', c: '#DC2626', t: 'NGUY HIỂM' };



      const _scrs = [



        { n: 'Sức Khỏe', v: _v1r, c: '#059669' },



        { n: 'Dòng Tiền', v: _v2r, c: '#3B82F6' },



        { n: 'An Toàn Nợ', v: _v3r, c: '#D97706' },



        { n: 'Tăng Vốn', v: _v4r, c: '#F97316' },



        { n: 'Đa Dạng Pha', v: _v5r, c: '#A855F7' },



      ];



      const radLegHTML =



        '<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">'



        + '<div style="font-size:48px;font-weight:900;color:' + _grd.c + '">' + _grd.g + '</div>'



        + '<div><div style="font-size:14px;font-weight:700;color:' + _grd.c + '">' + _grd.t + '</div>'



        + '<div style="font-size:11px;color:#6B7280">Tổng điểm: ' + (_overall * 100).toFixed(0) + '/100</div></div>'



        + '</div>'



        + _scrs.map(sc =>



          '<div style="margin-bottom:8px">'



          + '<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">'



          + '<span style="color:' + sc.c + ';font-weight:600">' + sc.n + '</span>'



          + '<span style="color:#6B7280">' + (sc.v * 100).toFixed(0) + '/100</span></div>'



          + '<div style="height:6px;background:#E5E7EB;border-radius:3px">'



          + '<div style="height:100%;width:' + (sc.v * 100).toFixed(0) + '%;background:' + sc.c + ';border-radius:3px"></div>'



          + '</div></div>'



        ).join('');







      // Pre-compute asset card HTML (avoids nested backtick issue in template literal)
      const diagAssetListHTML = PORTFOLIO.map((a, i) => generateAssetCardHTML(a, i, true)).join('');

      const html = `



<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:780px;margin:0 auto;color:#1C1C2E;line-height:1.5">







  <!-- HEADER -->



  <div style="background:linear-gradient(135deg,#0d0d1a,#1a1a3e);color:#fff;padding:24px 28px;border-radius:12px 12px 0 0;margin-bottom:0">



    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">



      <div>



        <div style="font-size:22px;font-weight:900;letter-spacing:.04em;color:#D4AF37">⚡ ASSET ARCHITECT OS</div>



        <div style="font-size:12px;color:#9CA3AF;margin-top:2px">Hệ Điều Hành Chẩn Đoán Danh Mục BĐS — Hoàng Việt</div>



      </div>



      <div style="text-align:right;font-size:11px;color:#9CA3AF">



        <div>📅 ${dateStr} lúc ${timeStr}</div>



        <div style="margin-top:3px">Tư Vấn Viên: <strong style="color:#D4AF37">${consultant}</strong></div>



      </div>



    </div>



    <div style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(255,255,255,.1);display:flex;gap:40px;flex-wrap:wrap">



      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Khách Hàng</span><br><strong style="font-size:15px">${clientName}</strong></div>



      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Liên Hệ</span><br><strong>${clientPhone}</strong></div>



      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Mục Tiêu Buổi Khám</span><br><span style="font-size:12px;color:#D1D5DB">${rxNote || 'Chẩn đoán & tái cơ cấu danh mục'}</span></div>



    </div>



  </div>







  <!-- EXECUTIVE SUMMARY -->



  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">I. TÓM TẮT DANH MỤC</div>



    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">



      ${[



          { l: 'Tổng Giá Trị', v: totalMkt.toFixed(1) + ' Tỷ', c: '#D4AF37' },



          { l: 'Vốn Tự Có', v: totalEq.toFixed(1) + ' Tỷ', c: '#1C1C2E' },



          { l: 'Tổng Dư Nợ', v: totalDebt.toFixed(1) + ' Tỷ', c: totalDebt > 0 ? '#D97706' : '#1C1C2E' },



          { l: 'Dòng Tiền/Tháng', v: (totalCF >= 0 ? '+' : '') + totalCF.toFixed(0) + ' Tr', c: totalCF >= 0 ? '#059669' : '#DC2626' },



        ].map(x => `<div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:12px;text-align:center">



        <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${x.l}</div>



        <div style="font-size:20px;font-weight:800;color:${x.c};font-family:monospace">${x.v}</div>



      </div>`).join('')}



    </div>



  </div>







  <!-- PROFILE NĐT -->



  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">II. CHẨN ĐOÁN PROFILE NHÀ ĐẦU TƯ</div>



    <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">



      <div style="text-align:center;min-width:80px">



        <div style="font-size:40px">${pCfg.icon}</div>



        <div style="font-size:12px;font-weight:700;color:#1C1C2E;margin-top:4px">${pCfg.name}</div>



        <div style="font-size:10px;color:#9CA3AF">${pCfg.eng}</div>



      </div>



      <div style="flex:1;min-width:200px">



        <p style="margin:0 0 8px;font-size:12px;color:#374151">${pCfg.desc}</p>



        <p style="margin:0 0 6px;font-size:11px;color:#D97706"><strong>⚠️ Điểm yếu:</strong> ${pCfg.weakness}</p>



        <p style="margin:0;font-size:11px;color:#059669"><strong>💊 Toa thuốc:</strong> ${pCfg.rx}</p>



      </div>



      ${radarSVG ? `<div style="width:180px">${radarSVG.replace(/width="\d+"/, 'width="180"').replace(/height="\d+"/, 'height="180"').replace(/viewBox="0 0 [\d]+ [\d]+"/, 'viewBox="0 0 260 260"')}</div>` : ''}



    </div>



    <div style="margin-top:14px;padding:10px 14px;background:#F1F5F9;border-radius:6px">



      <div style="display:flex;gap:24px;flex-wrap:wrap;">



        <span style="font-size:11px;color:#374151">Health Score TB: <strong>${avgHealth}/100</strong></span>



        <span style="font-size:11px;color:#374151">Tài sản: <strong>${n}</strong></span>



        <span style="font-size:11px;color:#374151">Pha 3: <strong>${calcs.filter(({ c }) => c.phase === 3).length}/${n}</strong></span>



        <span style="font-size:11px;color:#374151">CF: <strong style="color:${totalCF >= 0 ? '#059669' : '#DC2626'}">${totalCF >= 0 ? '+' : ''}${totalCF.toFixed(0)} Tr/tháng</strong></span>



      </div>



    </div>



  </div>







  <!-- ASSET TABLE -->



  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">III. DANH MỤC TÀI SẢN CHI TIẾT</div>



    <div id="diag-asset-list-wrapper">
      ${diagAssetListHTML}
    </div>



  </div>











  <!-- CHI TIET -->



  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">IV. PHÂN TÍCH TÀI CHÍNH CHI TIẾT</div>



    <table style="width:100%;border-collapse:collapse;font-size:11px">



      <thead>



        <tr style="background:#EEF2FF;border-bottom:2px solid #C7D2FE">



          <th style="text-align:left;padding:8px 10px;color:#4338CA;font-weight:600">Tài Sản</th>



          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">DSCR</th>



          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">ROE/năm</th>



          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">Giá Sàn HV</th>



          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">Vòng Chu Kỳ</th>



          <th style="text-align:left;padding:8px 10px;color:#4338CA;font-weight:600">Lưu Ý</th>



        </tr>



      </thead>



      <tbody>



        ${detailRowsHTML}



      </tbody>



    </table>



    <div style="margin-top:10px;font-size:10px;color:#6B7280">



      * DSCR = Dòng tiền thuần / Trả nợ &nbsp;|&nbsp; HV = Hòa Vốn &nbsp;|&nbsp; ROE = Lợi Nhuận Ròng / Vốn Tự Có &nbsp;|&nbsp; Chu Kỳ Cycle 0–100



    </div>



  </div>











  <!-- RADAR SECTION -->



  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">V. RADAR SỨC KHỎE DANH MỤC</div>



    <div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap">



      <div style="flex-shrink:0">



        ${radarDisplay}



      </div>



      <div style="flex:1;min-width:200px">



        ${radLegHTML}



      </div>



    </div>



  </div>







  <!-- ALERTS -->



  ${alerts.length > 0 ? `



  <div style="background:#FFF7ED;border:1px solid #FED7AA;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#C2410C;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">⚠️ VI. CẢNH BÁO ĐỎ</div>



    ${alerts.map(al => `<div style="padding:7px 0;border-bottom:1px solid #FED7AA;font-size:11px;color:${al.type === 'danger' ? '#DC2626' : '#D97706'}">



      ${al.type === 'danger' ? '🚨' : '💣'} ${al.msg}



    </div>`).join('')}



  </div>` : ''}







  <!-- PRESCRIPTION / RECOS -->



  <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-top:none;padding:20px 28px">



    <div style="font-size:13px;font-weight:700;color:#15803D;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">💊 VII. TOA THUỐC TÁI CƠ CẤU</div>



    ${recos.map((r, i) => `<div style="padding:8px 12px;margin-bottom:8px;background:#fff;border-left:3px solid #10B981;border-radius:0 6px 6px 0;font-size:12px;color:#1C1C2E">



      <strong style="color:#15803D">${i + 1}.</strong> ${r}



    </div>`).join('')}



  </div>















  <!-- FOOTER -->



  <div style="background:#1C1C2E;color:#fff;padding:16px 28px;border-radius:0 0 12px 12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">



    <div style="font-size:10px;color:#9CA3AF">



      Asset Architect OS v1.1 &nbsp;·&nbsp; Tài liệu này chỉ dùng cho mục đích tư vấn nội bộ &nbsp;·&nbsp; Không thay thế tư vấn pháp lý/tài chính chuyên nghiệp



    </div>



    <div style="font-size:11px;color:#D4AF37;font-weight:700">



      ${consultant} &nbsp; | &nbsp; ${dateStr}



    </div>



  </div>







</div>



  `;







      const preview = document.getElementById('rx-preview');



      const empty = document.getElementById('rx-empty');



      const printBtn = document.getElementById('rx-print-btn');



      preview.style.display = 'block';



      preview.innerHTML = html;

      // TỰ ĐỘNG CLONE FULL CARD GIAO DIỆN DARK MODE VÀO BÁO CÁO (Xóa nút Sửa/Xóa để in cho đẹp)
      const wrapper = document.getElementById('diag-asset-list-wrapper');
      const sourceList = document.getElementById('asset-list');
      if (wrapper && sourceList) {
        wrapper.innerHTML = sourceList.innerHTML;
        try { wrapper.querySelectorAll('button').forEach(btn => btn.remove()); } catch (e) { }
      }

      if (empty) empty.style.display = 'none';

      if (printBtn) printBtn.style.display = 'inline-flex';

    }







    // ── DIAGNOSIS ENGINE ────────────────────────────────────────────────







    function calcAsset(a) {



      const now = new Date().getFullYear();



      const years = now - (a.year || now);



      const equity = a.cost * (1 - (a.loanpct || 0) / 100);       // Tỷ



      const gainAbs = a.market - a.cost;                        // Tỷ



      const gainPct = a.cost > 0 ? gainAbs / a.cost * 100 : 0;







      // Monthly financials (in Triệu)



      const rent = a.rent || 0;



      const mgmt = a.mgmt || 0;



      const maint_m = (a.maint || 0) / 12;



      const noi = rent - mgmt - maint_m;  // Net Operating Income







      // AUTO-CALC: Tự tính Dư Nợ Còn Lại theo công thức khấu hao
      const initialLoanM = a.cost * (a.loanpct || 0) / 100 * 1000; // Triệu
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth() + 1; // 1-12
      const monthsElapsed = Math.max(0,
        (currentYear - (a.year || currentYear)) * 12 + (currentMonth - (a.month || 1)));
      const graceMonths = a.grace || 0;
      const n_amort = Math.max(1, (a.loanterm || 20) * 12 - graceMonths); // Tháng trả gốc thực
      const k = Math.max(0, Math.min(monthsElapsed - graceMonths, n_amort)); // Tháng đã trả gốc
      // Ưu đãi & ân hạn còn lại → rateM PHẢI được khai báo trước autoDebtM
      const prefRemaining = Math.max(0, (a.prefmonths || 0) - monthsElapsed);
      const graceRemaining = Math.max(0, (a.grace || 0) - monthsElapsed);
      const effectiveRate = prefRemaining > 0 ? (a.rate || 0) : (a.floatrate || a.rate || 0);
      const rateM = effectiveRate / 100 / 12;
      let autoDebtM;
      if (initialLoanM <= 0) {
        autoDebtM = 0;
      } else if (k <= 0) {
        autoDebtM = initialLoanM;
      } else {
        // VN Bank Standard: Gốc trả đều (Chia đều nợ gốc cho n_amort)
        autoDebtM = initialLoanM * Math.max(0, 1 - k / n_amort);
      }
      const extraPaidM = (a.extrapaid || 0) * 1000;
      const debtB = Math.max(0, autoDebtM - extraPaidM); // Triệu



      const n_m = (a.loanterm || 20) * 12;



      const intOnly = debtB * rateM;          // Lãi thuần mỗi tháng



      // Nếu còn trong ân hạn gốc → chưa trả gốc. Nếu hết → tính PMT trên dư nợ và kỳ hạn còn lại
      const n_remain = Math.max(1, n_m - monthsElapsed); // Kỳ hạn vay còn lại (tháng)
      // PP Việt Nam: Trả gốc đều mỗi tháng (Lấy dư nợ hiện tại chia đều cho thời gian còn lại)
      const principal = graceRemaining > 0 ? 0
        : (n_remain > 0 ? debtB / n_remain : 0);



      const totalDebt = intOnly + principal;



      const cashflow = noi - totalDebt;     // Triệu/tháng







      const dscr = totalDebt > 0 ? noi / totalDebt : null;



      // ROE Rental (Bị vô hiệu hóa để nhường chỗ cho ROE Gọp Thực Tế - Real ROE)






      // Giá sàn hòa vốn (Tỷ)



      // Tính chuẩn xác tổng Lãi đã cắn theo từng tháng (Đồng bộ với bảng hiển thị Dư Nợ)
      const loanAmt = a.cost * (a.loanpct || 0) / 100; // Vay ban đầu (Tỷ)
      let totalInterestPaid = 0;
      const rateM_pref = (a.rate || 0) / 100 / 12;
      const rateM_float = (a.floatrate || a.rate || 0) / 100 / 12;
      const pref_m = a.prefmonths || 0;
      for (let i = 1; i <= monthsElapsed; i++) {
        let k_i = Math.max(0, i - 1 - graceMonths);
        let debt_i = loanAmt * Math.max(0, 1 - k_i / n_amort);
        let rate_i = (i <= pref_m) ? rateM_pref : rateM_float;
        totalInterestPaid += debt_i * rate_i;
      }
      const laiCD = totalInterestPaid; // Lãi cộng dồn thực tế (Tỷ)

      // Áp dụng phép chia margin Gross-up chuẩn tài chính: Thu về = (Gốc + Lãi) / 0.96
      // Trong đó 4% là Thuế TNCN (2%) + Môi giới/Pháp lý (2%)
      const floorPrice = (a.cost + laiCD) / 0.96;

      // TÍNH TOÁN CÁP ĐỘ CHUYÊN GIA: ROE THỰC TẾ (REAL ROE)
      // Lợi nhuận ròng (Net Profit) = Tiền thu về sau thuế phí (96% Market) trừ đi [Vốn khởi điểm + Toàn bộ Lãi đã vứt cho Bank]
      const netProfit = (a.market * 0.96) - a.cost - laiCD;
      const roeTotal = equity > 0 ? (netProfit / equity) * 100 : 0;
      const holdYears = Math.max(1, monthsElapsed / 12);
      const roeAnnual = roeTotal / holdYears;







      // Ghi chú tài sản chưa bàn giao



      const deliveryNote = (a.rentstatus === 'chua-ban-giao' && (a.delivery || 0) > 0)



        ? `Chưa nhận nhà — dự kiến nhận sau ${a.delivery} tháng. Thu thuê ước tính: ${(a.rentExpected || 0)} Tr/tháng.`



        : null;







      // Phân loại 4 Pha (2-Layer Architecture)



      const md = window.MARKET_DATA;



      const distData = md ? md.districts.find(d => d.name === a.district) : null;



      const cycle = distData ? distData.cycle : 50;



      const yoy = distData ? distData.yoy : 0;



      const viewsTin = distData ? distData.views_tin : 5;



      const cat_lo = distData ? distData.cat_lo : 0;








      // ============================================================
      // PHÂN LOẠI PHA — HARDCODED LOOKUP TABLE (Q2/2026)
      // Cập nhật thủ công theo thực tế thị trường
      // ============================================================
      const PHASE_MAP = {
        // Pha 1 — Chính Sách (vùng ven, hạ tầng sơ khai, ít dân)
        'Đan Phượng': 1, 'Sóc Sơn': 1, 'Mê Linh': 1,
        'Thạch Thất': 1, 'Từ Sơn (BN)': 1, 'Văn Giang (HY)': 1,
        // Pha 2 — Di Dân (hạ tầng đang lên, dân đang đổ về, yoy cao)
        'Hoài Đức': 2, 'Đông Anh': 2, 'Hoàng Mai': 2,
        'Thanh Trì': 2, 'Gia Lâm': 2,
        // Pha 3 — Dòng Tiền (khu trưởng thành, dân cư ổn định, thanh khoản tốt)
        'Đống Đa': 3, 'Cầu Giấy': 3, 'Hà Đông': 3,
        'Thanh Xuân': 3, 'Hai Bà Trưng': 3, 'Ba Đình': 3,
        'Nam Từ Liêm': 3, 'Tây Hồ': 3, 'Bắc Từ Liêm': 3,
        'Hoàn Kiếm': 3, 'Long Biên': 3,
      };

      // Pha 4 (Tích Sản) = KH tự chọn mục tiêu
      let phase, phaseWarning = null;
      if (a.goal === 'tich-san') {
        phase = 4;
      } else {
        phase = PHASE_MAP[a.district] || 1;  // default Pha 2 nếu chưa phân loại
      }

      // Cảnh báo chiến lược lệch pha
      const isCashflow = a.goal === 'cho-thue';
      const isShortTerm = a.goal === 'tang-gia' && (a.loanpct || 0) > 40;
      if (phase === 1 && isCashflow)
        phaseWarning = 'Khu vực Pha 1 chưa có dân cư — rất khó cho thuê. Chiến lược dòng tiền không phù hợp.';
      if (phase === 1 && isShortTerm)
        phaseWarning = 'Pha 1: Thanh khoản thấp, lướt sóng đòn bẩy cao = rủi ro kẹp hàng.';
      if (phase === 2 && isCashflow)
        phaseWarning = 'Pha 2: Dân đang về, thị trường cho thuê chưa ổn định. Nên chờ Pha 3.';
      if (phase === 3 && isShortTerm)
        phaseWarning = 'Pha 3: Khu trưởng thành, tăng giá chậm. Chiến lược lướt sóng không tối ưu.';

      // ── Health Score (4 trụ cột) ────────────────────────────────────────────
      // Trụ 1: DSCR (phòng thủ — sức sống hàng tháng)
      const dscrScore = dscr !== null ? Math.min(dscr * 100, 100) : 70;

      // Trụ 2: ROE (tấn công — sinh lời trên vốn tự có, chuẩn 12%/năm cho thị trường VN)
      const roeScore = Math.max(0, Math.min(roeAnnual / 12 * 100, 100));

      // Trụ 3: Lãi Vốn (tăng trưởng tài sản, chuẩn 20% là tối đa 100đ)
      const gainScore = Math.max(0, Math.min(gainPct / 20 * 100, 100));

      // Trụ 4: Market Score (Views/Tin + Phase khớp chiến lược)
      const vtScore = Math.max(0, Math.min(viewsTin / 20 * 100, 100));
      const phaseAlignScore = phaseWarning ? 50 : 100; // Có lệch pha = 50đ, khớp pha = 100đ
      const marketScore = (vtScore + phaseAlignScore) / 2;

      const health = Math.round(dscrScore * 0.25 + roeScore * 0.50 + gainScore * 0.15 + marketScore * 0.10);
      const unitPrice = (a.area || 0) > 0 ? (a.market * 1000) / a.area : 0;

      return {
        gainPct, gainAbs, equity, noi, totalDebt, cashflow, dscr, roeTotal, roeAnnual,
        floorPrice, phase, phaseWarning, deliveryNote, cycle, yoy, viewsTin, cat_lo, health, distData, intOnly, principal, years, unitPrice, autoDebt: debtB, interestPaid: laiCD
      };



    }







    function renderDiagnosis(portfolio) {



      document.getElementById('diag-empty').style.display = 'none';



      document.getElementById('diag-content').style.display = 'block';

      // -- Render asset list panel (mirror Triage, read-only) ---------------
      (() => {
        const cntBadge = document.getElementById('diag-asset-count-badge');
        if (cntBadge) cntBadge.textContent = portfolio.length + ' t\u00e0i s\u1ea3n';
        const diagList = document.getElementById('diag-asset-list');
        if (diagList) {
          diagList.innerHTML = portfolio.map((a, i) => generateAssetCardHTML(a, i, true)).join('');
        }
      })();
      // -- End asset list panel ----------------------------------------------







      const n = portfolio.length;



      document.getElementById('diag-title').textContent = `Kết Quả Chẩn Đoán — ${n} Tài Sản`;



      document.getElementById('diag-subtitle').textContent = `Thực hiện: ${new Date().toLocaleDateString('vi-VN')} lúc ${new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}`;







      const calcs = portfolio.map(a => ({ a, c: calcAsset(a) }));







      // ── Sandwich: Show strengths first ────────────────────────────────



      const strengths = [];



      const totalValue = calcs.reduce((s, { a }) => s + (a.market || 0), 0);



      strengths.push(`Tổng giá trị danh mục: <strong>${totalValue.toFixed(1)} Tỷ</strong>`);



      const phase1 = calcs.filter(({ c }) => c.phase === 1);



      if (phase1.length > 0) strengths.push(`${phase1.length} tài sản ở <strong>Pha 1 Bứt Tốc</strong> — tiềm năng tăng trưởng cao`);



      const posCF = calcs.filter(({ c }) => c.cashflow > 0);



      if (posCF.length > 0) strengths.push(`${posCF.length} tài sản có <strong>dòng tiền dương</strong> — <em>khiën chắc</em> trong chương trình phảng tự do tài chính`);



      if (strengths.length === 0) strengths.push('Danh mục đã được ghi nhận — tiếp tục phân tích để tọi ưu hóa.');



      document.getElementById('diag-strengths').innerHTML =



        `<span class="alert-icon">🏆</span><div><strong>Danh mục có: </strong>${strengths.join(' | ')}</div>`;







      // ── KPI Row (4 thẻ tổng hợp) ────────────────────────────────────



      const totalCF = calcs.reduce((s, { c }) => s + c.cashflow, 0);



      const _totalMkt3 = calcs.reduce((s, { a }) => s + (a.market || 0), 0);
      const avgHealth = Math.round(_totalMkt3 > 0
        ? calcs.reduce((s, { a, c }) => s + (a.market || 0) * c.health, 0) / _totalMkt3
        : calcs.reduce((s, { c }) => s + c.health, 0) / n);



      const totalEquity = calcs.reduce((s, { c }) => s + c.equity, 0);



      const totalMarket = calcs.reduce((s, { a }) => s + (a.market || 0), 0);



      const totalCost = calcs.reduce((s, { a }) => s + (a.cost || 0), 0);
      const totalDebtVal = calcs.reduce((s, { c }) => s + (c.autoDebt || 0) / 1000, 0);



      const mktGain = totalMarket - totalCost;



      const mktColor = mktGain >= 0 ? 'ok' : 'danger';



      const ph3Count = calcs.filter(({ c }) => c.phase === 3).length;







      const cfBreakdown = calcs.slice(0, 4).map(({ a, c }) =>



        `<span style="white-space:nowrap">${(a.name || '').split(' ')[0]}: <strong style="color:${c.cashflow >= 0 ? 'var(--emerald)' : 'var(--red)'}">${c.cashflow >= 0 ? '+' : ''}${c.cashflow.toFixed(0)}Tr</strong></span>`



      ).join(' | ') + (n > 4 ? ' …' : '');



      const cfColor = totalCF >= 0 ? 'ok' : 'danger';



      const hColor = avgHealth >= 70 ? 'ok' : avgHealth >= 45 ? 'warn' : 'danger';



      const ph3Color = ph3Count === 0 ? 'danger' : ph3Count / n >= 0.3 ? 'ok' : 'warn';







      document.getElementById('diag-kpi').innerHTML = `



    <div class="stat-card ${mktColor}"><div class="stat-label">Tổng Giá Trị Tài Sản</div><div class="stat-value">${totalMarket.toFixed(1)}<small style="font-size:14px"> Tỷ</small></div><div class="stat-sub">Vốn gốc: ${totalCost.toFixed(1)} Tỷ &nbsp;|&nbsp; <span style="color:${mktGain >= 0 ? 'var(--emerald)' : 'var(--red)'}">${mktGain >= 0 ? '+' : ''}${mktGain.toFixed(1)} Tỷ</span></div></div>

    <div class="stat-card gold"><div class="stat-label">Vốn Tự Có (Equity)</div><div class="stat-value">${totalEquity.toFixed(1)}<small style="font-size:14px"> Tỷ</small></div><div class="stat-sub">Vốn thực tế không bao gồm nợ</div></div>

    <div class="stat-card ${totalDebtVal > 0 ? 'warn' : ''}"><div class="stat-label">Tổng Dư Nợ</div><div class="stat-value">${totalDebtVal.toFixed(1)}<small style="font-size:14px"> Tỷ</small></div><div class="stat-sub">Nợ vay hiện tại &mdash; ${n} tài sản</div></div>

    <div class="stat-card ${cfColor} ${cfColor === 'danger' ? 'breathing' : ''}"><div class="stat-label">Dòng Tiền Ròng/Tháng</div><div class="stat-value" style="color:${totalCF >= 0 ? 'var(--emerald)' : 'var(--red)'}">${totalCF >= 0 ? '+' : ''}${totalCF.toFixed(1)}<small style="font-size:14px"> Tr</small></div><div class="stat-sub" style="font-size:10px;line-height:1.5">${cfBreakdown}</div></div>

    <div class="stat-card ${ph3Color}"><div class="stat-label">Tài Sản Pha 3 (Dòng Tiền)</div><div class="stat-value">${ph3Count}<small style="font-size:14px"> / ${n}</small></div><div class="stat-sub">${ph3Count === 0 ? '🔴 Không có nguồn dòng tiền' : '✅ Mạch máu hệ thống ổn định'}</div></div>

    <div class="stat-card ${hColor}"><div class="stat-label">Health Score TB</div><div class="stat-value">${avgHealth}<small style="font-size:14px">/100</small></div><div class="stat-sub">${avgHealth >= 70 ? '🟢 An toàn' : avgHealth >= 45 ? '🟡 Cần theo dõi' : '🔴 Nguy hiểm'}</div></div>`;












      // ── Investor Profile Box ──────────────────────────────────────────────



      const profKey = classifyProfile(portfolio, calcs);



      const pCfg = PROFILES[profKey];



      const profBox = document.getElementById('investor-profile-box');



      profBox.style.display = 'block';



      profBox.innerHTML = `



    <div class="card" style="border-color:${pCfg.color}44;background:rgba(0,0,0,0.2)">



      <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">



        <div style="text-align:center;min-width:80px">



          <div style="font-size:44px;line-height:1">${pCfg.icon}</div>



          <div style="font-family:var(--mono);font-size:11px;color:${pCfg.color};font-weight:700;letter-spacing:.05em;margin-top:6px">${pCfg.name}</div>



          <div style="font-size:10px;color:var(--text-3);margin-top:2px">${pCfg.eng}</div>



        </div>



        <div style="flex:1;min-width:200px">



          <div style="font-size:13px;color:var(--text-1);margin-bottom:10px;line-height:1.5">${pCfg.desc}</div>



          <div style="font-size:12px;color:var(--yellow);margin-bottom:7px">



            ⚠️ <strong>Điểm yếu cốt lõi:</strong> ${pCfg.weakness}



          </div>



          <div style="font-size:12px;color:${pCfg.color}">



            💊 <strong>Toa thuốc:</strong> ${pCfg.rx}



          </div>



        </div>



      </div>



    </div>



  `;







      // ── Radar Chart ──────────────────────────────────────────────────────



      renderRadarChart(portfolio, calcs);







      // ── Red Alerts (Module 2 — Báo Động Đỏ) ───────────────────────────



      const alerts = [];



      calcs.forEach(({ a, c }) => {



        if (c.viewsTin < 3 && c.distData)



          alerts.push({ type: 'danger', icon: '🟴', msg: `<strong>${a.district}</strong>: Views/Tin = ${c.viewsTin} — Thanh khoản cạn kiệt. Khó thoát hàng.` });



        if (c.roeAnnual < 8 && a.goal === 'cho-thue')



          alerts.push({ type: 'warn', icon: '📉', msg: `<strong>${a.name}</strong>: ROE thực = ${c.roeAnnual.toFixed(1)}% — Dưới chuẩn 18%. Gửi tiết kiệm còn có lượi hơn.` });



        if (a.market < c.floorPrice)



          alerts.push({ type: 'danger', icon: '🛈', msg: `<strong>${a.name}</strong>: Giá thị trường <strong>${a.market}Tỷ</strong> thấp hơn Giá sàn hòa vốn <strong>${c.floorPrice.toFixed(2)}Tỷ</strong>. Bán hôm nay = lỗ thực.` });



      });
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








      document.getElementById('diag-alerts').innerHTML = alerts.length > 0



        ? alerts.map(al => `<div class="alert alert-${al.type}"><span class="alert-icon">${al.icon}</span><span>${al.msg}</span></div>`).join('')



        : `<div class="alert alert-ok"><span class="alert-icon">✅</span><span>Không có cảnh báo đỏ — Danh mục ở trạng thái kiểm soát được.</span></div>`;











      // ── Auto Recommendations ──────────────────────────────────────────────



      (() => {



        const sorted = [...calcs].sort((a, b) => a.c.cashflow - b.c.cashflow);



        const worst = sorted[0];     // CF âm nhất



        const bestCF = sorted[sorted.length - 1]; // CF dương nhất



        const lowestH = [...calcs].sort((a, b) => a.c.health - b.c.health)[0];



        const recos = [];



        if (worst && worst.c.cashflow < -10)



          recos.push(`🔴 <strong>Cắt hoại tử:</strong> "${worst.a.name}" — đang đốt <strong>${Math.abs(worst.c.cashflow).toFixed(1)} Tr/tháng</strong>. Ưu tiên thoát trong Cửa sổ 0–3 tháng.`);



        if (bestCF && bestCF.c.cashflow > 0)



          recos.push(`🟢 <strong>Giữ vững:</strong> "${bestCF.a.name}" — dòng tiền dương <strong>+${bestCF.c.cashflow.toFixed(1)} Tr/tháng</strong>. Đây là mạch máu của hệ thống.`);



        const ph3Assets = calcs.filter(({ c }) => c.phase === 3);



        if (ph3Assets.length === 0)



          recos.push(`⚡ <strong>Bơm máu:</strong> Chưa có tài sản Pha 3 — Dòng tiền. Cần tái cơ cấu ngay để tạo nguồn thu ổn định.`);



        const ph1Assets = calcs.filter(({ c }) => c.phase === 1);



        if (ph1Assets.length === 0 && profKey !== 'prey')



          recos.push(`🚀 <strong>Mở rộng:</strong> Chưa có tài sản Pha 1 — Chính sách, Hạ Tầng. Xem xét phân bổ 20–30% vốn vào khu vực Cycle thấp đang đầu chu kỳ.`);



        if (recos.length === 0)



          recos.push(`✅ Danh mục đang cân bằng tốt. Tiếp tục duy trì cấu trúc hiện tại và theo dõi Cycle Index hàng tháng.`);



        document.getElementById('diag-recos').innerHTML = recos.length === 0 ? '' :
          `<div style="padding:14px 16px;background:rgba(212,175,55,0.05);border:1px solid var(--gold-dim);border-radius:var(--r-md)">
         <div style="font-size:11px;font-weight:700;color:var(--gold);letter-spacing:.07em;text-transform:uppercase;margin-bottom:10px">💊 Đơn Thuốc Tái Cơ Cấu</div>
         ${recos.map(r => `<div style="font-size:12px;color:var(--text-2);padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">${r}</div>`).join('')}
       </div>`;



      })();







      // ── Asset Matrix 4 Pha ───────────────────────────────────────────



      const phData = [1, 2, 3, 4].map(p => calcs.filter(({ c }) => c.phase === p));



      const PHASE_CFG = [



        {
          label: 'Pha 1 — Chính sách, Hạ Tầng', color: 'var(--blue,#3B82F6)', icon: '🔵',



          desc: 'Tiềm năng X2-X3 theo hạ tầng. Rủi ro biến động vùng — lướt sóng 1-3 năm.'
        },



        {
          label: 'Pha 2 — Di Dân Cơ Học', color: 'var(--gold)', icon: '🟡',



          desc: 'Vùng ven đô thị hóa. Dân đang về, giá tăng — rủi ro pháp lý & CĐT. Nắm giữ 3-5 năm.'
        },



        {
          label: 'Pha 3 — Dòng tiền', color: 'var(--emerald)', icon: '🟢',



          desc: 'Mạch máu của hệ thống — tạo thu nhập hàng tháng để gánh lãi cho các pha tăng trưởng.'
        },



        {
          label: 'Pha 4 — Tích Sản Dài Hạn', color: 'var(--text-3)', icon: '⬛',



          desc: 'Vốn nhàn rỗi, đòn bẩy thấp, >7 năm. Hầu hết là cơ hội mua ngộp hoặc vùng đặc biệt.'
        }



      ];







      document.getElementById('diag-matrix-note').textContent = `${n} tài sản`;



      document.getElementById('diag-matrix').innerHTML = PHASE_CFG.map((cfg, pi) => {



        const items = phData[pi];



        const pct = n > 0 ? Math.round(items.length / n * 100) : 0;



        const phNum = pi + 1;



        return `



      <div style="margin-bottom:16px">



        <div style="display:flex;justify-content:space-between;margin-bottom:4px">



          <span style="font-size:12px;font-weight:600;color:${cfg.color}">${cfg.icon} ${cfg.label}</span>



          <span style="font-family:var(--mono);font-size:12px;color:var(--text-2)">${items.length} tài sản (${pct}%)</span>



        </div>



        <div class="progress-bar"><div class="progress-fill" style="width:${pct}%;background:${cfg.color}"></div></div>



        <div style="font-size:11px;color:var(--text-3);margin-top:3px">${cfg.desc}</div>



        ${items.map(({ a, c }) => `



          <div style="font-size:11px;color:var(--text-2);margin-left:8px;margin-top:4px;display:flex;gap:6px;align-items:center">



            · ${a.name}



            ${c.phaseWarning ? `<span style="color:var(--yellow);font-size:10px">⚠️ ${c.phaseWarning}</span>` : ''}



            ${phNum === 4 && a.goal === 'tich-san' ? '<span class="badge badge-muted" style="font-size:9px">Tư vấn viên chọn</span>' : ''}



          </div>`).join('')}



      </div>`;



      }).join('');










      // ── Details per asset ──────────────────────────────────────────────



      document.getElementById('diag-details').innerHTML = calcs.map(({ a, c }) => {



        const hColor = c.health >= 70 ? 'var(--emerald)' : c.health >= 45 ? 'var(--yellow)' : 'var(--red)';



        const cfColor = c.cashflow >= 0 ? 'var(--emerald)' : 'var(--red)';



        return `



      <div style="padding:10px 0;border-bottom:1px solid var(--bg-border)">



        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">



          <div style="font-weight:600;font-size:12px">${a.name}${c.deliveryNote ? ' 🔑' : ''}</div>



          <span class="badge ${assetVerdict(a, c).cls}" style="font-size:10px">${assetVerdict(a, c).label}</span>



        </div>



        ${c.deliveryNote ? `<div style="font-size:11px;color:var(--gold);margin-bottom:6px;padding:3px 8px;background:rgba(212,175,55,0.08);border-radius:4px;border-left:2px solid var(--gold)">⏳ ${c.deliveryNote}</div>` : ''}



        <div style="display:flex;flex-wrap:wrap;gap:16px;font-family:var(--mono);font-size:11px">



          <span>Health: <strong style="color:${hColor}">${c.health}/100</strong></span>

          <span>Đơn giá: <strong>${c.unitPrice > 0 ? c.unitPrice.toFixed(1) + ' Tr/m²' : 'N/A'}</strong></span>



          <span>DSCR: <strong style="color:${c.dscr !== null ? (c.dscr < 0.3 ? 'var(--red)' : c.dscr < 0.8 ? 'var(--yellow)' : 'var(--emerald)') : 'var(--text-2)'}">${c.dscr !== null ? c.dscr.toFixed(2) : 'N/A'}</strong></span>



          <span>ROE: <strong style="color:${c.roeAnnual < 8 ? 'var(--yellow)' : 'var(--emerald)'}">${c.roeAnnual.toFixed(1)}%</strong></span>



          <span>CF: <strong style="color:${cfColor}">${c.cashflow >= 0 ? '+' : ''}${c.cashflow.toFixed(1)} Tr</strong></span>



          <span>Sàn HV: <strong>${c.floorPrice.toFixed(2)} Tỷ</strong></span>



          <span>Ân hạn: <strong style="color:${(a.grace || 0) <= 3 ? 'var(--yellow)' : 'var(--text-1)'}">${a.grace || 0} th</strong></span>



        </div>



      </div>`;



      }).join('');







      // ── Market Data Snapshot ───────────────────────────────────────────



      const md = window.MARKET_DATA;



      if (md) {



        document.getElementById('diag-market-stamp').textContent = md.updated;



        const districts = [...new Set(portfolio.map(a => a.district).filter(Boolean))];



        const rows = districts.map(name => {



          const d = md.districts.find(x => x.name === name);



          if (!d) return '';



          const cColor = d.cycle > 70 ? 'var(--red)' : d.cycle > 50 ? 'var(--yellow)' : 'var(--emerald)';



          const vtColor = d.views_tin < 3 ? 'var(--red)' : d.views_tin < 8 ? 'var(--yellow)' : 'var(--emerald)';



          return `<tr>



        <td>${d.name}</td>



        <td style="color:${cColor};text-align:right">${d.cycle}/100</td>



        <td style="text-align:right">${d.gia}</td>



        <td style="color:${vtColor};text-align:right">${d.views_tin}</td>



        <td style="color:${d.yoy >= 20 ? 'var(--emerald)' : 'var(--text-1)'};text-align:right">${d.yoy}%</td>



        <td style="color:${d.cat_lo > 20 ? 'var(--red)' : 'var(--text-2)'};text-align:right">${d.cat_lo}%</td>



      </tr>`;



        }).join('');



        document.getElementById('diag-market').innerHTML = rows



          ? `<table class="mkt-table"><thead><tr><th>Khu Vực</th><th>Cycle</th><th>Giá/m²</th><th>Views/Tin</th><th>YoY</th><th>Cắt Lỗ</th></tr></thead><tbody>${rows}</tbody></table>`



          : '<div style="color:var(--text-3);font-size:12px;padding:8px">Chưa chọn khu vực cho tài sản nào.</div>';



      } else {



        document.getElementById('diag-market').innerHTML = '<div class="alert alert-warn"><span class="alert-icon">⚠️</span><span>Chưa có dữ liệu thị trường. Chạy auto_crawl_daily.bat để cập nhật.</span></div>';



      }



    }







    // ── WHAT-IF SIMULATOR (Sprint 4) ────────────────────────────────



    let SIM_ASSET_IDX = 0;







    function openSimulator(portfolio) {



      if (!portfolio || portfolio.length === 0) return;



      document.getElementById('sim-empty').style.display = 'none';



      document.getElementById('sim-content').style.display = 'block';







      // Portfolio overview stats



      const statsBox = document.getElementById('sim-portfolio-stats');



      if (statsBox) {



        const pCalcs = portfolio.map(a => ({ a, c: calcAsset(a) }));



        const ptMkt = portfolio.reduce((s, a) => s + (a.market || 0), 0);



        const ptDebt = pCalcs.reduce((s, { c }) => s + (c.autoDebt || 0) / 1000, 0);



        const ptCF = pCalcs.reduce((s, { c }) => s + c.cashflow, 0);



        const ptH = Math.round(pCalcs.reduce((s, { c }) => s + c.health, 0) / portfolio.length);



        const mkSim = (label, val, color) =>



          `<div style="text-align:center;padding:10px;background:rgba(255,255,255,.03);border-radius:8px">



         <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${label}</div>



         <div style="font-family:monospace;font-size:16px;font-weight:700;color:${color}">${val}</div>



       </div>`;



        statsBox.innerHTML =



          mkSim('Tổng Tài Sản', ptMkt.toFixed(1) + ' Tỷ', 'var(--gold)') +



          mkSim('Tổng Dư Nợ', ptDebt.toFixed(1) + ' Tỷ', ptDebt > 0 ? 'var(--yellow)' : 'var(--text-1)') +



          mkSim('CF/Tháng', (ptCF >= 0 ? '+' : '') + ptCF.toFixed(0) + ' Tr', ptCF >= 0 ? 'var(--emerald)' : 'var(--red)') +



          mkSim('Health TB', ptH + '/100', ptH >= 70 ? 'var(--emerald)' : ptH >= 45 ? 'var(--yellow)' : 'var(--red)');



      }







      // Build asset selector buttons



      const list = document.getElementById('sim-asset-list');



      list.innerHTML = portfolio.map((a, i) => `



    <button class="btn btn-secondary btn-sm" id="sim-btn-${i}"



      onclick="selectSimAsset(${i})" style="transition:all 0.2s">



      ${i + 1}. ${a.name}



    </button>`).join('');







      selectSimAsset(0);



      renderComboSim(portfolio);



    }







    function selectSimAsset(idx) {



      SIM_ASSET_IDX = idx;



      document.querySelectorAll('#sim-asset-list .btn').forEach((b, i) => {



        b.classList.toggle('btn-primary', i === idx);



        b.classList.toggle('btn-secondary', i !== idx);



      });



      renderScenarios();



    }







    function renderScenarios() {



      const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;



      if (!portfolio.length) return;



      const a = portfolio[SIM_ASSET_IDX];



      const c = calcAsset(a);







      const SCENARIOS = [



        {



          id: 'ban-ngay', icon: '💰', title: 'Kịch Bản A — Bán Ngay',



          desc: 'Bán tài sản theo giá thị trường hiện tại',



          color: 'var(--red)',



          inputs: [



            { id: 'sa-price', label: 'Giá bán dự kiến (Tỷ)', type: 'number', step: 0.1, def: a.market }



          ],



          calc: (inputs) => {



            const sellPrice = parseFloat(inputs['sa-price']) || a.market;



            const taxFee = sellPrice * 0.025;   // Thuế 2% + phi 0.5%



            const netProc = sellPrice - (a.debt || 0) - taxFee;



            const gain = sellPrice - a.cost;



            const gainPct = a.cost > 0 ? gain / a.cost * 100 : 0;



            const costHeld = c.totalDebt * 12 * c.years;  // Chi phí đã bỏ



            const roi = a.cost > 0 ? gain / a.cost * 100 : 0;



            return [



              { label: 'Thu về thực tế', val: `${netProc.toFixed(2)} Tỷ`, color: netProc >= 0 ? 'var(--emerald)' : 'var(--red)' },



              { label: 'Lãi/lỗ vốn', val: `${gain >= 0 ? '+' : ''}${gain.toFixed(2)} Tỷ (${gainPct.toFixed(1)}%)`, color: gain >= 0 ? 'var(--emerald)' : 'var(--red)' },



              { label: 'Thuế + Phí', val: `${taxFee.toFixed(2)} Tỷ`, color: 'var(--yellow)' },



              { label: 'Nợ còn lại trả', val: `${(a.debt || 0).toFixed(2)} Tỷ`, color: 'var(--text-2)' },



            ];



          }



        },



        {



          id: 'cho-wait', icon: '⏳', title: 'Kịch Bản B — Chờ N Tháng',



          desc: 'Giữ tài sản thêm, bán sau khi giá tăng',



          color: 'var(--gold)',



          inputs: [



            { id: 'sb-months', label: 'Chờ thêm (tháng)', type: 'number', step: 1, def: 12 },



            { id: 'sb-growth', label: 'Tăng giá mỗi năm (%)', type: 'number', step: 0.5, def: (a.district ? (window.MARKET_DATA?.districts.find(d => d.name === a.district)?.yoy || 10) : 10) }



          ],



          calc: (inputs) => {



            const months = parseInt(inputs['sb-months']) || 12;



            const growthY = parseFloat(inputs['sb-growth']) || 10;



            const growthM = growthY / 100 / 12;



            const futurePrice = a.market * Math.pow(1 + growthM, months);



            const taxFee = futurePrice * 0.025;



            const netProc = futurePrice - (a.debt || 0) - taxFee;



            const cfCost = c.totalDebt * months;  // Tiền đổ vào trong khi chờ



            const gain = futurePrice - a.cost;



            const gainPct = a.cost > 0 ? gain / a.cost * 100 : 0;



            const vsNow = netProc - (a.market - (a.debt || 0) - a.market * 0.025);



            return [



              { label: 'Giá bán tương lai', val: `${futurePrice.toFixed(2)} Tỷ`, color: 'var(--gold)' },



              { label: 'Thu về thực tế', val: `${netProc.toFixed(2)} Tỷ`, color: 'var(--emerald)' },



              { label: 'Hơn bán ngay', val: `${vsNow >= 0 ? '+' : ''}${vsNow.toFixed(2)} Tỷ`, color: vsNow >= 0 ? 'var(--emerald)' : 'var(--red)' },



              { label: 'Chi phí dòng tiền chờ', val: `${cfCost.toFixed(1)} Tr/tổng`, color: 'var(--yellow)' },



            ];



          }



        },



        {



          id: 'refi', icon: '🏦', title: 'Kịch Bản C — Tái Cơ Cấu Lãi',



          desc: 'Đàm phán giảm lãi hoặc chuyển ngân hàng',



          color: 'var(--emerald)',



          inputs: [



            { id: 'sc-newrate', label: 'Lãi suất mới (%/năm)', type: 'number', step: 0.5, def: Math.max(6, (a.rate || 8) - 2) },



            { id: 'sc-fee', label: 'Phí tái cơ cấu (Triệu)', type: 'number', step: 5, def: 30 }



          ],



          calc: (inputs) => {



            const newRate = parseFloat(inputs['sc-newrate']) || 8;



            const fee = parseFloat(inputs['sc-fee']) || 30;



            const debtB = (a.debt || 0) * 1000;



            const newRateM = newRate / 100 / 12;



            const n_m = (a.loanterm || 20) * 12;



            const oldInt = debtB * (a.rate || 0) / 100 / 12;



            const newInt = debtB * newRateM;



            const savedM = oldInt - newInt;  // Tiết kiệm mỗi tháng (Triệu)



            const savedY = savedM * 12;



            const breakeven = fee / savedM;  // số tháng hoàn vốn phí



            const newCF = c.cashflow + savedM;



            return [



              { label: 'Lãi giảm mỗi tháng', val: `+${savedM.toFixed(1)} Triệu`, color: 'var(--emerald)' },



              { label: 'Tiết kiệm/năm', val: `+${savedY.toFixed(1)} Triệu`, color: 'var(--emerald)' },



              { label: 'HV phí tái cơ cấu', val: `${breakeven.toFixed(1)} tháng`, color: breakeven <= 12 ? 'var(--emerald)' : 'var(--yellow)' },



              { label: 'CF sau tái cơ cấu', val: `${newCF >= 0 ? '+' : ''}${newCF.toFixed(1)} Tr/th`, color: newCF >= 0 ? 'var(--emerald)' : 'var(--red)' },



            ];



          }



        }



      ];







      window._SIM_SCENARIOS = SCENARIOS;



      window._SIM_ASSET = a;



      window._SIM_CALC = c;







      document.getElementById('sim-scenarios').innerHTML = SCENARIOS.map(sc => `



    <div class="card" style="border-color:${sc.color}22">



      <div class="card-header">



        <span class="card-title" style="color:${sc.color}">${sc.icon} ${sc.title}</span>



      </div>



      <div style="font-size:11px;color:var(--text-2);margin-bottom:12px">${sc.desc}</div>



      ${sc.inputs.map(inp => `



        <div class="form-group">



          <label class="form-label">${inp.label}</label>



          <input type="${inp.type}" step="${inp.step}" value="${inp.def}"



            class="form-input" id="${inp.id}"



            oninput="runAllScenarios()">



        </div>`).join('')}



      <div id="result-${sc.id}" style="margin-top:8px"></div>



    </div>`).join('');







      runAllScenarios();



    }







    function runAllScenarios() {



      const SCENARIOS = window._SIM_SCENARIOS;



      if (!SCENARIOS) return;







      const results = [];



      SCENARIOS.forEach(sc => {



        const inputs = {};



        sc.inputs.forEach(inp => {



          const el = document.getElementById(inp.id);



          if (el) inputs[inp.id] = el.value;



        });



        const rows = sc.calc(inputs);



        results.push({ sc, rows });







        document.getElementById('result-' + sc.id).innerHTML = rows.map(r =>



          `<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--bg-border)">



        <span style="font-size:11px;color:var(--text-2)">${r.label}</span>



        <span style="font-family:var(--mono);font-size:12px;font-weight:600;color:${r.color}">${r.val}</span>



      </div>`).join('');



      });







      renderCompareTable(results);



    }







    function renderCompareTable(results) {



      const compare = document.getElementById('sim-compare');



      const body = document.getElementById('sim-compare-body');



      const rec = document.getElementById('sim-rec');



      compare.style.display = 'block';







      // Simple recommendation: which scenario gives best net return



      const a = window._SIM_ASSET;



      const vals = [



        parseFloat(document.getElementById('sa-price')?.value) - (a.debt || 0) - parseFloat(document.getElementById('sa-price')?.value) * 0.025,



        parseFloat(document.getElementById('sa-price')?.value) + 5,  // simplified



        (parseFloat(document.getElementById('sc-newrate')?.value) || 8)



      ];



      rec.textContent = vals[0] >= 0 ? '✨ Xem kết quả từng kịch bản ở trên' : '⚠️ Bán ngay có thể lỗ vốn';







      body.innerHTML = `



    <div style="overflow-x:auto">



    <table class="mkt-table" style="min-width:500px">



      <thead><tr>



        <th style="text-align:left">Chỉ Số</th>



        ${results.map(({ sc }) => `<th style="color:${sc.color}">${sc.icon} ${sc.title.split('—')[0]}</th>`).join('')}



      </tr></thead>



      <tbody>



        ${results[0].rows.map((_, ri) => `



          <tr>



            <td style="font-size:12px;color:var(--text-2)">${results[0].rows[ri].label}</td>



            ${results.map(({ rows }) => `<td style="color:${rows[ri]?.color};font-weight:600">${rows[ri]?.val || '-'}</td>`).join('')}



          </tr>`).join('')}



      </tbody>



    </table>



    </div>



    <div style="margin-top:12px;padding:12px;background:var(--bg-hover);border-radius:var(--r-sm);font-size:12px;color:var(--text-2)">



      💡 <strong style="color:var(--text-1)">Hướng dẫn:</strong> So sánh “Thu về thực tế” giữa A và B để biết nên bán ngay hay chờ. So sánh “CF sau tái cơ cấu” (C) với hiện tại để biết có đáng thương lượng lãi không.



    </div>`;



    }







    // [hook removed - merged into switchTab]







    // ── End Sprint 4 ───────────────────────────────────────────────────







    function getFormData() {



      const g = id => document.getElementById(id);



      const n = id => parseFloat(g(id)?.value) || 0;



      const s = id => g(id)?.value || '';



      return {



        name: s('f-name'), type: s('f-type'), district: s('f-district'),



        area: n('f-area'), year: n('f-year'), month: n('f-month') || 1, cost: n('f-cost'),



        market: n('f-market'), goal: s('f-goal'),



        loanpct: n('f-loanpct'), debt: 0, extrapaid: n('f-extrapaid') || 0, rate: n('f-rate'),



        prefmonths: n('f-prefmonths'), floatrate: n('f-floatrate'),



        grace: n('f-grace'), loanterm: n('f-loanterm'),



        rentstatus: s('f-rentstatus'), rent: n('f-rent'),



        delivery: n('f-delivery'),



        rentExpected: n('f-rent-expected'),



        mgmt: n('f-mgmt'), maint: n('f-maint')



      };



    }







    function submitForm() {



      const d = getFormData();



      if (!d.cost || !d.market) {



        alert('Vui lòng nhập Giá Vốn và Giá Hiện Tại tối thiểu.');



        return;



      }



      window.SESSION = d;



      localStorage.setItem('aa_session', JSON.stringify(d));



      switchTab('diagnosis');



      if (typeof renderDiagnosis === 'function') renderDiagnosis(d);



    }







    function clearForm() {



      document.getElementById('main-form').reset();



      onRentStatusChange('dang-thue');



      onLoanPctChange(60);



    }







    // ── Restore Session ───────────────────────────────────────────



    function restoreSession() {



      loadPortfolio();



    }







    // ── Init ──────────────────────────────────────────────────────



    document.addEventListener('DOMContentLoaded', async () => {



      await loadMarketData();



      restoreSession();



    });




    // ── SLIDER HELPERS (simple) ────────────────────────────────
    function _sliderSync(slider) {
      // Update filled track color based on current value
      const min = parseFloat(slider.min) || 0;
      const max = parseFloat(slider.max) || 100;
      const val = parseFloat(slider.value) || min;
      const pct = ((val - min) / (max - min) * 100).toFixed(1);
      // Color thresholds per slider
      const warnMap = { 'sl-loanpct': 60, 'sl-rate': 12 };
      const dangerMap = { 'sl-loanpct': 75, 'sl-rate': 16 };
      const warn = warnMap[slider.id];
      const danger = dangerMap[slider.id];
      let fill = '#6366f1';
      slider.classList.remove('warn', 'danger');
      if (danger && val >= danger) { fill = '#ef4444'; slider.classList.add('danger'); }
      else if (warn && val >= warn) { fill = '#f59e0b'; slider.classList.add('warn'); }
      slider.style.background = `linear-gradient(to right, ${fill} ${pct}%, rgba(255,255,255,0.12) ${pct}%)`;
    }

    function _initSlidersOnLoad() {
      [['sl-loanpct', 'f-loanpct'], ['sl-rate', 'f-rate'], ['sl-qs-buy', 'qs-buy'], ['sl-qs-now', 'qs-now'], ['sl-qs-loan', 'qs-loan'], ['sl-prefmonths', 'f-prefmonths'], ['sl-area', 'f-area'], ['sl-cost', 'f-cost'], ['sl-market', 'f-market'], ['sl-floatrate', 'f-floatrate'], ['sl-grace', 'f-grace'], ['sl-loanterm', 'f-loanterm'], ['sl-rent', 'f-rent'], ['sl-mgmt', 'f-mgmt'], ['sl-maint', 'f-maint']].forEach(function (p) {
        var sl = document.getElementById(p[0]);
        var inp = document.getElementById(p[1]);
        if (!sl || !inp) { console.warn('Slider not found:', p[0]); return; }

        // Slider → Number sync
        sl.addEventListener('input', function () {
          inp.value = this.value;
          _sliderSync(sl);
          // Trigger input event for bound logic (like onLoanPctChange)
          inp.dispatchEvent(new Event('input', { bubbles: true }));
        });

        // Number → Slider sync (when user types into number field)
        inp.addEventListener('input', function () {
          sl.value = this.value;
          _sliderSync(sl);
        });
        // Init slider position from current input value
        var initVal = parseFloat(inp.value) || parseFloat(inp.getAttribute('placeholder')) || parseFloat(sl.min) || 0;
        sl.value = initVal;
        _sliderSync(sl);
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', _initSlidersOnLoad);
    } else { _initSlidersOnLoad(); }

    // legacy CSS color function stub
    function _sliderTrackColor(slider, pct, warnT, dangerT, val) {
      // Update filled track color via background gradient
      let fillColor = '#6366f1';
      slider.classList.remove('warn', 'danger');
      if (dangerT && val >= dangerT) { fillColor = '#ef4444'; slider.classList.add('danger'); }
      else if (warnT && val >= warnT) { fillColor = '#f59e0b'; slider.classList.add('warn'); }
      slider.style.background = `linear-gradient(to right, ${fillColor} ${pct}%, rgba(255,255,255,0.12) ${pct}%)`;
    }

    // sliders initialized via _initSlidersOnLoad above

    // ── AUTO DEBT DISPLAY ──────────────────────────────────────
    function updateAutoDebtDisplay() {
      var el = document.getElementById('auto-debt-display');
      if (!el) return;
      var cost = parseFloat(document.getElementById('f-cost')?.value) || 0;
      var loanpct = parseFloat(document.getElementById('f-loanpct')?.value) || 0;
      var yearBuy = parseInt(document.getElementById('f-year')?.value) || new Date().getFullYear();
      var monthBuy = parseInt(document.getElementById('f-month')?.value) || 1;
      var loanterm = parseFloat(document.getElementById('f-loanterm')?.value) || 20;
      var grace = parseFloat(document.getElementById('f-grace')?.value) || 0;
      var prefmonths = parseFloat(document.getElementById('f-prefmonths')?.value) || 0;
      var rate = parseFloat(document.getElementById('f-rate')?.value) || 0;
      var floatrate = parseFloat(document.getElementById('f-floatrate')?.value) || rate;
      var extrapaid = parseFloat(document.getElementById('f-extrapaid')?.value) || 0;

      var now = new Date();
      var monthsElapsed = Math.max(0, (now.getFullYear() - yearBuy) * 12 + (now.getMonth() + 1 - monthBuy));
      var prefRemaining = Math.max(0, prefmonths - monthsElapsed);
      var graceRemaining = Math.max(0, grace - monthsElapsed);
      var n_amort = Math.max(1, loanterm * 12 - grace);
      var k = Math.max(0, Math.min(monthsElapsed - grace, n_amort));
      var initialLoan = cost * loanpct / 100; // Tỷ
      if (initialLoan <= 0) { el.textContent = '— Tỷ (chưa nhập thông tin vay)'; return; }

      var effectiveRate = prefRemaining > 0 ? rate : (floatrate || rate);
      var rateM = effectiveRate / 100 / 12;
      var autoDebt;
      if (k <= 0) {
        autoDebt = initialLoan;
      } else {
        autoDebt = initialLoan * Math.max(0, 1 - k / n_amort); // VN Standard: Gốc trả đều
      }
      autoDebt = Math.max(0, autoDebt - extrapaid);
      var paidOff = initialLoan - autoDebt;

      // Tính tổng số tiền lãi đã trả (Cộng dồn từng tháng một)
      var totalInterestPaid = 0;
      var rateM_pref = rate / 100 / 12;
      var rateM_float = (floatrate || rate) / 100 / 12;
      for (var i = 1; i <= monthsElapsed; i++) {
        var k_i = Math.max(0, i - 1 - grace);
        // Dư nợ đầu kỳ của tháng i
        var debt_i = initialLoan * Math.max(0, 1 - k_i / n_amort);
        // Áp dụng đúng lãi suất theo thời gian ưu đãi
        var rate_i = (i <= prefmonths) ? rateM_pref : rateM_float;
        totalInterestPaid += debt_i * rate_i;
      }

      var paidOffM = Math.max(0, paidOff) * 1000;
      var totalInterestPaidM = totalInterestPaid * 1000;

      // Custom format the numbers to include commas, rounded to whole millions (no decimals)
      var formatTrieu = (num) => Math.round(num).toLocaleString('en-US') + ' Tr';

      // 3 decimal places for Billions
      el.textContent = autoDebt.toFixed(3) + ' Tỷ (Đã trả Gốc: ' + formatTrieu(paidOffM) + ' | Đã trả Lãi: ' + formatTrieu(totalInterestPaidM) + ')';
    }
    // Hook to relevant fields on load
    document.addEventListener('DOMContentLoaded', function () {
      ['f-cost', 'f-loanpct', 'f-year', 'f-month', 'f-loanterm', 'f-grace', 'f-rate', 'f-floatrate', 'f-prefmonths', 'f-extrapaid'].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.addEventListener('input', updateAutoDebtDisplay);
      });
      updateAutoDebtDisplay();
    });