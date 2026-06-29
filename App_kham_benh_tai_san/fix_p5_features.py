import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n')

results = []
def rep(old, new, tag):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        results.append(f'✅ {tag}')
    else:
        results.append(f'❌ {tag} — NOT FOUND')

# ══════════════════════════════════════════════════════════════
# P5-25: Session AutoSave Badge + Timestamp trong Header
# ══════════════════════════════════════════════════════════════
rep(
    '    <div class="header-right">\n      <div id="market-stamp">',
    '''    <div class="header-right">
      <div id="save-badge" style="display:none;align-items:center;gap:5px;font-family:var(--mono);font-size:11px;color:var(--emerald);padding:3px 9px;background:rgba(0,194,122,0.08);border:1px solid var(--emerald-dim);border-radius:var(--r-sm);transition:opacity 1s">
        💾 <span id="save-time"></span>
      </div>
      <div id="market-stamp">''',
    'P5-25a: Thêm save-badge vào header'
)

rep(
    "function savePortfolio() {\n  localStorage.setItem('aa_portfolio', JSON.stringify(PORTFOLIO));\n}",
    """function savePortfolio() {
  localStorage.setItem('aa_portfolio', JSON.stringify(PORTFOLIO));
  // AutoSave badge
  const sb = document.getElementById('save-badge');
  const st = document.getElementById('save-time');
  if (sb && st) {
    st.textContent = new Date().toLocaleTimeString('vi',{hour:'2-digit',minute:'2-digit'});
    sb.style.display = 'flex';
    sb.style.opacity = '1';
    clearTimeout(sb._fadeTimer);
    sb._fadeTimer = setTimeout(() => { sb.style.opacity = '0.5'; }, 3000);
  }
}""",
    'P5-25b: savePortfolio cập nhật badge timestamp'
)

# ══════════════════════════════════════════════════════════════
# P5-26: Export / Import JSON Portfolio
# ══════════════════════════════════════════════════════════════
# Update portfolio-panel header: thêm nút Export/Import + hidden file input
rep(
    '      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">\n        <div class="section-title" style="margin:0">🏠 Danh Mục Tài Sản <span id="asset-count-badge" class="badge badge-gold" style="margin-left:6px">0 tài sản</span></div>\n        <button class="btn btn-primary btn-sm" id="btn-diagnose-all" onclick="diagnoseAll()" style="display:none">🩺 Chẩn đoán toàn danh mục →</button>',
    '''      <input type="file" id="import-file" accept=".json" style="display:none" onchange="handleImport(event)">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px">
        <div class="section-title" style="margin:0">🏠 Danh Mục Tài Sản <span id="asset-count-badge" class="badge badge-gold" style="margin-left:6px">0 tài sản</span></div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">
          <button class="btn btn-secondary btn-sm" onclick="importPortfolio()" title="Import danh mục từ file JSON backup">📥 Import</button>
          <button class="btn btn-secondary btn-sm" id="btn-export" onclick="exportPortfolio()" style="display:none" title="Xuất danh mục ra file JSON để backup">📤 Export</button>
          <button class="btn btn-primary btn-sm" id="btn-diagnose-all" onclick="diagnoseAll()" style="display:none">🩺 Chẩn đoán →</button>
        </div>''',
    'P5-26a: Thêm nút Export/Import vào portfolio panel'
)

# Show/hide export btn in renderAssetList
rep(
    "  badge.textContent = `${PORTFOLIO.length} tài sản`;\n  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';\n  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';",
    """  badge.textContent = `${PORTFOLIO.length} tài sản`;
  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';
  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';
  const btnExp = document.getElementById('btn-export');
  if (btnExp) btnExp.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';""",
    'P5-26b: Hiện nút Export khi có tài sản'
)

# Add Export/Import functions
rep(
    'function savePortfolio() {',
    '''function exportPortfolio() {
  if (!PORTFOLIO.length) { alert('Danh mục rỗng, không có gì để xuất!'); return; }
  const data = JSON.stringify(PORTFOLIO, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `danh-muc-bds-${new Date().toISOString().slice(0,10)}.json`;
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
      if (!confirm('Import ' + data.length + ' tài sản?\\nDữ liệu hiện tại sẽ bị thay thế.')) return;
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

function savePortfolio() {''',
    'P5-26c: Export/Import functions'
)

