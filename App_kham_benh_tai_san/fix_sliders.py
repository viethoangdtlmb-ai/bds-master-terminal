"""
fix_sliders.py
==============
Fix 2 issues:
1. CSS: range slider không nhìn thấy track
2. JS: số không nhảy khi kéo slider
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── FIX 1: Thay CSS cũ bằng CSS mới hoạt động ─────────────────
OLD_CSS = """/* ── HYBRID SLIDER ─────────────────────────────── */
.slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}
.slider-top {
  display: flex;
  align-items: center;
  gap: 8px;
}
.slider-top .form-input {
  width: 72px;
  flex-shrink: 0;
  text-align: center;
}
.slider-top .input-unit-label {
  flex-shrink: 0;
}
.range-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(to right, var(--accent) 0%, var(--accent) var(--pct, 50%), rgba(255,255,255,0.15) var(--pct, 50%));
  outline: none;
  cursor: pointer;
  margin: 4px 0 0;
}
.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg-card);
  box-shadow: 0 0 6px rgba(99,102,241,0.6);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.25);
  box-shadow: 0 0 10px rgba(99,102,241,0.9);
}
.range-slider.warn::-webkit-slider-thumb { background: var(--yellow); }
.range-slider.danger::-webkit-slider-thumb { background: var(--red); }
.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 2px;
}"""

NEW_CSS = """/* ── HYBRID SLIDER ─────────────────────────────── */
.slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}
.slider-top {
  display: flex;
  align-items: center;
  gap: 8px;
}
.slider-top .form-input {
  width: 72px;
  flex-shrink: 0;
  text-align: center;
  font-weight: 600;
}
.slider-top .input-unit-label {
  flex-shrink: 0;
}
/* Track + Thumb — works across Chrome/Edge/Firefox */
.range-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: rgba(255,255,255,0.12);
  outline: none;
  cursor: pointer;
  margin: 2px 0;
  transition: background 0.1s;
}
.range-slider::-webkit-slider-runnable-track {
  height: 6px;
  border-radius: 3px;
  background: transparent;
}
.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6366f1;
  border: 3px solid #1e1e3f;
  box-shadow: 0 0 8px rgba(99,102,241,0.8), 0 2px 4px rgba(0,0,0,0.4);
  cursor: pointer;
  margin-top: -7px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.range-slider::-webkit-slider-thumb:hover,
