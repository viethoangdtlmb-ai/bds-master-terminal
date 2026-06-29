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

# ══ 1: GLOBALS — PROFILES constant + classifyProfile function ══
GLOBALS = '''
// ── Investor Profile System ─────────────────────────────────────────
const PROFILES = {
  ruler: {
    icon:'👑', name:'NGƯỜI CAI TRỊ', eng:'The Ruler', color:'var(--gold)',
    desc:'Tài sản đa dạng, đòn bẩy kiểm soát tốt. Pha 3 — Dòng tiền đang nuôi cả hệ thống.',
    weakness:'Sự trì trệ thế hệ kế cận, cấu trúc quản trị cũ lỗi thời.',
    rx:'Tiếp tục thâu tóm Pha 1 — Chính sách, Hạ Tầng để không ai thay thế đế chế. Consolidate & Expand.',
  },
  guardian: {
    icon:'🛡️', name:'NGƯỜI BẢO VỆ', eng:'The Guardian', color:'var(--emerald)',
    desc:'Bảo toàn vốn tốt, ít rủi ro. Tiền đang "ngủ yên" — tăng trưởng chậm hơn tiềm năng.',
    weakness:'Lạm phát âm thầm ăn mòn sức mua. Thiếu tài sản tăng trưởng.',
    rx:'Chuyển 20–30% danh mục sang Pha 1 để tăng hệ số nhân vốn. Giữ Pha 3 làm lõi phòng thủ.',
  },
  predator: {
    icon:'🐺', name:'KẺ SĂN MỒI', eng:'The Predator', color:'var(--blue,#3B82F6)',
    desc:'Cấu trúc tấn công. Đặt cược vào tăng trưởng Pha 1/2. Dòng tiền chưa phải ưu tiên.',
    weakness:'FOMO ngược — sợ bỏ lỡ kèo thập kỷ. Dễ vỡ nếu thị trường đứng yên > 18 tháng.',
    rx:'Cần ít nhất 1 tài sản Pha 3 tạo "máu" nuôi đòn bẩy. Cân bằng offense với defense.',
  },
  prey: {
    icon:'🩸', name:'CON MỒI', eng:'The Prey', color:'var(--red)',
    desc:'Cảnh báo nguy hiểm. Dòng tiền âm nặng, đòn bẩy cao — đang là "nhiên liệu" cho ngân hàng.',
    weakness:'Sự ngoan cố và hối tiếc quá khứ. Nguy cơ vỡ nợ kỹ thuật.',
    rx:'CẤP CỨU: Cắt ngay tài sản gánh lãi nặng nhất. Giải phóng dòng tiền — thoát khỏi bẫy trước khi quá muộn.',
  },
};

function classifyProfile(portfolio, calcs) {
  const n = portfolio.length;
  if (!n) return 'prey';
  const totalMarket = calcs.reduce((s,{a}) => s+(a.market||0), 0);
  const totalDebt   = calcs.reduce((s,{a}) => s+(a.debt||0), 0);
  const totalCF     = calcs.reduce((s,{c}) => s+c.cashflow, 0);
  const avgLoan     = calcs.reduce((s,{a}) => s+(a.loanpct||0), 0) / n;
  const ph1 = calcs.filter(({c}) => c.phase===1).length / n;
  const ph2 = calcs.filter(({c}) => c.phase===2).length / n;
  const ph3 = calcs.filter(({c}) => c.phase===3).length / n;
  const debtR = totalMarket > 0 ? totalDebt/totalMarket : 0;
  // Con Mồi: CF rất âm, đòn bẩy cao, không có Pha3
  if (totalCF < -15 && avgLoan > 55 && ph3 < 0.2) return 'prey';
  // Kẻ Săn Mồi: Pha1+Pha2 nhiều, đòn bẩy cao
  if ((ph1 + ph2) >= 0.6 && avgLoan > 40) return 'predator';
  // Người Cai Trị: cân bằng, nợ thấp, CF ổn
  if (ph3 >= 0.3 && debtR < 0.4 && totalCF > -10) return 'ruler';
  // Người Bảo Vệ: Pha3 nhiều, vay ít
  if (ph3 >= 0.35 || (ph3 > 0 && avgLoan < 35)) return 'guardian';
  if ((ph1 + ph2) >= 0.5) return 'predator';
  return 'prey';
}

function assetVerdict(a, c) {
  if (c.health < 38 || (c.cashflow < -20 && (a.grace||0) <= 3))
    return {label:'🚨 NÊN BÁN',      cls:'badge-danger'};
  if (a.market < c.floorPrice && c.viewsTin < 3)
    return {label:'⚠️ XEM XÉT BÁN', cls:'badge-warn'};
  if (c.health >= 65 && c.cashflow > 0)
    return {label:'✅ GIỮ VỮNG',     cls:'badge-ok'};
  if (c.phase === 3 && (c.dscr||0) > 0.8)
    return {label:'✅ GIỮ VỮNG',     cls:'badge-ok'};
  if (a.market < c.floorPrice && c.cycle < 60)
    return {label:'⏳ GIỮ 6–12T',    cls:'badge-gold'};
  return {label:'👁️ THEO DÕI',       cls:'badge-muted'};
}

'''

