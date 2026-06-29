import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('index.html', encoding='utf-8') as f: v = f.read()
old = 'Lãi Suất Ưu Đãi Hiện Tại'
new = 'Lãi Suất Ưu Đãi'
count = v.count(old)
v = v.replace(old, new)
with open('index.html', 'w', encoding='utf-8') as f: f.write(v)
print(f'Replaced {count} occurrences')
