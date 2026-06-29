import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n').replace('\r', '\n')
results = []

def rep(old, new, tag):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        results.append(f'✅ {tag}')
    else:
        results.append(f'❌ {tag}')

# ══ 1: HTML — Add radar section between investor-profile-box and Asset Matrix ══
OLD_RADAR_ANCHOR = '''      <!-- Asset Matrix 4 Pha -->
      <div class="grid-2" style="margin-bottom:20px">'''

NEW_RADAR_ANCHOR = '''      <!-- Sprint 4: Radar Chart -->
      <div id="diag-radar-section" style="display:none;margin-bottom:20px">
        <div class="grid-2" style="align-items:start">
          <div class="card" style="text-align:center">
            <div class="card-header"><span class="card-title">🕸️ Radar Sức Khỏe Danh Mục</span></div>
            <div id="diag-radar" style="display:flex;justify-content:center;padding:8px 0"></div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">📐 5 Trục Đánh Giá</span></div>
            <div id="diag-radar-legend" style="padding:4px 0"></div>
          </div>
        </div>
      </div>
      <!-- Asset Matrix 4 Pha -->
      <div class="grid-2" style="margin-bottom:20px">'''

rep(OLD_RADAR_ANCHOR, NEW_RADAR_ANCHOR, 'Radar section HTML')

# ══ 2: JS — Call renderRadarChart in renderDiagnosis (after profile box) ══
OLD_PROFILE_BOX_END = '''  // ── Red Alerts (Module 2 — Báo Động Đỏ) ───────────────────────────'''

NEW_PROFILE_BOX_END = '''  // ── Radar Chart ──────────────────────────────────────────────────────
  renderRadarChart(portfolio, calcs);

  // ── Red Alerts (Module 2 — Báo Động Đỏ) ───────────────────────────'''

rep(OLD_PROFILE_BOX_END, NEW_PROFILE_BOX_END, 'callRadarChart in renderDiagnosis')

