import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Cart UI: Add Hot Deals dropdown and Idle Cash warning
target_cart_ui = """  <div class="cart-body" id="cart-buy-new" style="border-top:1px solid var(--bg-border);background:rgba(255,255,255,0.02);padding:16px 20px;display:none;">
    <div style="font-weight:700;color:var(--text-1);font-size:13px;margin-bottom:12px">🛒 Mua Thêm Tài Sản Mới</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div>"""

repl_cart_ui = """  <div class="cart-body" id="cart-buy-new" style="border-top:1px solid var(--bg-border);background:rgba(255,255,255,0.02);padding:16px 20px;display:none;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <div style="font-weight:700;color:var(--text-1);font-size:13px">🛒 Mua Thêm Tài Sản Mới</div>
    </div>
    
    <div style="margin-bottom:12px">
      <label style="font-size:10px;color:var(--text-3);display:block;margin-bottom:4px;font-weight:700;color:var(--gold)">Rổ Hàng Nổi Bật (Khuyến Nghị)</label>
      <select id="cn-hot-deals" class="form-input" style="padding:6px;font-size:12px;background:rgba(212,175,55,0.1);color:var(--gold);border-color:var(--gold)" onchange="fillHotDeal()">
        <option value="">-- Tự nhập thủ công --</option>
        <option value="mega-gw">🏙️ Shophouse Mega Grand World (Giá: 12T, Thu: 80Tr/th)</option>
        <option value="thanh-oai">🏞️ Đất Đấu Giá Thanh Oai Lô Góc (Giá: 5T, Lãi Vốn: 15%/năm)</option>
        <option value="chung-cu">🏢 Căn Hộ Dòng Tiền MIniapart (Giá: 3T, Thu: 20Tr/th)</option>
      </select>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div>"""

if target_cart_ui in content:
    content = content.replace(target_cart_ui, repl_cart_ui)
    print("Injected Hot Deals UI")


# 2. Add fillHotDeal() JS logic and Idle Cash Warning logic
target_cart_js = """  function addBuyNewToCart() {"""

repl_cart_js = """  function fillHotDeal() {
    const v = document.getElementById('cn-hot-deals').value;
    if(v === 'mega-gw') {
      document.getElementById('cn-price').value = 12;
      document.getElementById('cn-debt').value = 6;
      document.getElementById('cn-noi').value = 80;
    } else if (v === 'thanh-oai') {
      document.getElementById('cn-price').value = 5;
      document.getElementById('cn-debt').value = 0;
      document.getElementById('cn-noi').value = 0;
    } else if (v === 'chung-cu') {
      document.getElementById('cn-price').value = 3;
      document.getElementById('cn-debt').value = 0;
      document.getElementById('cn-noi').value = 20;
    }
  }

  function addBuyNewToCart() {"""

if target_cart_js in content:
    content = content.replace(target_cart_js, repl_cart_js)
    print("Injected fillHotDeal JS")

target_summary_js = """    const capFormatted = Math.abs(totalCapNeeded) >= 1000 ? (Math.abs(totalCapNeeded)/1000).toFixed(2)+' Tỷ' : Math.abs(totalCapNeeded).toFixed(1)+' Tr';

    document.getElementById('cart-summary').innerHTML = `
      <div style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:14px;font-weight:700;text-align:center">Hiệu Suất Tổng Hợp (${items.length} TS)</div>"""

repl_summary_js = """    const capFormatted = Math.abs(totalCapNeeded) >= 1000 ? (Math.abs(totalCapNeeded)/1000).toFixed(2)+' Tỷ' : Math.abs(totalCapNeeded).toFixed(1)+' Tr';

    let idleCashWarning = '';
    if (totalCapNeeded > 500) { // Nếu dư ra trên 500tr
      idleCashWarning = `<div style="font-size:11px;color:#fca5a5;background:rgba(239,68,68,0.1);padding:6px 10px;border-radius:6px;margin-top:8px;border:1px dashed #fca5a5;animation:pulse 2s infinite">
        ⚠️ <strong>Cảnh Báo Nguồn Vốn Chết:</strong> Nếu không tái đầu tư khoản tiền mặt này, tốc độ trượt giá lạm phát ròng sẽ ăn mòn khoảng <strong>~${(totalCapNeeded * 0.05).toFixed(1)} Triệu/Năm</strong> sức mua. 
      </div>`;
      // Làm nút Mua Mới đập nhịp tim
      document.getElementById('btn-show-buy').style.animation = 'pulse 1.5s infinite';
      document.getElementById('btn-show-buy').style.backgroundColor = 'rgba(212,175,55,0.15)';
    } else {
      document.getElementById('btn-show-buy').style.animation = '';
      document.getElementById('btn-show-buy').style.backgroundColor = 'transparent';
    }

    document.getElementById('cart-summary').innerHTML = `
      <div style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:14px;font-weight:700;text-align:center">Hiệu Suất Tổng Hợp (${items.length} TS)</div>"""

