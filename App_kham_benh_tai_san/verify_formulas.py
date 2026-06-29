import io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("KIEM TRA CONG THUC calcAsset() - SO LIEU THUC TE")
print("=" * 60)

# Nha Pho Hoai Duc: cost=6Ty, market=9Ty, loan=65%, rate=8%, term=20yr, grace=6th
# rent=18Tr, mgmt=2Tr, maint=12Tr/yr
cost=6; market=9; loanpct=65; rate=8; loanterm=20; grace=6
rent=18; mgmt=2; maint_annual=12
year_buy=2022; year_now=2026

# 1. Equity
equity = cost * (1 - loanpct/100)
debt   = cost * loanpct/100
print(f"\n1. EQUITY: {cost} x (1 - {loanpct}%) = {equity:.2f} Ty  [OK]")
print(f"   Du no : {debt:.2f} Ty = {debt*1000:.0f} Trieu")

# 2. NOI
maint_m = maint_annual / 12
noi = rent - mgmt - maint_m
print(f"\n2. NOI: {rent} - {mgmt} - {maint_m:.1f} = {noi:.1f} Tr/thang  [OK]")

# 3. Loan payment
debtM  = debt * 1000
rateM  = rate / 100 / 12
n_m    = loanterm * 12          # current code
n_fix  = loanterm * 12 - grace  # fixed: tru grace period

intOnly = debtM * rateM
pmt_code = debtM*rateM / (1 - (1+rateM)**(-n_m))
pmt_fix  = debtM*rateM / (1 - (1+rateM)**(-n_fix))
princ_code = pmt_code - intOnly
princ_fix  = pmt_fix  - intOnly

print(f"\n3. TRA NO (sau an han):")
print(f"   Lai thang     = {intOnly:.2f} Tr  [OK]")
print(f"   [BUG] n_m={n_m}th  -> principal = {princ_code:.2f} Tr/thang")
print(f"   [FIX] n_m={n_fix}th -> principal = {princ_fix:.2f} Tr/thang")
print(f"   Chenh lech    = {princ_fix-princ_code:.2f} Tr/thang ({(princ_fix-princ_code)/princ_fix*100:.1f}% thap hon thuc te)")

# 4. Cashflow
totalDebt_grace = intOnly  # during grace: chi tra lai
totalDebt_code  = intOnly + princ_code
totalDebt_fix   = intOnly + princ_fix
cf_grace = noi - totalDebt_grace
cf_code  = noi - totalDebt_code
cf_fix   = noi - totalDebt_fix
print(f"\n4. CASHFLOW:")
print(f"   Trong an han : {noi:.1f} - {totalDebt_grace:.2f} = {cf_grace:.2f} Tr/thang  [OK]")
print(f"   [BUG] sau an han : {cf_code:.2f} Tr/thang")
print(f"   [FIX] sau an han : {cf_fix:.2f} Tr/thang")

# 5. DSCR
dscr_grace = noi / totalDebt_grace
dscr_code  = noi / totalDebt_code
dscr_fix   = noi / totalDebt_fix
print(f"\n5. DSCR:")
print(f"   Trong an han : {dscr_grace:.3f}  [OK - dung]")
print(f"   [BUG] sau an han : {dscr_code:.3f}")
print(f"   [FIX] sau an han : {dscr_fix:.3f}")

# 6. ROE
roe_code = (cf_grace * 12) / (equity * 1000) * 100
print(f"\n6. ROE (Cash ROE - chi tinh cashflow, KHONG tinh tang gia):")
print(f"   ROE = {cf_grace:.2f} x 12 / {equity*1000:.0f}Tr = {roe_code:.1f}%/nam  [OK - la Cash ROE]")
print(f"   [NOTE] ROE toan phan = cashflow + tang gia / von tu co = chua tinh")

# 7. FLOOR PRICE BUG
years = year_now - year_buy
laiCD_bug  = cost * rate/100 * years        # BUG: rate on full cost
laiCD_fix  = debt * rate/100 * years        # FIX: rate on debt only
floor_bug  = cost + laiCD_bug + cost*0.02 + cost*0.015
floor_fix  = cost + laiCD_fix + cost*0.02 + cost*0.015
print(f"\n7. GIA SAN HOA VON (nam mua={year_buy}, nam nay={year_now}, so nam={years}):")
print(f"   Chi phi 3.5%  = cost x 2% + cost x 1.5% = {cost*0.035:.3f} Ty (OK)")
print(f"   [BUG] Lai tich luy = COST x rate x nam = {cost} x {rate}% x {years} = {laiCD_bug:.3f} Ty  <- SAI!")
print(f"         -> Gia san = {floor_bug:.3f} Ty (qua cao)")
print(f"   [FIX] Lai tich luy = DEBT x rate x nam = {debt:.1f} x {rate}% x {years} = {laiCD_fix:.3f} Ty")
print(f"         -> Gia san = {floor_fix:.3f} Ty")
print(f"   Chenh lech    = {floor_bug-floor_fix:.3f} Ty ({(floor_bug-floor_fix)/floor_fix*100:.1f}% cao hon THUC TE)")
print(f"   Ket qua: market={market}Ty > floor_fix={floor_fix:.3f}Ty -> {'TREN san OK' if market>=floor_fix else 'DUOI san CANH BAO'}")

# 8. Health Score check
dscr  = dscr_grace     # khi dang an han
roe   = roe_code
viewsTin = 18.1        # Hoai Duc tu MARKET_DATA
dscrScore = min(dscr * 100, 100)
roeScore  = max(0, min(roe / 18 * 100, 100))
vtScore   = max(0, min(viewsTin / 20 * 100, 100))
health    = round(dscrScore*0.4 + roeScore*0.4 + vtScore*0.2)
print(f"\n8. HEALTH SCORE:")
print(f"   dscrScore = min({dscr:.2f} x 100, 100) = {dscrScore:.1f}")
print(f"   roeScore  = min({roe:.1f} / 18 x 100, 100) = {roeScore:.1f}")
print(f"   vtScore   = min({viewsTin} / 20 x 100, 100) = {vtScore:.1f}")
print(f"   Health = 40% x {dscrScore:.1f} + 40% x {roeScore:.1f} + 20% x {vtScore:.1f} = {health}/100")
print(f"   [NOTE] DSCR=null khi khong vay -> default 70 (hoi tuy tien)")

print(f"\n{'='*60}")
print("TON KET CAC LO HONG CONG THUC:")
print(f"  BUG 1 (QUAN TRONG): floorPrice dung 'cost x rate x years'")
print(f"         -> Nen dung 'debt x rate x years' (chi tinh lai phan vay)")
print(f"         -> Sai {floor_bug-floor_fix:.3f} Ty / {(floor_bug-floor_fix)/floor_fix*100:.1f}%")
print(f"  BUG 2 (NHO)       : n_m khong tru grace period khi tinh PMT sau an han")
print(f"         -> Principal thap hon thuc te {princ_fix-princ_code:.2f} Tr/thang")
print(f"  NOTE 1 (OK)        : ROE chi tinh Cash ROE (chua co capital gain)")
print(f"  NOTE 2 (OK)        : DSCR=null -> 70 (acceptable for dashboard)")
print(f"{'='*60}")