rep('// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    GLOBALS + '// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    'Add PROFILES + classifyProfile + assetVerdict globals')

# ══ 2: Populate investor-profile-box after KPI row ══
PROFILE_BOX = '''
  // ── Investor Profile Box ──────────────────────────────────────────────
  const profKey = classifyProfile(portfolio, calcs);
  const pCfg    = PROFILES[profKey];
  const profBox = document.getElementById('investor-profile-box');
  profBox.style.display = 'block';
  profBox.innerHTML = `
    <div class="card" style="border-color:${pCfg.color}44;background:rgba(0,0,0,0.2)">
      <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
        <div style="text-align:center;min-width:80px">
          <div style="font-size:44px;line-height:1">${pCfg.icon}</div>
          <div style="font-family:var(--mono);font-size:11px;color:${pCfg.color};font-weight:700;letter-spacing:.05em;margin-top:6px">${pCfg.name}</div>
          <div style="font-size:10px;color:var(--text-3);margin-top:2px">${pCfg.eng}</div>
        </div>
        <div style="flex:1;min-width:200px">
          <div style="font-size:13px;color:var(--text-1);margin-bottom:10px;line-height:1.5">${pCfg.desc}</div>
          <div style="font-size:12px;color:var(--yellow);margin-bottom:7px">
            ⚠️ <strong>Điểm yếu cốt lõi:</strong> ${pCfg.weakness}
          </div>
          <div style="font-size:12px;color:${pCfg.color}">
            💊 <strong>Toa thuốc:</strong> ${pCfg.rx}
          </div>
        </div>
      </div>
    </div>
  `;

'''

rep('  // ── Red Alerts (Module 2 — Báo Động Đỏ) ───────────────────────────',
    PROFILE_BOX + '  // ── Red Alerts (Module 2 — Báo Động Đỏ) ───────────────────────────',
    'Populate investor-profile-box')

# ══ 3: Auto-Recommendations block before Asset Matrix ══
RECO_BLOCK = '''
  // ── Auto Recommendations ──────────────────────────────────────────────
  (() => {
    const sorted  = [...calcs].sort((a,b) => a.c.cashflow - b.c.cashflow);
    const worst   = sorted[0];     // CF âm nhất
    const bestCF  = sorted[sorted.length-1]; // CF dương nhất
    const lowestH = [...calcs].sort((a,b) => a.c.health - b.c.health)[0];
    const recos   = [];
    if (worst && worst.c.cashflow < -10)
      recos.push(`🔴 <strong>Cắt hoại tử:</strong> "${worst.a.name}" — đang đốt <strong>${Math.abs(worst.c.cashflow).toFixed(1)} Tr/tháng</strong>. Ưu tiên thoát trong Cửa sổ 0–3 tháng.`);
    if (bestCF && bestCF.c.cashflow > 0)
      recos.push(`🟢 <strong>Giữ vững:</strong> "${bestCF.a.name}" — dòng tiền dương <strong>+${bestCF.c.cashflow.toFixed(1)} Tr/tháng</strong>. Đây là mạch máu của hệ thống.`);
    const ph3Assets = calcs.filter(({c}) => c.phase===3);
    if (ph3Assets.length === 0)
      recos.push(`⚡ <strong>Bơm máu:</strong> Chưa có tài sản Pha 3 — Dòng tiền. Cần tái cơ cấu ngay để tạo nguồn thu ổn định.`);
    const ph1Assets = calcs.filter(({c}) => c.phase===1);
    if (ph1Assets.length === 0 && profKey !== 'prey')
      recos.push(`🚀 <strong>Mở rộng:</strong> Chưa có tài sản Pha 1 — Chính sách, Hạ Tầng. Xem xét phân bổ 20–30% vốn vào khu vực Cycle thấp đang đầu chu kỳ.`);
    if (recos.length === 0)
      recos.push(`✅ Danh mục đang cân bằng tốt. Tiếp tục duy trì cấu trúc hiện tại và theo dõi Cycle Index hàng tháng.`);
    const existing = document.getElementById('diag-alerts').innerHTML;
    document.getElementById('diag-alerts').innerHTML = existing +
      `<div style="margin-top:16px;padding:14px 16px;background:rgba(212,175,55,0.05);border:1px solid var(--gold-dim);border-radius:var(--r-md)">
         <div style="font-size:11px;font-weight:700;color:var(--gold);letter-spacing:.07em;text-transform:uppercase;margin-bottom:10px">💊 Đơn Thuốc Tái Cơ Cấu</div>
         ${recos.map(r=>`<div style="font-size:12px;color:var(--text-2);padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">${r}</div>`).join('')}
       </div>`;
  })();

'''

rep('  // ── Asset Matrix 4 Pha ───────────────────────────────────────────',
    RECO_BLOCK + '  // ── Asset Matrix 4 Pha ───────────────────────────────────────────',
    'Add auto-recommendations block')

# ══ 4: HOLD/SELL badge in diag-details per asset ══
OLD_DETAIL_HEADER = '''        <div style="font-weight:600;font-size:12px;margin-bottom:6px">${a.name}</div>'''
NEW_DETAIL_HEADER = '''        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
          <div style="font-weight:600;font-size:12px">${a.name}</div>
          <span class="badge ${assetVerdict(a,c).cls}" style="font-size:10px">${assetVerdict(a,c).label}</span>
        </div>'''

rep(OLD_DETAIL_HEADER, NEW_DETAIL_HEADER, 'HOLD/SELL badge in diag-details')

# ══ WRITE BACK ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 2 KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
ok = sum(1 for r in results if r.startswith('✅'))
err = sum(1 for r in results if r.startswith('❌'))
print(f'\n{ok} thành công / {err} lỗi')
print('✅ PROFILES' if 'PROFILES' in v else '❌ PROFILES')
print('✅ classifyProfile' if 'classifyProfile' in v else '❌ classifyProfile')
print('✅ assetVerdict' if 'assetVerdict' in v else '❌ assetVerdict')
print('✅ profBox' if 'profBox' in v else '❌ profBox')
print('✅ Đơn Thuốc' if 'Đơn Thuốc Tái Cơ Cấu' in v else '❌ Đơn Thuốc')
print('✅ HOLD/SELL badge' if 'assetVerdict(a,c).label' in v else '❌ HOLD/SELL badge')
