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

# ══ P4-24: Favicon emoji 💎 ══
rep(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>💎</text></svg>">',
    'P4-24: Thêm Favicon 💎'
)

# ══ P4-19: Rút ngắn tab text ══
rep(
    '<span class="tab-step">01</span> 🏥 Triage — Nhập Liệu',
    '<span class="tab-step">01</span> 🏥 Triage',
    'P4-19a: Tab Triage rút gọn'
)
rep(
    '<span class="tab-step">02</span> 🩺 Diagnosis — Chẩn Đoán',
    '<span class="tab-step">02</span> 🩺 Chẩn Đoán',
    'P4-19b: Tab Diagnosis rút gọn'
)
rep(
    '<span class="tab-step">03</span> 🎮 Surgery — What-If',
    '<span class="tab-step">03</span> 🎮 Surgery',
    'P4-19c: Tab Surgery rút gọn'
)
rep(
    '<span class="tab-step">04</span> 📋 Prescription — Báo Cáo',
    '<span class="tab-step">04</span> 📋 Báo Cáo',
    'P4-19d: Tab Prescription rút gọn'
)

# ══ P4-20: Badge Pha trong Asset Card ══
# c_q is already computed from P2 fix, c_q.phase is available
# Add phase constants before the list.innerHTML
rep(
    '  list.innerHTML = PORTFOLIO.map((a, i) => {\n    const gain     = a.market && a.cost ? ((a.market - a.cost) / a.cost * 100) : 0;',
    '''  const PHASE_META = {
    1:{ label:'Pha 1 — Chính Sách', color:'#3B82F6', bg:'rgba(59,130,246,.12)' },
    2:{ label:'Pha 2 — Di Dân',     color:'#EAB308', bg:'rgba(234,179,8,.12)'  },
    3:{ label:'Pha 3 — Dòng Tiền',  color:'#10B981', bg:'rgba(16,185,129,.12)' },
    4:{ label:'Pha 4 — Tích Sản',   color:'#A855F7', bg:'rgba(168,85,247,.12)' },
  };
  list.innerHTML = PORTFOLIO.map((a, i) => {
    const gain     = a.market && a.cost ? ((a.market - a.cost) / a.cost * 100) : 0;''',
    'P4-20a: Khai báo PHASE_META'
)

# Add phase badge computation after c_q line
rep(
    '    const c_q  = calcAsset(a);\n    const dscr = c_q.dscr !== null ? c_q.dscr.toFixed(2) : \'N/A\';',
    '''    const c_q  = calcAsset(a);
    const phMeta = PHASE_META[c_q.phase] || PHASE_META[2];
    const phaseBadge = `<span style="display:inline-flex;align-items:center;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700;background:${phMeta.bg};color:${phMeta.color};border:1px solid ${phMeta.color}33;white-space:nowrap">${phMeta.label}</span>`;
    const dscr = c_q.dscr !== null ? c_q.dscr.toFixed(2) : 'N/A';''',
    'P4-20b: Tính phaseBadge cho mỗi asset'
)

# Add health score mini display + phase badge into card
rep(
    '''      <div style="flex:1;min-width:180px">
        <div style="font-weight:600;font-size:13px">${a.name}</div>
        <div style="font-size:11px;color:var(--text-2)">${TYPE_LABEL[a.type]||a.type} · ${a.district||'Chưa chọn'} · ${GOAL_LABEL[a.goal]||a.goal}</div>
      </div>''',
    '''      <div style="flex:1;min-width:180px">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px">
          <span style="font-weight:600;font-size:13px">${a.name}</span>
          ${phaseBadge}
        </div>
        <div style="font-size:11px;color:var(--text-2)">${TYPE_LABEL[a.type]||a.type} · ${a.district||'Chưa chọn'} · ${GOAL_LABEL[a.goal]||a.goal}</div>
      </div>''',
    'P4-20c: Hiển thị phase badge trong asset card'
)

