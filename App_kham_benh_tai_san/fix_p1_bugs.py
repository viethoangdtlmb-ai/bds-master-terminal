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

# ══ BUG 1: Xóa div portfolio-summary trùng lặp ══
DUPE_DIV = '\n      <div id="portfolio-summary" style="display:none;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;background:var(--bg-card);border:1px solid var(--bg-border);border-radius:var(--r-md);padding:14px 16px"></div>'
# Check how many times it appears
count_dupe = content.count(DUPE_DIV)
print(f'Bug 1: portfolio-summary duplicates found: {count_dupe}')
if count_dupe >= 2:
    # Remove the second occurrence only
    first_pos = content.find(DUPE_DIV)
    second_pos = content.find(DUPE_DIV, first_pos + 1)
    content = content[:second_pos] + content[second_pos + len(DUPE_DIV):]
    results.append('✅ Bug 1: Xóa div portfolio-summary trùng lặp')
elif count_dupe == 1:
    results.append('⚠️ Bug 1: Chỉ có 1 occurrence — không cần xóa')
else:
    results.append('❌ Bug 1: Không tìm thấy pattern')

# ══ BUG 2: Sửa §ất nền → Đất nền ══
rep(
    '\u003coption value="dat-nen"\u003e\xa7\u1ea5t n\u1ec1n\u003c/option\u003e',
    '<option value="dat-nen">Đất nền</option>',
    'Bug 2: Sửa §ất nền → Đất nền (unicode escape)'
)
# Also try direct string in case file was not unicode-escaped
if '§ất nền' in content:
    content = content.replace('§ất nền', 'Đất nền', 1)
    results.append('✅ Bug 2b: Sửa §ất nền → Đất nền (direct)')

# ══ BUG 3: loadTemplate nhận event parameter ══
# Fix function signature
rep(
    'function loadTemplate(key) {',
    'function loadTemplate(key, ev) {',
    'Bug 3a: loadTemplate nhận ev parameter'
)
# Fix event.target references
rep(
    "document.querySelectorAll('#templates-row .btn').forEach(b => b.classList.remove('btn-primary'));\n  event.target.classList.add('btn-primary');\n  setTimeout(() => event.target.classList.remove('btn-primary'), 1500);",
    "document.querySelectorAll('#templates-row .btn').forEach(b => b.classList.remove('btn-primary'));\n  if (ev && ev.target) { ev.target.classList.add('btn-primary'); setTimeout(() => ev.target.classList.remove('btn-primary'), 1500); }",
    'Bug 3b: Thay event.target → ev.target (safe)'
)
# Fix all onclick calls to pass event
for template_key in ['shophouse', 'datnen', 'chungcu', 'ketket', 'danhmuc']:
    OLD = f"onclick=\"loadTemplate('{template_key}')\""
    NEW = f"onclick=\"loadTemplate('{template_key}', event)\""
    if OLD in content:
        content = content.replace(OLD, NEW)
        results.append(f'✅ Bug 3c: onclick loadTemplate({template_key}) + event')

# ══ BUG 4: loadTemplate thêm Sprint 3 fields ══
# Add delivery and rentExpected to TEMPLATES
OLD_SH = "shophouse: { name:'Shophouse Làng Vân SH07', type:'shophouse', district:'Hoài Đức', area:80, year:2022, cost:9, market:8.5, goal:'cho-thue', loanpct:60, debt:4.8, rate:8.5, prefmonths:6, floatrate:13, grace:8, loanterm:18, rentstatus:'dang-thue', rent:20, mgmt:3.5, maint:15 },"
NEW_SH = "shophouse: { name:'Shophouse Làng Vân SH07', type:'shophouse', district:'Hoài Đức', area:80, year:2022, cost:9, market:8.5, goal:'cho-thue', loanpct:60, debt:4.8, rate:8.5, prefmonths:6, floatrate:13, grace:8, loanterm:18, rentstatus:'dang-thue', rent:20, mgmt:3.5, maint:15, delivery:0, rentExpected:0 },"
rep(OLD_SH, NEW_SH, 'Bug 4a: Thêm delivery+rentExpected vào template shophouse')

OLD_DN = "datnen:    { name:'Đất Nền Bắc Quốc Oai', type:'dat-nen', district:'Thạch Thất', area:120, year:2021, cost:3.5, market:3.2, goal:'tang-gia', loanpct:50, debt:1.5, rate:9, prefmonths:3, floatrate:13.5, grace:0, loanterm:15, rentstatus:'trong', rent:0, mgmt:0, maint:5 },"
NEW_DN = "datnen:    { name:'Đất Nền Bắc Quốc Oai', type:'dat-nen', district:'Thạch Thất', area:120, year:2021, cost:3.5, market:3.2, goal:'tang-gia', loanpct:50, debt:1.5, rate:9, prefmonths:3, floatrate:13.5, grace:0, loanterm:15, rentstatus:'trong', rent:0, mgmt:0, maint:5, delivery:0, rentExpected:0 },"
rep(OLD_DN, NEW_DN, 'Bug 4b: template datnen')

OLD_CC = "chungcu:   { name:'Chung Cư Vinhomes Hà Đông', type:'chung-cu', district:'Hà Đông', area:68, year:2020, cost:3.2, market:3.8, goal:'cho-thue', loanpct:70, debt:1.8, rate:7.5, prefmonths:2, floatrate:12.5, grace:0, loanterm:20, rentstatus:'dang-thue', rent:12, mgmt:2, maint:8 },"
NEW_CC = "chungcu:   { name:'Chung Cư Vinhomes Hà Đông', type:'chung-cu', district:'Hà Đông', area:68, year:2020, cost:3.2, market:3.8, goal:'cho-thue', loanpct:70, debt:1.8, rate:7.5, prefmonths:2, floatrate:12.5, grace:0, loanterm:20, rentstatus:'dang-thue', rent:12, mgmt:2, maint:8, delivery:0, rentExpected:0 },"
rep(OLD_CC, NEW_CC, 'Bug 4c: template chungcu')

