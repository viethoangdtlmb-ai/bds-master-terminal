import sys
import os
import json
import re

# Add VIP_Report path to import functions
sys.path.append(r'd:\1. BDS\AI-Assistant\08_Tech_Systems\VIP_Report')
from xem_bieu_do_vip import load_60_months_data, normalize_region
import openpyxl

def load_nr_from_excel():
    filepath = r"d:\1. BDS\AI-Assistant\08_Tech_Systems\Data_Crawler\Gia_Nha_Rieng_2021_2026.xlsx"
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    
    header = rows[0]
    regions = [str(h).strip() for h in header[2:] if h]
    
    data = {normalize_region(r): {} for r in regions if normalize_region(r)}
    
    for row in rows[1:]:
        if not row[0] or not row[1]: continue
        try:
            thang = int(row[0])
            nam = int(row[1])
            label = f"T{thang}/{str(nam)[2:]}" # T3/21
            for i, reg in enumerate(regions):
                val = row[2+i]
                norm = normalize_region(reg)
                if norm and val is not None:
                    try:
                        data[norm][label] = float(val)
                    except:
                        pass
        except:
            continue
    return data

cc_hist_raw, cc_months = load_60_months_data(r'd:\1. BDS\AI-Assistant\08_Tech_Systems\Data_Crawler\gia_chung_cu_ha_noi_22_quan_60thang.csv')
nr_hist_raw = load_nr_from_excel()

# Convert cc_hist_raw (which is a list of dicts [{'thang': 'T3/21', 'gia': 40.5}, ...]) to dict
cc_data = {}
for reg, lst in cc_hist_raw.items():
    cc_data[reg] = {}
    for item in lst:
        if item['gia'] is not None:
            cc_data[reg][item['thang']] = item['gia']

market_history = {
    'chung-cu': cc_data,
    'nha-rieng': nr_hist_raw
}

html_path = r'd:\1. BDS\AI-Assistant\08_Tech_Systems\App_kham_benh_tai_san\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Inject window.MARKET_HISTORY
json_str = json.dumps(market_history, ensure_ascii=False)
inject_str = f"\n            window.MARKET_HISTORY = {json_str};\n"

if 'window.MARKET_HISTORY = {' in html:
    html = re.sub(r'window\.MARKET_HISTORY = \{.*?\};\n', inject_str, html, flags=re.DOTALL)
else:
    # insert right after window.MARKET_DATA = ...
    html = re.sub(r'(window\.MARKET_DATA = \{.*?\};)', r'\1' + inject_str, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected MARKET_HISTORY successfully!")