# Also add Health score in KPI row
rep(
    '''        <div>
          <div style="color:var(--text-3);font-size:10px">CYCLE</div>
          <div style="color:${cycleColor}">${cycle}/100</div>
        </div>
      </div>
      <div style="display:flex;gap:6px;flex-shrink:0">''',
    '''        <div>
          <div style="color:var(--text-3);font-size:10px">CYCLE</div>
          <div style="color:${cycleColor}">${cycle}/100</div>
        </div>
        <div>
          <div style="color:var(--text-3);font-size:10px">HEALTH</div>
          <div style="color:${c_q.health>=65?'var(--emerald)':c_q.health>=40?'var(--yellow)':'var(--red)'};font-weight:700">${c_q.health}/100</div>
        </div>
      </div>
      <div style="display:flex;gap:6px;flex-shrink:0">''',
    'P4-20d: Thêm HEALTH score vào KPI row'
)

# ══ P4-22: PDF table font size improvements ══
# Find section III table font sizes in the HTML template (in buildPrescription)
# The table headers use font-size:11px for some cells
rep(
    "      <table style=\"width:100%;border-collapse:collapse;font-size:11px;font-family:'Segoe UI',sans-serif\">",
    "      <table style=\"width:100%;border-collapse:collapse;font-size:12px;font-family:'Segoe UI',sans-serif\">",
    'P4-22a: PDF table III font 11→12px'
)

# Section IV table (chi tiet)
rep(
    '    <table style="width:100%;border-collapse:collapse;font-size:11px">',
    '    <table style="width:100%;border-collapse:collapse;font-size:12px">',
    'P4-22b: PDF table IV font 11→12px'
)

# ══ P4: Highlight khu vực trong Market Data table ══
# Add CSS to highlight matched districts in mkt-table
rep(
    '.mkt-table tr:hover td { background: var(--bg-hover); }',
    '.mkt-table tr:hover td { background: var(--bg-hover); }\n.mkt-table tr.highlight td { background: rgba(212,175,55,0.06); border-left: 2px solid var(--gold-dim); }',
    'P4: CSS highlight matched districts'
)

# In renderDiagnosis, highlight portfolio districts in market table
# Find the market table render section
rep(
    '  // Market table — show all districts',
    '''  // Mark portfolio districts for highlight in market table
  const portfolioDistricts = new Set(portfolio.map(a => a.district));
  // Market table — show all districts''',
    'P4: Portfolio districts set for highlight'
)
rep(
    "          const highlight = portfolioDistricts.has(d.name) ? ' highlight' : '';",
    "          const highlight = portfolioDistricts.has(d.name) ? ' highlight' : '';",
    'P4: Already highlighted (no-op check)'
)

# Find and update the district row rendering in renderDiagnosis  
rep(
    "      rows += `<tr><td>${d.name}</td>",
    "      rows += `<tr class=\"${portfolioDistricts.has(d.name)?'highlight':''}\"><td>${portfolioDistricts.has(d.name)?'<strong>'+d.name+'</strong>':d.name}</td>",
    'P4: Highlight portfolio districts in market table'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== P4 DESIGN POLISH RESULTS ===')
for r in results: print(' ', r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob,cb = s.count('{'),s.count('}')
    bt = s.count('`')
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"})')

checks = [
    ('Favicon',             'rel="icon"' in v),
    ('Tab Triage short',    'tab-step">01</span> 🏥 Triage\n' in v or '">01</span> 🏥 Triage\r' in v),
    ('PHASE_META defined',  'PHASE_META' in v),
    ('phaseBadge',          'phaseBadge' in v),
    ('Phase badge in card', 'phMeta.label' in v),
    ('HEALTH in KPI',       'HEALTH' in v),
    ('PDF font 12px',       'font-size:12px' in v),
    ('Highlight CSS',       'highlight' in v and 'border-left: 2px solid var(--gold-dim)' in v),
]
ok = err = 0
for name, check in checks:
    print(f'  {"✅" if check else "❌"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\nTotal: {ok} OK / {err} err')
print(f'File: {len(v):,} bytes')
