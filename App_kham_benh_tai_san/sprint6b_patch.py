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

# ══ 1: Ensure Radar is rendered before reading its SVG ══
rep(
    'const radarSVG = document.getElementById(\'diag-radar\')?.innerHTML || \'\';',
    '''// Ensure radar is always freshly rendered
  renderRadarChart(portfolio, calcs);
  const radarSVG = document.getElementById('diag-radar')?.innerHTML || '';''',
    'Call renderRadarChart in buildPrescription'
)

# ══ 2: Renumber: IV → V (Alerts), V → VI (Toa Thuoc) ══
rep(
    '⚠️ IV. CẢNH BÁO ĐỎ',
    '⚠️ V. CẢNH BÁO ĐỎ',
    'Renumber: Alerts IV → V'
)
rep(
    '💊 V. TOA THUỐC TÁI CƠ CẤU',
    '💊 VI. TOA THUỐC TÁI CƠ CẤU',
    'Renumber: Toa Thuoc V → VI'
)

# ══ 3: Insert Section IV (Chi Tiet) between asset table and alerts ══
CHITET_SECTION = '''
  <!-- CHI TIET -->
  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">IV. PHÂN TÍCH TÀI CHÍNH CHI TIẾT</div>
    <table style="width:100%;border-collapse:collapse;font-size:11px">
      <thead>
        <tr style="background:#EEF2FF;border-bottom:2px solid #C7D2FE">
          <th style="text-align:left;padding:8px 10px;color:#4338CA;font-weight:600">Tài Sản</th>
          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">DSCR</th>
          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">ROE/năm</th>
          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">Giá Sàn HV</th>
          <th style="text-align:center;padding:8px 10px;color:#4338CA;font-weight:600">Vòng Chu Kỳ</th>
          <th style="text-align:left;padding:8px 10px;color:#4338CA;font-weight:600">Lưu Ý</th>
        </tr>
      </thead>
      <tbody>
        ${calcs.map(({a,c},i) => {
          const dscrColor = c.dscr===null?'#6B7280':c.dscr>=1?'#059669':c.dscr>=0.5?'#D97706':'#DC2626';
          const dscrTxt   = c.dscr===null?'N/A':(c.dscr.toFixed(2)+(c.dscr<0.5?' 🚨':c.dscr<1?' ⚠️':' ✅'));
          const roeColor  = c.roeAnnual>=18?'#059669':c.roeAnnual>=8?'#D97706':'#DC2626';
          const floorColor= a.market>=(c.floorPrice||0)?'#059669':'#DC2626';
          const notes = [];
          if (c.phaseWarning) notes.push(c.phaseWarning);
          if (c.deliveryNote) notes.push('🔑 '+c.deliveryNote);
          if ((a.grace||0)>0) notes.push(`💣 Ân hạn còn ${a.grace}T`);
          if ((a.prefmonths||0)>0 && (a.prefmonths||0)<=3) notes.push(`⚡ Ưu đãi còn ${a.prefmonths}T`);
          return \`<tr style="border-bottom:1px solid #F1F5F9;\${i%2===1?'background:#FAFAFA':''}">
            <td style="padding:8px 10px;font-weight:600;color:#1C1C2E">\${a.name}</td>
            <td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:\${dscrColor}">\${dscrTxt}</td>
            <td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:\${roeColor}">\${c.roeAnnual.toFixed(1)}%</td>
            <td style="padding:8px 10px;text-align:center;font-family:monospace;color:\${floorColor}">\${(c.floorPrice||0).toFixed(2)} Tỷ</td>
            <td style="padding:8px 10px;text-align:center;font-family:monospace;color:#6B7280">\${c.cycle?c.cycle+'/100':'N/A'}\${c.yoy?' | YoY '+c.yoy+'%':''}</td>
            <td style="padding:8px 10px;font-size:10px;color:#374151">\${notes.join(' • ') || '—'}</td>
          </tr>\`;
        }).join('')}
      </tbody>
    </table>
    <div style="margin-top:10px;font-size:10px;color:#6B7280">
      * DSCR = Dòng tiền thuần / Trả nợ &nbsp;|&nbsp; HV = Hòa Vốn &nbsp;|&nbsp; ROE = Lợi Nhuận Ròng / Vốn Tự Có &nbsp;|&nbsp; Chu Kỳ Cycle 0–100
    </div>
  </div>

'''

rep(
    '  <!-- ALERTS -->',
    CHITET_SECTION + '  <!-- ALERTS -->',
    'Insert Section IV Chi Tiet before Alerts'
)

