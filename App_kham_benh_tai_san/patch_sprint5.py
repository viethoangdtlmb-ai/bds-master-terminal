import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Hide the Old Combo A+B UI
# We add `display:none !important;` to the wrapper. Let's find the wrapper.
# From earlier, "runComboSim()" is near "▶ Chạy Giả Lập Tổ Hợp". We can just search for that button and hide its parent tree.
# Finding the block starting from `<div class="card" style="margin-top:20px">` before "🔄 Giả Lập Tổ Hợp — Bán A + Mua B"
t_hide = """<div class="card-header" style="margin-bottom:16px">
              <span class="card-title">🔄 Giả Lập Tổ Hợp — Bán A + Mua B</span>
            </div>"""
r_hide = """<div class="card-header" style="margin-bottom:16px; display:none !important">
              <span class="card-title">🔄 Giả Lập Tổ Hợp — Bán A + Mua B</span>
            </div><div style="display:none !important">"""
if t_hide in content:
    content = content.replace(t_hide, r_hide)
    
t_hide2 = """<button class="btn btn-primary" onclick="runComboSim()" """
r_hide2 = """</div><!-- End Hidden Combo A+B --><button class="btn btn-primary" style="display:none !important" onclick="runComboSim()" """
if t_hide2 in content:
    content = content.replace(t_hide2, r_hide2)


# 2. Modify Scenario A (Bán Ngay) to add 'sa-fees'
target_sa_inputs = """          inputs: [
            { id: 'sa-price', label: 'Giá bán dự kiến (Tỷ)', type: 'number', step: 0.1, def: a.market },
            { id: 'sa-wait', label: 'TG chờ chốt (Tháng)', type: 'number', step: 1, def: 3 },
            { id: 'sa-reinvest', label: 'Lãi tái ĐT (%/năm)', type: 'number', step: 0.5, def: 8 }
          ],"""
repl_sa_inputs = """          inputs: [
            { id: 'sa-price', label: 'Giá bán dự kiến (Tỷ)', type: 'number', step: 0.1, def: a.market },
            { id: 'sa-wait', label: 'TG chờ chốt (Tháng)', type: 'number', step: 1, def: 3 },
            { id: 'sa-fees', label: 'Thuế/Phí Môi giới (%)', type: 'number', step: 0.5, def: 3 },
            { id: 'sa-pen', label: 'Phạt Bank Trước Hạn (%)', type: 'number', step: 0.5, def: (a.year && (new Date().getFullYear() - a.year <= 2) ? 2 : 0) }
          ],"""
if target_sa_inputs in content:
    content = content.replace(target_sa_inputs, repl_sa_inputs)

target_sa_calc = """            const sellPrice = parseFloat(inputs['sa-price']) || a.market;
            const waitMonths = parseInt(inputs['sa-wait']) || 3;
            const reinvestRate = parseFloat(inputs['sa-reinvest']) || 8;
            const taxFee = sellPrice * 0.04;   // Thuế 2% + phí 2%
            const sunkCost = c.totalDebt * waitMonths; // Tiền lãi bank nuôi nhà lúc đợi chốt khách (Triệu)
            const netProc = sellPrice - (a.debt || 0) - taxFee - (sunkCost / 1000); // Lợi nhuận ròng
            const gain = sellPrice - a.cost - (sunkCost / 1000);"""
repl_sa_calc = """            const sellPrice = parseFloat(inputs['sa-price']) || a.market;
            const waitMonths = parseInt(inputs['sa-wait']) || 3;
            const feePct = parseFloat(inputs['sa-fees']) || 3;
            const penPct = parseFloat(inputs['sa-pen']) || 0;
            const debtTy = (c.autoDebt || 0) / 1000;
            const taxFee = sellPrice * (feePct / 100);
            const penFee = debtTy * (penPct / 100);
            const sunkCost = c.totalDebt * waitMonths; // Tiền lãi bank nuôi nhà lúc đợi chốt khách (Triệu)
            const netProc = sellPrice - debtTy - taxFee - penFee - (sunkCost / 1000); // Tiền mặt thu về ròng
            const gain = sellPrice - a.cost - taxFee - penFee - (sunkCost / 1000);"""
if target_sa_calc in content:
    content = content.replace(target_sa_calc, repl_sa_calc)

target_sa_rows = """              { label: 'Tiền Mặt (Bơm/Rút Ròng)', val: `+${netProc.toFixed(2)} Tỷ`, color: 'var(--emerald)' },
              { label: 'Chi Phí Đánh Đổi', val: `-${(taxFee + sunkCost / 1000).toFixed(2)} Tỷ`, color: 'var(--red)' }"""
repl_sa_rows = """              { label: 'Tiền Mặt (Bơm/Rút Ròng)', val: `+${netProc.toFixed(2)} Tỷ`, color: 'var(--emerald)' },
              { label: 'Chi Phí Đánh Đổi', val: `-${(taxFee + penFee + sunkCost / 1000).toFixed(2)} Tỷ (Bao gồm phí/phạt)`, color: 'var(--red)' }"""
if target_sa_rows in content:
    content = content.replace(target_sa_rows, repl_sa_rows)

