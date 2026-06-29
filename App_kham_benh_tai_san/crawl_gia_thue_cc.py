# -*- coding: utf-8 -*-
"""
crawl_gia_thue_cc.py
========================
Crawl giá thuê chung cư trung bình (tr/m²/tháng) từ batdongsan.com.vn,
sau đó tính Rental Yield (%) = (Giá thuê TB × 12) / Giá bán hiện tại × 100.

Dựa trên cùng kiến trúc crawl_lich_su_gia_cc.py (Playwright + Regex).

Cài đặt:
  pip install playwright openpyxl
  playwright install chromium

Chạy:
  python crawl_gia_thue_cc.py
"""

import sys, io, re, time, random, csv
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright chưa cài. Chạy: pip install playwright && playwright install chromium")
    sys.exit(1)

# ============================================================
# CONFIG
# ============================================================

OUTPUT_DIR = Path(__file__).parent

# 18 quận có dữ liệu trong báo cáo (loại trừ Sóc Sơn, Mê Linh, Thạch Thất, Từ Sơn - không có dữ liệu)
DISTRICTS = {
    "Ba Đình":       "ba-dinh",
    "Bắc Từ Liêm":  "bac-tu-liem",
    "Cầu Giấy":      "cau-giay",
    "Đan Phượng":    "dan-phuong",
    "Đông Anh":      "dong-anh",
    "Đống Đa":       "dong-da",
    "Gia Lâm":       "gia-lam",
    "Hà Đông":       "ha-dong",
    "Hai Bà Trưng":  "hai-ba-trung",
    "Hoài Đức":      "hoai-duc",
    "Hoàn Kiếm":     "hoan-kiem",
    "Hoàng Mai":     "hoang-mai",
    "Long Biên":     "long-bien",
    "Nam Từ Liêm":   "nam-tu-liem",
    "Tây Hồ":        "tay-ho",
    "Thanh Trì":     "thanh-tri",
    "Thanh Xuân":    "thanh-xuan",
    "Văn Giang (HY)": "van-giang",
}

# URL cho thuê chung cư
RENT_URL = "https://batdongsan.com.vn/cho-thue-can-ho-chung-cu-{slug}"

# Dữ liệu giá bán hiện tại (T3/2026) từ CSV gốc
GIA_BAN_T3_2026 = {
    "Ba Đình": 179.6,
    "Bắc Từ Liêm": 105.8,
    "Cầu Giấy": 110.5,
    "Đan Phượng": 67.8,
    "Đông Anh": 121.2,
    "Đống Đa": 117.1,
    "Gia Lâm": 73.8,
    "Hà Đông": 77.1,
    "Hai Bà Trưng": 112.2,
    "Hoài Đức": 80.0,
    "Hoàn Kiếm": 473.1,
    "Hoàng Mai": 87.3,
    "Long Biên": 89.2,
    "Nam Từ Liêm": 95.7,
    "Tây Hồ": 149.8,
    "Thanh Trì": 74.8,
    "Thanh Xuân": 108.6,
    "Văn Giang (HY)": 72.2,
}

# ============================================================
# EXTRACT RENTAL PRICE
# ============================================================

def extract_avg_rental_price(html: str) -> dict:
    """
    Trích xuất giá thuê trung bình từ HTML.
    Chiến lược:
    1. Tìm dữ liệu chart giá thuê từ __NEXT_DATA__ (tương tự giá bán)
    2. Nếu không có, tìm giá hiển thị trực tiếp trên listing
    """
    result = {"gia_thue_trm2": None, "so_tin": None, "note": ""}
    
    # --- Cách 1: Tìm giá TB từ chart data (month-value pairs) ---
    pts = re.findall(r'\{"month"\s*:\s*"([2]\d{3}-\d{2})"\s*,\s*"value"\s*:\s*([\d.]+)\}', html)
    if pts:
        # Lấy 3 tháng gần nhất để tính trung bình
        values = [(m, float(v)) for m, v in pts]
        values.sort(key=lambda x: x[0], reverse=True)
        recent = values[:3]
        if recent:
            avg = sum(v for _, v in recent) / len(recent)
            result["gia_thue_trm2"] = round(avg, 2)
            result["note"] = f"Chart data ({len(values)} điểm, TB 3T gần nhất)"
            return result
    
    # --- Cách 2: Tìm giá từ listing trực tiếp ---
    # Pattern: "X triệu/m²/tháng" hoặc "X tr/m²"
    price_per_m2 = re.findall(r'([\d.,]+)\s*(?:triệu|tr)\s*/\s*m', html)
    if price_per_m2:
        try:
            prices = [float(p.replace(",", ".")) for p in price_per_m2 if 0.05 < float(p.replace(",", ".")) < 2.0]
            if prices:
                result["gia_thue_trm2"] = round(sum(prices) / len(prices), 3)
                result["note"] = f"Listing avg ({len(prices)} mẫu)"
                return result
        except:
            pass
    
    # --- Cách 3: Tìm giá tổng từ listing rồi ước tính ---
    # Pattern: "X triệu/tháng" (giá thuê tổng, không phải /m²)
    total_prices = re.findall(r'([\d.,]+)\s*(?:triệu|tr)\s*/\s*th', html)
    if total_prices:
        try:
            prices = [float(p.replace(",", ".")) for p in total_prices if 3 < float(p.replace(",", ".")) < 100]
            if prices:
                avg_total = sum(prices) / len(prices)
                # Ước tính diện tích trung bình chung cư = 70m²
                result["gia_thue_trm2"] = round(avg_total / 70, 3)
                result["so_tin"] = len(prices)
                result["note"] = f"Total price / 70m² ({len(prices)} mẫu)"
                return result
        except:
            pass
    
    # --- Cách 4: Tìm tổng số tin đăng ---
    tin_match = re.search(r'Hiện có\s*([\d.]+)\s*bất', html)
    if tin_match:
        result["so_tin"] = int(tin_match.group(1).replace(".", ""))
    
    result["note"] = "Không tìm thấy dữ liệu giá thuê"
    return result

