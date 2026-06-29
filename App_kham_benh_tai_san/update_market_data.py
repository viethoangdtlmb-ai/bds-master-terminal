"""
update_market_data.py
Đọc dashboard_data.json từ bds-dashboard → Inject vào window.MARKET_DATA trong index.html
Chạy sau khi crawl xong:
  python update_market_data.py
"""
import io, sys, json, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = Path(__file__).parent
DATA_JSON = BASE.parent / 'bds-dashboard' / 'data' / 'dashboard_data.json'
INDEX_HTML = BASE / 'index.html'

print(f'Đọc: {DATA_JSON}')
with open(DATA_JSON, encoding='utf-8') as f:
    data = json.load(f)
print(f'✅ Data: {data["updated"]} | {len(data["districts"])} quận')

data_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
print(f'Kích thước JSON: {len(data_str):,} chars')

# Đọc index.html
with open(INDEX_HTML, encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n')

# Tìm và thay thế window.MARKET_DATA = {...};
pattern = r'window\.MARKET_DATA = \{[^;]+\};'
match = re.search(pattern, content)
if not match:
    print('❌ Không tìm thấy window.MARKET_DATA trong index.html!')
    sys.exit(1)

old_len = len(match.group())
new_data_line = f'window.MARKET_DATA = {data_str};'
content = content[:match.start()] + new_data_line + content[match.end():]

print(f'Thay thế: {old_len:,} chars → {len(new_data_line):,} chars')

# Ghi lại
content = content.replace('\n', '\r\n')
with open(INDEX_HTML, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print(f'✅ Đã cập nhật index.html!')
print(f'   Ngày cập nhật: {data["updated"]}')
print(f'   Khoảng: {data.get("date_range", "N/A")}')
print(f'   Số quận: {len(data["districts"])}')
print(f'\nReload F5 tại http://localhost:8765 để xem dữ liệu mới.')
