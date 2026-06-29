import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()
v = v.replace('\r\n', '\n')

# Find the rxHTML template literal block
# Try to locate buildPrescription template section
start = v.find('rxHTML = `')
if start == -1:
    start = v.find('rx-preview\').innerHTML')
print(f'Start found at: {start}')

# Strategy: directly replace margin-top:28px section wrapper divs with rx-section class
# These appear exclusively in the PDF template as section wrappers
old_div = '<div style="margin-top:28px">'
new_div = '<div class="rx-section" style="margin-top:28px">'
count = v.count(old_div)
print(f'Found {count} occurrences of section wrapper')
v = v.replace(old_div, new_div)

# Verify
print(f'rx-section count after: {v.count("rx-section")}')

v = v.replace('\n', '\r\n')
with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(v)

with open('index.html', encoding='utf-8') as f:
    v2 = f.read()
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
s = sc[0]
ob, cb = s.count('{'), s.count('}')
bt = s.count('`')
print(f'Script brace {ob}/{cb} btk {bt} ({"even" if bt%2==0 else "ODD"})')

checks = [
    ('toast addAsset',    'Đã thêm' in v2),
    ('rx-section PDF',    'class="rx-section"' in v2),
    ('page-break-inside', 'page-break-inside: avoid' in v2),
    ('mobile 768',        'max-width: 768px' in v2),
    ('cb-year',           'id="cb-year"' in v2),
    ('showToast fn',      'function showToast' in v2),
]
ok = err = 0
for name, check in checks:
    print(f'  {"OK" if check else "ERR"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\n{ok}/{len(checks)} OK | File: {len(v2):,} bytes | {v2.count(chr(10)):,} lines')
