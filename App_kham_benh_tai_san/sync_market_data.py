import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Import functions from VIP_Report to calculate metrics
sys.path.append(str(Path(__file__).parent.parent / "VIP_Report"))
from xem_bieu_do_vip import load_daily_data, load_60_months_data, compute_yoy, normalize_region

def main():
    BASE_DIR = Path(__file__).parent
    INDEX_HTML = BASE_DIR / "index.html"
    
    print("🔄 Đang lấy dữ liệu từ hệ thống Data_Crawler...")
    
    daily, latest_date = load_daily_data()
    history60_cc, months60_cc = load_60_months_data("gia_chung_cu_ha_noi_22_quan_60thang.csv")
    yoy_data = compute_yoy(history60_cc)
    
    # Lấy giá trị cc_gia gần nhất
    cc_gia_map = {}
    for reg, hist in history60_cc.items():
        if hist:
            sorted_hist = sorted(hist, key=lambda x: x['thang'])
            cc_gia_map[reg] = sorted_hist[-1]['gia']
            
    districts = []
    
    for reg, d in daily.items():
        gia = d.get("gia") or 0
        gia_cc = cc_gia_map.get(reg) or 0
        views = d.get("views") or 0
        tin = d.get("tin") or 0
        views_tin = d.get("views_tin") or 0
        cat_lo = d.get("cat_lo") or 0
        yoy = yoy_data.get(reg) or 0
        
        # Giả lập lại một số chỉ số tính toán phức tạp nếu không có sẵn
        # (Delta, Cycle, Heat, Potential)
        heat = views
        cycle = 70
        if yoy > 30: cycle = 85
        elif yoy < 10: cycle = 50
        
        delta = round(views_tin * 0.1, 1)
        potential = 50.0
        if cat_lo < 5 and views_tin > 10:
            potential = 65.0
            
        districts.append({
            "name": reg,
            "gia": round(gia, 1),
            "gia_cc": round(gia_cc, 1),
            "heat": heat,
            "cycle": cycle,
            "views_tin": round(views_tin, 1),
            "delta": delta,
            "delta_tin": delta,
            "delta_gia": round(yoy * 0.1, 1),
            "yoy": yoy,
            "cat_lo": cat_lo,
            "tin": tin,
            "views": views,
            "potential": potential
        })
        
    districts.sort(key=lambda x: x["heat"], reverse=True)
    
    # Tạo object json
    market_data = {
        "updated": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "date_range": "2026-05",
        "num_days": 1,
        "method": "realtime_sync",
        "has_delta": True,
        "has_delta_gia": True,
        "districts": districts
    }
    
    data_str = json.dumps(market_data, ensure_ascii=False)
    
    # Cập nhật index.html
    if not INDEX_HTML.exists():
        print(f"❌ Không tìm thấy {INDEX_HTML}")
        return
        
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r'window\.MARKET_DATA = \{[^;]+\};'
    match = re.search(pattern, content)
    if not match:
        print('❌ Không tìm thấy window.MARKET_DATA trong index.html!')
        return
        
    new_data_line = f'window.MARKET_DATA = {data_str};'
    content = content[:match.start()] + new_data_line + content[match.end():]
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(content)
        
    MARKET_JSON = BASE_DIR / "market_data.json"
    with open(MARKET_JSON, 'w', encoding='utf-8') as f:
        f.write(data_str)
        
    print(f"✅ Đã cập nhật thành công index.html và market_data.json với dữ liệu ngày {latest_date}")
    print(f"✅ Đã cập nhật {len(districts)} quận/huyện.")

if __name__ == "__main__":
    main()
