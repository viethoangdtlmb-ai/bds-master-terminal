import os, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('_portfolio_alerts.js', 'r', encoding='utf-8') as f:
    new_code = f.read()

print(f'Original lines: {len(lines)}')

# Verify insertion point: line 10278 should be '      });'
# (closing of calcs.forEach, 0-indexed: 10277)
target_line = lines[10277].strip()
print(f'Line 10278: {target_line}')

if target_line != '});':
    print('ERROR: Expected "});" at line 10278. Found:', target_line)
    raise SystemExit(1)

# Insert new portfolio alerts code AFTER line 10278 (0-indexed: after index 10277)
# i.e., insert at position 10278
lines.insert(10278, new_code)

print(f'New lines: {len(lines)}')

# Write to temp file
with open('index_temp.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

temp_size = os.path.getsize('index_temp.html')
if temp_size < 210000:
    print(f'ERROR: Temp file too small ({temp_size} bytes). Aborting.')
    os.remove('index_temp.html')
    raise SystemExit(1)

shutil.move('index_temp.html', 'index.html')
print(f'SUCCESS: Portfolio alerts inserted. File: {temp_size} bytes.')