# ══ 4: Insert Section VII (Radar Chart full-width) between Toa Thuoc and Footer ══
RADAR_SECTION = '''

  <!-- RADAR SECTION -->
  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">VII. RADAR SỨC KHỎE DANH MỤC</div>
    <div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap">
      <div style="flex-shrink:0">
        ${radarSVG ? radarSVG
            .replace(/width="[^"]*"/, 'width="240"')
            .replace(/height="[^"]*"/, 'height="240"')
            : '<div style="color:#9CA3AF;font-size:12px">Radar chưa được khởi tạo — vui lòng chẩn đoán trước khi xuất PDF.</div>'}
      </div>
      <div style="flex:1;min-width:200px">
        ${(() => {
          const avgH = calcs.reduce((s,{c})=>s+c.health,0)/calcs.length;
          const totalCFr = calcs.reduce((s,{c})=>s+c.cashflow,0);
          const avgL = portfolio.reduce((s,a)=>s+(a.loanpct||0),0)/portfolio.length;
          const avgG = calcs.reduce((s,{c})=>s+(c.gainPct||0),0)/calcs.length;
          const phases = new Set(calcs.map(({c})=>c.phase));
          const v1 = Math.max(0,Math.min(1,avgH/100));
          const v2 = Math.max(0,Math.min(1,(totalCFr+50*calcs.length)/(100*calcs.length)));
          const v3 = Math.max(0,Math.min(1,1-avgL/100));
          const v4 = Math.max(0,Math.min(1,(avgG+10)/60));
          const v5 = phases.size/4;
          const overall=(v1+v2+v3+v4+v5)/5;
          const grade=overall>=0.7?{g:'A',c:'#059669',t:'MẠNH'}:overall>=0.5?{g:'B',c:'#D97706',t:'CẦN TỐI ƯU'}:overall>=0.35?{g:'C',c:'#F97316',t:'RỦI RO TRUNG BÌNH'}:{g:'D',c:'#DC2626',t:'NGUY HIỂM'};
          const scores=[
            {n:'Sức Khỏe',   v:v1, c:'#059669'},
            {n:'Dòng Tiền',  v:v2, c:'#3B82F6'},
            {n:'An Toàn Nợ', v:v3, c:'#D97706'},
            {n:'Tăng Vốn',   v:v4, c:'#F97316'},
            {n:'Đa Dạng Pha',v:v5, c:'#A855F7'},
          ];
          return \`<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">
              <div style="font-size:48px;font-weight:900;color:\${grade.c};">\${grade.g}</div>
              <div>
                <div style="font-size:14px;font-weight:700;color:\${grade.c}">\${grade.t}</div>
                <div style="font-size:11px;color:#6B7280">Tổng điểm: \${(overall*100).toFixed(0)}/100</div>
              </div>
            </div>
            \${scores.map(s=>\`<div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:\${s.c};font-weight:600">\${s.n}</span>
                <span style="color:#6B7280">\${(s.v*100).toFixed(0)}/100</span>
              </div>
              <div style="height:6px;background:#E5E7EB;border-radius:3px">
                <div style="height:100%;width:\${(s.v*100).toFixed(0)}%;background:\${s.c};border-radius:3px"></div>
              </div>
            </div>\`).join('')}\`;
        })()}
      </div>
    </div>
  </div>

'''

rep(
    '  <!-- FOOTER -->',
    RADAR_SECTION + '  <!-- FOOTER -->',
    'Insert Section VII Radar before Footer'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 6B (PDF RADAR + CHI TIET) KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()

checks = [
    ('renderRadarChart in buildPrescription', 'Ensure radar is always freshly'),
    ('Section IV Chi Tiet',                  'PHÂN TÍCH TÀI CHÍNH CHI TIẾT'),
    ('DSCR + ROE table',                     'Giá Sàn HV'),
    ('Phase warning in table',               'phaseWarning'),
    ('Section V Alerts renumbered',          'V. CẢNH BÁO ĐỎ'),
    ('Section VI Toa Thuoc renumbered',      'VI. TOA THUỐC'),
    ('Section VII Radar',                    'VII. RADAR SỨC KHỎE'),
    ('Grade A/B/C/D inline',                 'NGUY HIỂM'),
    ('Bar chart per metric',                 'MẠNH'),
]
import re
scripts = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
for i, sc in enumerate(scripts[:-1], 1):
    ob, cb = sc.count('{'), sc.count('}')
    print(f'Script {i} braces: {ob}/{cb} diff={ob-cb}')

ok = err = 0
for name, pat in checks:
    if pat in v:
        print(f'  OK  {name}'); ok += 1
    else:
        print(f'  XX  {name}'); err += 1
print(f'\nTotal: {ok} OK / {err} loi')