# ══════════════════════════════════════════════════════════════
# P5-28: Tooltips cho DSCR / CYCLE / HEALTH trong Asset Card
# ══════════════════════════════════════════════════════════════
rep(
    '          <div style="color:var(--text-3);font-size:10px">DSCR</div>',
    '          <div style="color:var(--text-3);font-size:10px;cursor:help" title="DSCR = Thu nhập / Trả nợ tháng. ≥1.0 = Thoải mái ✅ | 0.5-1.0 = Căng ⚠️ | <0.5 = Nguy hiểm 🚨">DSCR</div>',
    'P5-28a: Tooltip DSCR'
)
rep(
    '          <div style="color:var(--text-3);font-size:10px">CYCLE</div>',
    '          <div style="color:var(--text-3);font-size:10px;cursor:help" title="Chu kỳ thị trường 0-100. >70 = đỉnh chu kỳ (nguy hiểm mua) | <40 = đáy (cơ hội) | theo dữ liệu crawler">CYCLE</div>',
    'P5-28b: Tooltip CYCLE'
)
rep(
    '          <div style="color:var(--text-3);font-size:10px">HEALTH</div>',
    '          <div style="color:var(--text-3);font-size:10px;cursor:help" title="Health Score 0-100 = 40% DSCR + 40% ROE + 20% Views/Tin. ≥65 MẠNH | 40-65 CẦN TỐI ƯU | <40 NGUY HIỂM">HEALTH</div>',
    'P5-28c: Tooltip HEALTH'
)

# ══════════════════════════════════════════════════════════════
# P5-29: Giá Sàn Hoà Vốn trong Asset Card KPI row
# ══════════════════════════════════════════════════════════════
rep(
    '''        <div>
          <div style="color:var(--text-3);font-size:10px;cursor:help" title="Health Score 0-100 = 40% DSCR + 40% ROE + 20% Views/Tin. ≥65 MẠNH | 40-65 CẦN TỐI ƯU | <40 NGUY HIỂM">HEALTH</div>
          <div style="color:${c_q.health>=65?'var(--emerald)':c_q.health>=40?'var(--yellow)':'var(--red)'};font-weight:700">${c_q.health}/100</div>
        </div>
      </div>
      <div style="display:flex;gap:6px;flex-shrink:0">''',
    '''        <div>
          <div style="color:var(--text-3);font-size:10px;cursor:help" title="Health Score 0-100 = 40% DSCR + 40% ROE + 20% Views/Tin. ≥65 MẠNH | 40-65 CẦN TỐI ƯU | <40 NGUY HIỂM">HEALTH</div>
          <div style="color:${c_q.health>=65?'var(--emerald)':c_q.health>=40?'var(--yellow)':'var(--red)'};font-weight:700">${c_q.health}/100</div>
        </div>
        <div>
          <div style="color:var(--text-3);font-size:10px;cursor:help" title="Giá bán tối thiểu để hòa vốn (vốn gốc + lãi NH theo năm giữ + phí 2% + phí sang tên 1.5%)">GIÁ SÀN</div>
          <div style="color:${a.market>=c_q.floorPrice?'var(--emerald)':'var(--red)'};">${c_q.floorPrice.toFixed(2)} Tỷ${a.market>=c_q.floorPrice?' ✅':' 🔴'}</div>
        </div>
      </div>
      <div style="display:flex;gap:6px;flex-shrink:0">''',
    'P5-29: Thêm GIÁ SÀN hoà vốn vào KPI row'
)

# ══════════════════════════════════════════════════════════════
# P5-27: Quick Print từ Triage (tóm tắt danh mục)
# ══════════════════════════════════════════════════════════════
rep(
    "          <button class=\"btn btn-primary btn-sm\" id=\"btn-diagnose-all\" onclick=\"diagnoseAll()\" style=\"display:none\">🩺 Chẩn đoán →</button>",
    """          <button class="btn btn-secondary btn-sm" id="btn-print-quick" onclick="quickPrintSummary()" style="display:none" title="In tóm tắt nhanh không cần Prescription">🖨️</button>
          <button class="btn btn-primary btn-sm" id="btn-diagnose-all" onclick="diagnoseAll()" style="display:none">🩺 Chẩn đoán →</button>""",
    'P5-27a: Thêm nút Quick Print vào portfolio panel'
)

# Show quick print btn in renderAssetList
rep(
    "  const btnExp = document.getElementById('btn-export');\n  if (btnExp) btnExp.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';",
    """  const btnExp = document.getElementById('btn-export');
  if (btnExp) btnExp.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';
  const btnQP = document.getElementById('btn-print-quick');
  if (btnQP) btnQP.style.display = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';""",
    'P5-27b: Hiện Quick Print khi có tài sản'
)

