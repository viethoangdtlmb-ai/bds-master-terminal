# -*- coding: utf-8 -*-
"""Test crawl next data"""
import sys, io, json, re, time
from curl_cffi import requests
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

URL = "https://batdongsan.com.vn/ban-can-ho-chung-cu-nam-tu-liem"

def extract_price(html):
    # Regex tim cac JSON dang: {"month":"2023-01","value":45.2}
    prices = []
    
    # 1. Tim window.__PRICES_... neu co
    m1 = re.search(r'__NEXT_DATA__.*?"([\[{].*?)\s*</script>', html, re.DOTALL)
    if m1:
        text = m1.group(1)
        # Scan tat ca cac format "month":"202x-xx","value":10.5
        pts = re.findall(r'{"month"\s*:\s*"([^"]+)"\s*,\s*"value"\s*:\s*([\d.]+)}', text)
        for m, v in pts:
            prices.append((m, float(v)))
            
    # 2. Tim Highcharts or general chart series arrays
    if not prices:
        # Array labels: ["2020-01", "2020-02" ...]
        m_labels = re.search(r'"labels"\s*:\s*(\[[^\]]+\])', html)
        # Array data: [100.5, 102.3 ...]  (co the nam trong dataset)
        m_data = re.search(r'"data"\s*:\s*(\[[^\]]+\])', html)
        
        if m_labels and m_data:
            try:
                lbs = json.loads(m_labels.group(1))
                dts = json.loads(m_data.group(1))
                if lbs and str(lbs[0]).startswith("20") and len(lbs) == len(dts):
                    for l, d in zip(lbs, dts):
                        if d is not None:
                            prices.append((str(l), float(d)))
            except: pass
            
    return prices

print("Crawling...")
session = requests.Session(impersonate="chrome110")
resp = session.get(URL, timeout=30)
html = resp.text

print(f"Status: {resp.status_code}")
print(f"HTML: {len(html)/1024:.1f} KB")

prices = extract_price(html)
if prices:
    print(f"FOUND {len(prices)} points:")
    prices.sort(key=lambda x: x[0])  # Sort by month
    for m, v in prices:
        print(f"  {m} = {v}")
else:
    print("NO PRICE DATA FOUND IN HTML")
    # Luu file de manual debug
    out = Path(r"d:\1. BDS\AI-Assistant\App_kham_benh_tai_san\debug_html.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved HTML to {out}")

