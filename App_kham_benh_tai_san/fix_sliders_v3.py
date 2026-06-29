"""
fix_sliders_v3.py - Clean approach: JS addEventListener only, no oninput attributes
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── 1. Remove oninput from slider elements ─────────────────────
# sl-loanpct
v = re.sub(
    r'(<input type="range" class="range-slider" id="sl-loanpct"[^>]*?) oninput="[^"]*"',
    r'\1',
    v
)
# sl-rate
v = re.sub(
    r'(<input type="range" class="range-slider" id="sl-rate"[^>]*?) oninput="[^"]*"',
    r'\1',
    v
)
# sl-prefmonths
v = re.sub(
    r'(<input type="range" class="range-slider" id="sl-prefmonths"[^>]*?) oninput="[^"]*"',
    r'\1',
    v
)
print('✅ Removed oninput attributes from slider HTML elements')

# ── 2. Simplify f-loanpct oninput (remove slider sync - JS will handle) ──
v = v.replace(
    'oninput="onLoanPctChange(this.value); var sl=document.getElementById(\'sl-loanpct\'); if(sl){sl.value=this.value; _sliderSync(sl);}"',
    'oninput="onLoanPctChange(this.value);"',
    1
)
print('✅ Simplified f-loanpct oninput')

# ── 3. Replace _initSlidersOnLoad with bidirectional sync ──────
OLD_INIT = """function _initSlidersOnLoad() {
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
}"""

NEW_INIT = """function _initSlidersOnLoad() {
  [['sl-loanpct','f-loanpct'],['sl-rate','f-rate'],['sl-prefmonths','f-prefmonths']].forEach(([sid,iid]) => {
    const sl  = document.getElementById(sid);
    const inp = document.getElementById(iid);
    if (!sl || !inp) return;

    // ── SLIDER → NUMBER (bidirectional, all in JS) ──
    sl.addEventListener('input', function() {
      inp.value = this.value;
      _sliderSync(this);
      // Trigger any existing oninput on the number field
      var ev = document.createEvent('Event');
      ev.initEvent('input', true, true);
      inp.dispatchEvent(ev);
    });

    // ── NUMBER → SLIDER ──
    inp.addEventListener('input', function() {
      sl.value = this.value;
      _sliderSync(sl);
    });

    // ── INIT: sync slider to current input value ──
    var initVal = parseFloat(inp.value) ||
                  parseFloat(inp.getAttribute('placeholder')) ||
                  parseFloat(sl.min) || 0;
    sl.value  = initVal;
    inp.value = initVal;
    _sliderSync(sl);
  });
}"""

if OLD_INIT in v:
    v = v.replace(OLD_INIT, NEW_INIT, 1)
    print('✅ _initSlidersOnLoad upgraded with bidirectional sync')
else:
    print('❌ OLD_INIT not found — checking partial...')
    if '_initSlidersOnLoad' in v:
        # Find manually
        idx = v.find('function _initSlidersOnLoad')
        print(f'  Found at {idx}: {repr(v[idx:idx+200])}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('No oninput on sl-loanpct', 'id="sl-loanpct"' in v2 and 'id="sl-loanpct" min="0" max="80" step="1" value="60" oninput' not in v2),
    ('sl.addEventListener input', 'sl.addEventListener' in v2),
    ('inp.value = this.value',   'inp.value = this.value' in v2),
    ('sl.value = this.value',    'sl.value  = this.value' in v2 or 'sl.value = this.value' in v2),
    ('createEvent input',        'createEvent' in v2),
    ('_sliderSync still exists', 'function _sliderSync' in v2),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
s = sc[0]; ob, cb = s.count('{'), s.count('}')
ok = sum(1 for _,c in checks if c)
for name, c in checks: print(f'  {"OK" if c else "ERR"} {name}')
print(f'Syntax brace: {ob}/{cb} {"✅" if ob==cb else "❌ MISMATCH"}')
print(f'{ok}/{len(checks)} verified')
print('DONE — Hard reload Ctrl+Shift+R!')