# ══ 3: JS — Add renderRadarChart function before DIAGNOSIS ENGINE ══
RADAR_FUNC = '''
// ── Radar Chart Engine ──────────────────────────────────────────────────
function renderRadarChart(portfolio, calcs) {
  const box = document.getElementById('diag-radar');
  const legend = document.getElementById('diag-radar-legend');
  const section = document.getElementById('diag-radar-section');
  if (!box || !legend || !section || !calcs.length) return;
  section.style.display = 'block';

  const n = calcs.length;
  const avgHealth = calcs.reduce((s,{c}) => s+c.health, 0) / n;
  const totalCF   = calcs.reduce((s,{c}) => s+c.cashflow, 0);
  const avgLoan   = portfolio.reduce((s,a) => s+(a.loanpct||0), 0) / n;
  const avgGainPct= calcs.reduce((s,{c}) => s+(c.gainPct||0), 0) / n;
  const phases    = new Set(calcs.map(({c}) => c.phase));

  // Each metric normalized 0→1
  const scores = [
    { label:'Sức Khỏe',   val: Math.max(0, Math.min(1, avgHealth/100)),                     color:'#10B981', desc:`TB ${avgHealth.toFixed(0)}/100` },
    { label:'Dòng Tiền',  val: Math.max(0, Math.min(1, (totalCF + 50*n)/(100*n))),          color:'#3B82F6', desc:`${totalCF>=0?'+':''}${totalCF.toFixed(0)} Tr/tháng` },
    { label:'An Toàn Nợ', val: Math.max(0, Math.min(1, 1 - avgLoan/100)),                   color:'#EAB308', desc:`Vay TB ${avgLoan.toFixed(0)}%` },
    { label:'Tăng Vốn',   val: Math.max(0, Math.min(1, (avgGainPct + 10)/60)),              color:'#F97316', desc:`Lãi vốn TB ${avgGainPct.toFixed(1)}%` },
    { label:'Đa Dạng',    val: phases.size / 4,                                              color:'#A855F7', desc:`${phases.size}/4 Pha` },
  ];

  // SVG geometry
  const CX=130, CY=130, R=90, N=5;
  const W=260;
  function ptAt(val, i) {
    const ang = (i*2*Math.PI/N) - Math.PI/2;
    return { x: CX + R*val*Math.cos(ang), y: CY + R*val*Math.sin(ang) };
  }
  function polyPath(val) {
    return Array.from({length:N},(_,i)=>ptAt(val,i))
      .map((p,i)=>(i===0?'M':'L')+p.x.toFixed(1)+' '+p.y.toFixed(1)).join(' ')+'Z';
  }

  // Background grid (4 levels)
  const gridSVG = [0.25,0.5,0.75,1].map((lv,gi) =>
    `<path d="${polyPath(lv)}" fill="none" stroke="rgba(255,255,255,${0.04+gi*0.02})" stroke-width="${gi===3?1.5:0.7}"/>`
  ).join('');

  // Axis lines + labels
  const axesSVG = scores.map((sc,i) => {
    const tip = ptAt(1,i);
    const lbl = ptAt(1.28,i);
    return `<line x1="${CX}" y1="${CY}" x2="${tip.x.toFixed(1)}" y2="${tip.y.toFixed(1)}" stroke="rgba(255,255,255,.1)" stroke-width="1"/>
      <text x="${lbl.x.toFixed(1)}" y="${(lbl.y+4).toFixed(1)}" text-anchor="middle" fill="${sc.color}" font-size="9.5" font-family="monospace" font-weight="600">${sc.label}</text>`;
  }).join('');

  // Data polygon
  const dataPath = scores.map((sc,i)=>ptAt(sc.val,i))
    .map((p,i)=>(i===0?'M':'L')+p.x.toFixed(1)+' '+p.y.toFixed(1)).join(' ')+'Z';

  // Dots + value labels
  const dotsSVG = scores.map((sc,i) => {
    const p = ptAt(sc.val, i);
    const vStr = (sc.val*100).toFixed(0);
    return `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="5" fill="${sc.color}" stroke="#0d0d1a" stroke-width="1.5"/>`;
  }).join('');

  // Aura ring at center showing overall score
  const overallScore = scores.reduce((s,sc)=>s+sc.val,0)/N;
  const overallColor = overallScore>=0.65?'#10B981':overallScore>=0.4?'#EAB308':'#EF4444';

  const svg = `<svg width="${W}" height="${W}" viewBox="0 0 ${W} ${W}" style="max-width:100%">
    <circle cx="${CX}" cy="${CY}" r="${R*1.1}" fill="rgba(255,255,255,.01)" stroke="rgba(255,255,255,.03)" stroke-width="1"/>
    ${gridSVG}
    ${axesSVG}
    <path d="${dataPath}" fill="${overallColor}22" stroke="${overallColor}" stroke-width="2" stroke-linejoin="round"/>
    ${dotsSVG}
    <text x="${CX}" y="${CY-6}" text-anchor="middle" fill="${overallColor}" font-size="22" font-weight="700" font-family="monospace">${(overallScore*100).toFixed(0)}</text>
    <text x="${CX}" y="${CY+12}" text-anchor="middle" fill="#9CA3AF" font-size="9" font-family="monospace">/100 Tổng Điểm</text>
  </svg>`;

  box.innerHTML = svg;

  // Legend
  const grade = overallScore>=0.7?{g:'A',c:'#10B981',t:'Danh mục MẠNH'}:overallScore>=0.5?{g:'B',c:'#EAB308',t:'Cần Tối Ưu'}:overallScore>=0.35?{g:'C',c:'#F97316',t:'Nguy Cơ Trung Bình'}:{g:'D',c:'#EF4444',t:'NGUY HIỂM — Cần Cấp Cứu'};
  legend.innerHTML = `
    <div style="margin-bottom:16px;padding:12px;background:${grade.c}11;border-radius:8px;border:1px solid ${grade.c}33;text-align:center">
      <div style="font-size:32px;font-weight:900;color:${grade.c};font-family:monospace">${grade.g}</div>
      <div style="font-size:12px;color:${grade.c};font-weight:600;margin-top:2px">${grade.t}</div>
    </div>
    ${scores.map(sc=>{
      const bar = Math.round(sc.val*10);
      return `<div style="margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
          <span style="color:${sc.color};font-weight:600">${sc.label}</span>
          <span style="color:var(--text-2)">${sc.desc}</span>
        </div>
        <div style="height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden">
          <div style="height:100%;width:${(sc.val*100).toFixed(0)}%;background:${sc.color};border-radius:3px;transition:width 0.5s"></div>
        </div>
      </div>`;
    }).join('')}
  `;
}

'''

