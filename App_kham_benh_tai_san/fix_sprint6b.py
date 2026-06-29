import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n')

BS = chr(92)  # backslash
DL = chr(36)  # dollar
BT = chr(96)  # backtick

results = []

def rep(old, new, tag, allow_multi=False):
    global content
    count = content.count(old)
    if count == 1 or (allow_multi and count > 0):
        content = content.replace(old, new, 1)
        results.append(f'OK  {tag} ({count} found)')
    elif count == 0:
        results.append(f'XX  {tag} — NOT FOUND')
    else:
        results.append(f'!!  {tag} — {count} matches, skipping (ambiguous)')

# ══════════════════════════════════════════════════════════════
# FIX 1: Pre-compute detailRowsHTML and radLegHTML before const html
# ══════════════════════════════════════════════════════════════

PRE_COMPUTE = '''  // Pre-compute complex HTML blocks to avoid nested template literal issues
  const PHASE_COL_ARR = ['','#3B82F6','#EAB308','#10B981','#9CA3AF'];
  const detailRowsHTML = calcs.map(({a,c},i) => {
    const rowBg      = i%2===1 ? 'background:#FAFAFA' : '';
    const dscrColor  = c.dscr===null?'#6B7280':c.dscr>=1?'#059669':c.dscr>=0.5?'#D97706':'#DC2626';
    const dscrTxt    = c.dscr===null?'N/A':(c.dscr.toFixed(2)+(c.dscr<0.5?' 🚨':c.dscr<1?' ⚠️':' ✅'));
    const roeColor   = c.roeAnnual>=18?'#059669':c.roeAnnual>=8?'#D97706':'#DC2626';
    const floorColor = a.market>=(c.floorPrice||0)?'#059669':'#DC2626';
    const noteArr = [];
    if (c.phaseWarning) noteArr.push(c.phaseWarning);
    if (c.deliveryNote) noteArr.push('🔑 '+c.deliveryNote);
    if ((a.grace||0)>0) noteArr.push('💣 Ân hạn còn '+a.grace+'T');
    if ((a.prefmonths||0)>0 && (a.prefmonths||0)<=3) noteArr.push('⚡ Ưu đãi còn '+a.prefmonths+'T');
    return '<tr style="border-bottom:1px solid #F1F5F9;'+rowBg+'">'
      + '<td style="padding:8px 10px;font-weight:600;color:#1C1C2E">'+a.name+'</td>'
      + '<td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:'+dscrColor+'">'+dscrTxt+'</td>'
      + '<td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:'+roeColor+'">'+c.roeAnnual.toFixed(1)+'%</td>'
      + '<td style="padding:8px 10px;text-align:center;font-family:monospace;color:'+floorColor+'">'+(c.floorPrice||0).toFixed(2)+' Tỷ</td>'
      + '<td style="padding:8px 10px;text-align:center;font-family:monospace;color:#6B7280">'+(c.cycle?c.cycle+'/100':'N/A')+(c.yoy?' | YoY '+c.yoy+'%':'')+'</td>'
      + '<td style="padding:8px 10px;font-size:10px;color:#374151">'+(noteArr.join(' • ')||'—')+'</td>'
      + '</tr>';
  }).join('');

  const _avgHr  = calcs.reduce((s,{c})=>s+c.health,0)/calcs.length;
  const _cfr    = calcs.reduce((s,{c})=>s+c.cashflow,0);
  const _avgLr  = portfolio.reduce((s,a)=>s+(a.loanpct||0),0)/portfolio.length;
  const _avgGr  = calcs.reduce((s,{c})=>s+(c.gainPct||0),0)/calcs.length;
  const _phsR   = new Set(calcs.map(({c})=>c.phase));
  const _v1r=Math.max(0,Math.min(1,_avgHr/100));
  const _v2r=Math.max(0,Math.min(1,(_cfr+50*calcs.length)/(100*calcs.length)));
  const _v3r=Math.max(0,Math.min(1,1-_avgLr/100));
  const _v4r=Math.max(0,Math.min(1,(_avgGr+10)/60));
  const _v5r=_phsR.size/4;
  const _overall=(_v1r+_v2r+_v3r+_v4r+_v5r)/5;
  const _grd=_overall>=0.7?{g:'A',c:'#059669',t:'MẠNH'}:_overall>=0.5?{g:'B',c:'#D97706',t:'CẦN TỐI ƯU'}:_overall>=0.35?{g:'C',c:'#F97316',t:'RỦI RO TRUNG BÌNH'}:{g:'D',c:'#DC2626',t:'NGUY HIỂM'};
  const _scrs=[
    {n:'Sức Khỏe',   v:_v1r,c:'#059669'},
    {n:'Dòng Tiền',  v:_v2r,c:'#3B82F6'},
    {n:'An Toàn Nợ', v:_v3r,c:'#D97706'},
    {n:'Tăng Vốn',   v:_v4r,c:'#F97316'},
    {n:'Đa Dạng Pha',v:_v5r,c:'#A855F7'},
  ];
  const radLegHTML =
    '<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">'
    + '<div style="font-size:48px;font-weight:900;color:'+_grd.c+'">'+_grd.g+'</div>'
    + '<div><div style="font-size:14px;font-weight:700;color:'+_grd.c+'">'+_grd.t+'</div>'
    + '<div style="font-size:11px;color:#6B7280">Tổng điểm: '+(_overall*100).toFixed(0)+'/100</div></div>'
    + '</div>'
    + _scrs.map(sc =>
        '<div style="margin-bottom:8px">'
        + '<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">'
        + '<span style="color:'+sc.c+';font-weight:600">'+sc.n+'</span>'
        + '<span style="color:#6B7280">'+(sc.v*100).toFixed(0)+'/100</span></div>'
        + '<div style="height:6px;background:#E5E7EB;border-radius:3px">'
        + '<div style="height:100%;width:'+(sc.v*100).toFixed(0)+'%;background:'+sc.c+';border-radius:3px"></div>'
        + '</div></div>'
      ).join('');

'''

