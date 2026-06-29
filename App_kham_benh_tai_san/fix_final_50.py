import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n')

results = []
def rep(old, new, tag):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        results.append(f'✅ {tag}')
    else:
        results.append(f'❌ {tag} — NOT FOUND')

# ══════════════════════════════════════════════════════════════
# FIX 1: Mobile Responsive — @media breakpoints
# ══════════════════════════════════════════════════════════════
rep(
    '@media print {',
    '''/* ── Mobile Responsive ────────────────────────────── */
@media (max-width: 768px) {
  .header-inner { flex-direction: column; gap: 8px; text-align: center; }
  .header-right  { flex-wrap: wrap; justify-content: center; }
  nav { overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .nav-tabs { flex-wrap: nowrap; min-width: max-content; gap: 2px; }
  .nav-tab { font-size: 12px; padding: 8px 10px; white-space: nowrap; }
  .tab-step { display: none; }
  .grid-2, .grid-3 { grid-template-columns: 1fr !important; }
  .card-sm { flex-direction: column; align-items: flex-start !important; }
  .card-sm > div[style*="display:flex;gap:20px"],
  .card-sm > div[style*="display:flex;gap:6px"] { width: 100%; }
  #portfolio-summary { grid-template-columns: repeat(2, 1fr) !important; }
  .form-group { min-width: 0; }
  #combo-sim-section .grid-2 { grid-template-columns: 1fr !important; }
  .panel-placeholder { padding: 24px 12px; }
  #rx-preview { padding: 12px !important; }
}

@media (max-width: 480px) {
  main { padding: 12px 8px; }
  .card { padding: 12px; }
  #portfolio-summary { grid-template-columns: 1fr !important; }
  .nav-tab { font-size: 11px; padding: 6px 8px; }
}

@media print {''',
    'FIX 1: Mobile responsive — @media 768px + 480px'
)

# ══════════════════════════════════════════════════════════════
# FIX 2: Toast notification cho loadTemplate
# ══════════════════════════════════════════════════════════════

# Add toast CSS before the media queries
rep(
    '/* ── Mobile Responsive',
    '''/* ── Toast Notification ────────────────────────── */
#toast-notify {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 10px 18px;
  background: rgba(16,185,129,0.95);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  z-index: 9999;
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
}
#toast-notify.show {
  opacity: 1;
  transform: translateY(0);
}

/* ── Mobile Responsive''',
    'FIX 2a: Toast CSS'
)

# Add toast HTML div before </body>
rep(
    '</body>',
    '<div id="toast-notify"></div>\n</body>',
    'FIX 2b: Toast HTML element'
)

# Add showToast function
rep(
    'function resetQuickScan() {',
    '''function showToast(msg, duration) {
  const t = document.getElementById('toast-notify');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), duration || 2000);
}

function resetQuickScan() {''',
    'FIX 2c: showToast function'
)

# Call showToast in loadTemplate
rep(
    "  if (ev && ev.target) { ev.target.classList.add('btn-primary'); setTimeout(() => ev.target.classList.remove('btn-primary'), 1500); }",
    "  if (ev && ev.target) { ev.target.classList.add('btn-primary'); setTimeout(() => ev.target.classList.remove('btn-primary'), 1500); }\n  showToast('✅ Đã tải mẫu: ' + t.name, 2000);",
    'FIX 2d: showToast trong loadTemplate'
)

# Also toast for addAsset
rep(
    "  PORTFOLIO.push(asset);\n  savePortfolio();\n  renderAssetList();",
    "  PORTFOLIO.push(asset);\n  savePortfolio();\n  renderAssetList();\n  showToast('✅ Đã thêm: ' + asset.name, 2500);",
    'FIX 2e: showToast trong addAsset'
)

