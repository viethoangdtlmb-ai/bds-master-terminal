import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update runAllScenarios to store inputs
target_run = """        const rows = sc.calc(inputs);
        results.push({ sc, rows });"""
repl_run = """        const rows = sc.calc(inputs);
        results.push({ sc, rows, inputs });"""
if target_run in content:
    content = content.replace(target_run, repl_run)

# 2. Update saveToCart to save inputs
target_save = """    window._STRATEGY_CART[window._SIM_ASSET.name] = {
      asset: window._SIM_ASSET,
      calc: window._SIM_CALC,
      scenario: res.sc,
      rows: res.rows
    };"""
repl_save = """    window._STRATEGY_CART[window._SIM_ASSET.name] = {
      asset: window._SIM_ASSET,
      calc: window._SIM_CALC,
      scenario: res.sc,
      rows: res.rows,
      inputs: res.inputs
    };"""
if target_save in content:
    content = content.replace(target_save, repl_save)

# 3. Add getVirtualPortfolio logic
new_js_logic = """  function getVirtualPortfolio() {
    const base = JSON.parse(JSON.stringify(window.SESSION_PORTFOLIO || PORTFOLIO));
    const cartItems = Object.values(window._STRATEGY_CART || {});
    if (cartItems.length === 0) return base;

    let vPort = [];
    base.forEach(a => {
        const item = cartItems.find(it => !it.isBuyNew && it.asset.name === a.name);
        if (!item) {
            vPort.push(a);
            return;
        }
        const scId = item.scenario.id;
        if (scId.startsWith('ban-')) {
            // Bán -> Loại bỏ khỏi danh mục
            return;
        } else if (scId === 'tai-co-cau') {
            a.rate = parseFloat(item.inputs['sc-rate']) || a.rate;
            a.grace = parseFloat(item.inputs['sc-grace']) || a.grace;
            a.loanterm = parseFloat(item.inputs['sc-term']) || a.loanterm;
            vPort.push(a);
        } else if (scId === 'cai-tao') {
            const capex = (parseFloat(item.inputs['sd-capex']) || 0) / 1000;
            const newRent = parseFloat(item.inputs['sd-rent']) || a.rent;
            a.cost = (a.cost || 0) + capex;
            a.rent = newRent;
            // Market value delta based on NOI cap rate 4.5%
            const c = calcAsset(a);
            const mgmt = a.rent > 0 && a.mgmt > 0 ? (a.rent * (a.mgmt/100)) : 0;
            const maint = (a.market || 0) * 1000 * (a.maint/100) / 12; // Approximation
            const newNOI = a.rent - mgmt - maint;
            const deltaNOI = newNOI - (c.noi || 0);
            if (deltaNOI > 0) {
                const addVal = (deltaNOI * 12) / 0.045 / 1000;
                a.market = (a.market || 0) + addVal;
            }
            vPort.push(a);
        } else {
            vPort.push(a);
        }
    });

    cartItems.forEach(it => {
        if (it.isBuyNew) {
            vPort.push({
                _id: 'v-new-' + Date.now(),
                name: it.name,
                type: 'nha-rieng',
                market: it.price,
                cost: it.price,
                debt: it.debtTy * 1000,
                autoDebt: it.debtTy * 1000,
                year: new Date().getFullYear(),
                rate: 9, // estimated
                rent: it.cf + ((it.debtTy*1000) * (9/100/12)), // Reverse engineer rent roughly
                mgmt: 0,
                maint: 0
            });
        }
    });
    return vPort;
  }

  window._IS_VIRTUAL_MODE = false;
  function toggleVirtualMode() {
    window._IS_VIRTUAL_MODE = !window._IS_VIRTUAL_MODE;
    buildPrescription();
  }
"""
# inject right before function buildPrescription
if "function buildPrescription() {" in content:
    content = content.replace("function buildPrescription() {", new_js_logic + "function buildPrescription() {")

# 4. Modify buildPrescription to use Virtual Portfolio and add Toggle Button
target_build = """    function buildPrescription() {
      try {
        const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;"""
repl_build = """    function buildPrescription() {
      try {
        let portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;
        if (window._IS_VIRTUAL_MODE) {
            portfolio = getVirtualPortfolio();
        }"""
if target_build in content:
    content = content.replace(target_build, repl_build)

# 5. Add UI switch in Rx Header
target_header = """<div style="font-size:12px;color:#9CA3AF;margin-top:2px">Hệ Điều Hành Chẩn Đoán Danh Mục BĐS — Hoàng Việt</div>
</div>"""
repl_header = """<div style="font-size:12px;color:#9CA3AF;margin-top:2px">Hệ Điều Hành Chẩn Đoán Danh Mục BĐS — Hoàng Việt</div>
</div>
<div>
  <button class="btn btn-sm" style="background:${window._IS_VIRTUAL_MODE ? '#059669' : '#374151'};color:#fff;border:1px solid ${window._IS_VIRTUAL_MODE ? '#10b981' : '#4B5563'}" onclick="toggleVirtualMode()">
    ${window._IS_VIRTUAL_MODE ? '✅ ĐANG XEM: DANH MỤC SAU CƠ CẤU' : '👁️ XEM DANH MỤC SAU KHI DÙNG TÚI CHIẾN LƯỢC'}
  </button>
</div>"""
if target_header in content:
    content = content.replace(target_header, repl_header)
    
with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched Virtual Portfolio logic")