if target_summary_js in content:
    content = content.replace(target_summary_js, repl_summary_js)
    print("Injected Idle Cash JS")

target_summary_end_js = """      </div>
    `;
  }
</script>"""

repl_summary_end_js = """      </div>
      ${idleCashWarning}
    `;
  }
</script>"""

if target_summary_end_js in content:
    content = content.replace(target_summary_end_js, repl_summary_end_js)
    print("Injected Idle Cash warning rendering")

# 3. Add Pulse animation to CSS
target_css = """@media (max-width: 600px) {
  #cart-modal { width: 100%; right: -100%; }
}
</style>"""

repl_css = """@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(212,175,55,0.4); }
  50% { transform: scale(1.02); box-shadow: 0 0 10px 0 rgba(212,175,55,0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(212,175,55,0); }
}
@media (max-width: 600px) {
  #cart-modal { width: 100%; right: -100%; }
}
</style>"""
if target_css in content:
    content = content.replace(target_css, repl_css)
    print("Injected Pulse CSS")

# 4. Modify LTV Assessment in Diagnosis
# Target is around const ltv = (d.stats.debt / Math.max(1, d.stats.market)) * 100;
# We want to add Lazy Equity warning if LTV < 30
target_ltv_diag = """      if (ltv > 70) { lblLtv = 'QUÁ RỦI RO'; ltvScore -= 8; }
      else if (ltv > 50) { lblLtv = 'RỦI RO CAO'; ltvScore -= 4; }
      else if (ltv <= 15) { lblLtv = 'LTV QUÁ THẤP'; ltvScore -= 2; }
      else { lblLtv = 'AN TOÀN / KHỎE'; ltvScore += 2; }"""

repl_ltv_diag = """      if (ltv > 70) { lblLtv = 'QUÁ RỦI RO'; ltvScore -= 8; }
      else if (ltv > 50) { lblLtv = 'RỦI RO CAO'; ltvScore -= 4; }
      else if (ltv < 30) { lblLtv = 'LAZY EQUITY (LƯỜI ĐÒN BẨY)'; ltvScore -= 6; }
      else { lblLtv = 'AN TOÀN / TỐI ƯU'; ltvScore += 2; }"""

if target_ltv_diag in content:
    content = content.replace(target_ltv_diag, repl_ltv_diag)
    print("Injected LTV Lazy Equity penalty")

target_alert_push = """      if (ltv > 65) {
        alerts.push({ id: 'sys-ltv', lvl: 'red', type: 'System', title: 'Danh mục siêu đòn bẩy (LTV > 65%)', txt: 'Đứng trước bờ vực margin call nếu tt giảm. Cần CƠ CẤU BÁN 1 TÀI SẢN NGAY LẬP TỨC để hạ nợ.' });
      }"""

repl_alert_push = """      if (ltv > 65) {
        alerts.push({ id: 'sys-ltv', lvl: 'red', type: 'System', title: 'Danh mục siêu đòn bẩy (LTV > 65%)', txt: 'Đứng trước bờ vực rủi ro thanh khoản nếu TT chững lại. Cần CƠ CẤU BÁN ít nhất 1 TÀI SẢN để hạ nợ.' });
      } else if (ltv < 30) {
        alerts.push({ id: 'sys-ltv-low', lvl: 'yellow', type: 'System', title: '⚠️ Báo  Động: Lazy Equity (Lười dùng vốn)', txt: 'Danh mục đang lãng phí >70% hạn mức tín dụng. Khoản vốn tự có đang bị "chết lâm sàng". Đề xuất thế chấp 30% danh mục lấy tiền đi thâu tóm tài sản tạo dòng tiền (Thu nhập thụ động).' });
      }"""

if target_alert_push in content:
    content = content.replace(target_alert_push, repl_alert_push)
    print("Injected LTV Alerts")


with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