# ══════════════════════════════════════════════════════════════
# FIX 3: Combo Sim — thêm trường Năm Mua
# ══════════════════════════════════════════════════════════════
rep(
    '''              <div class="form-group">
                <label class="form-label">Ân Hạn Nợ Gốc</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-grace" placeholder="0" min="0">
                  <span class="input-unit-label">tháng</span>
                </div>
              </div>
            </div>
          </div>
        </div>''',
    '''              <div class="form-group">
                <label class="form-label">Ân Hạn Nợ Gốc</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-grace" placeholder="0" min="0">
                  <span class="input-unit-label">tháng</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Năm Mua (dự kiến)</label>
                <input type="number" class="form-input" id="cb-year" placeholder="2026" min="2000" max="2030">
              </div>
            </div>
          </div>
        </div>''',
    'FIX 3a: Thêm trường Năm Mua vào combo form'
)

# Update runComboSim to use cb-year
rep(
    "    year:      new Date().getFullYear(),",
    "    year:      n('cb-year') || new Date().getFullYear(),",
    'FIX 3b: runComboSim dùng cb-year'
)

# ══════════════════════════════════════════════════════════════
# FIX 4: PDF page-break CSS
# ══════════════════════════════════════════════════════════════
rep(
    '  @page { size: A4; margin: 15mm 15mm 20mm 15mm; }',
    '''  @page { size: A4; margin: 15mm 15mm 20mm 15mm; }
  /* Prevent page breaks inside key sections */
  #rx-preview table { page-break-inside: avoid; }
  #rx-preview .rx-section { page-break-inside: avoid; margin-bottom: 8px; }
  #rx-preview svg { page-break-inside: avoid; }
  /* Force page break before Radar section for clean layout */
  #rx-preview .rx-section:nth-child(5) { page-break-before: always; }''',
    'FIX 4: PDF page-break-inside:avoid + Radar page-break-before'
)

# Add rx-section class to buildPrescription sections
# Wrap each section div with the class
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">I. TÓM TẮT',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">I. TÓM TẮT',
    'FIX 4b: rx-section class vào Section I'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">II. CHẨN ĐOÁN',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">II. CHẨN ĐOÁN',
    'FIX 4c: rx-section class vào Section II'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">III. DANH',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">III. DANH',
    'FIX 4d: rx-section class vào Section III'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">IV. PHÂN',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">IV. PHÂN',
    'FIX 4e: rx-section class vào Section IV'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">V. RADAR',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">V. RADAR',
    'FIX 4f: rx-section class vào Section V'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">VI. CẢNH',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">VI. CẢNH',
    'FIX 4g: rx-section class vào Section VI'
)
rep(
    '  <div style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">VII. TOA',
    '  <div class="rx-section" style="margin-top:28px">\n      <div style="font-size:14px;font-weight:700;color:#1C1C2E;border-bottom:2px solid #D4AF37;padding-bottom:6px;margin-bottom:14px">VII. TOA',
    'FIX 4h: rx-section class vào Section VII'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== FINAL FIX RESULTS ===')
for r in results: print(' ', r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob,cb = s.count('{'),s.count('}')
    bt = s.count('`')
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"})')

checks = [
    ('Mobile 768px',        'max-width: 768px' in v),
    ('Mobile 480px',        'max-width: 480px' in v),
    ('Tab-step hide',       '.tab-step { display: none' in v),
    ('Grid-2 1fr',          ".grid-2, .grid-3 { grid-template-columns: 1fr" in v),
    ('Toast CSS',           '#toast-notify' in v),
    ('Toast HTML',          'id="toast-notify"' in v),
    ('showToast fn',        'function showToast' in v),
    ('Toast in loadTemplate','Đã tải mẫu' in v),
    ('Toast in addAsset',   'Đã thêm' in v),
    ('cb-year field',       'id="cb-year"' in v),
    ('cb-year in runCombo', "n('cb-year')" in v),
    ('page-break-inside',   'page-break-inside: avoid' in v),
    ('page-break-before',   'page-break-before: always' in v),
    ('rx-section class',    'class="rx-section"' in v),
]
ok = err = 0
for name, check in checks:
    print(f'  {"✅" if check else "❌"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\nTotal: {ok}/{len(checks)} OK')
print(f'File: {len(v):,} bytes | {v.count(chr(10)):,} lines')
