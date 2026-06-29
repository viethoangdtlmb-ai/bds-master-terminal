import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ── 1. Fix dashboard_data.json ────────────────────────────────
DATA_PATH   = r'd:/1. BDS/AI-Assistant/bds-dashboard/data/dashboard_data.json'
CONFIG_PATH = r'd:/1. BDS/AI-Assistant/bds-dashboard/data/chi_so_config.json'
HTML_PATH   = r'd:/1. BDS/AI-Assistant/App_kham_benh_tai_san/index.html'

INVALID_CC = ['Sóc Sơn', 'Thạch Thất']  # CC > Nhà → dữ liệu sai

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
for d in data['districts']:
    if d['name'] in INVALID_CC:
        print(f"  Fix {d['name']}: gia_cc {d['gia_cc']} → null")
        d['gia_cc'] = None
        fixed += 1

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[1] dashboard_data.json: {fixed} khu vực đã fix\n")

# ── 2. Update chi_so_config.json ──────────────────────────────
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

if 'gia_cc_override' not in config:
    config['gia_cc_override'] = {}

config['gia_cc_override']['_comment'] = 'null = dữ liệu CC không tin cậy (CC > Nhà, vùng ven thiếu CC)'
for name in INVALID_CC:
    config['gia_cc_override'][name] = None
    print(f"  Config {name}: gia_cc_override = null")

with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
print(f"[2] chi_so_config.json: cập nhật gia_cc_override\n")

# ── 3. Re-embed MARKET_DATA vào HTML ─────────────────────────
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace old embedded MARKET_DATA
import re
new_embed = 'window.MARKET_DATA = ' + json.dumps(data, ensure_ascii=False) + ';'
# Find and replace the window.MARKET_DATA = {...}; block
pattern = r'window\.MARKET_DATA\s*=\s*\{.*?\};'
html_new = re.sub(pattern, new_embed, html, count=1, flags=re.DOTALL)

if html_new == html:
    print("[3] WARNING: MARKET_DATA block not found in HTML")
else:
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_new)
    print("[3] index.html: MARKET_DATA re-embedded với gia_cc đã fix\n")

# ── 4. Verify ─────────────────────────────────────────────────
print("── Kiểm tra lại ──")
for d in data['districts']:
    gia    = d.get('gia') or 0
    gia_cc = d.get('gia_cc')
    flag = ''
    if gia_cc is not None and gia_cc > gia:
        flag = '⚠️ STILL INVALID'
    elif gia_cc is None:
        flag = '→ CC: N/A (fixed)'
    if flag:
        print(f"  {d['name']:<22} Nhà:{gia:>7.1f} CC:{str(gia_cc):>7}  {flag}")
print("Xong!")
