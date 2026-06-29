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

# ══ P3-10: Quick Scan — nút Reset sau khi chạy ══
rep(
    '''        <div style="display:flex;gap:10px;align-items:center">
          <button class="btn btn-primary" onclick="runQuickScan()">⚡ Chẩn đoán nhanh</button>
          <div id="qs-result" style="display:none"></div>
        </div>''',
    '''        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
          <button class="btn btn-primary" onclick="runQuickScan()">⚡ Chẩn đoán nhanh</button>
          <button class="btn btn-secondary btn-sm" id="qs-reset-btn" onclick="resetQuickScan()" style="display:none">↺ Quét lại</button>
          <div id="qs-result" style="display:none"></div>
        </div>''',
    'P3-10a: Thêm nút "Quét lại" vào Quick Scan'
)

# Add resetQuickScan function in JS (after runQuickScan)
rep(
    '''// ── Loan Branch ───────────────────────────────────────────────''',
    '''function resetQuickScan() {
  ['qs-district','qs-buy','qs-now','qs-loan','qs-year'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  const res = document.getElementById('qs-result');
  if (res) { res.innerHTML = ''; res.style.display = 'none'; }
  const btn = document.getElementById('qs-reset-btn');
  if (btn) btn.style.display = 'none';
}

// ── Loan Branch ───────────────────────────────────────────────''',
    'P3-10b: Thêm function resetQuickScan()'
)

# Show reset button after running quick scan
rep(
    '''  const res = document.getElementById('qs-result');
  res.style.display = 'flex';
  res.style.gap = '12px';
  res.style.alignItems = 'center';
  res.style.flexWrap = 'wrap';
  res.innerHTML = `''',
    '''  const res = document.getElementById('qs-result');
  res.style.display = 'flex';
  res.style.gap = '12px';
  res.style.alignItems = 'center';
  res.style.flexWrap = 'wrap';
  const qsResetBtn = document.getElementById('qs-reset-btn');
  if (qsResetBtn) qsResetBtn.style.display = 'inline-flex';
  res.innerHTML = `''',
    'P3-10c: Hiện nút Reset sau khi chạy scan'
)

# ══ P3-13: Empty portfolio — hướng dẫn bước đầu ══
rep(
    '''    <!-- Quick Scan Banner -->
    <div id="quick-scan-banner" class="card" style="border-color:var(--gold-dim);background:rgba(212,175,55,0.04);margin-bottom:20px">''',
    '''    <!-- Onboarding Guide (chỉ hiện khi portfolio rỗng, ẩn sau khi thêm tài sản) -->
    <div id="onboarding-guide" class="card" style="border-color:var(--bg-border);background:rgba(59,130,246,0.04);margin-bottom:16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap">
      <div style="font-size:28px">🏗️</div>
      <div style="flex:1">
        <div style="font-size:13px;font-weight:700;color:var(--text-1);margin-bottom:4px">Bắt đầu buổi khám tài sản</div>
        <div style="font-size:12px;color:var(--text-2)">
          <span style="color:var(--gold);font-weight:600">① Nhập tài sản</span> qua form bên dưới hoặc dùng Quick-Load Template
          &nbsp;→&nbsp;
          <span style="color:var(--emerald);font-weight:600">② Thêm vào danh mục</span>
          &nbsp;→&nbsp;
          <span style="color:var(--blue,#60A5FA);font-weight:600">③ Chẩn đoán toàn danh mục</span>
        </div>
      </div>
    </div>

    <!-- Quick Scan Banner -->
    <div id="quick-scan-banner" class="card" style="border-color:var(--gold-dim);background:rgba(212,175,55,0.04);margin-bottom:20px">''',
    'P3-13: Thêm onboarding guide khi portfolio rỗng'
)

# Hide onboarding-guide when portfolio has assets
rep(
    '''  badge.textContent = `${PORTFOLIO.length} tài sản`;
  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';
  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';''',
    '''  badge.textContent = `${PORTFOLIO.length} tài sản`;
  panel.style.display = PORTFOLIO.length > 0 ? 'block' : 'none';
  btnD.style.display  = PORTFOLIO.length > 0 ? 'inline-flex' : 'none';
  const guide = document.getElementById('onboarding-guide');
  if (guide) guide.style.display = PORTFOLIO.length > 0 ? 'none' : 'flex';''',
    'P3-13b: Ẩn onboarding-guide khi đã có tài sản'
)

