import csv, sys, io
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = defaultdict(list)
with open(r'd:\1. BDS\AI-Assistant\App_kham_benh_tai_san\gia_chung_cu_ha_noi_22_quan_60thang.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        k = row['Khu_vuc']
        price = row['Gia_TB (tr/m2)']
        month = row['Thang']
        if price != 'N/A':
            # normalize month into a sortable index, roughly
            data[k].append({'month': month, 'price': float(price)})

results = []
for k, rows in sorted(data.items()):
    if len(rows) < 24: continue # filter out too little data
    prices = [r['price'] for r in rows]
    
    # 1. Stress Test: Credit Crunch (Late 2022 to Mid 2023)
    # T9/2022 was roughly index 18 (if T3/21 is 0), T6/2023 was roughly index 27
    crunch_start_price = None
    crunch_end_price = None
    for i, r in enumerate(rows):
        if r['month'] == 'T9/22': crunch_start_price = r['price']
        if r['month'] == 'T6/23': crunch_end_price = r['price']
    
    crunch_resilience = 0
    if crunch_start_price and crunch_end_price:
        crunch_resilience = ((crunch_end_price - crunch_start_price) / crunch_start_price) * 100

    # 2. Cycle Phase Classification (Classic 4-Phase Model)
    # Determine looking at last 6 months vs peak and historical median
    peak = max(prices)
    current = prices[-1]
    dist_from_peak = ((current - peak) / peak) * 100
    
    last_3 = prices[-3:]
    prior_3 = prices[-6:-3]
    recent_trend = ((last_3[-1] - last_3[0]) / last_3[0]) * 100
    avg_growth_6m = ((last_3[-1] - prior_3[0]) / prior_3[0]) * 100
    
    yoy = ((prices[-1] - prices[-13]) / prices[-13] * 100) if len(prices) >= 13 else 0
    
    # Simple phase classification logic
    if dist_from_peak < -5 and recent_trend <= 0:
        phase = 'SUY THOAI (Recession)'
    elif dist_from_peak < -3 and recent_trend > 0:
        phase = 'PHUC HOI (Recovery)'
    elif dist_from_peak >= -2 and yoy > 30 and recent_trend > 5:
        phase = 'BUNG NO (Bubble/Hyper-Supply)'
    elif dist_from_peak >= -3 and yoy > 10:
        phase = 'TANG TRUONG (Expansion)'
    else:
        phase = 'DI NGANG (Stagnation)'

    # 3. BCG Matrix Typology (Growth vs Market Share/Price Level)
    # Price level (High > 100, Mid > 75, Low < 75)
    # Growth YoY (High > 40, Mid > 25, Low < 25)
    typology = "N/A"
    if current > 100 and yoy > 40: typology = 'STAR (Ngoi Sao)'
    elif current > 100 and yoy <= 40: typology = 'CASH COW (Con bo Sua)'
    elif current < 90 and yoy > 40: typology = 'QUESTION MARK (An So)'
    elif current < 90 and yoy <= 40: typology = 'DOG (Ke bam tru)'
    else: typology = 'MID-TIER'
        
    results.append({
        'name': k,
        'crunch_resilience': crunch_resilience,
        'phase': phase,
        'typology': typology,
        'yoy': yoy,
        'current': current
    })

print('=' * 85)
print('DEEP ANALYSIS V2: CYCLE PHASES & STRESS TESTING')
print('=' * 85)

print('\n[1] CHU KY THI TRUONG (REAL ESTATE CYCLE CLOCK)')
print('Dua vao khoang cach toi dinh, xu huong 3 thang gan va YoY de xac dinh pha hien tai.')
phases_group = defaultdict(list)
for r in results:
    phases_group[r['phase']].append(f"{r['name']} ({r['yoy']:+.1f}% YoY)")

for phase, items in phases_group.items():
    print(f'>> {phase}:')
    for item in items:
        print(f'   - {item}')

print('\n[2] MA TRAN DAU TU (BCG MATRIX TYPOLOGY)')
print('STAR: Dat + Tang Manh | CASH COW: Dat + Tang Vua (An toan) | QUESTION MARK: Re + Tang Manh | DOG: Re + Tang Cham')
type_group = defaultdict(list)
for r in results:
    type_group[r['typology']].append(f"{r['name']} ({r['current']:.1f} tr/m2)")

for typo, items in type_group.items():
    print(f'>> {typo}:')
    for item in items:
        print(f'   - {item}')

print('\n[3] STRESS TEST: SIET TIN DUNG 2022-2023 (T9/22 -> T6/23)')
print('Quoc gia siet tin dung, lai suat len 12%. Khu vuc nao giu gia tot nhat? (Tinh % tang/giam)')
for r in sorted(results, key=lambda x: x['crunch_resilience'], reverse=True):
    safe_str = "SIE U PHONG THU" if r["crunch_resilience"] > 10 else "An toan" if r["crunch_resilience"] > 0 else "De ton thuong"
    print(f'  {r["name"]:<20} {r["crunch_resilience"]:>+6.1f}% -> {safe_str}')
