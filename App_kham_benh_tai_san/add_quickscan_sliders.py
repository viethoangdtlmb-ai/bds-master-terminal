"""
Script to dynamically add slider-row for Quick Scan inputs.
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

sliders_config = [
    # input_id, sl_id, min, max, step, def_val, labels_html
    ('qs-buy', 'sl-qs-buy', '1', '50', '0.5', '9.0', '<span>1</span><span>25</span><span>50Tỷ</span>'),
    ('qs-now', 'sl-qs-now', '1', '50', '0.5', '8.5', '<span>1</span><span>25</span><span>50Tỷ</span>'),
    ('qs-loan', 'sl-qs-loan', '0', '100', '1', '60', '<span>0%</span><span>50%</span><span>100%</span>')
]

for conf in sliders_config:
    iid, sid, smin, smax, sstep, sval, slabels = conf
    
    if f'id="{sid}"' in v:
        print(f'✅ {sid} already exists, skipping.')
        continue

    idx = v.find(f'id="{iid}"')
    if idx == -1:
        print(f'❌ Cannot find id="{iid}"')
        continue
    
    idx_close = v.find('</div>', idx)
    if idx_close == -1:
        print(f'❌ Cannot find closing </div> after {iid}')
        continue
    
    insert_point = idx_close + 6
    
    slider_html = f'''
            <div class="slider-row">
              <input type="range" class="range-slider" id="{sid}" min="{smin}" max="{smax}" step="{sstep}" value="{sval}">
              <div class="range-labels">{slabels}</div>
            </div>'''
            
    v = v[:insert_point] + slider_html + v[insert_point:]
    print(f'✅ Injected {sid} after {iid}')

old_init = "]"  # we want to append to the array. Let's be careful.
# Find the exact array in _initSlidersOnLoad
# It looks like: [['sl-loanpct','f-loanpct'],...,['sl-maint','f-maint']]
import re
match = re.search(r"(\[\['sl-loanpct','f-loanpct'\].*?\])", v)
if match:
    old_array = match.group(1)
    new_array = old_array
    for conf in sliders_config:
        iid, sid = conf[:2]
        if f"'{sid}','{iid}'" not in new_array:
            new_array += f",['{sid}','{iid}']"
    v = v.replace(old_array, new_array, 1)
    print('✅ Updated _initSlidersOnLoad pairs array for Quick Scan')
else:
    print('❌ Could not find old_init pattern in JS')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)
