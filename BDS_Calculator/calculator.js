// ============================================================
// calculator.js — Pure ROI Calculator Logic
// ============================================================

// -------- Formatters --------
const fmtTr = v => {
    const a = Math.abs(v);
    const sign = v < 0 ? '-' : '';
    if (a >= 1000) return sign + (a / 1000).toFixed(2) + ' tỷ';
    return sign + Math.round(a) + ' tr';
};
const fmtPct = v => v.toFixed(1) + '%';
const fmtBillion = v => (v / 1000).toFixed(3) + ' tỷ';

// -------- Main Calc --------
function calc() {
    const area       = +document.getElementById('areaI').value;
    const priceBillion = +document.getElementById('priceI').value;
    const delivery   = +document.getElementById('deliveryI').value;
    let eqPct      = +document.getElementById('equityPctI').value;
    let rate       = +document.getElementById('rateI').value;
    let graceMonths= +document.getElementById('graceLSI').value;
    const monthlyRent= +document.getElementById('rentI').value;
    const apprPct    = +document.getElementById('apprI').value;
    const holdYears  = +document.getElementById('holdI').value;

    // ---- Tinh toan ----
    const tongGia_coVAT   = priceBillion * 1000;                   // Tong gia co VAT (trieu)

    // Update price unit info
    const donGia = area > 0 ? (tongGia_coVAT / area).toFixed(1) : 0;
    document.getElementById('priceUnitInfo').textContent = `(~ ${donGia} tr/m²)`;

    // ---- Tiep tuc tinh toan ----
    const tongGia_chuaVAT = tongGia_coVAT / 1.10;                 // Nguoc lai chua VAT (de tinh tang gia BDS)
    const chieuKhau       = 0;                                     // Khong con auto chiet khau
    const tongGiaSauCK    = tongGia_coVAT - chieuKhau;             // Gia thuc mua sau CK

    const vonTuCo  = tongGiaSauCK * (eqPct / 100);
    const vonVay   = tongGiaSauCK - vonTuCo;
    const monthlyRate = (rate / 100) / 12;

    let totalInterestPaid = 0;
    const totalMonths = holdYears * 12;
    for (let m = 1; m <= totalMonths; m++) {
        if (m > graceMonths && monthlyRate > 0) {
            totalInterestPaid += vonVay * monthlyRate;
        }
    }

    // Doanh thu thue: tinh sau khi nhan nha
    let totalRentIncome = 0;
    for (let m = 1; m <= totalMonths; m++) {
        if (m >= delivery + 1) {
            totalRentIncome += monthlyRent * 0.92; // 8% phi moi gioi + bao tri
        }
    }

    // Gia ban (tinh tren gia chua VAT luc mua, tang gia hang nam)
    const giaGocBan       = tongGia_chuaVAT * Math.pow(1 + apprPct / 100, holdYears);
    const giaGocBanCoVAT  = giaGocBan * 1.10;
    const thueBanNha      = giaGocBanCoVAT * 0.02;
    const tienThuVeSauTraNo = giaGocBanCoVAT - thueBanNha - vonVay;

    const tongThuVe = totalRentIncome + tienThuVeSauTraNo;
    const laiRong   = tongThuVe - vonTuCo - totalInterestPaid;
    const roiNam    = (Math.pow(Math.max(0.1, ((laiRong + vonTuCo) / vonTuCo)), 1 / holdYears) - 1) * 100;

    // ---- Render Big Metrics ----
    const laiColor = laiRong >= 0 ? '#1D9E75' : '#E24B4A';
    const roiColor = roiNam >= 12 ? '#1D9E75' : roiNam >= 7 ? '#BA7517' : '#E24B4A';

    document.getElementById('bigMetrics').innerHTML = `
        <div class="big-metric" style="background:#E6F1FB;">
            <div class="big-val" style="color:#0C447C;">${fmtTr(vonTuCo)}</div>
            <div class="big-lbl" style="color:#185FA5;">Vốn chủ sở hữu</div>
        </div>
        <div class="big-metric" style="background:${laiRong >= 0 ? '#E1F5EE' : '#FCEBEB'}; border-color:${laiRong >= 0 ? '#5DCAA5' : '#F09595'};">
            <div class="big-val" style="color:${laiColor};">${fmtTr(laiRong)}</div>
            <div class="big-lbl" style="color:${laiColor};">${laiRong >= 0 ? 'Tổng lợi nhuận ròng' : 'Tổng lỗ ròng'}</div>
        </div>
        <div class="big-metric" style="background:${roiNam >= 12 ? '#E1F5EE' : roiNam >= 7 ? '#FAEEDA' : '#FCEBEB'}; border-color:${roiColor};">
            <div class="big-val" style="color:${roiColor};">${fmtPct(roiNam)}</div>
            <div class="big-lbl" style="color:${roiColor};">ROE bình quân/năm</div>
        </div>
    `;

    // ---- Render Table ----
    document.getElementById('breakdownBody').innerHTML = `
        <tr><td class="t-lbl">Tổng giá trị căn hộ (chưa VAT)</td><td class="t-val">${fmtTr(tongGia_chuaVAT)}</td></tr>
        <tr><td class="t-lbl">Thuế VAT 10%</td><td class="t-val t-neg">+${fmtTr(tongGia_coVAT - tongGia_chuaVAT)}</td></tr>
        <tr><td class="t-lbl">Vốn chủ sở hữu (${eqPct}%)</td><td class="t-val" style="color:#185FA5;">${fmtTr(vonTuCo)}</td></tr>
        <tr><td class="t-lbl">Nợ vay ngân hàng (${100-eqPct}%)</td><td class="t-val t-neg">${fmtTr(vonVay)}</td></tr>
        <tr><td class="t-lbl">Ân hạn gốc lãi</td><td class="t-val" style="color:#378ADD;">${graceMonths} tháng${rate === 0 ? ' — 0% trong ân hạn' : ''}</td></tr>
        <tr><td class="t-lbl">Tổng chi phí lãi vay thực đóng</td><td class="t-val t-neg">-${fmtTr(totalInterestPaid)}</td></tr>
        <tr><td class="t-lbl">Tổng lợi nhuận từ cho thuê (ròng)</td><td class="t-val t-pos">+${fmtTr(totalRentIncome)}</td></tr>
        <tr>
            <td class="t-lbl">
                Giá trị BĐS tại thời điểm bán (dự kiến)<br>
                <small style="font-weight:normal;color:var(--color-text-secondary);font-size:12px;">≈ ${(giaGocBanCoVAT / area).toFixed(1)} tr/m² (có VAT)</small>
            </td>
            <td class="t-val">${fmtTr(giaGocBanCoVAT)}</td>
        </tr>
        <tr><td class="t-lbl">Thuế bán nhà (2% giá có VAT)</td><td class="t-val t-neg">-${fmtTr(thueBanNha)}</td></tr>
        <tr><td class="t-lbl">Trả nợ gốc khi bán</td><td class="t-val t-neg">-${fmtTr(vonVay)}</td></tr>
        <tr style="background:var(--color-background-secondary);border-top:2px solid var(--color-border-tertiary);">
            <td class="t-lbl" style="font-weight:700;color:var(--color-text-primary);">TỔNG THU VỀ (Bán + Thuê)</td>
            <td class="t-val t-pos" style="font-size:16px;">${fmtTr(tongThuVe)}</td>
        </tr>
        <tr style="background:var(--color-background-secondary);">
            <td class="t-lbl" style="font-weight:700;color:var(--color-text-primary);">LỢI NHUẬN RÒNG (Sau lãi vay)</td>
            <td class="t-val" style="font-size:16px;color:${laiColor}">${fmtTr(laiRong)}</td>
        </tr>
    `;

    // ---- Render Verdict ----
    let verdictCls = roiNam >= 12 ? 'ok' : roiNam >= 7 ? 'warn' : 'bad';
    let verdictTitle = roiNam >= 12 ? 'KẾ HOẠCH ĐẦU TƯ: TUYỆT VỜI ✅' : roiNam >= 7 ? 'KẾ HOẠCH ĐẦU TƯ: CẦN CÂN NHẮC ⚠️' : 'KẾ HOẠCH ĐẦU TƯ: RỦI RO CAO ❌';
    let verdictText  = roiNam >= 12
        ? `Với tỷ suất sinh lời ${fmtPct(roiNam)}/năm trên vốn tự có, khoản đầu tư này rất hấp dẫn. Đòn bẩy tài chính và ân hạn ${graceMonths} tháng giúp tối ưu dòng tiền giai đoạn đầu.`
        : roiNam >= 7
        ? `Lợi nhuận ở mức chấp nhận được (${fmtPct(roiNam)}/năm). Cần chú ý biến động lãi suất sau khi hết ân hạn ${graceMonths} tháng và tốc độ tăng giá thực tế của khu vực.`
        : `Tiền lãi vay đang ăn mòn vốn chủ. Hãy xem xét: (1) Giảm tỷ lệ vay, (2) Tìm mức giá mua thấp hơn, (3) Tăng thời gian nắm giữ, (4) Thay đổi tỷ lệ vốn tự có.`;

    document.getElementById('verdict').innerHTML = `
        <div class="${verdictCls}">
            <div class="vt">${verdictTitle}</div>
            <div class="vs">${verdictText}</div>
        </div>
    `;
}

