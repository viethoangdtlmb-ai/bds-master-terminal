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

# ══ 1: Replace placeholder Tab 4 with full Prescription UI ══
OLD_TAB4 = '''  <!-- TAB 4: PRESCRIPTION -->
  <div id="tab-prescription" class="tab-panel">
    <div class="panel-placeholder">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Bước 4 — Prescription</div>
      <div class="ph-sub">PDF Bệnh Án 7 trang sẽ xuất tại đây. Tính năng V1.5.</div>
    </div>
  </div>'''

NEW_TAB4 = '''  <!-- TAB 4: PRESCRIPTION -->
  <div id="tab-prescription" class="tab-panel">
    <!-- Control Panel (screen only) -->
    <div class="no-print" style="margin-bottom:24px">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:20px">
        <div>
          <div style="font-size:20px;font-weight:700">📋 Prescription — Bệnh Án Tài Sản</div>
          <div style="font-size:12px;color:var(--text-2)">Tạo và xuất báo cáo PDF chuyên nghiệp cho buổi tư vấn</div>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <button class="btn btn-secondary" onclick="buildPrescription()">🔄 Tạo / Cập Nhật Báo Cáo</button>
          <button class="btn btn-primary" onclick="window.print()" id="rx-print-btn" style="display:none">🖨️ In / Xuất PDF</button>
          <button class="btn btn-secondary btn-sm" onclick="switchTab('surgery')">← Surgery</button>
        </div>
      </div>

      <!-- Client info form -->
      <div class="card" style="margin-bottom:16px">
        <div class="card-header"><span class="card-title">👤 Thông Tin Khách Hàng</span></div>
        <div class="grid-2" style="gap:12px">
          <div class="form-group">
            <label class="form-label">Họ Tên Khách Hàng</label>
            <input class="form-input" id="rx-client-name" placeholder="Nguyễn Văn A">
          </div>
          <div class="form-group">
            <label class="form-label">Điện Thoại</label>
            <input class="form-input" id="rx-client-phone" placeholder="0912 345 678">
          </div>
          <div class="form-group">
            <label class="form-label">Tên Tư Vấn Viên</label>
            <input class="form-input" id="rx-consultant" placeholder="Hoàng Việt" value="Hoàng Việt">
          </div>
          <div class="form-group">
            <label class="form-label">Ghi Chú Buổi Khám</label>
            <input class="form-input" id="rx-note" placeholder="Mục tiêu: tái cơ cấu danh mục Q2/2026">
          </div>
        </div>
      </div>

      <div id="rx-empty" style="text-align:center;padding:40px;color:var(--text-3)">
        ⬆️ Nhấn <strong style="color:var(--gold)">"Tạo / Cập Nhật Báo Cáo"</strong> để xem preview và xuất PDF
      </div>
    </div>

    <!-- Print Preview (also used by printer) -->
    <div id="rx-preview" style="display:none"></div>
  </div>'''

rep(OLD_TAB4, NEW_TAB4, 'Tab 4 Prescription UI')

# ══ 2: Add print CSS to <style> tag ══
PRINT_CSS = '''
/* ── Print / PDF Styles ─────────────────────────────────────────── */
@media print {
  body { background:#fff !important; color:#1a1a2e !important; }
  .no-print, header, nav, #rx-empty { display:none !important; }
  .tab-panel { display:none !important; }
  #tab-prescription { display:block !important; }
  #rx-preview { display:block !important; }
  #rx-preview * { color-adjust: exact; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  @page { size: A4; margin: 15mm 15mm 20mm 15mm; }
}

'''

rep('</style>', PRINT_CSS + '</style>', 'Print CSS')