# ============================================================
# CRAWLER
# ============================================================

def crawl_rental_district(slug: str, name: str, ctx) -> dict:
    url = RENT_URL.format(slug=slug)
    print(f"\n  📍 {name} → {url}")
    
    try:
        page = ctx.new_page()
        # Block resources không cần để tăng tốc
        page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,ico,css}", lambda route: route.abort())
        
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        
        # Đợi Cloudflare + lazy load
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        page.wait_for_timeout(2000)
        
        html = page.content()
        page.close()
        
        result = extract_avg_rental_price(html)
        
        if result["gia_thue_trm2"]:
            print(f"    ✅ Giá thuê TB: {result['gia_thue_trm2']} tr/m²/tháng — {result['note']}")
        else:
            print(f"    ⚠️  {result['note']} (HTML = {len(html)/1024:.1f}KB)")
            # Lưu HTML debug
            debug_path = OUTPUT_DIR / f"_debug_rental_{slug}.html"
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"    📄 Đã lưu HTML debug: {debug_path.name}")
        
        return result
    except Exception as e:
        print(f"    ❌ Lỗi: {e}")
        try: page.close()
        except: pass
        return {"gia_thue_trm2": None, "so_tin": None, "note": f"Error: {e}"}

# ============================================================
# YIELD CALCULATION
# ============================================================

def calculate_yield(gia_thue_trm2: float, gia_ban_trm2: float) -> float:
    """Tính Rental Yield = (Giá thuê × 12 tháng) / Giá bán × 100%"""
    if not gia_thue_trm2 or not gia_ban_trm2 or gia_ban_trm2 == 0:
        return 0
    return round((gia_thue_trm2 * 12 / gia_ban_trm2) * 100, 2)

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("  CRAWL GIÁ THUÊ CHUNG CƯ — TÍNH RENTAL YIELD")
    print("  Nguồn: batdongsan.com.vn | T4/2026")
    print("=" * 60)
    
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        for name, slug in DISTRICTS.items():
            data = crawl_rental_district(slug, name, ctx)
            gia_ban = GIA_BAN_T3_2026.get(name, 0)
            gia_thue = data.get("gia_thue_trm2")
            
            rental_yield = calculate_yield(gia_thue, gia_ban) if gia_thue else None
            
            results[name] = {
                "gia_ban_trm2": gia_ban,
                "gia_thue_trm2": gia_thue,
                "rental_yield_pct": rental_yield,
                "so_tin": data.get("so_tin"),
                "note": data.get("note", ""),
            }
            
            time.sleep(random.uniform(4, 8))
        
        browser.close()
    
    # ============================================================
    # EXPORT CSV
    # ============================================================
    
    csv_path = OUTPUT_DIR / "rental_yield_ha_noi.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Quận/Huyện", "Giá Bán (tr/m²)", "Giá Thuê (tr/m²/tháng)", "Rental Yield (%)", "Số Tin Thuê", "Ghi Chú"])
        
        for name in sorted(results.keys()):
            r = results[name]
            w.writerow([
                name,
                r["gia_ban_trm2"],
                r["gia_thue_trm2"] or "N/A",
                r["rental_yield_pct"] or "N/A",
                r["so_tin"] or "N/A",
                r["note"],
            ])
    
    print(f"\n{'=' * 60}")
    print(f"✅ Đã lưu kết quả: {csv_path}")
    
    # ============================================================
    # CONSOLE SUMMARY
    # ============================================================
    
    print(f"\n{'=' * 60}")
    print(f"  BẢNG RENTAL YIELD — CHUNG CƯ HÀ NỘI T4/2026")
    print(f"{'=' * 60}")
    print(f"{'Quận':<18} {'Giá Bán':>10} {'Giá Thuê':>10} {'Yield':>8} {'Ghi Chú'}")
    print("-" * 70)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1].get("rental_yield_pct") or 0, reverse=True)
    for name, r in sorted_results:
        gia_ban = f"{r['gia_ban_trm2']:.1f}"
        gia_thue = f"{r['gia_thue_trm2']:.3f}" if r['gia_thue_trm2'] else "N/A"
        yld = f"{r['rental_yield_pct']:.2f}%" if r['rental_yield_pct'] else "N/A"
        print(f"{name:<18} {gia_ban:>10} {gia_thue:>10} {yld:>8} {r['note']}")

if __name__ == "__main__":
    main()
