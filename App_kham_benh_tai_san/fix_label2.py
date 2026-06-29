import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:/1. BDS/AI-Assistant/App_kham_benh_tai_san/index.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

marker = 'opt.textContent = `'
idx = html.find(marker)
end = html.find('`;', idx) + 2
old = html[idx:end]
print('Old:', repr(old))

new = "opt.textContent = `${d.name} \u2014 Cycle ${d.cycle} | Nh\u00e0: ${d.gia} tr/m\u00b2${d.gia_cc != null ? ' | CC: ' + d.gia_cc + ' tr/m\u00b2' : ' | CC: N/A'}`;"
html = html[:idx] + new + html[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
print('New:', repr(new))
