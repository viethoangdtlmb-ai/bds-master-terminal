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

# ══ P2-1: Portfolio Summary CF dùng calcAsset thay vì tính thủ công ══
rep(
    '''      const tCF   = PORTFOLIO.reduce((s,a) => {
        const noi = (a.rent||0)-(a.mgmt||0)-(a.maint||0)/12;
        const dtb = (a.debt||0)*1000*(a.rate||0)/100/12;
        return s + noi - dtb;
      }, 0);''',
    '''      const tCF   = PORTFOLIO.reduce((s,a) => s + calcAsset(a).cashflow, 0);''',
    'P2-1: Portfolio Summary CF dùng calcAsset (có principal + ân hạn)'
)

# ══ P2-2: Asset List DSCR dùng calcAsset thay vì chỉ tính lãi suất ══
rep(
    '''    const equity   = a.cost * (1 - (a.loanpct||0)/100);
    const noi      = (a.rent||0) - (a.mgmt||0) - ((a.maint||0)/12);
    const debt_mth = a.loanpct > 0 && a.debt > 0
      ? (a.debt * 1000 * (a.rate/100/12))
      : 0;
    const dscr = debt_mth > 0 ? (noi / debt_mth).toFixed(2) : 'N/A';
    const dscrColor = dscr === 'N/A' ? 'var(--text-2)' : (parseFloat(dscr) < 0.3 ? 'var(--red)' : parseFloat(dscr) < 0.8 ? 'var(--yellow)' : 'var(--emerald)');''',
    '''    const c_q  = calcAsset(a);
    const dscr = c_q.dscr !== null ? c_q.dscr.toFixed(2) : 'N/A';
    const dscrColor = dscr === 'N/A' ? 'var(--text-2)' : (parseFloat(dscr) < 0.3 ? 'var(--red)' : parseFloat(dscr) < 0.8 ? 'var(--yellow)' : 'var(--emerald)');''',
    'P2-2: Asset List DSCR dùng calcAsset (full debt service)'
)

# ══ P2-3: Combo form thêm Type và Area ══
# Add 2 fields after cb-district
OLD_COMBO_GRID_END = '''              <div class="form-group">
                <label class="form-label">Khu Vực</label>
                <select class="form-select" id="cb-district">
                  <option value="">— Chọn khu vực —</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Giá Vốn (Tỷ)</label>'''

NEW_COMBO_GRID_END = '''              <div class="form-group">
                <label class="form-label">Khu Vực</label>
                <select class="form-select" id="cb-district">
                  <option value="">— Chọn khu vực —</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Loại BĐS</label>
                <select class="form-select" id="cb-type">
                  <option value="nha-rieng">Nhà riêng / Nhà phố</option>
                  <option value="shophouse">Shophouse</option>
                  <option value="chung-cu">Chung cư</option>
                  <option value="dat-nen">Đất nền</option>
                  <option value="biet-thu">Biệt thự</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Diện Tích (m²)</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-area" placeholder="80" min="1">
                  <span class="input-unit-label">m²</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Giá Vốn (Tỷ)</label>'''

rep(OLD_COMBO_GRID_END, NEW_COMBO_GRID_END, 'P2-3a: Thêm trường Type + Area vào combo form')

# Update runComboSim to read cb-type and cb-area
rep(
    "    type:      'nha-rieng',\n    district:  s('cb-district'),\n    area:      0,",
    "    type:      s('cb-type') || 'nha-rieng',\n    district:  s('cb-district'),\n    area:      n('cb-area') || 80,",
    'P2-3b: runComboSim dùng cb-type và cb-area'
)

# ══ P2-4: classifyProfile — no-loan edge case ══
rep(
    '''  const debtR = totalMarket > 0 ? totalDebt/totalMarket : 0;
  // Con Mồi: CF rất âm, đòn bẩy cao, không có Pha3
  if (totalCF < -15 && avgLoan > 55 && ph3 < 0.2) return 'prey';''',
    '''  const debtR = totalMarket > 0 ? totalDebt/totalMarket : 0;
  // Edge case: không vay / tiền mặt — tối thiểu là Người Bảo Vệ (không bao giờ là Con Mồi)
  if (totalDebt < 0.1 && avgLoan < 5) return ph3 >= 0.3 ? 'ruler' : 'guardian';
  // Con Mồi: CF rất âm, đòn bẩy cao, không có Pha3
  if (totalCF < -15 && avgLoan > 55 && ph3 < 0.2) return 'prey';''',
    'P2-4: Profile edge case no-loan → guardian/ruler thay vì prey'
)

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('=== P2 FIX RESULTS ===')
for r in results: print(' ', r)

# Health check
with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
sc = re.findall(r'<script>(.*?)</script>', v, re.DOTALL)
print(f'\nScript blocks: {len(sc)}')
for i, s in enumerate(sc[:-1], 1):
    ob, cb = s.count('{'), s.count('}')
    bt = s.count('`')
    print(f'Script {i}: brace {ob}/{cb} btk {bt}({"even" if bt%2==0 else "ODD"})')

checks = [
    ('CF dùng calcAsset',       'calcAsset(a).cashflow' in v),
    ('DSCR dùng c_q.dscr',      'c_q.dscr' in v),
    ('cb-type field',           'id="cb-type"' in v),
    ('cb-area field',           'id="cb-area"' in v),
    ('runComboSim dùng cb-type', "s('cb-type')" in v),
    ('No-loan profile guard',   'totalDebt < 0.1 && avgLoan < 5' in v),
    ('Dat nen correct',         'Đất nền' in v and '§ất nền' not in v),
]
ok = err = 0
for name, check in checks:
    print(f'  {"✅" if check else "❌"}  {name}')
    if check: ok += 1
    else: err += 1
print(f'\nTotal: {ok} OK / {err} err')