rep('// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    RADAR_FUNC + '// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    'Add renderRadarChart function')

# ══ 4: Surgery — Add portfolio-level "Cắt tài sản & xem tác động" section ══
# Add a "Portfolio Impact" card before the asset selector in Surgery
OLD_SIM_ASSET_SELECTOR = '''      <!-- Asset Selector -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-header"><span class="card-title">🏠 Chọn Tài Sản Để Giả Lập</span></div>
        <div id="sim-asset-list" style="display:flex;flex-wrap:wrap;gap:8px;padding:4px 0"></div>
      </div>'''

NEW_SIM_ASSET_SELECTOR = '''      <!-- Portfolio Impact Overview -->
      <div class="card" style="margin-bottom:20px" id="sim-portfolio-overview">
        <div class="card-header"><span class="card-title">📊 Tổng Quan Danh Mục Hiện Tại</span></div>
        <div id="sim-portfolio-stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;padding:4px 0"></div>
      </div>
      <!-- Asset Selector -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-header"><span class="card-title">🏠 Chọn Tài Sản Để Giả Lập Kịch Bản</span></div>
        <div id="sim-asset-list" style="display:flex;flex-wrap:wrap;gap:8px;padding:4px 0"></div>
      </div>'''

rep(OLD_SIM_ASSET_SELECTOR, NEW_SIM_ASSET_SELECTOR, 'Portfolio overview in Surgery HTML')

# ══ 5: openSimulator — render portfolio stats ══
OLD_SIM_OPEN = '''  // Build asset selector buttons
  const list = document.getElementById('sim-asset-list');'''

NEW_SIM_OPEN = '''  // Portfolio overview stats
  const statsBox = document.getElementById('sim-portfolio-stats');
  if (statsBox) {
    const pCalcs = portfolio.map(a => ({ a, c: calcAsset(a) }));
    const ptMkt  = portfolio.reduce((s,a) => s+(a.market||0), 0);
    const ptDebt = portfolio.reduce((s,a) => s+(a.debt||0), 0);
    const ptCF   = pCalcs.reduce((s,{c}) => s+c.cashflow, 0);
    const ptH    = Math.round(pCalcs.reduce((s,{c}) => s+c.health, 0) / portfolio.length);
    const mkSim  = (label, val, color) =>
      `<div style="text-align:center;padding:10px;background:rgba(255,255,255,.03);border-radius:8px">
         <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${label}</div>
         <div style="font-family:monospace;font-size:16px;font-weight:700;color:${color}">${val}</div>
       </div>`;
    statsBox.innerHTML =
      mkSim('Tổng Tài Sản', ptMkt.toFixed(1)+' Tỷ', 'var(--gold)') +
      mkSim('Tổng Dư Nợ',   ptDebt.toFixed(1)+' Tỷ', ptDebt>0?'var(--yellow)':'var(--text-1)') +
      mkSim('CF/Tháng',     (ptCF>=0?'+':'')+ptCF.toFixed(0)+' Tr', ptCF>=0?'var(--emerald)':'var(--red)') +
      mkSim('Health TB',    ptH+'/100', ptH>=70?'var(--emerald)':ptH>=45?'var(--yellow)':'var(--red)');
  }

  // Build asset selector buttons
  const list = document.getElementById('sim-asset-list');'''

rep(OLD_SIM_OPEN, NEW_SIM_OPEN, 'Portfolio stats in openSimulator')

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 4 KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
checks = [
    ('Radar HTML section',    'diag-radar-section'),
    ('Radar JS function',     'function renderRadarChart'),
    ('Radar called in diag',  'renderRadarChart(portfolio, calcs)'),
    ('SVG pentagon logic',    'polyPath(lv)'),
    ('Grade A/B/C/D',         "g:'A'"),
    ('Portfolio overview HTML','sim-portfolio-stats'),
    ('Portfolio stats in open','Portfolio overview stats'),
]
ok = err = 0
for name, pat in checks:
    if pat in v:
        print(f'  OK  {name}'); ok += 1
    else:
        print(f'  XX  {name}'); err += 1
print(f'\nTotal: {ok} OK / {err} loi')
