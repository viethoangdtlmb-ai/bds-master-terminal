import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = 'index.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\r\n', '\n').replace('\r', '\n')
results = []

def rep(old, new, tag):
    global content
    if old in content:
        content = content.replace(old, new, 1)
        results.append(f'✅ {tag}')
    else:
        results.append(f'❌ {tag}')

# ══ 1: HTML — Add Combo Sim section inside sim-content ══
OLD_SIM_CLOSE = '''      </div>
    </div>
  </div>

  <!-- TAB 4: PRESCRIPTION -->'''

COMBO_HTML = '''
      <!-- ═══ Giả Lập Tổ Hợp ═══════════════════════════════════════════ -->
      <div class="card" style="margin-top:24px;border-color:rgba(168,85,247,.25)" id="combo-sim-section">
        <div class="card-header">
          <span class="card-title" style="color:#A855F7">🔄 Giả Lập Tổ Hợp — Bán A + Mua B</span>
          <span class="badge badge-muted">Xem tác động lên toàn danh mục</span>
        </div>
        <div style="font-size:12px;color:var(--text-2);margin-bottom:20px">
          Mô phỏng: bán 1+ tài sản hiện hữu → dùng tiền mua 1 tài sản mới. So sánh danh mục Trước / Sau.
        </div>

        <!-- Step 1: Sell -->
        <div style="margin-bottom:20px">
          <div class="section-title" style="font-size:11px;color:#EF4444;margin-bottom:10px">🔴 BƯỚC 1 — Chọn Tài Sản Bán Đi</div>
          <div id="combo-sell-list" style="display:flex;flex-wrap:wrap;gap:8px"></div>
        </div>

        <!-- Step 2: Buy -->
        <div style="margin-bottom:20px">
          <div class="section-title" style="font-size:11px;color:#10B981;margin-bottom:10px">🟢 BƯỚC 2 — Tài Sản Mua Mới</div>
          <div class="card" style="background:rgba(16,185,129,.04);border-color:rgba(16,185,129,.15)">
            <div class="grid-2">
              <div class="form-group">
                <label class="form-label">Tên Tài Sản</label>
                <input class="form-input" id="cb-name" placeholder="Tài sản mới B">
              </div>
              <div class="form-group">
                <label class="form-label">Khu Vực</label>
                <select class="form-select" id="cb-district">
                  <option value="">— Chọn khu vực —</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Giá Vốn (Tỷ)</label>
                <div class="input-unit">
                  <input type="number" step="0.1" class="form-input" id="cb-cost" placeholder="5.0">
                  <span class="input-unit-label">Tỷ</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Giá Thị Trường (Tỷ)</label>
                <div class="input-unit">
                  <input type="number" step="0.1" class="form-input" id="cb-market" placeholder="5.5">
                  <span class="input-unit-label">Tỷ</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Tỷ Lệ Vay (%)</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-loanpct" placeholder="60" min="0" max="100">
                  <span class="input-unit-label">%</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Dư Nợ (Tỷ)</label>
                <div class="input-unit">
                  <input type="number" step="0.1" class="form-input" id="cb-debt" placeholder="3.0">
                  <span class="input-unit-label">Tỷ</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Lãi Suất (%/năm)</label>
                <div class="input-unit">
                  <input type="number" step="0.5" class="form-input" id="cb-rate" placeholder="8.5">
                  <span class="input-unit-label">%/năm</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Thu Thuê / Tháng</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-rent" placeholder="20">
                  <span class="input-unit-label">Triệu</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Mục Tiêu Đầu Tư</label>
                <select class="form-select" id="cb-goal">
                  <option value="cho-thue">Cho thuê — Pha 3 (Dòng tiền)</option>
                  <option value="tang-gia">Tăng giá — Pha 1/2</option>
                  <option value="tich-san">Tích sản dài hạn — Pha 4</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Ân Hạn Nợ Gốc</label>
                <div class="input-unit">
                  <input type="number" class="form-input" id="cb-grace" placeholder="0" min="0">
                  <span class="input-unit-label">tháng</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Run Button -->
        <div style="margin-bottom:20px">
          <button class="btn btn-primary" onclick="runComboSim()" style="background:linear-gradient(135deg,#7C3AED,#A855F7)">
            ▶ Chạy Giả Lập Tổ Hợp
          </button>
          <span style="font-size:11px;color:var(--text-3);margin-left:12px">So sánh Danh Mục Trước / Sau khi thực hiện</span>
        </div>

        <!-- Result -->
        <div id="combo-result" style="display:none"></div>
      </div>
'''

