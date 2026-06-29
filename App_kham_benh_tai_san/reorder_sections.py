import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n')

results = []

# ══ Locate section boundaries in the html template ══
# We'll find the content between section markers and rearrange

A_ALERTS   = '  <!-- ALERTS -->'
A_PRESC    = '  <!-- PRESCRIPTION / RECOS -->'
A_RADAR    = '\n  <!-- RADAR SECTION -->'
A_FOOTER   = '\n  <!-- FOOTER -->'

def section_between(start_marker, end_marker, s):
    """Return the text from start_marker (inclusive) to end_marker (exclusive)"""
    si = s.find(start_marker)
    ei = s.find(end_marker)
    if si < 0 or ei < 0 or ei < si:
        return None, -1, -1
    return s[si:ei], si, ei

# Extract RADAR section (from <!-- RADAR SECTION --> to <!-- FOOTER -->)
radar_txt, radar_s, radar_e = section_between(A_RADAR, A_FOOTER, content)
if radar_txt is None:
    print('ERROR: Cannot find RADAR section or FOOTER')
    sys.exit(1)
print(f'Radar section found: chars {radar_s}–{radar_e}, len={len(radar_txt)}')

# Extract ALERTS section (from <!-- ALERTS --> to <!-- PRESCRIPTION -->)
alerts_txt, alerts_s, alerts_e = section_between(A_ALERTS, A_PRESC, content)
if alerts_txt is None:
    print('ERROR: Cannot find ALERTS section')
    sys.exit(1)
print(f'Alerts section found: chars {alerts_s}–{alerts_e}, len={len(alerts_txt)}')

# Extract PRESCRIPTION section (from <!-- PRESCRIPTION --> to <!-- RADAR SECTION -->)
presc_txt, presc_s, presc_e = section_between(A_PRESC, A_RADAR, content)
if presc_txt is None:
    print('ERROR: Cannot find PRESCRIPTION section')
    sys.exit(1)
print(f'Presc section found: chars {presc_s}–{presc_e}, len={len(presc_txt)}')

# Find the location right after CHI TIET section ends (== start of ALERTS)
chi_tiet_end = alerts_s

# Verify order: chi_tiet_end < alerts_s < alerts_e < presc_s < presc_e < radar_s < radar_e
print(f'Order check: {chi_tiet_end} < {alerts_s} < {alerts_e} < {presc_s} < {presc_e} < {radar_s} < {radar_e}')

# ══ Modify section titles ══
# RADAR: currently "VII. RADAR" → change to "V. RADAR"
radar_new = radar_txt.replace('VII. RADAR SỨC KHỎE DANH MỤC', 'V. RADAR SỨC KHỎE DANH MỤC')
# ALERTS: currently "V. CẢNH BÁO ĐỎ" → "VI. CẢNH BÁO ĐỎ"
alerts_new = alerts_txt.replace('⚠️ V. CẢNH BÁO ĐỎ', '⚠️ VI. CẢNH BÁO ĐỎ')
# PRESCRIPTION: currently "VI. TOA THUỐC" → "VII. TOA THUỐC"
presc_new  = presc_txt.replace('💊 VI. TOA THUỐC TÁI CƠ CẤU', '💊 VII. TOA THUỐC TÁI CƠ CẤU')

print(f'Radar title updated: {"V. RADAR" in radar_new}')
print(f'Alerts title updated: {"VI. CẢNH BÁO" in alerts_new}')
print(f'Presc title updated: {"VII. TOA THUỐC" in presc_new}')

# ══ Reconstruct the section block ══
# New order: [before_alerts] + RADAR(V) + ALERTS(VI) + PRESC(VII) + FOOTER...
before_alerts = content[:chi_tiet_end]
after_presc   = A_FOOTER + content[content.find(A_FOOTER) + len(A_FOOTER):]

new_content = (
    before_alerts
    + radar_new          # V. RADAR (moved up)
    + '\n' + alerts_new  # VI. CẢNH BÁO
    + presc_new          # VII. TOA THUỐC
    + after_presc        # <!-- FOOTER --> onwards
)

# Sanity: check new content still has all markers
for m in [A_RADAR, A_ALERTS, A_PRESC, A_FOOTER]:
    if m in new_content:
        print(f'Marker OK: {repr(m[:30])}')
    else:
        print(f'MISSING: {repr(m[:30])}')

# ══ Write ══
content = new_content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

# ══ Final checks ══
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1],1):
    ob,cb = s.count('{'),s.count('}')
    bt = s.count('`')
    bsdl = s.count(chr(92)+chr(36))
    print(f'Script {i}: brace {ob}/{cb} backtick {bt}({"even" if bt%2==0 else "ODD"}) bs$={bsdl}')

checks = [
    ('Section order: IV then V RADAR',  'IV. PHÂN TÍCH TÀI CHÍNH CHI TIẾT' in v and v.find('V. RADAR') > v.find('IV. PHÂN TÍCH')),
    ('V. RADAR before VI. CẢNH BÁO',    v.find('V. RADAR') < v.find('VI. CẢNH BÁO')),
    ('VI. CẢNH BÁO before VII. TOA',     v.find('VI. CẢNH BÁO') < v.find('VII. TOA THUỐC')),
    ('No old VII. RADAR left',           'VII. RADAR' not in v),
    ('No old V. CẢNH BÁO left',          '⚠️ V. CẢNH BÁO ĐỎ' not in v),
    ('No old VI. TOA left',              '💊 VI. TOA THUỐC TÁI CƠ CẤU' not in v),
]
ok = err = 0
for name, check in checks:
    if check: print(f'  OK  {name}'); ok += 1
    else: print(f'  XX  {name}'); err += 1
print(f'\nTotal: {ok} OK / {err} err')
