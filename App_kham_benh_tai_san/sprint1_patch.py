import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    raw = f.read()

content = raw.replace('\r\n', '\n').replace('\r', '\n')
results = []

def replace_once(old, new, tag):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        results.append(f'✅ {tag}')
    else:
        results.append(f'❌ {tag} — KHÔNG TÌM THẤY')

# ══ A: ĐỔI TÊN 4 PHA ══
replace_once("label:'Pha 1 — Bứt Tốc'",
             "label:'Pha 1 — Chính sách, Hạ Tầng'",
             'Pha 1 label')

replace_once("desc:'Hạ tầng đang kéo, dân cư chưa về — lướt sóng 1-3 năm. Rủi ro thanh khoản cao.'",
             "desc:'Tiềm năng X2-X3 theo hạ tầng. Rủi ro biến động vùng — lướt sóng 1-3 năm.'",
             'Pha 1 desc')

replace_once("label:'Pha 3 — Trưởng Thành'",
             "label:'Pha 3 — Dòng tiền'",
             'Pha 3 label')

replace_once("desc:'Khu vực ổn định, có dòng tiền thuê — ưu tiên 5-7 năm. Tăng trưởng ổn.'",
             "desc:'Mạch máu của hệ thống — tạo thu nhập hàng tháng để gánh lãi cho các pha tăng trưởng.'",
             'Pha 3 desc')

replace_once("desc:'Dân đang về, giá vẫn tăng — đầu tư 3-5 năm, chưa có dòng tiền thuê.'",
             "desc:'Vùng ven đô thị hóa. Dân đang về, giá tăng — rủi ro pháp lý & CĐT. Nắm giữ 3-5 năm.'",
             'Pha 2 desc')

# Fix typo
if 'muâu ngộp' in content:
    content = content.replace('muâu ngộp', 'mua ngộp')
    results.append('✅ Fix typo muâu→mua ngộp')

# Fix typo in asset list card
replace_once('<div style="color:var(--text-3);font-size:10px">"LÃI VỐN</div>',
             '<div style="color:var(--text-3);font-size:10px">LÃI VỐN</div>',
             'Fix spurious quote in asset card')

# ══ B: CẬP NHẬT KPI Pha 3: logic + label ══
# Đổi màu: cũ = nhiều Pha3 → danger; mới = không có Pha3 → danger
replace_once(
    "const ph3Color = ph3Count/n >= 0.5 ? 'danger' : ph3Count > 0 ? 'warn' : 'ok';",
    "const ph3Color = ph3Count === 0 ? 'danger' : ph3Count/n >= 0.3 ? 'ok' : 'warn';",
    'ph3Color logic')

# Thêm totalMarket, totalCost sau totalEquity
replace_once(
    "  const totalEquity = calcs.reduce((s,{c}) => s+c.equity, 0);",
    "  const totalEquity = calcs.reduce((s,{c}) => s+c.equity, 0);\n  const totalMarket = calcs.reduce((s,{a}) => s+(a.market||0), 0);\n  const totalCost   = calcs.reduce((s,{a}) => s+(a.cost||0), 0);\n  const mktGain     = totalMarket - totalCost;\n  const mktColor    = mktGain >= 0 ? 'ok' : 'danger';",
    'Add totalMarket vars')

# ══ C: CẬP NHẬT KPI CARD Pha 3 + thêm card 5 ══
old_ph3_card = '''    <div class="stat-card ${ph3Color}"><div class="stat-label">Tài Sản Pha 3</div><div class="stat-value">${ph3Count}<small style="font-size:14px"> / ${n}</small></div><div class="stat-sub">${ph3Count>0?'⚠️ Đang ngủ đông — cần phâu thuật':'✅ Tất cả đang tăng trưởng'}</div></div>`;'''

new_ph3_card = '''    <div class="stat-card ${ph3Color}"><div class="stat-label">Tài Sản Pha 3 (Dòng Tiền)</div><div class="stat-value">${ph3Count}<small style="font-size:14px"> / ${n}</small></div><div class="stat-sub">${ph3Count===0?'🔴 Không có nguồn dòng tiền':'✅ Mạch máu hệ thống ổn định'}</div></div>
    <div class="stat-card ${mktColor}"><div class="stat-label">Tổng Giá Trị Tài Sản</div><div class="stat-value">${totalMarket.toFixed(1)}<small style="font-size:14px"> Tỷ</small></div><div class="stat-sub">Vốn gốc: ${totalCost.toFixed(1)} Tỷ &nbsp;|&nbsp; <span style="color:${mktGain>=0?'var(--emerald)':'var(--red)'}">${mktGain>=0?'+':''}${mktGain.toFixed(1)} Tỷ</span></div></div>`;'''