// -------- Event Listeners & Sync --------
const sliderIds = ['price', 'area', 'delivery', 'equityPct', 'rate', 'graceLS', 'rent', 'appr', 'hold'];
sliderIds.forEach(id => {
    const range = document.getElementById(id);
    const input = document.getElementById(id + 'I');

    range.addEventListener('input', () => {
        input.value = range.value;
        calc();
    });

    input.addEventListener('input', () => {
        range.value = input.value;
        calc();
    });
});

// -------- Hidden Interest Rate Calc --------
function calcHiddenRate() {
    const pVay = +document.getElementById('pVayI').value;
    const pTts = +document.getElementById('pTtsI').value;
    const loanPct = +document.getElementById('loanPctI').value / 100;
    const htlsMonths = +document.getElementById('htlsMonthsI').value;

    const cashNeeded = pVay * (1 - loanPct);
    const loanEquivalent = pTts - cashNeeded;
    const hiddenInterest = pVay - pTts;

    let verdictHTML = '';

    if (loanEquivalent <= 0) {
        verdictHTML = `<div class="warn">
            <div class="vt">KHÔNG THỂ TÍNH TOÁN</div>
            <div class="vs">Giá TTS quá thấp hoặc tỷ lệ vay quá nhỏ, số vốn ban đầu đã đủ để thanh toán sớm.</div>
        </div>`;
    } else if (hiddenInterest <= 0) {
        verdictHTML = `<div class="ok">
            <div class="vt">LÃI SUẤT ẨN: 0% / NĂM</div>
            <div class="vs">Giá vay và Giá TTS bằng nhau. Bạn đang được vay hoàn toàn MIỄN PHÍ. Chắc chắn nên chọn VAY.</div>
            <div style="margin-top:20px;">
                <button onclick="applyToROI('VAY')" style="width:100%; padding:12px; background:#378ADD; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">ÁP DỤNG P.A VAY XUỐNG DƯỚI ↓</button>
            </div>
        </div>`;
    } else {
        const annualRate = (hiddenInterest / loanEquivalent) * (12 / htlsMonths) * 100;
        const years = htlsMonths / 12;
        const compoundRate = (Math.pow((loanEquivalent + hiddenInterest) / loanEquivalent, 1 / years) - 1) * 100;
        
        verdictHTML = `<div class="ok" style="background:#E6F1FB; border-color:#378ADD; color:#0C447C;">
            <div class="vt" style="font-size:18px;">LÃI SUẤT THỰC (LÃI ĐƠN): ${annualRate.toFixed(2)}% / năm</div>
            <div style="font-size:12px; opacity:0.8; margin-bottom:12px;">* Nếu tính theo Lãi kép (vốn hóa toàn bộ, không trả tiền hàng tháng): ${compoundRate.toFixed(2)}% / năm</div>
            <div class="vs" style="margin-top:8px; border-top: 1px solid rgba(55,138,221,0.2); padding-top: 12px;">
                <strong>Bản chất:</strong> Bạn đang mượn thêm <strong>${loanEquivalent.toFixed(2)} tỷ</strong> và phải trả trước tiền lãi <strong>${hiddenInterest.toFixed(2)} tỷ</strong> (được giấu vào chênh lệch giá).<br><br>
                <strong>Khuyến nghị:</strong> Nếu bạn có thể tự huy động vốn bên ngoài với lãi suất (thanh toán hàng tháng) <strong>thấp hơn ${annualRate.toFixed(2)}%/năm</strong>, hãy chọn <strong>THANH TOÁN SỚM</strong>. Ngược lại, hãy chọn gói <strong>VAY CỦA CĐT</strong>.
            </div>
            <div style="display:flex; gap:10px; margin-top:20px;">
                <button onclick="applyToROI('VAY')" style="flex:1; padding:12px; background:#378ADD; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer; font-size:13px; transition: opacity 0.2s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">ÁP DỤNG P.A VAY ↓</button>
                <button onclick="applyToROI('TTS')" style="flex:1; padding:12px; background:#1D9E75; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer; font-size:13px; transition: opacity 0.2s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">ÁP DỤNG P.A TTS ↓</button>
            </div>
        </div>`;
    }

    document.getElementById('hiddenRateVerdict').innerHTML = verdictHTML;
}

