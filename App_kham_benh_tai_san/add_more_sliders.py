"""
Script to dynamically add slider-row for multiple inputs.
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

sliders_config = [
    # input_id, sl_id, min, max, step, def_val, labels_html
    ('f-area', 'sl-area', '20', '500', '1', '80', '<span>20</span><span>250</span><span>500m²</span>'),
    ('f-cost', 'sl-cost', '1', '50', '0.5', '5', '<span>1</span><span>25</span><span>50Tỷ</span>'),
    ('f-market', 'sl-market', '1', '50', '0.5', '5', '<span>1</span><span>25</span><span>50Tỷ</span>'),
    ('f-debt', 'sl-debt', '0', '50', '0.5', '2', '<span>0</span><span>25</span><span>50Tỷ</span>'),
    ('f-floatrate', 'sl-floatrate', '5', '20', '0.5', '12', '<span>5%</span><span>15%</span><span>20%</span>'),
    ('f-grace', 'sl-grace', '0', '36', '1', '8', '<span>0</span><span>18</span><span>36T</span>'),
    ('f-loanterm', 'sl-loanterm', '1', '35', '1', '20', '<span>1</span><span>15</span><span>35năm</span>'),
    ('f-rent', 'sl-rent', '0', '150', '1', '10', '<span>0</span><span>75</span><span>150Tr</span>'),
    ('f-mgmt', 'sl-mgmt', '0', '20', '0.1', '2', '<span>0</span><span>10</span><span>20Tr</span>'),
    ('f-maint', 'sl-maint', '0', '100', '1', '5', '<span>0</span><span>50</span><span>100Tr</span>')
]

for conf in sliders_config:
    iid, sid, smin, smax, sstep, sval, slabels = conf
    
    # 1. Skip if already added
    if f'id="{sid}"' in v:
        print(f'✅ {sid} already exists, skipping.')
        continue

    # 2. Find the input element to locate the parent input-unit div
    idx = v.find(f'id="{iid}"')
    if idx == -1:
        print(f'❌ Cannot find id="{iid}"')
        continue
    
    # 3. Find the closing </div> of the input-unit that contains this input
    # The structure: <div class="input-unit"> ... <input ...> ... </div>
    idx_close = v.find('</div>', idx)
    if idx_close == -1:
        print(f'❌ Cannot find closing </div> after {iid}')
        continue
    
    # 4. Insert the slider-row right after the closing </div>
    insert_point = idx_close + 6  # length of '</div>'
    
    slider_html = f'''
            <div class="slider-row">
              <input type="range" class="range-slider" id="{sid}" min="{smin}" max="{smax}" step="{sstep}" value="{sval}">
              <div class="range-labels">{slabels}</div>
            </div>'''
            
    v = v[:insert_point] + slider_html + v[insert_point:]
    print(f'✅ Injected {sid} after {iid}')

# 5. Add them to _initSlidersOnLoad pairs
old_init = "['sl-loanpct','f-loanpct'],['sl-rate','f-rate'],['sl-prefmonths','f-prefmonths']"
if old_init in v:
    new_init = old_init
    for conf in sliders_config:
        iid, sid = conf[:2]
        if f"'{sid}','{iid}'" not in v:
            new_init += f",['{sid}','{iid}']"
    v = v.replace(old_init, new_init, 1)
    print('✅ Updated _initSlidersOnLoad pairs array')
else:
    print('❌ Could not find old_init pattern in JS')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)
