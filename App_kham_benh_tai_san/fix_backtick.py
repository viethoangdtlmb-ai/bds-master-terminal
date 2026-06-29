import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# In sprint6b_patch.py, Python wrote \` (backslash + backtick) instead of `
# This causes JavaScript syntax errors. Fix: replace \` with ` in the file.
BAD  = '\\\\'  + '`'   # This is the literal 2-char sequence: backslash + backtick
GOOD = '`'

count = content.count(BAD)
print(f'Tim thay {count} lan backlash-backtick sai')

if count > 0:
    # Show first few occurrences for debugging
    import re
    idx = 0
    shown = 0
    while True:
        pos = content.find(BAD, idx)
        if pos == -1 or shown >= 5: break
        print(f'  Line ~{content[:pos].count(chr(10))+1}: ...{repr(content[max(0,pos-15):pos+20])}')
        idx = pos + 1
        shown += 1

    content = content.replace(BAD, GOOD)
    # Verify fix
    remaining = content.count(BAD)
    print(f'Con lai sau sua: {remaining}')

    content = content.replace('\r\n', '\n').replace('\r', '\n')
    content = content.replace('\n', '\r\n')
    with open(FILE, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print('Da sua va luu file!')
else:
    print('Khong tim thay ky tu sai. Kiem tra nguyen nhan khac...')

# Final brace check
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()

import re
scripts = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nSo script blocks: {len(scripts)}')
for i, sc in enumerate(scripts[:-1], 1):
    ob, cb = sc.count('{'), sc.count('}')
    status = 'OK' if ob == cb else 'LECH!'
    print(f'Script {i}: {{ = {ob}, }} = {cb} [{status}]')
print(f'Total lines: {len(v.splitlines())}')