# ══ P3-14: f-prefmonths yellow border (sync với f-grace) ══
rep(
    '''              <input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0">''',
    '''              <input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0" style="border-color:var(--yellow)">''',
    'P3-14: f-prefmonths border vàng (sync với f-grace)'
)
# Also add hint text like f-grace
rep(
    '''              <div class="input-unit">
                <input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0" style="border-color:var(--yellow)">
                <span class="input-unit-label">tháng</span>
              </div>
            </div>''',
    '''              <div class="input-unit">
                <input type="number" class="form-input" id="f-prefmonths" placeholder="6" min="0" style="border-color:var(--yellow)">
                <span class="input-unit-label">tháng</span>
              </div>
              <div style="font-size:11px;color:var(--yellow);margin-top:4px">⏰ Hết ưu đãi, lãi suất tăng mạnh lên thả nổi</div>
            </div>''',
    'P3-14b: Thêm hint text cho f-prefmonths'
)

# ══ P3-15: Radar — ghi chú khi chỉ có 1 tài sản ══
rep(
    '''  const grade = overallScore>=0.7?{g:'A',c:'#10B981',t:'Danh mục MẠNH'}:overallScore>=0.5?{g:'B',c:'#EAB308',t:'Cần Tối Ưu'}:overallScore>=0.35?{g:'C',c:'#F97316',t:'Nguy Cơ Trung Bình'}:{g:'D',c:'#EF4444',t:'NGUY HIỂM — Cần Cấp Cứu'};
  legend.innerHTML = `''',
    '''  const grade = overallScore>=0.7?{g:'A',c:'#10B981',t:'Danh mục MẠNH'}:overallScore>=0.5?{g:'B',c:'#EAB308',t:'Cần Tối Ưu'}:overallScore>=0.35?{g:'C',c:'#F97316',t:'Nguy Cơ Trung Bình'}:{g:'D',c:'#EF4444',t:'NGUY HIỂM — Cần Cấp Cứu'};
  const singleAssetNote = n < 2 ? '<div style="font-size:10px;color:var(--text-3);margin-bottom:10px;padding:6px 8px;background:rgba(168,85,247,.06);border-radius:4px;border:1px solid rgba(168,85,247,.15)">💡 Cần ≥ 2 tài sản để Radar phản ánh đầy đủ sức khỏe danh mục</div>' : \'\';
  legend.innerHTML = `${singleAssetNote}` + `''',
    'P3-15: Radar note khi n < 2 tài sản'
)
# Close the legend.innerHTML template properly 
rep(
    '''  legend.innerHTML = `${singleAssetNote}` + `
    <div style="margin-bottom:16px;padding:12px;background:${grade.c}11;border-radius:8px;border:1px solid ${grade.c}33;text-align:center">''',
    '''  legend.innerHTML = singleAssetNote + `
    <div style="margin-bottom:16px;padding:12px;background:${grade.c}11;border-radius:8px;border:1px solid ${grade.c}33;text-align:center">''',
    'P3-15b: Fix legend innerHTML concatenation'
)

# ══ P3-17: Prescription empty state cải thiện ══
rep(
    '''    <div id="rx-empty" class="panel-placeholder">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Chưa có báo cáo</div>
      <div class="ph-sub">Nhập thông tin khách hàng ở trên và bấm "Tạo / Cập Nhật Báo Cáo".</div>
    </div>''',
    '''    <div id="rx-empty" class="panel-placeholder">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Chưa có báo cáo</div>
      <div class="ph-sub" style="max-width:420px">
        1️⃣ <strong>Thêm tài sản</strong> ở tab Triage
        &nbsp;→&nbsp;
        2️⃣ <strong>Chẩn đoán</strong> danh mục
        &nbsp;→&nbsp;
        3️⃣ Nhập thông tin KH bên trên → <strong>Tạo Báo Cáo</strong>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="switchTab('triage')" style="margin-top:8px">← Về Triage</button>
    </div>''',
    'P3-17: Cải thiện Prescription empty state + nút về Triage'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== P3 UX FIX RESULTS ===')
for r in results: print(' ', r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob, cb = s.count('{'), s.count('}')
    bt = s.count('`')
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"})')

checks = [
    ('Reset button',           'id="qs-reset-btn"' in v),
    ('resetQuickScan fn',      'function resetQuickScan()' in v),
    ('Onboarding guide',       'id="onboarding-guide"' in v),
    ('Guide hide logic',       'onboarding-guide' in v and 'style.display' in v),
    ('prefmonths yellow',      'id="f-prefmonths"' in v and 'border-color:var(--yellow)' in v),
    ('prefmonths hint',        'Hết ưu đãi' in v),
    ('Radar 1-asset note',     'Cần ≥ 2 tài sản' in v),
    ('Prescription empty CTA', 'Về Triage' in v and 'rx-empty' in v),
]
ok = err = 0
for name, check in checks:
    print(f'  {"✅" if check else "❌"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\nTotal: {ok} OK / {err} err')
