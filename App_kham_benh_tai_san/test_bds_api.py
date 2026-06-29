"""
Script lấy dữ liệu giá BĐS 60 tháng từ batdongsan.com.vn
API: POST https://batdongsan.com.vn/Origins/CommonData/GetPricingHistory
"""
import requests
import json
import csv
import time

# Cookie từ browser session đã đăng nhập
COOKIES = {
    "ajs_anonymous_id": "123b7412-402b-4736-af71-c5e7962f32bb",
    "BDS.UMS.Cookie": "CfDJ8GsOAEqwP6xPtxb1UfIzE28-Mez-wWs9YV-kmwsByNfbsdUhVyQCe5IB10zxW5lS_xz8JSLFB5-eRikZEyY8uDQAgVPYX72Tb9Ub_Ors_VOfIDAIbtufqQatzXFazBCU4AUROw6A1HGwezwnnShxkbKzJFB1oX_l9CQ3a_PKXunPh1W1IJ0jVdQit2B1DolGQJHWxFCkwes7N16zaRTnaYr_u7TfWb_dB_PUmw0JA3VSvZRiPVOKh9gMHR6b_x4PH5dMhd5_wO3gNxiNLtfcNF_fcH7AHDhFhHGq1fpHruKsKJTCcbJKskrqqbC-xLoliXhPCdCFS2xa4702xjuiV5MyZ-3FbNvqPsd0Kn0N6jVDa9Edh66UYzYBmMUcfKwTd_cfQNqStZjy9_60NLBqDzZ0mG4sicsv5cq3LhzYWPEdKYZRXQwRJsS4f6pNYj3e8Dv3cQtmKHdZNiChCCpz2IPcCTORGhXigdZK644-Vutsotme4eHEtp45s8Z0y2KwGAHV4hn981CTlndhQkaERQ7AhybPri0cJQS6GVvtpQ5VChUYgAsKwVPQbjqcMgPoNE33aZiq2VSGOOPBO7lphalsOMrV8IZDBCbzGRQJlKmIP3OJuoQJ9P7BbJ7COPT8E1bmngnuQ-IXrKkGB7ewWHFlIgqqJoxpjQ-FVJSUIgHeUx8G2GekVYO820PY5peB1Q",
}

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://batdongsan.com.vn/",
    "Origin": "https://batdongsan.com.vn",
}

API_URL = "https://batdongsan.com.vn/Origins/CommonData/GetPricingHistory"

# encryptedParams cho từng khu vực (Chung Cư - productType=38)
CC_DISTRICTS = {
    "Ba Dinh": "fd67c56d27be144928af2b1ebc911983b8d058ae090c447fa2e39bffd8e1a46a5ef3754b3a41827d0934250b81572a528439721717ee66dc34bd4c198ac5b9fe62df66c88f7385f61a17fa16c8c89a1b32f88507bbe50e1680cda05b1b1b927383915daeb7f99ec80b223678ac04574d",
    "Bac Tu Liem": "fd67c56d27be144928af2b1ebc911983b8d058ae090c447fa2e39bffd8e1a46a5ef3754b3a41827d0934250b81572a52d5fc4cc88fdb9ce097e40e83d9434d39d12bd7816bd6c4945f6daa3c41c42dad8cb13d3df2e542e096dfb442d8f7baaaba8a57c6572632fff9ae8700984011d2e51fda3202c0916a",
    "Ha Dong": "fd67c56d27be144928af2b1ebc911983b8d058ae090c447fa2e39bffd8e1a46a5ef3754b3a41827d0934250b81572a5271f854bffa63c355b345ea440025c4984ccaa23e67bef70523bcb37087eb94ac24371e6784085b49758477eebdb8b8ad4d961f649429739eb69475a908081c7b1182ae35df2a69a4",
    "Hoai Duc": "fd67c56d27be144928af2b1ebc911983b8d058ae090c447fa2e39bffd8e1a46a5ef3754b3a41827d0934250b81572a52ac3dae40cb44ae3db345ea440025c4984ccaa23e67bef70523bcb37087eb94ac24371e6784085b49758477eebdb8b8ad4d961f649429739eb69475a908081c7b1182ae35df2a69a4",
    "Cau Giay": "fd67c56d27be144928af2b1ebc911983b8d058ae090c447fa2e39bffd8e1a46a5ef3754b3a41827d0934250b81572a521efb47d59bee85f234bd4c198ac5b9fe62df66c88f7385f61a17fa16c8c89a1b32f88507bbe50e1680cda05b1b1b927383915daeb7f99ec80b223678ac04574d",
}

def get_price_history(district_name, encrypted_params, product_type=38):
    """Gọi API lấy lịch sử giá"""
    payload = {
        "encryptedParams": encrypted_params,
        "productType": product_type,
        "countOfYears": 5
    }
    try:
        resp = requests.post(API_URL, json=payload, cookies=COOKIES, headers=HEADERS, timeout=15)
        print(f"[{district_name}] Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            return data
        else:
            print(f"  Error response: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def extract_monthly_data(response_json):
    """Trích xuất dữ liệu tháng từ response"""
    monthly = []
    if not response_json:
        return monthly
    
    # Try different JSON structures
    chart_points = None
    if "chartPoints" in response_json:
        chart_points = response_json["chartPoints"]
    elif "data" in response_json and "chartPoints" in response_json.get("data", {}):
        chart_points = response_json["data"]["chartPoints"]
    elif isinstance(response_json, list):
        chart_points = response_json
    
    if chart_points:
        for point in chart_points:
            label = point.get("label", point.get("Label", ""))
            avg = point.get("avg", point.get("Avg", point.get("price", "")))
            min_p = point.get("min", point.get("Min", ""))
            max_p = point.get("max", point.get("Max", ""))
            monthly.append({
                "label": label,
                "avg": avg,
                "min": min_p,
                "max": max_p
            })
    
    return monthly

# Test với Ba Đình
print("=== Testing API Connection ===")
result = get_price_history("Ba Dinh", CC_DISTRICTS["Ba Dinh"])
if result:
    print("Raw response structure:", json.dumps(result, indent=2, ensure_ascii=False)[:1000])
    monthly = extract_monthly_data(result)
    print(f"\nExtracted {len(monthly)} months for Ba Dinh:")
    for m in monthly[:5]:
        print(f"  {m}")
else:
    print("API call failed - need to update cookies from browser")