.range-slider::-webkit-slider-thumb:active {
  transform: scale(1.3);
  box-shadow: 0 0 14px rgba(99,102,241,1);
}
.range-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #6366f1;
  border: 3px solid #1e1e3f;
  cursor: pointer;
}
.range-slider::-moz-range-track {
  height: 6px;
  border-radius: 3px;
  background: rgba(255,255,255,0.12);
}
.range-slider.warn::-webkit-slider-thumb { background: #f59e0b; box-shadow: 0 0 8px rgba(245,158,11,0.8); }
.range-slider.warn::-moz-range-thumb     { background: #f59e0b; }
.range-slider.danger::-webkit-slider-thumb { background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.9); }
.range-slider.danger::-moz-range-thumb     { background: #ef4444; }
.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: rgba(255,255,255,0.4);
  margin-top: 1px;
  padding: 0 2px;
}"""

if OLD_CSS in v:
    v = v.replace(OLD_CSS, NEW_CSS, 1)
    print('✅ CSS fixed')
else:
    print('⚠️  Old CSS pattern not found exactly, trying partial...')
    # Try replace just the .range-slider block
    old_track = '.range-slider {\n  -webkit-appearance: none;\n  appearance: none;\n  width: 100%;\n  height: 4px;'
    if old_track in v:
        print('  Found partial, doing full replace of style block')

# ── FIX 2: Thay JS cũ ─────────────────────────────────────────
OLD_JS = """// ── SLIDER SYNC ─────────────────────────────────────────────
function initSlider(sliderId, inputId, min, max, warningThreshold, dangerThreshold) {
  const slider = document.getElementById(sliderId);
  const input  = document.getElementById(inputId);
  if (!slider || !input) return;

  function updateSlider(val) {
    const v = Math.max(min, Math.min(max, parseFloat(val) || min));
    const pct = ((v - min) / (max - min) * 100).toFixed(1);
    slider.style.setProperty('--pct', pct + '%');
    slider.value = v;
    // Color coding
    slider.classList.remove('warn','danger');
    if (dangerThreshold && v >= dangerThreshold) slider.classList.add('danger');
    else if (warningThreshold && v >= warningThreshold) slider.classList.add('warn');
  }

  slider.addEventListener('input', () => {
    input.value = slider.value;
    updateSlider(slider.value);
    // Trigger existing oninput if any
    if (input.oninput) input.oninput.call(input);
    else { input.dispatchEvent(new Event('input')); }
  });

  input.addEventListener('input', () => updateSlider(input.value));
  // Init on load
  updateSlider(input.value || slider.value || min);
}

function initAllSliders() {
  initSlider('sl-loanpct',   'f-loanpct',    0,  80, 60, 75);   // warn 60%, danger 75%
  initSlider('sl-rate',      'f-rate',        5,  20, 12, 16);   // warn 12%, danger 16%
  initSlider('sl-prefmonths','f-prefmonths',  0,  36, null, null);
}

// Run after DOM ready
document.addEventListener('DOMContentLoaded', initAllSliders);"""

NEW_JS = """// ── SLIDER SYNC ─────────────────────────────────────────────
function _sliderTrackColor(slider, pct, warnT, dangerT, val) {
  // Update filled track color via background gradient
  let fillColor = '#6366f1';
  slider.classList.remove('warn','danger');
  if (dangerT && val >= dangerT) { fillColor = '#ef4444'; slider.classList.add('danger'); }
  else if (warnT && val >= warnT) { fillColor = '#f59e0b'; slider.classList.add('warn'); }
  slider.style.background = `linear-gradient(to right, ${fillColor} ${pct}%, rgba(255,255,255,0.12) ${pct}%)`;
}

function initSlider(sliderId, inputId, min, max, warningThreshold, dangerThreshold) {
  const slider = document.getElementById(sliderId);
  const input  = document.getElementById(inputId);
  if (!slider || !input) return;

  function syncFromVal(val, source) {
    const v = Math.max(min, Math.min(max, parseFloat(val) || min));
    const pct = ((v - min) / (max - min) * 100).toFixed(1);
    if (source !== 'slider') slider.value = v;
    if (source !== 'input')  input.value  = v;
    _sliderTrackColor(slider, pct, warningThreshold, dangerThreshold, v);

    // Trigger existing HTML oninput attribute handler
    const onInputAttr = input.getAttribute('oninput');
    if (onInputAttr) {
      try { new Function('event', onInputAttr).call(input, { target: input }); } catch(e) {}
    }
    // Also dispatch native event for any addEventListener listeners
    try { input.dispatchEvent(new Event('input', { bubbles: true })); } catch(e) {}
  }

  slider.addEventListener('input', () => syncFromVal(slider.value, 'slider'));
  input.addEventListener('input', () => syncFromVal(input.value, 'input'));

  // Init: use current input value or placeholder
  const initVal = parseFloat(input.value) || parseFloat(input.getAttribute('placeholder')) || min;
  syncFromVal(initVal, 'both');
}

function initAllSliders() {
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

if OLD_JS in v:
    v = v.replace(OLD_JS, NEW_JS, 1)
    print('✅ JS fixed')
else:
    print('❌ Old JS pattern not found')
    # Try finding initAllSliders block
    idx = v.find('function initAllSliders')
    if idx > 0:
        print(f'  initAllSliders found at {idx}, manual snippet:')
        print(repr(v[idx:idx+200]))

with open('index.html', 'w', encoding='utf-8') as f:
    v = f.write(v)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('New CSS track',     '::-webkit-slider-runnable-track' in v2),
    ('Thumb margin-top',  'margin-top: -7px' in v2),
    ('Track gradient JS', '_sliderTrackColor' in v2),
    ('Attr oninput fix',  'getAttribute' in v2),
    ('DOM ready fix',     "readyState === 'loading'" in v2),
    ('Moz range',         '::-moz-range-thumb' in v2),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
s  = sc[0]; ob, cb = s.count('{'), s.count('}')
ok = sum(1 for _,c in checks if c)
for name, c in checks: print(f'  {"OK" if c else "ERR"} {name}')
print(f'Syntax brace: {ob}/{cb} {"OK" if ob==cb else "MISMATCH"}')
print(f'{ok}/{len(checks)} verified')
print('DONE — Reload F5!')