# 3. Add [ ➕ Mua Thêm Tài Sản Nhúng ] into Cart Modal UI
t_cart_html = """  <div class="cart-footer" id="cart-summary"></div>
</div>"""
r_cart_html = """  <div class="cart-body" id="cart-buy-new" style="border-top:1px solid var(--bg-border);background:rgba(255,255,255,0.02);padding:16px 20px;display:none;">
    <div style="font-weight:700;color:var(--text-1);font-size:13px;margin-bottom:12px">🛒 Mua Thêm Tài Sản Mới</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div>
        <label style="font-size:10px;color:var(--text-3);display:block;margin-bottom:4px">Giá Mua Tỷ</label>
        <input type="number" id="cn-price" class="form-input" style="padding:6px;font-size:12px" value="4">
      </div>
      <div>
        <label style="font-size:10px;color:var(--text-3);display:block;margin-bottom:4px">Vay Bank Tỷ</label>
        <input type="number" id="cn-debt" class="form-input" style="padding:6px;font-size:12px" value="0">
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
      <div>
        <label style="font-size:10px;color:var(--text-3);display:block;margin-bottom:4px">Thu Thuần (NOI) Tr/th</label>
        <input type="number" id="cn-noi" class="form-input" style="padding:6px;font-size:12px" value="15">
      </div>
      <div>
        <label style="font-size:10px;color:var(--text-3);display:block;margin-bottom:4px">Kỳ Hạn (Năm) / Lãi %</label>
        <input type="text" id="cn-term" class="form-input" style="padding:6px;font-size:12px" value="20 / 9%">
      </div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="btn btn-primary btn-sm" style="flex:1" onclick="addBuyNewToCart()">➕ Thêm Vào Túi</button>
      <button class="btn btn-secondary btn-sm" onclick="document.getElementById('cart-buy-new').style.display='none'">Hủy</button>
    </div>
  </div>
  <div style="padding:0 20px 16px"><button id="btn-show-buy" class="btn btn-secondary btn-sm" style="width:100%; border:1px dashed var(--gold); color:var(--gold)" onclick="document.getElementById('cart-buy-new').style.display='block';this.style.display='none'">➕ Mua Thêm Tài Sản Nhúng</button></div>
  <div class="cart-footer" id="cart-summary"></div>
</div>"""
if t_cart_html in content:
    content = content.replace(t_cart_html, r_cart_html)

# 4. Add logic for addBuyNewToCart() in JS
t_cart_js = """  function renderCartModal() {"""
r_cart_js = """  function addBuyNewToCart() {
    const price = parseFloat(document.getElementById('cn-price').value) || 0;
    const debtTy = parseFloat(document.getElementById('cn-debt').value) || 0;
    const noi = parseFloat(document.getElementById('cn-noi').value) || 0;
    const termStr = document.getElementById('cn-term').value.split('/');
    const term = parseFloat(termStr[0]) || 20;
    const rate = parseFloat(termStr[1]) || 9;
    
    // tính toán nhanh nợ
    const monthlyInt = (debtTy * 1000) * (rate / 100 / 12);
    const monthlyPrin = (debtTy * 1000) / (term * 12);
    const debtService = monthlyInt + monthlyPrin;
    const cashflow = noi - debtService;
    const capNeeded = price - debtTy; // Tiền mặt phải bỏ ra
    
    const sId = 'buy-' + Date.now();
    window._STRATEGY_CART[sId] = {
      isBuyNew: true,
      id: sId,
      name: 'Tài Sản Mới Mua Thêm (Nhúng)',
      price: price,
      debtTy: debtTy,
      cf: cashflow,
      capNeeded: capNeeded
    };
    
    document.getElementById('cart-buy-new').style.display = 'none';
    document.getElementById('btn-show-buy').style.display = 'block';
    renderCartModal();
  }

  function renderCartModal() {"""
if t_cart_js in content:
    content = content.replace(t_cart_js, r_cart_js)

t_cart_js2 = """    items.forEach(it => {
      const navRow = it.rows.find(r => r.label === 'Tổng TS Ròng (NAV)');"""
r_cart_js2 = """    items.forEach(it => {
      if(it.isBuyNew) {
        totalNavDelta += (it.price - it.debtTy);
        totalCfDelta += it.cf;
        totalCapNeeded -= (it.capNeeded * 1000); // trừ tiền túi
        
        itemsHtml += `<div style="background:rgba(212,175,55,0.05);border:1px solid var(--gold);border-radius:10px;padding:14px;margin-bottom:12px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:13px;font-weight:700;color:var(--gold)">➕ ${it.name}</div>
            <button class="btn btn-sm" style="color:var(--red);background:rgba(239,68,68,0.1);padding:4px 10px;border-radius:6px;border:none" onclick="removeCartItem('${it.id}')">Xóa ✕</button>
          </div>
          <div style="font-family:var(--mono);font-size:11.5px;display:grid;grid-template-columns:1fr 1fr;gap:10px">
            <div style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px"><span style="color:var(--text-3);display:block;margin-bottom:2px;font-size:10px">Delta NAV</span> <strong style="color:var(--emerald);font-size:13px">+${(it.price - it.debtTy).toFixed(2)} Tỷ</strong></div>
            <div style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px"><span style="color:var(--text-3);display:block;margin-bottom:2px;font-size:10px">Delta Cashflow</span> <strong style="color:${it.cf>=0?'var(--emerald)':'var(--red)'};font-size:13px">${it.cf>=0?'+':''}${it.cf.toFixed(1)} Tr</strong></div>
            <div style="grid-column: span 2;background:rgba(0,0,0,0.3);padding:8px;border-radius:6px"><span style="color:var(--text-3);display:block;margin-bottom:2px;font-size:10px">Vốn Cần Tiêm (Capital Needed)</span> <strong style="color:var(--red);font-size:13px">-${Math.abs(it.capNeeded).toFixed(2)} Tỷ</strong></div>
          </div>
        </div>`;
        return; // skip the rest
      }
      
      const navRow = it.rows.find(r => r.label === 'Tổng TS Ròng (NAV)');"""
if t_cart_js2 in content:
    content = content.replace(t_cart_js2, r_cart_js2)


with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated index.html")