replace_once(old_ph3_card, new_ph3_card, 'KPI cards: Pha3 + Tổng Giá Trị')

# ══ D: GRID-4 → auto-fit để chứa 5 thẻ ══
replace_once(
    '<div class="grid-4" id="diag-kpi" style="margin-bottom:20px">',
    '<div id="diag-kpi" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px;margin-bottom:20px">',
    'diag-kpi grid style')

# ══ E: PORTFOLIO SUMMARY STRIP trong HTML Triage ══
replace_once(
    '      <div id="asset-list"></div>\n    </div>',
    '      <div id="portfolio-summary" style="display:none;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;background:var(--bg-card);border:1px solid var(--bg-border);border-radius:var(--r-md);padding:14px 16px"></div>\n      <div id="asset-list"></div>\n    </div>',
    'Portfolio summary HTML')

# ══ F: CẬP NHẬT renderAssetList() — thêm summary strip logic ══
old_render_end = '''  badge.textContent = `${PORTFOLIO.length} tài sản`;
  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';
  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';'''

new_render_end = '''  badge.textContent = `${PORTFOLIO.length} tài sản`;
  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';
  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';

  // Portfolio Summary Strip
  const sumDiv = document.getElementById('portfolio-summary');
  if (sumDiv) {
    if (PORTFOLIO.length === 0) { sumDiv.style.display = 'none'; }
    else {
      const tMkt  = PORTFOLIO.reduce((s,a) => s+(a.market||0), 0);
      const tCost = PORTFOLIO.reduce((s,a) => s+(a.cost||0), 0);
      const tEq   = PORTFOLIO.reduce((s,a) => s+(a.cost||0)*(1-(a.loanpct||0)/100), 0);
      const tDebt = PORTFOLIO.reduce((s,a) => s+(a.debt||0), 0);
      const tCF   = PORTFOLIO.reduce((s,a) => {
        const noi = (a.rent||0)-(a.mgmt||0)-(a.maint||0)/12;
        const dtb = (a.debt||0)*1000*(a.rate||0)/100/12;
        return s + noi - dtb;
      }, 0);
      const gain  = tMkt - tCost;
      const mkStat = (label, val, sub, color) =>
        `<div style="text-align:center"><div style="font-size:10px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${label}</div><div style="font-family:var(--mono);font-size:18px;font-weight:700;color:${color}">${val}</div><div style="font-size:11px;color:var(--text-2);margin-top:2px">${sub}</div></div>`;
      sumDiv.style.display = 'grid';
      sumDiv.innerHTML =
        mkStat('Tổng Giá Trị', tMkt.toFixed(1)+' Tỷ',
          (gain>=0?'+':'')+gain.toFixed(1)+' Tỷ so vốn gốc',
          'var(--gold)') +
        mkStat('Vốn Tự Có', tEq.toFixed(1)+' Tỷ',
          PORTFOLIO.length+' tài sản',
          'var(--text-1)') +
        mkStat('Tổng Dư Nợ', tDebt.toFixed(1)+' Tỷ',
          'Nợ NH hiện tại',
          tDebt>0?'var(--yellow)':'var(--text-1)') +
        mkStat('Dòng Tiền/Tháng', (tCF>=0?'+':'')+tCF.toFixed(1)+' Tr',
          'Ước tính lãi vay cơ bản',
          tCF>=0?'var(--emerald)':'var(--red)');
    }
  }'''

replace_once(old_render_end, new_render_end, 'renderAssetList summary strip logic')

# ══ WRITE BACK ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 1 KẾT QUẢ ===')
for r in results:
    print(r)

# Verify
with open(FILE, 'r', encoding='utf-8') as f:
    verify = f.read()

ok  = sum(1 for r in results if r.startswith('✅'))
err = sum(1 for r in results if r.startswith('❌'))
print(f'\nTổng: {ok} thành công / {err} lỗi')
if 'Pha 1 — Chính sách' in verify: print('✅ Verify: Pha 1 đúng')
if 'Pha 3 — Dòng tiền' in verify:  print('✅ Verify: Pha 3 đúng')
if 'totalMarket' in verify:         print('✅ Verify: totalMarket có')
if 'Tổng Giá Trị Tài Sản' in verify:print('✅ Verify: Card tổng giá trị có')
if 'portfolio-summary' in verify:   print('✅ Verify: Summary strip HTML có')
