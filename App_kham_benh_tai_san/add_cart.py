import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update runAllScenarios to inject Save button and store the result
target_1 = """        document.getElementById('result-' + sc.id).innerHTML = rows.map(r =>
          `<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--bg-border)">
<span style="font-size:11px;color:var(--text-2)">${r.label}</span>
<span style="font-family:var(--mono);font-size:12px;font-weight:600;color:${r.color}">${r.val}</span>
</div>`).join('');
      });
      renderCompareTable(results);"""

replacement_1 = """        document.getElementById('result-' + sc.id).innerHTML = rows.map(r =>
          `<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--bg-border)">
<span style="font-size:11px;color:var(--text-2)">${r.label}</span>
<span style="font-family:var(--mono);font-size:12px;font-weight:600;color:${r.color}">${r.val}</span>
</div>`).join('') + `<button class="btn btn-primary btn-sm" style="width:100%;margin-top:12px;background:rgba(255,255,255,0.05);color:${sc.color};border:1px solid ${sc.color}44" onclick="saveToCart('${sc.id}')">📍 Lưu Kịch Bản Này</button>`;
      });
      window._LAST_SCENARIOS_RESULTS = results;
      renderCompareTable(results);"""

if target_1 in content:
    content = content.replace(target_1, replacement_1)
    print("Replaced chunk 1 (Save Button injection)")
else:
    print("Target 1 not found")

# 2. Add Cart UI and Logic before <script> window.MARKET_DATA
target_2 = "  <script>\n    window.MARKET_DATA ="

