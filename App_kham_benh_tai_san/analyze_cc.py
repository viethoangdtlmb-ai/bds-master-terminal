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
            data[k].append({'month': month, 'price': float(price)})

print('=' * 75)
print('PHAN TICH GIA CHUNG CU 22 QUAN - 60 THANG (T3/2021 - T3/2026)')
print('=' * 75)

results = []
for k, rows in sorted(data.items()):
    if len(rows) < 3: continue
    first = rows[0]['price']
    last = rows[-1]['price']
    growth = ((last - first) / first) * 100
    t3_25 = None
    for r in rows:
        if r['month'] == 'T3/25': t3_25 = r['price']
    yoy = ((last - t3_25) / t3_25 * 100) if t3_25 else 0
    min_p = min(r['price'] for r in rows)
    max_p = max(r['price'] for r in rows)
    peak_month = [r['month'] for r in rows if r['price'] == max_p][0]
    
    month_map = {}
    for row in rows:
        month_map[row['month']] = row['price']
    milestones = ['T3/21','T3/22','T3/23','T3/24','T3/25','T3/26']
    phases = [month_map.get(m) for m in milestones]
    
    results.append({
        'name': k, 'first': first, 'last': last, 'growth': growth,
        'yoy': yoy, 'min': min_p, 'max': max_p, 'peak': peak_month,
        'rows': rows, 'phases': phases
    })

print(f'\n{"Khu vuc":<20} {"T3/21":>8} {"T3/26":>8} {"5Y Tang":>9} {"YoY":>8} {"Peak":>10}')
print('-' * 60)
for r in sorted(results, key=lambda x: x['growth'], reverse=True):
    print(f'{r["name"]:<20} {r["first"]:>7.1f} {r["last"]:>7.1f} {r["growth"]:>+8.1f}% {r["yoy"]:>+7.1f}% {r["peak"]:>10}')

print('\n' + '=' * 75)
print('TOP 5 TANG GIA MANH NHAT (5 nam):')
sorted_g = sorted(results, key=lambda x: x['growth'], reverse=True)
for i, r in enumerate(sorted_g[:5]):
    print(f'  {i+1}. {r["name"]:<20} +{r["growth"]:.1f}% ({r["first"]:.1f} -> {r["last"]:.1f} tr/m2)')

print('\nTOP 5 GIA CAO NHAT (T3/2026):')
sorted_p = sorted(results, key=lambda x: x['last'], reverse=True)
for i, r in enumerate(sorted_p[:5]):
    print(f'  {i+1}. {r["name"]:<20} {r["last"]:.1f} tr/m2')

print('\nTOP 5 GIA RE NHAT (T3/2026):')
for i, r in enumerate(sorted_p[-5:][::-1]):
    print(f'  {i+1}. {r["name"]:<20} {r["last"]:.1f} tr/m2 (+{r["growth"]:.0f}% trong 5 nam)')

print('\nTOP 5 YoY (T3/25 -> T3/26):')
sorted_y = sorted(results, key=lambda x: x['yoy'], reverse=True)
for i, r in enumerate(sorted_y[:5]):
    print(f'  {i+1}. {r["name"]:<20} +{r["yoy"]:.1f}% YoY ({r["last"]:.1f} tr/m2)')

print('\n' + '=' * 75)
print('TANG TRUONG THEO TUNG NAM:')
print(f'{"Khu vuc":<20} {"21-22":>8} {"22-23":>8} {"23-24":>8} {"24-25":>8} {"25-26":>8}')
print('-' * 65)
for r in sorted(results, key=lambda x: x['growth'], reverse=True):
    vals = r['phases']
    parts = []
    for i in range(len(vals)-1):
        if vals[i] and vals[i+1]:
            chg = ((vals[i+1] - vals[i]) / vals[i]) * 100
            parts.append(f'{chg:>+7.1f}%')
        else:
            parts.append(f'{"N/A":>8}')
    print(f'{r["name"]:<20} {" ".join(parts)}')

print('\n' + '=' * 75)
print('TIN HIEU THI TRUONG:')

print('\n[A] DANG GIAM TU DINH (>3%):')
found = False
for r in sorted(results, key=lambda x: (x['last']/x['max'])):
    drop = ((r['last'] - r['max']) / r['max']) * 100
    if drop < -3:
        found = True
        print(f'  - {r["name"]:<20} {r["last"]:.1f} tr/m2 (dinh {r["max"]:.1f} vao {r["peak"]}, {drop:.1f}%)')
if not found: print('  Khong co')

print('\n[B] VAN DANG O DINH:')
for r in sorted(results, key=lambda x: x['last'], reverse=True):
    drop = ((r['last'] - r['max']) / r['max']) * 100
    if drop >= -3:
        print(f'  - {r["name"]:<20} {r["last"]:.1f} tr/m2')

print('\n[C] TOC DO 12T GAN vs 12T TRUOC:')
for r in sorted(results, key=lambda x: x['growth'], reverse=True):
    rows = r['rows']
    if len(rows) >= 24:
        r12 = rows[-12:]
        p12 = rows[-24:-12]
        r12_chg = ((r12[-1]['price'] - r12[0]['price']) / r12[0]['price']) * 100
        p12_chg = ((p12[-1]['price'] - p12[0]['price']) / p12[0]['price']) * 100
        signal = 'TANG TOC' if r12_chg > p12_chg else 'GIAM TOC'
        print(f'  {r["name"]:<20} 12T gan: +{r12_chg:>5.1f}% | 12T truoc: +{p12_chg:>5.1f}% -> {signal}')

print('\n' + '=' * 75)
print('TONG QUAN:')
avg_first = sum(r['first'] for r in results) / len(results)
avg_last = sum(r['last'] for r in results) / len(results)
avg_growth = ((avg_last - avg_first) / avg_first) * 100
avg_yoy = sum(r['yoy'] for r in results) / len(results)
print(f'  Gia TB T3/21:    {avg_first:.1f} tr/m2')
print(f'  Gia TB T3/26:    {avg_last:.1f} tr/m2')
print(f'  Tang TB 5 nam:   +{avg_growth:.1f}%')
print(f'  Tang TB YoY:     +{avg_yoy:.1f}%')
