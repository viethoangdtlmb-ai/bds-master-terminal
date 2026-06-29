import csv, sys, io, statistics
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

results = []
for k, rows in sorted(data.items()):
    if len(rows) < 12: continue
    prices = [r['price'] for r in rows]
    
    # 1. Volatility (Risk): Std Dev of month-over-month growth variations
    mom_growths = []
    for i in range(1, len(prices)):
        mom_growths.append((prices[i] - prices[i-1]) / prices[i-1] * 100)
    
    volatility = statistics.stdev(mom_growths) if len(mom_growths) > 1 else 0
    avg_mom = sum(mom_growths) / len(mom_growths)
    
    # Sharpe-like Ratio: Reward / Risk (Avg MoM Growth / Volatility)
    sharpe = (avg_mom / volatility) if volatility > 0 else 0
    
    # 2. Maximum Drawdown (Resilience)
    max_drawdown = 0
    peak = prices[0]
    for p in prices:
        if p > peak:
            peak = p
        drawdown = (peak - p) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    # 3. Momentum (RSI-like simple momentum over last 6 months vs prior 6 months)
    last_6 = prices[-6:]
    prior_6 = prices[-12:-6]
    mom_last_6 = ((last_6[-1] - last_6[0]) / last_6[0]) * 100 if last_6[0] > 0 else 0
    mom_prior_6 = ((prior_6[-1] - prior_6[0]) / prior_6[0]) * 100 if prior_6[0] > 0 else 0
    momentum_shift = mom_last_6 - mom_prior_6
    
    # Check consistency (months without drops)
    up_months = sum(1 for m in mom_growths if m > 0)
    consistency = up_months / len(mom_growths) * 100
    
    results.append({
        'name': k,
        'current_price': prices[-1],
        'avg_mom': avg_mom,
        'volatility': volatility,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'mom_last_6': mom_last_6,
        'mom_prior_6': mom_prior_6,
        'momentum_shift': momentum_shift,
        'consistency': consistency
    })

print('=' * 85)
print('DATA SCIENCE METRICS: RISK, REWARD & MOMENTUM')
print('=' * 85)

print('\n[1] HIEU SUAT TINH BAN - SHARPE RATIO PROXY (Tang truong / Rui ro)')
print('Chung cu nao giu tien on dinh nhat va tang truong tot nhat, it bien dong nhat?')
print(f'{"Khu vuc":<20} {"Sharpe Ratio":>15} {"MoM TB (%)":>12} {"Bien dong (%)":>15}')
print('-'*65)
for r in sorted(results, key=lambda x: x['sharpe'], reverse=True):
    print(f'{r["name"]:<20} {r["sharpe"]:>15.2f} {r["avg_mom"]:>12.2f} {r["volatility"]:>15.2f}')

print('\n[2] DO BEN VUNG (MACIMUM DRAWDOWN & Nhip TANG)')
print('Chung cu nao de rot gia sau nhat khi thi truong xau? (%)')
for r in sorted(results, key=lambda x: x['max_drawdown'], reverse=True):
    if r['max_drawdown'] > 5:
        print(f'  - {r["name"]:<20} Giam sau nhat: -{r["max_drawdown"]:.1f}% tu dinh')

print('\n[3] DO GIA TOC (MOMENTUM SHIFT - 6 Thang Gan kieu RSI)')
print('Khu vuc nao dang bom tien dot bien trong 6 thang qua so voi 6 thang truoc do?')
for r in sorted(results, key=lambda x: x['momentum_shift'], reverse=True):
    shift = r["momentum_shift"]
    status = "BOM TIEN MANH" if shift > 15 else "Tang toc nhe" if shift > 5 else "Ha nhiet"
    print(f'  {r["name"]:<20} Shift: {shift:>+6.1f} pct points (6T gan: +{r["mom_last_6"]:.1f}% vs truoc: +{r["mom_prior_6"]:.1f}%) -> {status}')

print('\n[4] CHI SO ON DINH (TY LE THANG TANG GIA)')
for r in sorted(results, key=lambda x: x['consistency'], reverse=True)[:5]:
    print(f'  {r["name"]:<20} Tang {r["consistency"]:.1f}% so thang')