# ══ 3: Add buildPrescription JS function ══
BUILD_RX_JS = '''
// ══ PRESCRIPTION ENGINE ════════════════════════════════════════════════
function buildPrescription() {
  const portfolio = window.SESSION_PORTFOLIO || PORTFOLIO;
  if (!portfolio || !portfolio.length) {
    alert('Chưa có danh mục! Quay lại Triage thêm tài sản trước.');
    return;
  }

  const calcs      = portfolio.map(a => ({ a, c: calcAsset(a) }));
  const n          = portfolio.length;
  const totalCF    = calcs.reduce((s,{c}) => s+c.cashflow, 0);
  const totalMkt   = portfolio.reduce((s,a) => s+(a.market||0), 0);
  const totalDebt  = portfolio.reduce((s,a) => s+(a.debt||0), 0);
  const totalEq    = calcs.reduce((s,{c}) => s+c.equity, 0);
  const avgHealth  = Math.round(calcs.reduce((s,{c}) => s+c.health, 0) / n);
  const profKey    = classifyProfile(portfolio, calcs);
  const pCfg       = PROFILES[profKey];
  const dateStr    = new Date().toLocaleDateString('vi-VN', {day:'2-digit',month:'2-digit',year:'numeric'});
  const timeStr    = new Date().toLocaleTimeString('vi-VN', {hour:'2-digit',minute:'2-digit'});

  // Client info
  const clientName  = document.getElementById('rx-client-name')?.value  || '_______________';
  const clientPhone = document.getElementById('rx-client-phone')?.value || '_______________';
  const consultant  = document.getElementById('rx-consultant')?.value   || 'Hoàng Việt';
  const rxNote      = document.getElementById('rx-note')?.value         || '';

  // Alerts
  const alerts = [];
  calcs.forEach(({a, c}) => {
    if (c.dscr !== null && c.dscr < 0.3)
      alerts.push({ type:'danger', msg:`${a.name}: DSCR = ${c.dscr.toFixed(2)} — nguy hiểm cao` });
    if ((a.grace||0) > 0 && (a.grace||0) <= 3)
      alerts.push({ type:'warn', msg:`${a.name}: Ân hạn còn ${a.grace} tháng — chuẩn bị tăng dòng tiền ra` });
    if ((a.prefmonths||0) > 0 && (a.prefmonths||0) <= 3)
      alerts.push({ type:'warn', msg:`${a.name}: Ưu đãi lãi suất hết trong ${a.prefmonths} tháng` });
    if (a.market < c.floorPrice)
      alerts.push({ type:'danger', msg:`${a.name}: Giá thị trường thấp hơn giá sàn hòa vốn ${c.floorPrice.toFixed(2)} Tỷ` });
  });

  // Recommendations
  const sorted = [...calcs].sort((a,b) => a.c.cashflow - b.c.cashflow);
  const recos = [];
  if (sorted[0] && sorted[0].c.cashflow < -10)
    recos.push(`CẮT HOẠI TỬ: "${sorted[0].a.name}" — đang đốt ${Math.abs(sorted[0].c.cashflow).toFixed(0)} Tr/tháng. Thoát trong 0–3 tháng.`);
  if (!calcs.find(({c}) => c.phase===3))
    recos.push('BƠM MÁU: Chưa có tài sản Pha 3 dòng tiền. Ưu tiên mua 1 tài sản cho thuê ổn định trong 6 tháng tới.');
  recos.push(pCfg.rx);

  // Radar SVG (copy from existing)
  const radarSVG = document.getElementById('diag-radar')?.innerHTML || '';

  // Phase labels
  const PHASE_LABEL = ['', 'Pha 1 — Chính sách, Hạ Tầng', 'Pha 2 — Di Dân Cơ Học', 'Pha 3 — Dòng tiền', 'Pha 4 — Tích Sản Dài Hạn'];
  const PHASE_COLOR = ['', '#3B82F6', '#EAB308', '#10B981', '#9CA3AF'];

  const html = `
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:780px;margin:0 auto;color:#1C1C2E;line-height:1.5">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg,#0d0d1a,#1a1a3e);color:#fff;padding:24px 28px;border-radius:12px 12px 0 0;margin-bottom:0">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">
      <div>
        <div style="font-size:22px;font-weight:900;letter-spacing:.04em;color:#D4AF37">⚡ ASSET ARCHITECT OS</div>
        <div style="font-size:12px;color:#9CA3AF;margin-top:2px">Hệ Điều Hành Chẩn Đoán Danh Mục BĐS — Hoàng Việt</div>
      </div>
      <div style="text-align:right;font-size:11px;color:#9CA3AF">
        <div>📅 ${dateStr} lúc ${timeStr}</div>
        <div style="margin-top:3px">Tư Vấn Viên: <strong style="color:#D4AF37">${consultant}</strong></div>
      </div>
    </div>
    <div style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(255,255,255,.1);display:flex;gap:40px;flex-wrap:wrap">
      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Khách Hàng</span><br><strong style="font-size:15px">${clientName}</strong></div>
      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Liên Hệ</span><br><strong>${clientPhone}</strong></div>
      <div><span style="font-size:10px;color:#9CA3AF;text-transform:uppercase">Mục Tiêu Buổi Khám</span><br><span style="font-size:12px;color:#D1D5DB">${rxNote || 'Chẩn đoán & tái cơ cấu danh mục'}</span></div>
    </div>
  </div>

  <!-- EXECUTIVE SUMMARY -->
  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">I. TÓM TẮT DANH MỤC</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
      ${[
        {l:'Tổng Giá Trị',    v:totalMkt.toFixed(1)+' Tỷ',      c:'#D4AF37'},
        {l:'Vốn Tự Có',       v:totalEq.toFixed(1)+' Tỷ',        c:'#1C1C2E'},
        {l:'Tổng Dư Nợ',      v:totalDebt.toFixed(1)+' Tỷ',      c:totalDebt>0?'#D97706':'#1C1C2E'},
        {l:'Dòng Tiền/Tháng', v:(totalCF>=0?'+':'')+totalCF.toFixed(0)+' Tr', c:totalCF>=0?'#059669':'#DC2626'},
      ].map(x=>`<div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:12px;text-align:center">
        <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${x.l}</div>
        <div style="font-size:20px;font-weight:800;color:${x.c};font-family:monospace">${x.v}</div>
      </div>`).join('')}
    </div>
  </div>

  <!-- PROFILE NĐT -->
  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">II. CHẨN ĐOÁN PROFILE NHÀ ĐẦU TƯ</div>
    <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
      <div style="text-align:center;min-width:80px">
        <div style="font-size:40px">${pCfg.icon}</div>
        <div style="font-size:12px;font-weight:700;color:#1C1C2E;margin-top:4px">${pCfg.name}</div>
        <div style="font-size:10px;color:#9CA3AF">${pCfg.eng}</div>
      </div>
      <div style="flex:1;min-width:200px">
        <p style="margin:0 0 8px;font-size:12px;color:#374151">${pCfg.desc}</p>
        <p style="margin:0 0 6px;font-size:11px;color:#D97706"><strong>⚠️ Điểm yếu:</strong> ${pCfg.weakness}</p>
        <p style="margin:0;font-size:11px;color:#059669"><strong>💊 Toa thuốc:</strong> ${pCfg.rx}</p>
      </div>
      ${radarSVG ? `<div style="width:180px">${radarSVG.replace(/width="\d+"/,'width="180"').replace(/height="\d+"/,'height="180"').replace(/viewBox="0 0 [\d]+ [\d]+"/,'viewBox="0 0 260 260"')}</div>` : ''}
    </div>
    <div style="margin-top:14px;padding:10px 14px;background:#F1F5F9;border-radius:6px">
      <div style="display:flex;gap:24px;flex-wrap:wrap;">
        <span style="font-size:11px;color:#374151">Health Score TB: <strong>${avgHealth}/100</strong></span>
        <span style="font-size:11px;color:#374151">Tài sản: <strong>${n}</strong></span>
        <span style="font-size:11px;color:#374151">Pha 3: <strong>${calcs.filter(({c})=>c.phase===3).length}/${n}</strong></span>
        <span style="font-size:11px;color:#374151">CF: <strong style="color:${totalCF>=0?'#059669':'#DC2626'}">${totalCF>=0?'+':''}${totalCF.toFixed(0)} Tr/tháng</strong></span>
      </div>
    </div>
  </div>

  <!-- ASSET TABLE -->
  <div style="background:#fff;border:1px solid #E2E8F0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#1C1C2E;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px">III. DANH MỤC TÀI SẢN CHI TIẾT</div>
    <table style="width:100%;border-collapse:collapse;font-size:11px">
      <thead>
        <tr style="background:#F8FAFC;border-bottom:2px solid #E2E8F0">
          <th style="text-align:left;padding:8px 10px;color:#6B7280;font-weight:600">#</th>
          <th style="text-align:left;padding:8px 10px;color:#6B7280;font-weight:600">Tài Sản</th>
          <th style="text-align:center;padding:8px 10px;color:#6B7280;font-weight:600">Pha</th>
          <th style="text-align:right;padding:8px 10px;color:#6B7280;font-weight:600">Giá TT</th>
          <th style="text-align:right;padding:8px 10px;color:#6B7280;font-weight:600">CF/Tháng</th>
          <th style="text-align:center;padding:8px 10px;color:#6B7280;font-weight:600">Health</th>
          <th style="text-align:center;padding:8px 10px;color:#6B7280;font-weight:600">Verdict</th>
        </tr>
      </thead>
      <tbody>
        ${calcs.map(({a,c},i) => {
          const v = assetVerdict(a,c);
          const verdictColor = v.cls==='badge-ok'?'#059669':v.cls==='badge-danger'?'#DC2626':v.cls==='badge-warn'?'#D97706':v.cls==='badge-gold'?'#D4AF37':'#6B7280';
          return `<tr style="border-bottom:1px solid #F1F5F9;${i%2===1?'background:#FAFAFA':''}">
            <td style="padding:8px 10px;color:#6B7280">${i+1}</td>
            <td style="padding:8px 10px">
              <div style="font-weight:600;color:#1C1C2E">${a.name}</div>
              <div style="font-size:9px;color:#9CA3AF">${a.district||''}</div>
            </td>
            <td style="padding:8px 10px;text-align:center">
              <span style="font-size:9px;font-weight:700;color:${PHASE_COLOR[c.phase]}">${'Pha ' + c.phase}</span>
            </td>
            <td style="padding:8px 10px;text-align:right;font-family:monospace;font-weight:600">${(a.market||0).toFixed(1)} Tỷ</td>
            <td style="padding:8px 10px;text-align:right;font-family:monospace;font-weight:600;color:${c.cashflow>=0?'#059669':'#DC2626'}">${c.cashflow>=0?'+':''}${c.cashflow.toFixed(0)} Tr</td>
            <td style="padding:8px 10px;text-align:center;font-family:monospace;font-weight:700;color:${c.health>=70?'#059669':c.health>=45?'#D97706':'#DC2626'}">${c.health}</td>
            <td style="padding:8px 10px;text-align:center">
              <span style="font-size:9px;font-weight:700;color:${verdictColor};padding:2px 6px;border:1px solid ${verdictColor}44;border-radius:4px">${v.label}</span>
            </td>
          </tr>`;
        }).join('')}
      </tbody>
    </table>
  </div>

  <!-- ALERTS -->
  ${alerts.length > 0 ? `
  <div style="background:#FFF7ED;border:1px solid #FED7AA;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#C2410C;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">⚠️ IV. CẢNH BÁO ĐỎ</div>
    ${alerts.map(al => `<div style="padding:7px 0;border-bottom:1px solid #FED7AA;font-size:11px;color:${al.type==='danger'?'#DC2626':'#D97706'}">
      ${al.type==='danger'?'🚨':'💣'} ${al.msg}
    </div>`).join('')}
  </div>` : ''}

  <!-- PRESCRIPTION / RECOS -->
  <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-top:none;padding:20px 28px">
    <div style="font-size:13px;font-weight:700;color:#15803D;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">💊 V. TOA THUỐC TÁI CƠ CẤU</div>
    ${recos.map((r,i) => `<div style="padding:8px 12px;margin-bottom:8px;background:#fff;border-left:3px solid #10B981;border-radius:0 6px 6px 0;font-size:12px;color:#1C1C2E">
      <strong style="color:#15803D">${i+1}.</strong> ${r}
    </div>`).join('')}
  </div>

  <!-- FOOTER -->
  <div style="background:#1C1C2E;color:#fff;padding:16px 28px;border-radius:0 0 12px 12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
    <div style="font-size:10px;color:#9CA3AF">
      Asset Architect OS v1.1 &nbsp;·&nbsp; Tài liệu này chỉ dùng cho mục đích tư vấn nội bộ &nbsp;·&nbsp; Không thay thế tư vấn pháp lý/tài chính chuyên nghiệp
    </div>
    <div style="font-size:11px;color:#D4AF37;font-weight:700">
      ${consultant} &nbsp; | &nbsp; ${dateStr}
    </div>
  </div>

</div>
  `;

  const preview = document.getElementById('rx-preview');
  const empty   = document.getElementById('rx-empty');
  const printBtn= document.getElementById('rx-print-btn');
  preview.style.display = 'block';
  preview.innerHTML = html;
  if (empty)   empty.style.display = 'none';
  if (printBtn) printBtn.style.display = 'inline-flex';
}

'''

rep('// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    BUILD_RX_JS + '// ── DIAGNOSIS ENGINE ────────────────────────────────────────────────',
    'Add buildPrescription JS function')

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 6 (PRESCRIPTION) KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()

checks = [
    ('Tab 4 UI',              'rx-client-name'),
    ('Print CSS',             '@media print'),
    ('buildPrescription fn',  'function buildPrescription'),
    ('Header section',        'ASSET ARCHITECT OS'),
    ('Profile section',       'CHẨN ĐOÁN PROFILE'),
    ('Asset table',           'DANH MỤC TÀI SẢN CHI TIẾT'),
    ('Alerts section',        'CẢNH BÁO ĐỎ'),
    ('Prescription section',  'TOA THUỐC TÁI CƠ CẤU'),
    ('Footer',                'Tài liệu này chỉ dùng'),
    ('Print button',          'window.print()'),
]
ok = err = 0
for name, pat in checks:
    if pat in v:
        print(f'  OK  {name}'); ok += 1
    else:
        print(f'  XX  {name}'); err += 1
print(f'\nTong: {ok} OK / {err} loi')