NEW_SIM_CLOSE = COMBO_HTML + '''      </div>
    </div>
  </div>

  <!-- TAB 4: PRESCRIPTION -->'''

rep(OLD_SIM_CLOSE, NEW_SIM_CLOSE, 'Combo Sim HTML in Surgery tab')

# ══ 2: JS — openSimulator hook → populate cb-district + combo sell list ══
OLD_SIM_SELECT_ASSET = '''  selectSimAsset(0);
}'''

NEW_SIM_SELECT_ASSET = '''  selectSimAsset(0);
  renderComboSim(portfolio);
}'''

rep(OLD_SIM_SELECT_ASSET, NEW_SIM_SELECT_ASSET, 'Call renderComboSim in openSimulator')

# ══ 3: JS — Add renderComboSim + runComboSim functions ══
COMBO_JS = '''
// ── Giả Lập Tổ Hợp ─────────────────────────────────────────────────────
let COMBO_SELL_IDS = new Set();

function renderComboSim(portfolio) {
  // Populate sell list
  const sellList = document.getElementById('combo-sell-list');
  if (!sellList) return;
  COMBO_SELL_IDS.clear();
  sellList.innerHTML = portfolio.map((a, i) => {
    const c = calcAsset(a);
    const cfSign = c.cashflow >= 0 ? '+' : '';
    const cfColor = c.cashflow >= 0 ? '#10B981' : '#EF4444';
    return `<button class="btn btn-secondary btn-sm combo-sell-btn" data-id="${a._id}"
        onclick="toggleComboSell('${a._id}', this)"
        style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-width:130px">
        <span style="font-weight:600">${i+1}. ${a.name}</span>
        <span style="font-size:10px;font-family:monospace;color:${cfColor}">${cfSign}${c.cashflow.toFixed(0)} Tr/th &nbsp;|&nbsp; H:${c.health}</span>
      </button>`;
  }).join('');

  // Populate cb-district dropdown
  const cbDist = document.getElementById('cb-district');
  if (cbDist && window.MARKET_DATA) {
    const existing = [...cbDist.options].map(o => o.value);
    window.MARKET_DATA.districts.forEach(d => {
      if (!existing.includes(d.name)) {
        const opt = document.createElement('option');
        opt.value = d.name;
        opt.textContent = `${d.name} — Cycle ${d.cycle}`;
        cbDist.appendChild(opt);
      }
    });
  }
}

function toggleComboSell(id, btn) {
  const numId = parseInt(id);
  if (COMBO_SELL_IDS.has(numId)) {
    COMBO_SELL_IDS.delete(numId);
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-secondary');
  } else {
    COMBO_SELL_IDS.add(numId);
    btn.classList.remove('btn-secondary');
    btn.classList.add('btn-primary');
  }
}

function runComboSim() {
  const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;
  if (!portfolio.length) { alert('Chưa có danh mục!'); return; }

  // Get new asset from form
  const g = id => document.getElementById(id);
  const n = id => parseFloat(g(id)?.value) || 0;
  const s = id => g(id)?.value || '';

  const newAsset = {
    _id: 'combo-new',
    name:      s('cb-name') || 'Tài sản mới B',
    type:      'nha-rieng',
    district:  s('cb-district'),
    area:      0,
    year:      new Date().getFullYear(),
    cost:      n('cb-cost'),
    market:    n('cb-market') || n('cb-cost'),
    goal:      s('cb-goal') || 'cho-thue',
    loanpct:   n('cb-loanpct'),
    debt:      n('cb-debt'),
    rate:      n('cb-rate') || 8.5,
    prefmonths:6,
    floatrate: 13,
    grace:     n('cb-grace'),
    loanterm:  20,
    rentstatus:n('cb-rent') > 0 ? 'dang-thue' : 'trong',
    rent:      n('cb-rent'),
    mgmt:      n('cb-rent') > 0 ? 1.5 : 0,
    maint:     8,
  };

  if (!newAsset.cost && COMBO_SELL_IDS.size === 0) {
    alert('Vui lòng chọn ít nhất 1 tài sản BÁN hoặc nhập tài sản MUA mới.');
    return;
  }

  // Before
  const beforePortfolio = portfolio;
  const beforeCalcs     = beforePortfolio.map(a => ({ a, c: calcAsset(a) }));

  // After: remove sold + add new (if cost filled)
  let afterPortfolio = portfolio.filter(a => !COMBO_SELL_IDS.has(a._id));
  if (newAsset.cost > 0) afterPortfolio = [...afterPortfolio, newAsset];
  if (!afterPortfolio.length) { alert('Danh mục sau giả lập sẽ trống rỗng!'); return; }
  const afterCalcs = afterPortfolio.map(a => ({ a, c: calcAsset(a) }));

  // Metrics
  function metrics(calcs, port) {
    const n = calcs.length;
    return {
      n,
      mkt:    port.reduce((s,a)=>s+(a.market||0),0),
      debt:   port.reduce((s,a)=>s+(a.debt||0),0),
      cf:     calcs.reduce((s,{c})=>s+c.cashflow,0),
      health: Math.round(calcs.reduce((s,{c})=>s+c.health,0)/n),
      equity: calcs.reduce((s,{c})=>s+c.equity,0),
      ph3:    calcs.filter(({c})=>c.phase===3).length,
      profile:classifyProfile(port, calcs),
    };
  }
  const B = metrics(beforeCalcs, beforePortfolio);
  const A = metrics(afterCalcs, afterPortfolio);

  function delta(before, after, fmt, higherBetter=true) {
    const diff = after - before;
    const sign = diff >= 0 ? '+' : '';
    const isGood = higherBetter ? diff > 0 : diff < 0;
    const color = Math.abs(diff) < 0.01 ? '#9CA3AF' : (isGood ? '#10B981' : '#EF4444');
    const arrow = Math.abs(diff) < 0.01 ? '→' : (diff > 0 ? '↑' : '↓');
    return { sign, diff, color, arrow, str: fmt(diff) };
  }

  const rows = [
    { label:'Số tài sản',      b: B.n+'',         a: A.n+'',
      d: delta(B.n,A.n,v=>(v>0?'+':'')+v,true) },
    { label:'Tổng Giá Trị',    b: B.mkt.toFixed(1)+' Tỷ', a: A.mkt.toFixed(1)+' Tỷ',
      d: delta(B.mkt,A.mkt,v=>(v>=0?'+':'')+v.toFixed(2)+' Tỷ',true) },
    { label:'Tổng Dư Nợ',      b: B.debt.toFixed(1)+' Tỷ',a: A.debt.toFixed(1)+' Tỷ',
      d: delta(B.debt,A.debt,v=>(v>=0?'+':'')+v.toFixed(2)+' Tỷ',false) },
    { label:'Vốn Tự Có',       b: B.equity.toFixed(1)+' Tỷ', a: A.equity.toFixed(1)+' Tỷ',
      d: delta(B.equity,A.equity,v=>(v>=0?'+':'')+v.toFixed(2)+' Tỷ',true) },
    { label:'CF / Tháng',       b: (B.cf>=0?'+':'')+B.cf.toFixed(0)+' Tr', a: (A.cf>=0?'+':'')+A.cf.toFixed(0)+' Tr',
      d: delta(B.cf,A.cf,v=>(v>=0?'+':'')+v.toFixed(0)+' Tr',true) },
    { label:'Health Score TB',  b: B.health+'/100', a: A.health+'/100',
      d: delta(B.health,A.health,v=>(v>=0?'+':'')+v,true) },
    { label:'Tài Sản Pha 3',   b: B.ph3+' / '+B.n, a: A.ph3+' / '+A.n,
      d: delta(B.ph3,A.ph3,v=>(v>=0?'+':'')+v,true) },
    { label:'Profile NĐT',      b: PROFILES[B.profile].icon+' '+PROFILES[B.profile].name,
                                 a: PROFILES[A.profile].icon+' '+PROFILES[A.profile].name,
      d: { color: B.profile===A.profile?'#9CA3AF':'#A855F7', arrow:'→', str: '' } },
  ];

  const soldNames = portfolio.filter(a=>COMBO_SELL_IDS.has(a._id)).map(a=>a.name);
  const summary = [
    soldNames.length ? `🔴 Đã bán: ${soldNames.join(', ')}` : null,
    newAsset.cost > 0 ? `🟢 Mua thêm: ${newAsset.name} (${newAsset.cost} Tỷ, ${(newAsset.rent||0)} Tr/tháng)` : null
  ].filter(Boolean).join('&nbsp;&nbsp;|&nbsp;&nbsp;');

  const resultEl = document.getElementById('combo-result');
  resultEl.style.display = 'block';
  resultEl.innerHTML = `
    <div style="background:rgba(168,85,247,.06);border:1px solid rgba(168,85,247,.2);border-radius:10px;padding:16px">
      <div style="font-size:11px;color:#A855F7;font-weight:700;letter-spacing:.07em;text-transform:uppercase;margin-bottom:14px">
        📊 Kết Quả Giả Lập Tổ Hợp
      </div>
      <div style="font-size:11px;color:var(--text-2);margin-bottom:16px;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:6px">${summary}</div>
      <div style="overflow-x:auto">
        <table style="width:100%;border-collapse:collapse;font-size:12px">
          <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,.1)">
              <th style="text-align:left;padding:8px 10px;color:var(--text-3);font-size:10px;text-transform:uppercase">Chỉ Số</th>
              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">TRƯỚC</th>
              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">SAU</th>
              <th style="text-align:center;padding:8px 10px;color:var(--text-3);font-size:10px">THAY ĐỔI</th>
            </tr>
          </thead>
          <tbody>
            ${rows.map(r => `<tr style="border-bottom:1px solid rgba(255,255,255,.04)">
              <td style="padding:8px 10px;color:var(--text-2);font-weight:500">${r.label}</td>
              <td style="padding:8px 10px;text-align:center;color:var(--text-1);font-family:monospace">${r.b}</td>
              <td style="padding:8px 10px;text-align:center;color:var(--text-1);font-family:monospace;font-weight:700">${r.a}</td>
              <td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:${r.d.color}">${r.d.arrow} ${r.d.str}</td>
            </tr>`).join('')}
          </tbody>
        </table>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(168,85,247,.06);border-radius:8px;font-size:12px">
        <strong style="color:#A855F7">💬 Nhận Định:</strong>
        <span style="color:var(--text-2)">
          ${A.cf > B.cf && A.health > B.health ? ' Tổ hợp này CẢI THIỆN cả dòng tiền và sức khỏe danh mục. Khuyến nghị THỰC HIỆN.' :
            A.cf > B.cf && A.health <= B.health ? ' Dòng tiền tốt hơn nhưng Health Score giảm. Chấp nhận nếu ưu tiên thanh khoản tháng gần.' :
            A.cf <= B.cf && A.health > B.health ? ' Health Score cải thiện nhưng dòng tiền kém hơn. Phù hợp chiến lược dài hạn.' :
            ' Tổ hợp này chưa tối ưu. Cân nhắc lại khu vực / giá mua hoặc chọn tài sản khác để bán.'}
        </span>
      </div>
    </div>
  `;
}

'''

rep('// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    COMBO_JS + '// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    'Add renderComboSim + runComboSim JS functions')

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 5 KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()

checks = [
    ('Combo HTML section',       'combo-sim-section'),
    ('Combo sell list HTML',     'combo-sell-list'),
    ('Combo buy form HTML',      'cb-cost'),
    ('Combo run button',         'runComboSim()'),
    ('renderComboSim JS',        'function renderComboSim'),
    ('toggleComboSell JS',       'function toggleComboSell'),
    ('runComboSim JS',           'function runComboSim'),
    ('Metrics function',         'function metrics(calcs, port)'),
    ('Before/After compare',     'TRƯỚC'),
    ('AI recommendation',        'Nhận Định'),
]
ok = err = 0
for name, pat in checks:
    if pat in v:
        print(f'  OK  {name}'); ok += 1
    else:
        print(f'  XX  {name}'); err += 1
print(f'\nTong: {ok} OK / {err} loi')
