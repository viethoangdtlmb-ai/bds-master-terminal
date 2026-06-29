import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:/1. BDS/AI-Assistant/App_kham_benh_tai_san/index.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# The exact string uses backtick template literals - find by unique substring
marker = 'opt.textContent = `'
idx = html.find(marker)
if idx == -1:
    print('marker not found')
else:
    end = html.find('`;', idx) + 2
    old = html[idx:end]
    print('Found:', repr(old))
    
    # Build new label
    new = "opt.textContent = `${d.name} \u2014 Cycle ${d.cycle} | Nh\u00e0: ${d.gia} tr/m\u00b2 | CC: ${d.gia_cc} tr/m\u00b2`;"
    html = html[:idx] + new + html[end:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Done! New label:', repr(new))
