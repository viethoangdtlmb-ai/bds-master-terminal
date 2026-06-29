"""
fix_sliders_v2.py - Simple inline oninput approach
==================================================
Thay vì JS phức tạp, gắn oninput trực tiếp vào từng slider element.
Đồng thời cập nhật oninput của số input để sync ngược lại slider.
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

changed = []

# ── 1. Slider loanpct: thêm oninput inline ────────────────────
OLD_SL_LOAN = '<input type="range" class="range-slider" id="sl-loanpct" min="0" max="80" step="5" value="60">'
NEW_SL_LOAN = '<input type="range" class="range-slider" id="sl-loanpct" min="0" max="80" step="1" value="60" oninput="var inp=document.getElementById(\'f-loanpct\'); inp.value=this.value; onLoanPctChange(this.value); _sliderSync(this);">'

if OLD_SL_LOAN in v:
    v = v.replace(OLD_SL_LOAN, NEW_SL_LOAN, 1)
    changed.append('✅ sl-loanpct inline oninput')

# ── 2. Slider rate: thêm oninput inline ───────────────────────
OLD_SL_RATE = '<input type="range" class="range-slider" id="sl-rate" min="5" max="20" step="0.5" value="8.5">'
NEW_SL_RATE = '<input type="range" class="range-slider" id="sl-rate" min="5" max="20" step="0.5" value="8.5" oninput="document.getElementById(\'f-rate\').value=this.value; _sliderSync(this);">'

if OLD_SL_RATE in v:
    v = v.replace(OLD_SL_RATE, NEW_SL_RATE, 1)
    changed.append('✅ sl-rate inline oninput')

# ── 3. Slider prefmonths: thêm oninput inline ─────────────────
OLD_SL_PREF = '<input type="range" class="range-slider" id="sl-prefmonths" min="0" max="36" step="1" value="6">'
NEW_SL_PREF = '<input type="range" class="range-slider" id="sl-prefmonths" min="0" max="36" step="1" value="6" oninput="document.getElementById(\'f-prefmonths\').value=this.value; _sliderSync(this);">'

if OLD_SL_PREF in v:
    v = v.replace(OLD_SL_PREF, NEW_SL_PREF, 1)
    changed.append('✅ sl-prefmonths inline oninput')

# ── 4. Cập nhật f-loanpct input để sync ngược slider ──────────
# Tìm oninput="onLoanPctChange(this.value)" và thêm sync slider
OLD_LOAN_INPUT = 'oninput="onLoanPctChange(this.value)"'
NEW_LOAN_INPUT = 'oninput="onLoanPctChange(this.value); var sl=document.getElementById(\'sl-loanpct\'); if(sl){sl.value=this.value; _sliderSync(sl);}"'
if OLD_LOAN_INPUT in v:
    v = v.replace(OLD_LOAN_INPUT, NEW_LOAN_INPUT, 1)
    changed.append('✅ f-loanpct input → sync slider')

# ── 5. Thay thế JS phức tạp bằng helper đơn giản ─────────────
# Remove/replace complex initSlider/initAllSliders + add simple helper
OLD_INIT_BLOCK = """// ── SLIDER SYNC ─────────────────────────────────────────────
function _sliderTrackColor(slider, pct, warnT, dangerT, val) {"""

NEW_SIMPLE_HELPERS = """// ── SLIDER HELPERS (simple) ────────────────────────────────
function _sliderSync(slider) {
  // Update filled track color based on current value
  const min = parseFloat(slider.min) || 0;
  const max = parseFloat(slider.max) || 100;
  const val = parseFloat(slider.value) || min;
  const pct = ((val - min) / (max - min) * 100).toFixed(1);
  // Color thresholds per slider
  const warnMap   = {'sl-loanpct': 60, 'sl-rate': 12};
  const dangerMap = {'sl-loanpct': 75, 'sl-rate': 16};
  const warn   = warnMap[slider.id];
  const danger = dangerMap[slider.id];
  let fill = '#6366f1';
  slider.classList.remove('warn','danger');
  if (danger && val >= danger) { fill = '#ef4444'; slider.classList.add('danger'); }
  else if (warn && val >= warn) { fill = '#f59e0b'; slider.classList.add('warn'); }
  slider.style.background = `linear-gradient(to right, ${fill} ${pct}%, rgba(255,255,255,0.12) ${pct}%)`;
}

function _initSlidersOnLoad() {
  // Init all sliders with current input values (or placeholder)
  [['sl-loanpct','f-loanpct'],['sl-rate','f-rate'],['sl-prefmonths','f-prefmonths']].forEach(([sid,iid]) => {
    const sl = document.getElementById(sid);
    const inp = document.getElementById(iid);
    if (!sl || !inp) return;
    const v = parseFloat(inp.value) || parseFloat(inp.getAttribute('placeholder')) || parseFloat(sl.min) || 0;
    sl.value = v; inp.value = v;
    _sliderSync(sl);
    // Sync number→slider on input
    inp.addEventListener('input', () => { sl.value = inp.value; _sliderSync(sl); });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', _initSlidersOnLoad);
} else { _initSlidersOnLoad(); }

// legacy CSS color function stub
function _sliderTrackColor(slider, pct, warnT, dangerT, val) {"""

if OLD_INIT_BLOCK in v:
    v = v.replace(OLD_INIT_BLOCK, NEW_SIMPLE_HELPERS, 1)
    # Remove the rest of old initSlider function up to initAllSliders call
    # Find and remove initAllSliders and old readyState block
    old_end = """function initAllSliders() {
  initSlider('sl-loanpct',   'f-loanpct',    0,  80, 60, 75);
  initSlider('sl-rate',      'f-rate',        5,  20, 12, 16);
  initSlider('sl-prefmonths','f-prefmonths',  0,  36, null, null);
}

// Run immediately + also on DOMContentLoaded as fallback
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAllSliders);
} else {
  initAllSliders();  // DOM already loaded
}"""
    if old_end in v:
        v = v.replace(old_end, '// sliders initialized via _initSlidersOnLoad above', 1)
        changed.append('✅ Old initSlider() removed')
    changed.append('✅ New simple helpers added')
else:
    changed.append('❌ _sliderTrackColor block not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

for c in changed: print(c)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('sl-loanpct oninput',     "oninput=\"var inp=document.getElementById" in v2),
    ('sl-rate oninput',        "_sliderSync(this);" in v2),
    ('_sliderSync defined',    'function _sliderSync' in v2),
    ('_initSlidersOnLoad',     '_initSlidersOnLoad' in v2),
    ('inp addEventListener',   'inp.addEventListener' in v2),
    ('No old initSlider',      'function initSlider(' not in v2),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
s = sc[0]; ob, cb = s.count('{'), s.count('}')
ok = sum(1 for _,c in checks if c)
for name, c in checks: print(f'  {"OK" if c else "ERR"} {name}')
print(f'Syntax brace: {ob}/{cb} {"✅" if ob==cb else "❌"}')
print(f'{ok}/{len(checks)} verified')
