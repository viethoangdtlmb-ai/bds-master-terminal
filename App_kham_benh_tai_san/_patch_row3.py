import os, shutil

# --- Replacement strings ---
OLD = '''        ${(a.prefmonths || 0) > 0 && (a.prefmonths || 0) <= 6 ? `<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">\u26a1 \u01afu \u0111\u00e3i h\u1ebft trong <strong>${a.prefmonths} th\u00e1ng</strong></span>` : ''}
      </div>'''

NEW = '''        ${(a.prefmonths || 0) > 0 && (a.prefmonths || 0) <= 6 ? `<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">\u26a1 \u01afu \u0111\u00e3i h\u1ebft trong <strong>${a.prefmonths} th\u00e1ng</strong></span>` : ''}
        ${c_q.phaseWarning ? `<span style="font-size:11px;color:var(--text-2);background:rgba(100,116,139,0.08);border:1px solid rgba(100,116,139,0.25);padding:2px 8px;border-radius:4px">\u26a0\ufe0f ${c_q.phaseWarning}</span>` : ''}
        ${parseFloat(dscr) < 0.3 && dscr !== 'N/A' ? `<span style="font-size:11px;color:var(--red);background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);padding:2px 8px;border-radius:4px">\U0001f6a8 DSCR=${dscr} \u2014 D\u00f2ng ti\u1ec1n s\u1eafp \u0111\u1ee9t g\u00e3y</span>` : ''}
      </div>'''

# --- Read ---
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if OLD not in content:
    print('ERROR: Target string not found. Checking nearby text...')
    idx = content.find('prefmonths || 0) <= 6')
    if idx >= 0:
        print('Found at char:', idx)
        print(repr(content[idx-20:idx+200]))
    raise SystemExit(1)

new_content = content.replace(OLD, NEW, 1)

# --- Write to temp file first (safe approach) ---
with open('index_temp.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# --- Verify temp file is complete ---
with open('index_temp.html', 'r', encoding='utf-8') as f:
    verify = f.read()

if len(verify) < len(content):
    print(f'ERROR: Temp file smaller than original ({len(verify)} < {len(content)}). Aborting.')
    os.remove('index_temp.html')
    raise SystemExit(1)

# --- Replace original ---
shutil.move('index_temp.html', 'index.html')
print(f'SUCCESS: phaseWarning + DSCR note added. File size: {len(new_content)} chars')