replacement_2 = """<style>
/* Strategy Cart UI */
#cart-fab {
  position:fixed; bottom:24px; right:24px; background:var(--gold); color:#000;
  border-radius:30px; padding:12px 20px; font-weight:700; font-size:13px;
  box-shadow:0 4px 16px rgba(0,0,0,0.6); cursor:pointer; z-index:9999;
  display: flex; align-items: center; gap: 8px; transition: transform 0.2s;
  border:1px solid rgba(255,255,255,0.2);
}
#cart-fab:hover { transform: scale(1.05); }
#cart-modal {
  position:fixed; top:0; right:-400px; width:380px; height:100%; background:var(--bg-card);
  box-shadow:-4px 0 24px rgba(0,0,0,0.8); z-index:10000; transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display:flex; flex-direction:column; border-left:1px solid var(--bg-border);
}
#cart-modal.open { right:0; }
.cart-header { padding:16px 20px; border-bottom:1px solid var(--bg-border); display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.2); }
.cart-body { flex:1; overflow-y:auto; padding:20px; }
.cart-footer { padding:20px; border-top:1px solid var(--bg-border); background:rgba(0,0,0,0.3); }
#cart-overlay {
  position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6);
  z-index:9998; display:none; backdrop-filter:blur(3px);
}
#cart-overlay.open { display:block; }
@media (max-width: 600px) {
  #cart-modal { width: 100%; right: -100%; }
}
</style>
<div id="cart-overlay" onclick="toggleCartModal()"></div>
<div id="cart-modal">
  <div class="cart-header">
    <div style="font-weight:700;color:var(--gold);font-size:16px">🛒 TÚI CHIẾN LƯỢC</div>
    <button class="btn btn-secondary btn-sm" onclick="toggleCartModal()">Đóng ✕</button>
  </div>
  <div class="cart-body" id="cart-items">
    <div style="color:var(--text-3);font-size:12px;text-align:center;margin-top:40px">Chưa có kịch bản nào được lưu.</div>
  </div>
  <div class="cart-footer" id="cart-summary"></div>
</div>
<div id="cart-fab" onclick="toggleCartModal()">
  🛒 Túi Chiến Lược <span id="cart-badge" style="background:#000;color:var(--gold);padding:2px 8px;border-radius:12px;font-size:12px;font-family:var(--mono)">0</span>
</div>
<script>
  window._STRATEGY_CART = {};
  function toggleCartModal() {
    document.getElementById('cart-modal').classList.toggle('open');
    document.getElementById('cart-overlay').classList.toggle('open');
    if (document.getElementById('cart-modal').classList.contains('open')) {
      renderCartModal();
    }
  }
  function saveToCart(scenarioId) {
    if(!window._LAST_SCENARIOS_RESULTS || !window._SIM_ASSET) return;
    const res = window._LAST_SCENARIOS_RESULTS.find(r => r.sc.id === scenarioId);
    if(!res) return;
    window._STRATEGY_CART[window._SIM_ASSET.name] = {
      asset: window._SIM_ASSET,
      calc: window._SIM_CALC,
      scenario: res.sc,
      rows: res.rows
    };
    renderCartModal();
    const fab = document.getElementById('cart-fab');
    fab.style.transform = 'scale(1.15)';
    setTimeout(() => fab.style.transform = 'scale(1)', 300);
  }
  function removeCartItem(assetName) {
    delete window._STRATEGY_CART[assetName];
    renderCartModal();
  }
  function renderCartModal() {
    const items = Object.values(window._STRATEGY_CART);
    document.getElementById('cart-badge').textContent = items.length;
    
    if(items.length === 0) {
      document.getElementById('cart-items').innerHTML = '<div style="color:var(--text-3);font-size:12px;text-align:center;margin-top:40px">Chưa có kịch bản nào được lưu.</div>';
      document.getElementById('cart-summary').innerHTML = '';
      return;
    }

    let itemsHtml = '';
    let totalNavDelta = 0;
    let totalCfDelta = 0;
    let totalCapNeeded = 0; 
    
    items.forEach(it => {
      const navRow = it.rows.find(r => r.label === 'Tổng TS Ròng (NAV)');
      const cfRow = it.rows.find(r => r.label === 'Cashflow / Tháng');
      const capRow = it.rows.find(r => r.label === 'Tiền Mặt (Bơm/Rút Ròng)');
      
      const newNavStr = navRow ? navRow.val.replace(/[^0-9.-]/g, '') : '0';
      const newNav = parseFloat(newNavStr) || 0;
      const oldNav = it.asset.market - (it.calc.autoDebt/1000);
      const deltaNav = newNav - oldNav;
      
      const newCfStr = cfRow ? cfRow.val.replace(/[^0-9.-]/g, '') : '0';
      const newCf = parseFloat(newCfStr) || 0;
      const oldCf = it.calc.cashflow;
      const deltaCf = newCf - oldCf;
      
      let capTriệu = 0;
      if (capRow) {
        // Find absolute value or sign from the string
        const capMatch = capRow.val.match(/([+-]?[0-9.]+)/);
        const capVal = capMatch ? parseFloat(capMatch[1]) : 0;
        const isTy = capRow.val.includes('Tỷ');
        capTriệu = isTy ? capVal * 1000 : capVal;
      }

      totalNavDelta += deltaNav;
      totalCfDelta += deltaCf;
      totalCapNeeded += capTriệu;

      itemsHtml += `<div style="background:rgba(255,255,255,0.03);border:1px solid var(--bg-border);border-radius:10px;padding:14px;margin-bottom:12px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.05)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
          <div style="font-size:13px;font-weight:700;color:var(--text-1)">${it.asset.name}</div>
          <button class="btn btn-sm" style="color:var(--red);background:rgba(239,68,68,0.1);padding:4px 10px;border-radius:6px;border:none" onclick="removeCartItem('${it.asset.name}')">Xóa ✕</button>
        </div>
        <div style="font-size:11.5px;color:${it.scenario.color};margin-bottom:12px;font-weight:600">${it.scenario.icon} ${it.scenario.title}</div>
        <div style="font-family:var(--mono);font-size:11.5px;display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px"><span style="color:var(--text-3);display:block;margin-bottom:2px;font-size:10px">Khoản Delta NAV</span> <strong style="color:${deltaNav>=0?'var(--emerald)':'var(--red)'};font-size:13px">${deltaNav>=0?'+':''}${deltaNav.toFixed(2)} Tỷ</strong></div>
          <div style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px"><span style="color:var(--text-3);display:block;margin-bottom:2px;font-size:10px">Delta Cashflow</span> <strong style="color:${deltaCf>=0?'var(--emerald)':'var(--red)'};font-size:13px">${deltaCf>=0?'+':''}${deltaCf.toFixed(1)} Tr</strong></div>
        </div>
      </div>`;
    });
    
    document.getElementById('cart-items').innerHTML = itemsHtml;
    
    const capSign = totalCapNeeded > 0 ? '+' : '';
    const capLabel = totalCapNeeded >= 0 ? 'Tổng Tiền Mặt Giải Phóng' : 'Tổng Phụ Phí / Sunk Cost';
    const capColor = totalCapNeeded >= 0 ? 'var(--emerald)' : 'var(--red)';
    const capFormatted = Math.abs(totalCapNeeded) >= 1000 ? (Math.abs(totalCapNeeded)/1000).toFixed(2)+' Tỷ' : Math.abs(totalCapNeeded).toFixed(1)+' Tr';

    document.getElementById('cart-summary').innerHTML = `
      <div style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:14px;font-weight:700;text-align:center">Hiệu Suất Tổng Hợp (${items.length} TS)</div>
      <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:13px">
        <span style="color:var(--text-2)">Thay đổi NAV</span>
        <span style="font-family:var(--mono);font-weight:600;color:${totalNavDelta>=0?'var(--emerald)':'var(--red)'};font-size:14px">${totalNavDelta>=0?'+':''}${totalNavDelta.toFixed(2)} Tỷ</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:13px">
        <span style="color:var(--text-2)">Dòng Tiền Cải Thiện</span>
        <span style="font-family:var(--mono);font-weight:600;color:${totalCfDelta>=0?'var(--emerald)':'var(--red)'};font-size:14px">${totalCfDelta>=0?'+':''}${totalCfDelta.toFixed(1)} Tr/tháng</span>
      </div>
      <div style="display:flex;justify-content:space-between;border-top:1px dashed var(--bg-border);padding-top:12px;font-size:13px">
        <span style="color:var(--text-2)">${capLabel}</span>
        <span style="font-family:var(--mono);font-weight:700;color:${capColor};font-size:14px">${capSign}${capFormatted}</span>
      </div>
    `;
  }
</script>
  <script>
    window.MARKET_DATA ="""

if target_2 in content:
    content = content.replace(target_2, replacement_2)
    print("Replaced chunk 2 (Cart UI and Logic)")
else:
    print("Target 2 not found")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
