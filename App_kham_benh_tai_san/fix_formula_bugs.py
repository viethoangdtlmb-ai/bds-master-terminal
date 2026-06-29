"""
fix_formula_bugs.py
BUG 1: floorPrice dùng cost×rate×years → fix: debt×rate×years
BUG 2: n_m không trừ grace period → fix: n_m - grace khi tính PMT sau ân hạn
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

results = []

# ── BUG 1: floorPrice ──────────────────────────────────────────────────────
# Tìm và thay: a.cost * (a.rate||0)/100 * years
# → (a.debt||0) > 0 ? (a.debt||0) : a.cost*(a.loanpct||0)/100) * (a.rate||0)/100 * years
OLD_FLOOR = '  const laiCD  = a.cost * (a.rate||0)/100 * years;'
NEW_FLOOR = ('  // BUG1 FIX: lãi chỉ tính trên phần vốn vay (debt), không phải toàn bộ cost\n'
             '  const loanAmt = (a.debt||0) > 0 ? (a.debt||0) : a.cost*(a.loanpct||0)/100;\n'
             '  const laiCD  = loanAmt * (a.rate||0)/100 * years;')

if OLD_FLOOR in v:
    v = v.replace(OLD_FLOOR, NEW_FLOOR, 1)
    results.append('✅ BUG 1 FIXED: floorPrice laiCD')
else:
    # Thử tìm với CRLF variant
    old_crlf = OLD_FLOOR.replace('\n', '\r\n')
    if old_crlf in v:
        v = v.replace(old_crlf, NEW_FLOOR.replace('\n', '\r\n'), 1)
        results.append('✅ BUG 1 FIXED (CRLF): floorPrice laiCD')
    else:
        results.append('❌ BUG 1 NOT FOUND — checking pattern...')
        # Pattern search
        idx = v.find('a.cost * (a.rate||0)/100 * years')
        if idx != -1:
            results.append(f'   Found at char {idx}: {repr(v[idx-20:idx+50])}')

# ── BUG 2: n_m + principal ──────────────────────────────────────────────────
# Tìm dòng principal để sửa n_m thành remaining term
OLD_PRINCIPAL = ('  const principal = a.grace > 0 ? 0 : '
                 '(n_m > 0 ? debtB*rateM/(1-Math.pow(1+rateM,-n_m)) - intOnly : 0);')
NEW_PRINCIPAL = ('  // BUG2 FIX: sau ân hạn, số tháng còn lại = term × 12 − grace months\n'
                 '  const n_remain  = Math.max(1, n_m - (a.grace||0));\n'
                 '  const principal = a.grace > 0 ? 0 : '
                 '(n_remain > 0 ? debtB*rateM/(1-Math.pow(1+rateM,-n_remain)) - intOnly : 0);')

if OLD_PRINCIPAL in v:
    v = v.replace(OLD_PRINCIPAL, NEW_PRINCIPAL, 1)
    results.append('✅ BUG 2 FIXED: principal n_m → n_remain')
else:
    old_crlf = OLD_PRINCIPAL.replace('\n', '\r\n')
    if old_crlf in v:
        v = v.replace(old_crlf, NEW_PRINCIPAL.replace('\n', '\r\n'), 1)
        results.append('✅ BUG 2 FIXED (CRLF): principal n_remain')
    else:
        results.append('❌ BUG 2 NOT FOUND — checking...')
        idx = v.find('const principal = a.grace > 0')
        if idx != -1:
            results.append(f'   Found at char {idx}: {repr(v[idx:idx+80])}')

# Write
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

print('=== FIX RESULTS ===')
for r in results: print(' ', r)

# Verify
with open('index.html', encoding='utf-8') as f:
    v2 = f.read()

checks = [
    ('BUG1 loanAmt',   'const loanAmt' in v2),
    ('BUG1 laiCD fix', 'loanAmt * (a.rate||0)/100 * years' in v2),
    ('BUG1 old gone',  'a.cost * (a.rate||0)/100 * years' not in v2),
    ('BUG2 n_remain',  'const n_remain' in v2),
    ('BUG2 PMT fix',   'Math.pow(1+rateM,-n_remain)' in v2),
    ('BUG2 old gone',  'Math.pow(1+rateM,-n_m))' not in v2),
]
ok = err = 0
for name, check in checks:
    print(f'  {"OK" if check else "ERR"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\n{ok}/{len(checks)} verified')

import re as re2
sc = re2.findall(r'<script>(.*?)</script>', v2, re2.DOTALL)
s = sc[0]
ob, cb = s.count('{'), s.count('}')
bt = s.count('`')
print(f'Syntax: brace {ob}/{cb} btk {bt} ({"even" if bt%2==0 else "ODD"})')
print('DONE.')
