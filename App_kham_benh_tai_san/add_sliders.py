"""
add_sliders.py
==============
Thêm slider hybrid cho 3 trường:
  1. f-loanpct  (Tỷ lệ vay 0-80%)
  2. f-rate      (Lãi suất ưu đãi 5-20%)
  3. f-prefmonths (Kỳ ưu đãi còn lại 0-36 tháng)
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── CSS cho slider ─────────────────────────────────────────────
SLIDER_CSS = """
/* ── HYBRID SLIDER ─────────────────────────────── */
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
}
"""

# Thêm CSS vào cuối block <style>
STYLE_END = '</style>'
if SLIDER_CSS.strip() not in v:
    v = v.replace(STYLE_END, SLIDER_CSS + STYLE_END, 1)
    print('✅ CSS slider added')

# ── JS cho slider sync ─────────────────────────────────────────
SLIDER_JS = """
// ── SLIDER SYNC ─────────────────────────────────────────────
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
document.addEventListener('DOMContentLoaded', initAllSliders);
"""

# Thêm JS trước </script>
SCRIPT_END = '</script>'
if 'initAllSliders' not in v:
    v = v.replace(SCRIPT_END, SLIDER_JS + '\n' + SCRIPT_END, 1)
    print('✅ JS slider added')

# ── Thay thế HTML cho 3 trường ────────────────────────────────

# 1. f-loanpct
OLD_LOANPCT = '<input type="number" class="form-input" id="f-loanpct" placeholder="60" min="0" max="100" oninput="onLoanPctChange(this.value)">'
NEW_LOANPCT = '''<div class="slider-wrap">
                <div class="slider-top">
                  <input type="number" class="form-input" id="f-loanpct" placeholder="60" min="0" max="100" oninput="onLoanPctChange(this.value)">
                  <span class="input-unit-label">%</span>
                </div>
                <input type="range" class="range-slider" id="sl-loanpct" min="0" max="80" step="5" value="60">
                <div class="range-labels"><span>0%</span><span>40%</span><span>80%</span></div>
              </div>'''

# 2. f-rate
OLD_RATE = '<input type="number" class="form-input" id="f-rate" placeholder="8.5" step="0.1" min="0">'
NEW_RATE = '''<div class="slider-wrap">
                <div class="slider-top">
                  <input type="number" class="form-input" id="f-rate" placeholder="8.5" step="0.5" min="0">
                  <span class="input-unit-label">%/năm</span>
                </div>
                <input type="range" class="range-slider" id="sl-rate" min="5" max="20" step="0.5" value="8.5">
                <div class="range-labels"><span>5%</span><span>⚠️12%</span><span>🔴16%</span><span>20%</span></div>
              </div>'''

# 3. f-prefmonths
OLD_PREF = '<input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0" style="border-color:var(--yellow)">'
NEW_PREF = '''<div class="slider-wrap">
                <div class="slider-top">
                  <input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0" style="border-color:var(--yellow)">
                  <span class="input-unit-label">tháng</span>
                </div>
                <input type="range" class="range-slider" id="sl-prefmonths" min="0" max="36" step="1" value="6">
                <div class="range-labels"><span>0</span><span>12</span><span>24</span><span>36T</span></div>
              </div>'''

changes = []
for old, new, name in [
    (OLD_LOANPCT, NEW_LOANPCT, 'f-loanpct'),
    (OLD_RATE,    NEW_RATE,    'f-rate'),
    (OLD_PREF,    NEW_PREF,    'f-prefmonths'),
]:
    if old in v:
        # Remove the separate span label since we moved it into slider-wrap
        v = v.replace(old, new, 1)
        changes.append(f'✅ Slider added: {name}')
    else:
        changes.append(f'❌ NOT FOUND: {name}')

# Remove orphan unit labels after replacement (they're now inside slider-wrap)
for unit in ['<span class="input-unit-label">%</span>', '<span class="input-unit-label">%/năm</span>',
             '<span class="input-unit-label">tháng</span>']:
    # Only remove if there's a duplicate (the one outside slider-wrap)
    count = v.count(unit)
    if count >= 2:
        # Find SECOND occurrence and remove it
        idx1 = v.find(unit)
        idx2 = v.find(unit, idx1+1)
        if idx2 > 0:
            v = v[:idx2] + v[idx2+len(unit):]
            changes.append(f'✅ Removed duplicate label: {unit[:30]}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

for c in changes: print(c)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('Slider CSS',        '.range-slider' in v2),
    ('Slider JS',         'initAllSliders' in v2),
    ('sl-loanpct',        'id="sl-loanpct"' in v2),
    ('sl-rate',           'id="sl-rate"' in v2),
    ('sl-prefmonths',     'id="sl-prefmonths"' in v2),
    ('initSlider func',   'function initSlider' in v2),
    ('Color warn',        'warningThreshold' in v2),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
s = sc[0]; ob, cb = s.count('{'), s.count('}')
ok = sum(1 for _,c in checks if c)
for name, c in checks:
    print(f'  {"OK" if c else "ERR"} {name}')
print(f'Syntax: brace {ob}/{cb} {"OK" if ob==cb else "MISMATCH"}')
print(f'{ok}/{len(checks)} verified')
print('DONE — Reload F5!')