OLD_KK = "ketket:    { name:'Nhà Phố Hoàng Mai', type:'nha-rieng', district:'Hoàng Mai', area:55, year:2023, cost:12, market:11.5, goal:'cho-thue', loanpct:65, debt:7, rate:8, prefmonths:14, floatrate:13, grace:12, loanterm:19, rentstatus:'trong', rent:0, mgmt:1, maint:10 },"
NEW_KK = "ketket:    { name:'Nhà Phố Hoàng Mai', type:'nha-rieng', district:'Hoàng Mai', area:55, year:2023, cost:12, market:11.5, goal:'cho-thue', loanpct:65, debt:7, rate:8, prefmonths:14, floatrate:13, grace:12, loanterm:19, rentstatus:'chua-ban-giao', rent:0, mgmt:1, maint:10, delivery:6, rentExpected:20 },"
rep(OLD_KK, NEW_KK, 'Bug 4d: template ketket (chua-ban-giao demo)')

OLD_DM = "danhmuc:   { name:'Danh Mục Hỗn Hợp', type:'nha-rieng', district:'Bắc Từ Liêm', area:100, year:2021, cost:8, market:9.5, goal:'tang-gia', loanpct:40, debt:2.5, rate:8.5, prefmonths:8, floatrate:13, grace:4, loanterm:17, rentstatus:'dang-thue', rent:25, mgmt:3, maint:12 },"
NEW_DM = "danhmuc:   { name:'Danh Mục Hỗn Hợp', type:'nha-rieng', district:'Bắc Từ Liêm', area:100, year:2021, cost:8, market:9.5, goal:'tang-gia', loanpct:40, debt:2.5, rate:8.5, prefmonths:8, floatrate:13, grace:4, loanterm:17, rentstatus:'dang-thue', rent:25, mgmt:3, maint:12, delivery:0, rentExpected:0 },"
rep(OLD_DM, NEW_DM, 'Bug 4e: template danhmuc')

# Add set calls for f-delivery and f-rent-expected in loadTemplate
rep(
    "  set('f-rent', t.rent); set('f-mgmt', t.mgmt); set('f-maint', t.maint);\n  onLoanPctChange(t.loanpct);\n  onRentStatusChange(t.rentstatus);",
    "  set('f-rent', t.rent); set('f-mgmt', t.mgmt); set('f-maint', t.maint);\n  set('f-delivery', t.delivery || ''); set('f-rent-expected', t.rentExpected || '');\n  onLoanPctChange(t.loanpct);\n  onRentStatusChange(t.rentstatus);",
    'Bug 4f: loadTemplate set f-delivery + f-rent-expected'
)

# ══ BUG 5: buildPrescription — Radar Section V guard ══
# Add null-check: if radarSVG is empty, generate inline minimal SVG message
# The renderRadarChart already handles it, but add guard for radLegHTML calcs length
OLD_RAD_GUARD = '  // Ensure radar is always freshly rendered\n  renderRadarChart(portfolio, calcs);\n  const radarSVG = document.getElementById(\'diag-radar\')?.innerHTML || \'\';'
NEW_RAD_GUARD = '''  // Ensure radar is always freshly rendered (write to diag-radar div, even hidden)
  renderRadarChart(portfolio, calcs);
  const radarSVG = (document.getElementById('diag-radar')?.innerHTML || '').trim();
  const radarDisplay = radarSVG
    ? radarSVG.replace(/width="[^"]*"/, 'width="240"').replace(/height="[^"]*"/, 'height="240"')
    : '<div style="color:#9CA3AF;font-size:12px;padding:20px;text-align:center">⚠️ Chưa có dữ liệu Radar — vui lòng chẩn đoán ít nhất 1 tài sản.</div>';'''
rep(OLD_RAD_GUARD, NEW_RAD_GUARD, 'Bug 5: Guard radarDisplay — fallback message khi empty')

# Now update the template reference from radarSVG ? radarSVG.replace... to radarDisplay
rep(
    '${radarSVG ? radarSVG\n            .replace(/width="[^"]*"/, \'width="240"\')\n            .replace(/height="[^"]*"/, \'height="240"\')\n            : \'<div style="color:#9CA3AF;font-size:12px">Radar chưa được khởi tạo — vui lòng chẩn đoán trước khi xuất PDF.</div>\'}',
    '${radarDisplay}',
    'Bug 5b: Template dùng radarDisplay thay vì inline ternary'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== P1 BUG FIX RESULTS ===')
for r in results: print(' ', r)

# Final JS health check
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob, cb = s.count('{'), s.count('}')
    bt = s.count('`')
    bsd = s.count(chr(92)+chr(36))
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"}) bs$={bsd}')

# Spot checks
spots = [
    ('No §ất nền',          '§ất nền' not in v),
    ('No duplicate summary', v.count('id="portfolio-summary"') == 1),
    ('loadTemplate has ev',  'function loadTemplate(key, ev)' in v),
    ('f-delivery set',       "set('f-delivery'" in v),
    ('f-rent-expected set',  "set('f-rent-expected'" in v),
    ('delivery in templates','delivery:0' in v),
    ('radarDisplay guard',   'radarDisplay' in v),
    ('onclick passes event', "loadTemplate('shophouse', event)" in v),
]
ok = err = 0
for name, check in spots:
    if check: print(f'  ✅ {name}'); ok += 1
    else: print(f'  ❌ {name}'); err += 1
print(f'\nTotal: {ok} OK / {err} err')
