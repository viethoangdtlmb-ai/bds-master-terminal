"""
fix_sliders_final.py
====================
CLEAN APPROACH: Giữ nguyên input-unit structure, đặt slider NGOÀI vào một div riêng.
Không đụng vào HTML gốc của form input.
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── STEP 1: Revert slider-wrap injection (khôi phục lại input-unit gốc) ───────
# Pattern hiện tại: input-unit > slider-wrap > [slider-top > number-input] + range + labels
# Ta cần: input-unit > [number-input + unit-span] (gốc) + [div.slider-row riêng bên dưới]

# Khôi phục f-loanpct về dạng gốc (xóa slider-wrap/slider-top wrapper)
OLD_LOANPCT_BLOCK = '''                <div class="slider-wrap">
                <div class="slider-top">
                  <input type="number" class="form-input" id="f-loanpct" placeholder="60" min="0" max="100" oninput="onLoanPctChange(this.value);">
                  
                </div>
                <input type="range" class="range-slider" id="sl-loanpct" min="0" max="80" step="1" value="60" oninput="(function(v){var el=document.getElementById('f-loanpct');if(el)el.value=v;})(this.value)">
                <div class="range-labels"><span>0%</span><span>40%</span><span>80%</span></div>
              </div>'''

NEW_LOANPCT_BLOCK = '''                <input type="number" class="form-input" id="f-loanpct" placeholder="60" min="0" max="100" oninput="onLoanPctChange(this.value);">
                <span class="input-unit-label">%</span>'''

if OLD_LOANPCT_BLOCK in v:
    v = v.replace(OLD_LOANPCT_BLOCK, NEW_LOANPCT_BLOCK, 1)
    print('✅ f-loanpct: reverted to original input-unit structure')
else:
    print('⚠ f-loanpct old block not found exactly, trying regex...')
    # Try regex approach
    pattern = r'<div class="slider-wrap">\s*<div class="slider-top">\s*(<input[^>]*id="f-loanpct"[^>]*>).*?</div>\s*(<input[^>]*id="sl-loanpct"[^>]*>)\s*<div class="range-labels">.*?</div>\s*</div>'
    m = re.search(pattern, v, re.DOTALL)
    if m:
        original_input = m.group(1)
        v = v[:m.start()] + '\n                ' + original_input + '\n                <span class="input-unit-label">%</span>' + v[m.end():]
        print('✅ f-loanpct: reverted via regex')

# ── STEP 2: Remove inlined slider-bound script block ───────────────────────
# Remove the inline <script>...(function initSlidersBound()...</script>
old_inline_script_start = '<script>\n(function initSlidersBound() {'
old_inline_script_end   = '})();\n</script>'
idx_s = v.find(old_inline_script_start)
idx_e = v.find(old_inline_script_end, idx_s)
if idx_s > 0 and idx_e > idx_s:
    v = v[:idx_s] + v[idx_e + len(old_inline_script_end):]
    print('✅ Removed inline initSlidersBound script')

# ── STEP 3: Add CLEAN slider rows AFTER each form-group (after input-unit closing div) ──
# Each slider goes into a simple <div class="slider-row"> right after the form-group content

SLIDER_ROW_STYLES = """
/* ── SLIDER ROW (standalone, no interference) ── */
.slider-row {
  margin: -4px 0 8px 0;
  padding: 0 2px;
}
.slider-row .range-slider {
  width: 100%;
  display: block;
}
.slider-row .range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: rgba(255,255,255,0.35);
  margin-top: 2px;
  padding: 0 2px;
}
"""
STYLE_END = '</style>'
if '.slider-row {' not in v:
    v = v.replace(STYLE_END, SLIDER_ROW_STYLES + STYLE_END, 1)
    print('✅ Added .slider-row CSS')

# ── STEP 4: Insert slider rows after each relevant form-group ───────────────
# Find the closing </div>s of each form-group for loanpct, rate, prefmonths
# Strategy: find the input element, then find the next </div></div> (closes input-unit and form-group)

def insert_slider_after_formgroup(html, input_id, slider_id, sl_min, sl_max, sl_step, sl_val, sl_labels, unit_label_text):
    """Insert a .slider-row div after the form-group containing input_id."""
    # Find the input element
    inp_pos = html.find(f'id="{input_id}"')
    if inp_pos < 0:
        print(f'  ❌ Cannot find {input_id}')
        return html
    
    # Find the end of parent form-group (look for </div> after the unit label)
    # The structure is: form-group > label + input-unit > [input + span]
    # After input-unit closes (</div>), form-group closes (</div>)
    # Find unit label first
    label_pos = html.find(f'>{unit_label_text}<', inp_pos)
    if label_pos < 0:
        label_pos = html.find('input-unit-label', inp_pos)
    
    # Find the </div></div> after that
    after_label = html.find('</div>', label_pos if label_pos > 0 else inp_pos + 100)
    after_fg    = html.find('</div>', after_label + 6)
    
    # Insert slider row here
    slider_html = f'\n            <div class="slider-row">\n              <input type="range" class="range-slider" id="{slider_id}" min="{sl_min}" max="{sl_max}" step="{sl_step}" value="{sl_val}" oninput="document.getElementById(\'{input_id}\').value=this.value">\n              <div class="range-labels">{sl_labels}</div>\n            </div>'
    
    html = html[:after_fg + 6] + slider_html + html[after_fg + 6:]
    print(f'  ✅ Slider {slider_id} inserted after {input_id} form-group')
    return html

v = insert_slider_after_formgroup(v, 'f-loanpct',   'sl-loanpct',   '0',  '80',   '1',   '60',  '<span>0%</span><span>40%</span><span>80%</span>', '%')
v = insert_slider_after_formgroup(v, 'f-rate',       'sl-rate',      '5',  '20',   '0.5', '8.5', '<span>5%</span><span>12%⚠</span><span>20%</span>', '%/năm')
v = insert_slider_after_formgroup(v, 'f-prefmonths', 'sl-prefmonths','0',  '36',   '1',   '6',   '<span>0T</span><span>12T</span><span>36T</span>',   'tháng')

# ── STEP 5: Add sync listeners in main JS (at _initSlidersOnLoad or replace) ──
# Update _initSlidersOnLoad to use the new standalone slider IDs
NEW_INIT = """function _initSlidersOnLoad() {
  [['sl-loanpct','f-loanpct'],['sl-rate','f-rate'],['sl-prefmonths','f-prefmonths']].forEach(function(p) {
    var sl  = document.getElementById(p[0]);
    var inp = document.getElementById(p[1]);
    if (!sl || !inp) { console.warn('Slider not found:', p[0]); return; }
    // Number → Slider sync (when user types into number field)
    inp.addEventListener('input', function() {
      sl.value = this.value;
      _sliderSync(sl);
    });
    // Init slider position from current input value
    var initVal = parseFloat(inp.value) || parseFloat(inp.getAttribute('placeholder')) || parseFloat(sl.min) || 0;
    sl.value = initVal;
    _sliderSync(sl);
  });
}"""

# Find and replace _initSlidersOnLoad
old_init_start = 'function _initSlidersOnLoad() {'
idx = v.find(old_init_start)
if idx > 0:
    # Find closing }
    depth = 0
    end = idx
    for i, c in enumerate(v[idx:], idx):
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
    v = v[:idx] + NEW_INIT + v[end+1:]
    print('✅ _initSlidersOnLoad updated')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('Slider row CSS',           '.slider-row {' in v2),
    ('sl-loanpct in slider-row', 'class="slider-row"' in v2 and 'sl-loanpct' in v2),
    ('sl-rate',                  'id="sl-rate"' in v2),
    ('sl-prefmonths',            'id="sl-prefmonths"' in v2),
    ('slider-wrap removed',      '<div class="slider-wrap">' not in v2),
    ('f-loanpct oninput clean',  'onLoanPctChange' in v2),
    ('Number input has label',   'input-unit-label' in v2),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
main = max(sc, key=len); ob, cb = main.count('{'), main.count('}')
ok = sum(1 for _,c in checks if c)
for name, c in checks: print(f'  {"OK" if c else "ERR"} {name}')
print(f'Main script brace: {ob}/{cb} {"✅" if ob==cb else "❌"}')
print(f'{ok}/{len(checks)} verified')