# Insert before "const html" in buildPrescription
# Anchor: the line right before the html template
OLD_HTML_START = '  const html = `'
rep(OLD_HTML_START, PRE_COMPUTE + '  const html = `', 'Insert pre-computed vars before html template')

# ══════════════════════════════════════════════════════════════
# FIX 2: Replace CHITET calcs.map in template with ${detailRowsHTML}
# ══════════════════════════════════════════════════════════════
# Find the exact broken block from file view (lines 1973-1991)
OLD_CHITET_ROWS = (
    '        ${calcs.map(({a,c},i) => {\n'
    '          const dscrColor = c.dscr===null?\'#6B7280\':c.dscr>=1?\'#059669\':c.dscr>=0.5?\'#D97706\':\'#DC2626\';\n'
    '          const dscrTxt   = c.dscr===null?\'N/A\':(c.dscr.toFixed(2)+(c.dscr<0.5?\' 🚨\':c.dscr<1?\' ⚠️\':\' ✅\'));\n'
    '          const roeColor  = c.roeAnnual>=18?\'#059669\':c.roeAnnual>=8?\'#D97706\':\'#DC2626\';\n'
    '          const floorColor= a.market>=(c.floorPrice||0)?\'#059669\':\'#DC2626\';\n'
    '          const notes = [];\n'
    '          if (c.phaseWarning) notes.push(c.phaseWarning);\n'
    '          if (c.deliveryNote) notes.push(\'🔑 \'+c.deliveryNote);\n'
    '          if ((a.grace||0)>0) notes.push(`💣 Ân hạn còn ${a.grace}T`);\n'
    '          if ((a.prefmonths||0)>0 && (a.prefmonths||0)<=3) notes.push(`⚡ Ưu đãi còn ${a.prefmonths}T`);\n'
)

NEW_CHITET_ROWS_PART = '        ${detailRowsHTML}\n'

# Build the full old block including the return statement and closing
# The return block has backslash-dollar signs; let's find the whole section by surrounding text
OLD_CHITET_FULL_ANCHOR_START = '      <tbody>\n        ${calcs.map(({a,c},i) => {'
OLD_CHITET_FULL_ANCHOR_END = '        }).join(\'\')}' + '\n      </tbody>'

if OLD_CHITET_FULL_ANCHOR_START in content and OLD_CHITET_FULL_ANCHOR_END in content:
    # Find start position
    start_pos = content.find(OLD_CHITET_FULL_ANCHOR_START)
    # Find the SECOND tbody (first is from III DANH MUC, second is from IV CHI TIET)
    start_pos2 = content.find(OLD_CHITET_FULL_ANCHOR_START, start_pos + 1)
    if start_pos2 > 0:
        # Use the second occurrence (CHITET section)
        end_pos = content.find(OLD_CHITET_FULL_ANCHOR_END, start_pos2) + len(OLD_CHITET_FULL_ANCHOR_END)
        old_block = content[start_pos2:end_pos]
        new_block = '      <tbody>\n        ${detailRowsHTML}\n      </tbody>'
        content = content[:start_pos2] + new_block + content[end_pos:]
        results.append(f'OK  Replace CHITET calcs.map with detailRowsHTML')
    else:
        results.append(f'XX  CHITET second tbody — not found (only 1 occurrence)')
else:
    results.append(f'XX  CHITET tbody anchor — not found')

# ══════════════════════════════════════════════════════════════
# FIX 3: Replace RADAR IIFE with ${radLegHTML}
# ══════════════════════════════════════════════════════════════
OLD_IIFE_START = '        ${(() => {\n          const avgH = calcs.reduce'
OLD_IIFE_END   = '        })()}'

if OLD_IIFE_START in content:
    s = content.find(OLD_IIFE_START)
    e = content.find(OLD_IIFE_END, s) + len(OLD_IIFE_END)
    old_iife = content[s:e]
    content = content[:s] + '        ${radLegHTML}' + content[e:]
    results.append(f'OK  Replace RADAR IIFE with radLegHTML')
else:
    results.append(f'XX  RADAR IIFE anchor — not found')

# ══════════════════════════════════════════════════════════════
# WRITE
# ══════════════════════════════════════════════════════════════
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== FIX SPRINT 6B ===')
for r in results: print(' ', r)

# Final checks
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc_blocks = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc_blocks)}')
for i, sc in enumerate(sc_blocks[:-1],1):
    ob,cb = sc.count('{'), sc.count('}')
    btk = sc.count(BT)
    bs_dl = sc.count(BS+DL)
    print(f'Script {i}: brace {ob}/{cb} btk={btk}({"even" if btk%2==0 else "ODD"}) bs$={bs_dl}')

checks = [
    ('Pre-computed detailRowsHTML', 'const detailRowsHTML = calcs.map'),
    ('Pre-computed radLegHTML',     'const radLegHTML ='),
    ('detailRowsHTML in template',  '${detailRowsHTML}'),
    ('radLegHTML in template',      '${radLegHTML}'),
    ('IIFE removed',                '${(() => {' not in v),
    ('Chi Tiet table intact',       'IV. PHÂN TÍCH TÀI CHÍNH'),
    ('Radar section intact',        'VII. RADAR'),
]
ok = err = 0
for name, check in checks:
    if isinstance(check, bool):
        passed = check
    else:
        passed = check in v
    if passed: print(f'  OK  {name}'); ok += 1
    else: print(f'  XX  {name}'); err += 1
print(f'\nTotal: {ok} OK / {err} loi')
