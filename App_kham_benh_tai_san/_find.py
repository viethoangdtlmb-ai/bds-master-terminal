import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    stripped = line.rstrip()
    if 'alerts.push' in stripped or 'diag-alerts' in stripped or 'phaseWarning' in stripped:
        print(f'{i+1}: {stripped[:130]}')
