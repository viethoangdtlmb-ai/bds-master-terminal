import os, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

orig_count = len(lines)
print(f'Original lines: {orig_count}')

# Verify targets (print first 60 chars safely)
for name, idx in [('Block A DSCR', 10253), ('Block B grace', 10269),
                   ('Block C prefmonths', 10277), ('Block D phaseWarning', 10569)]:
    print(f'{name}: {lines[idx].strip()[:60]}')

# Remove from BOTTOM to TOP
del lines[10569:10602]   # Block D: phaseWarning mismatch block
del lines[10277:10285]   # Block C: prefmonths alert
del lines[10269:10277]   # Block B: grace alert
del lines[10253:10261]   # Block A: DSCR alert

print(f'New lines: {len(lines)}')

with open('index_temp.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

temp_size = os.path.getsize('index_temp.html')
if temp_size < 200000:
    print(f'ERROR: Temp file too small ({temp_size}). Aborting.')
    os.remove('index_temp.html')
    raise SystemExit(1)

shutil.move('index_temp.html', 'index.html')
print(f'SUCCESS: {temp_size} bytes written.')
