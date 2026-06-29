# -*- coding: utf-8 -*-
"""
Tim API endpoint lich su gia tu batdongsan.com.vn
Su dung domcontentloaded + intercept ALL requests
"""
import sys, io, json, re, time
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright

# Thu nhieu URL co the co du lieu lich su gia
TEST_URLS = [
    "https://batdongsan.com.vn/ban-can-ho-chung-cu-hoang-mai",
    "https://batdongsan.com.vn/thong-ke-gia-bat-dong-san",
    "https://batdongsan.com.vn/bao-cao-thi-truong",
]

all_reqs = []
all_resps = []

def on_request(req):
    url = req.url
    if "batdongsan" in url and "." not in url.split("/")[-1]:
        all_reqs.append(url)

def on_response(resp):
    try:
        url = resp.url
        status = resp.status
        ct = resp.headers.get("content-type","")
        if "json" in ct and status == 200 and "batdongsan" in url:
            try:
                data = resp.json()
                size = len(str(data))
                all_resps.append({"url": url, "size": size, "preview": str(data)[:300]})
                print(f"  JSON: {url[:90]} [{size}c]")
            except:
                pass
    except:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    page = ctx.new_page()
    page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,ico,css}", lambda r: r.abort())
    page.on("request", on_request)
    page.on("response", on_response)

    for url in TEST_URLS[:1]:  # Chi test 1 URL truoc
        print(f"\nLoading: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)
            # Scroll de trigger lazy chart load
            for pct in [0.25, 0.5, 0.75, 1.0]:
                page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {pct})")
                page.wait_for_timeout(1500)
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"  Error: {e}")

    # Tim __NEXT_DATA__ trong cuoi cung
    html = page.content()
    page.close(); ctx.close(); browser.close()

print(f"\n=== REQUESTS ({len(all_reqs)}) ===")
for r in all_reqs[:30]:
    print(f"  {r}")

print(f"\n=== RESPONSES ({len(all_resps)}) ===")
for r in all_resps:
    print(f"  [{r['size']}c] {r['url']}")
    print(f"    {r['preview'][:150]}")

# Tim patterns trong HTML
print(f"\n=== HTML ANALYSIS ({len(html):,}c) ===")
check = {
    "__NEXT_DATA__": r'id="__NEXT_DATA__"',
    "priceHistory": r'"priceHistory"',
    "priceIndex": r'"priceIndex"',
    "month+price": r'"month"\s*:\s*"20[12]\d',
    "GiaTrungBinh": r'[Gg]ia[Tt]rung[Bb]inh|gia_trung_binh',
    "Microservice price": r'microservice.*[Pp]rice|[Pp]rice.*microservice',
}
for name, pat in check.items():
    if re.search(pat, html, re.IGNORECASE):
        m = re.search(pat, html, re.IGNORECASE)
        snippet = html[max(0,m.start()-30):m.end()+200]
        print(f"  FOUND [{name}]: ...{snippet[:150]}...")
    else:
        print(f"  miss  [{name}]")

# Luu ket qua
out_dir = Path(r"d:\1. BDS\AI-Assistant\App_kham_benh_tai_san")
with open(out_dir / "test_api_result.json", "w", encoding="utf-8") as f:
    json.dump({"requests": all_reqs, "responses": all_resps}, f, ensure_ascii=False, indent=2)
print(f"\nSaved: test_api_result.json")
