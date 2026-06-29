"""
fix_sliders_v4.py - Inline script block right after slider elements
===================================================================
Đặt script NGAY SAU form elements để chắc chắn elements tồn tại khi JS chạy.
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── Tìm điểm chèn: sau slider loanpct, ngay trước group dư nợ ─
# Từ phân tích trước: slider loanpct ở L3316-3317, form-group tiếp theo ở L3334
ANCHOR = '            <div class="form-group">\n\n\n\n              <label class="form-label">Dư Nợ Gốc Hiện Tại</label>'

INLINE_SCRIPT = """            <script>
(function initSlidersBound() {
  var pairs = [
    ['sl-loanpct','f-loanpct'],
    ['sl-rate','f-rate'],
    ['sl-prefmonths','f-prefmonths']
  ];
  pairs.forEach(function(p) {
    var sl  = document.getElementById(p[0]);
    var inp = document.getElementById(p[1]);
    if (!sl || !inp) { return; }
    // Slider → Number
    sl.addEventListener('input', function() {
      inp.value = this.value;
      inp.dispatchEvent(new Event('input', {bubbles:true}));
    });
    sl.addEventListener('change', function() {
      inp.value = this.value;
    });
    // Number → Slider
    inp.addEventListener('input', function() {
      sl.value = this.value;
    });
    // Set initial value from input placeholder
    var init = parseFloat(inp.value) || parseFloat(inp.placeholder) || parseFloat(sl.min) || 0;
    sl.value  = init;
    inp.value = init;
  });
})();
</script>
"""

if ANCHOR in v:
    v = v.replace(ANCHOR, INLINE_SCRIPT + ANCHOR, 1)
    print('✅ Inline script inserted after slider elements')
else:
    # Try normalized version
    anchor2 = '<div class="form-group">'
    # Find the one near "Dư Nợ Gốc"
    idx = v.find('Dư Nợ Gốc Hiện Tại')
    if idx > 0:
        # Find the nearest form-group div before it
        fg_idx = v.rfind('<div class="form-group">', 0, idx)
        if fg_idx > 0:
            insert_point = fg_idx
            v = v[:insert_point] + INLINE_SCRIPT.replace('            ', '') + v[insert_point:]
            print(f'✅ Inline script inserted at char {insert_point} (before Dư Nợ Gốc section)')
        else:
            print('❌ Could not find insertion point')
    else:
        print('❌ Anchor not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

# Verify
with open('index.html', encoding='utf-8') as f: v2 = f.read()
checks = [
    ('initSlidersBound defined', 'initSlidersBound' in v2),
    ('sl.addEventListener input', "sl.addEventListener('input'" in v2 or 'sl.addEventListener("input"' in v2),
    ('inp.value = this.value',   'inp.value = this.value' in v2),
    ('sl.value = this.value',    'sl.value = this.value' in v2),
    ('BEFORE Dư Nợ section',     v2.find('initSlidersBound') < v2.find('Dư Nợ Gốc')),
    ('AFTER sl-loanpct HTML',    v2.find('id="sl-loanpct"') < v2.find('initSlidersBound')),
]
import re
sc = re.findall(r'<script>(.*?)</script>', v2, re.DOTALL)
# count all script blocks
print(f'Total <script> blocks: {len(sc)}')
ok = sum(1 for _,c in checks if c)
for name, c in checks: print(f'  {"OK" if c else "ERR"} {name}')
print(f'{ok}/{len(checks)} verified')
print('DONE. Hard reload Ctrl+Shift+R to test!')
