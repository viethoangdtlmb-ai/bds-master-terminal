import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:/1. BDS/AI-Assistant/bds-dashboard/data/dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"{'Khu Vực':<22} {'Nhà/m²':>10} {'CC/m²':>10} {'Bất thường?'}")
print("-" * 62)

for d in sorted(data['districts'], key=lambda x: x['gia'] or 0, reverse=True):
    gia     = d.get('gia', 0) or 0
    gia_cc  = d.get('gia_cc', 0) or 0
    
    flags = []
    if gia == 0:       flags.append("❌ Nhà=0")
    if gia_cc == 0:    flags.append("❌ CC=0")
    if gia > 0 and gia_cc > 0 and gia_cc > gia:
        flags.append(f"⚠️ CC({gia_cc}) > Nhà({gia})")
    if gia > 0 and gia < 30:
        flags.append("⚠️ Nhà quá thấp")
    if gia_cc > 200:
        flags.append("⚠️ CC quá cao")
    
    flag_str = " | ".join(flags) if flags else "✅ OK"
    print(f"{d['name']:<22} {gia:>10.1f} {gia_cc:>10.1f}   {flag_str}")

print(f"\nTổng: {len(data['districts'])} khu vực | Cập nhật: {data['updated']}")