window.applyToROI = function(type) {
    if (type === 'VAY') {
        const pVay = document.getElementById('pVayI').value;
        const loanPct = document.getElementById('loanPctI').value;
        const htlsMonths = document.getElementById('htlsMonthsI').value;
        
        document.getElementById('price').value = pVay;
        document.getElementById('priceI').value = pVay;
        
        document.getElementById('equityPct').value = 100 - loanPct;
        document.getElementById('equityPctI').value = 100 - loanPct;
        
        document.getElementById('graceLS').value = htlsMonths;
        document.getElementById('graceLSI').value = htlsMonths;
    } else {
        const pTts = document.getElementById('pTtsI').value;
        
        document.getElementById('price').value = pTts;
        document.getElementById('priceI').value = pTts;
        
        // TTS: Không dùng HTLS, vốn tự có 100% (nếu có vay ngoài tự chỉnh lại sau)
        document.getElementById('equityPct').value = 100;
        document.getElementById('equityPctI').value = 100;
        
        document.getElementById('rate').value = 0;
        document.getElementById('rateI').value = 0;
        
        document.getElementById('graceLS').value = 0;
        document.getElementById('graceLSI').value = 0;
    }
    
    // Chỉ cập nhật số liệu ở dưới mà không tự động cuộn trang để tránh làm chớp mắt
    calc(); 
};

const hiddenIds = ['pVay', 'pTts', 'loanPct', 'htlsMonths'];
hiddenIds.forEach(id => {
    const range = document.getElementById(id);
    const input = document.getElementById(id + 'I');

    range.addEventListener('input', () => {
        input.value = range.value;
        calcHiddenRate();
    });

    input.addEventListener('input', () => {
        range.value = input.value;
        calcHiddenRate();
    });
});

// Run initial calculations
calc();
calcHiddenRate();

// -------- UI Toggles --------
document.getElementById('toggleHiddenRate').addEventListener('click', () => {
    const section = document.getElementById('hiddenRateSection');
    const icon = document.getElementById('toggleIcon');
    if (section.classList.contains('open')) {
        section.classList.remove('open');
        icon.textContent = '▼ MỞ RA';
    } else {
        section.classList.add('open');
        icon.textContent = '▲ ĐÓNG LẠI';
    }
});

// -------- Init --------
window.onload = () => {
    calc();
};
