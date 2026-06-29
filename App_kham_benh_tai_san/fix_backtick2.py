import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    raw = f.read()

# The CORRECT pattern: one backslash + one backtick (2 chars)
# In Python string: '\\' = one backslash, '`' = backtick
BAD  = chr(92) + chr(96)   # chr(92)=backslash, chr(96)=backtick — 100% safe
GOOD = chr(96)              # just a backtick

count = raw.count(BAD)
print(f'Tim thay {count} lan ky tu sai (backslash+backtick = {repr(BAD)})')

if count == 0:
    # The backslash might have been dropped by Python — check if the escaping
    # worked differently. Let's look at the CHITET_SECTION area directly.
    # Check for any unusual sequences near our injection points
    MARKERS = ['PHÂN TÍCH TÀI CHÍNH CHI TIẾT', 'VII. RADAR SỨC KHỎE']
    for m in MARKERS:
        idx = raw.find(m)
        if idx >= 0:
            snippet = raw[idx:idx+200]
            # Look for any backslash in this area
            bs_count = snippet.count(chr(92))
            print(f'  Doan "{m[:20]}": {bs_count} backslash trong 200 ky tu dau')
            for j, ch in enumerate(snippet[:200]):
                if ch == chr(92):
                    print(f'    Backslash tai vt {j}: ...{repr(snippet[max(0,j-5):j+15])}')

    # Check if the JS actually runs by looking for the IIFE pattern
    if '${(() =>' in raw:
        print('\nTim thay IIFE trong template literal — co the la nguyen nhan loi')
        # Show the problematic sections
        idx = raw.find('${(() =>')
        while idx >= 0:
            print(f'  IIFE tại line ~{raw[:idx].count(chr(10))+1}')
            idx = raw.find('${(() =>', idx+1)
    else:
        print('\nKhong co IIFE — van de khac')
else:
    print(f'Dang sua {count} ky tu sai...')
    fixed = raw.replace(BAD, GOOD)
    remaining = fixed.count(BAD)
    print(f'Con lai: {remaining}')
    
    fixed = fixed.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
    with open(FILE, 'w', encoding='utf-8', newline='') as f:
        f.write(fixed)
    print('Da sua xong!')

# JS brace check
import re
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
scripts = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
for i, sc in enumerate(scripts[:-1], 1):
    ob, cb = sc.count('{'), sc.count('}')
    print(f'Script {i}: {{ = {ob}, }} = {cb}, diff = {ob-cb}')