# Add quickPrintSummary function
rep(
    'function exportPortfolio() {',
    '''function quickPrintSummary() {
  if (!PORTFOLIO.length) return;
  const now = new Date().toLocaleDateString('vi-VN', {day:'2-digit',month:'2-digit',year:'numeric'});
  const tMkt = PORTFOLIO.reduce((s,a)=>s+(a.market||0),0);
  const tEq  = PORTFOLIO.reduce((s,a)=>s+(a.cost||0)*(1-(a.loanpct||0)/100),0);
  const tCF  = PORTFOLIO.reduce((s,a)=>s+calcAsset(a).cashflow,0);
  const rows = PORTFOLIO.map((a,i)=>{
    const c = calcAsset(a);
    const phLabel = {1:'Pha 1',2:'Pha 2',3:'Pha 3',4:'Pha 4'}[c.phase]||'?';
    const dscrTxt = c.dscr!==null?c.dscr.toFixed(2):'N/A';
    return `<tr style="border-bottom:1px solid #eee">
      <td style="padding:6px 8px">${i+1}. ${a.name}</td>
      <td style="padding:6px 8px;text-align:center">${phLabel}</td>
      <td style="padding:6px 8px;text-align:right">${a.market} Tỷ</td>
      <td style="padding:6px 8px;text-align:center;color:${dscrTxt==='N/A'?'#888':parseFloat(dscrTxt)>=1?'#059669':'#DC2626'}">${dscrTxt}</td>
      <td style="padding:6px 8px;text-align:center;color:${c.health>=65?'#059669':c.health>=40?'#D97706':'#DC2626'}">${c.health}/100</td>
    </tr>`;
  }).join('');
  const win = window.open('','_blank','width=800,height=600');
  win.document.write(`<!DOCTYPE html><html><head><title>Tóm Tắt Danh Mục — ${now}</title>
  <style>body{font-family:Arial,sans-serif;padding:24px;font-size:13px}h2{color:#1C1C2E}table{width:100%;border-collapse:collapse}th{background:#F1F5F9;padding:8px;text-align:left;font-size:11px;color:#6B7280;text-transform:uppercase}@media print{button{display:none}}</style>
  </head><body>
  <h2>📋 Tóm Tắt Danh Mục BĐS — ${now}</h2>
  <div style="display:flex;gap:24px;margin-bottom:16px;padding:12px;background:#F8FAFC;border-radius:8px">
    <div><div style="font-size:11px;color:#6B7280">Tổng Giá Trị</div><div style="font-size:20px;font-weight:700;color:#D4AF37">${tMkt.toFixed(1)} Tỷ</div></div>
    <div><div style="font-size:11px;color:#6B7280">Vốn Tự Có</div><div style="font-size:20px;font-weight:700">${tEq.toFixed(1)} Tỷ</div></div>
    <div><div style="font-size:11px;color:#6B7280">CF/Tháng</div><div style="font-size:20px;font-weight:700;color:${tCF>=0?'#059669':'#DC2626'}">${tCF>=0?'+':''}${tCF.toFixed(1)} Tr</div></div>
  </div>
  <table><thead><tr><th>Tài Sản</th><th>Pha</th><th>Giá TT</th><th>DSCR</th><th>Health</th></tr></thead>
  <tbody>${rows}</tbody></table>
  <div style="margin-top:16px;font-size:11px;color:#9CA3AF">Asset Architect OS — In nhanh từ Triage · ${now}</div>
  <button onclick="window.print()" style="margin-top:12px;padding:8px 16px;background:#D4AF37;border:none;cursor:pointer;border-radius:4px;font-weight:700">🖨️ In / Xuất PDF</button>
  </body></html>`);
  win.document.close();
}

function exportPortfolio() {''',
    'P5-27c: quickPrintSummary function'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== P5 FEATURE RESULTS ===')
for r in results: print(' ', r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob, cb = s.count('{'), s.count('}')
    bt = s.count('`')
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"})')

checks = [
    ('P5-25 Save badge HTML',       'id="save-badge"' in v),
    ('P5-25 Save badge JS',         'save-time' in v and '_fadeTimer' in v),
    ('P5-26 Import file input',     'id="import-file"' in v),
    ('P5-26 Export fn',             'function exportPortfolio()' in v),
    ('P5-26 Import fn',             'function importPortfolio()' in v),
    ('P5-26 handleImport fn',       'function handleImport' in v),
    ('P5-27 Quick print btn',       'id="btn-print-quick"' in v),
    ('P5-27 quickPrintSummary fn',  'function quickPrintSummary()' in v),
    ('P5-28 DSCR tooltip',          'DSCR = Thu nhập' in v),
    ('P5-28 CYCLE tooltip',         'Chu kỳ thị trường' in v),
    ('P5-28 HEALTH tooltip',        'Health Score 0-100' in v),
    ('P5-29 GIÁ SÀN in card',       'GIÁ SÀN' in v),
    ('P5-29 floorPrice display',    'c_q.floorPrice.toFixed' in v),
]
ok = err = 0
for name, check in checks:
    print(f'  {"✅" if check else "❌"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\nTotal: {ok}/{len(checks)} OK')
print(f'File: {len(v):,} bytes | {v.count(chr(10)):,} lines')
