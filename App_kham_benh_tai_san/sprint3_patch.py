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
        results.append(f'❌ {tag} — KHÔNG TÌM THẤY')
        # debug: find close match
        key = old[:60].strip()
        if key in content:
            results.append(f'   ⚠️  Đoạn đầu tìm được nhưng không match đầy đủ')

# ══ 1: HTML — Add f-delivery into chua-ban-giao-note ══
OLD_NOTE_INNER = '''                  <span style="font-size:11px;color:var(--text-2)">Thu thuê dự kiến sau khi nhận nhà:</span>
                  <div class="input-unit" style="max-width:160px">
                    <input type="number" class="form-input" id="f-rent-expected" placeholder="20" min="0">
                    <span class="input-unit-label">Triệu</span>
                  </div>'''

NEW_NOTE_INNER = '''                  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:4px">
                    <div>
                      <div style="font-size:11px;color:var(--text-2);margin-bottom:4px">📅 Nhận nhà sau:</div>
                      <div class="input-unit" style="max-width:120px">
                        <input type="number" class="form-input" id="f-delivery" placeholder="6" min="0">
                        <span class="input-unit-label">tháng</span>
                      </div>
                    </div>
                    <div>
                      <div style="font-size:11px;color:var(--text-2);margin-bottom:4px">💰 Thu thuê dự kiến:</div>
                      <div class="input-unit" style="max-width:130px">
                        <input type="number" class="form-input" id="f-rent-expected" placeholder="20" min="0">
                        <span class="input-unit-label">Triệu/tháng</span>
                      </div>
                    </div>
                  </div>'''

rep(OLD_NOTE_INNER, NEW_NOTE_INNER, 'Delivery field in HTML form')

# ══ 2: getFormData — add delivery field ══
rep(
    "rentstatus: s('f-rentstatus'), rent: n('f-rent'),\n    rentExpected: n('f-rent-expected'),",
    "rentstatus: s('f-rentstatus'), rent: n('f-rent'),\n    delivery: n('f-delivery'),\n    rentExpected: n('f-rent-expected'),",
    'getFormData delivery field'
)

# ══ 3: calcAsset — delivery warning before Phase calc ══
OLD_PHASE_SECTION = '''  // Phân loại 4 Pha (2-Layer Architecture)
  const md = window.MARKET_DATA;'''

NEW_PHASE_SECTION = '''  // Ghi chú tài sản chưa bàn giao
  const deliveryNote = (a.rentstatus === 'chua-ban-giao' && (a.delivery||0) > 0)
    ? `Chưa nhận nhà — dự kiến nhận sau ${a.delivery} tháng. Thu thuê ước tính: ${(a.rentExpected||0)} Tr/tháng.`
    : null;

  // Phân loại 4 Pha (2-Layer Architecture)
  const md = window.MARKET_DATA;'''

rep(OLD_PHASE_SECTION, NEW_PHASE_SECTION, 'calcAsset deliveryNote')

# ══ 4: calcAsset return — include deliveryNote ══
rep(
    'return { gainPct, gainAbs, equity, noi, totalDebt, cashflow, dscr, roeAnnual,\n           floorPrice, phase, phaseWarning, cycle, yoy, viewsTin, cat_lo, health, distData, intOnly, principal, years, marketSignal };',
    'return { gainPct, gainAbs, equity, noi, totalDebt, cashflow, dscr, roeAnnual,\n           floorPrice, phase, phaseWarning, deliveryNote, cycle, yoy, viewsTin, cat_lo, health, distData, intOnly, principal, years, marketSignal };',
    'calcAsset return deliveryNote'
)

# ══ 5: diag-details — show deliveryNote ══
OLD_DETAIL_HDR = '''          <div style="font-weight:600;font-size:12px">${a.name}</div>
          <span class="badge ${assetVerdict(a,c).cls}" style="font-size:10px">${assetVerdict(a,c).label}</span>'''

NEW_DETAIL_HDR = '''          <div style="font-weight:600;font-size:12px">${a.name}${c.deliveryNote?' 🔑':''}</div>
          <span class="badge ${assetVerdict(a,c).cls}" style="font-size:10px">${assetVerdict(a,c).label}</span>'''

rep(OLD_DETAIL_HDR, NEW_DETAIL_HDR, 'deliveryNote icon in diag-details')

# After the closing of that flex div, add the delivery note row
OLD_DETAIL_CLOSE_DIV = '''        </div>
        ${c.deliveryNote ? `<div style="font-size:11px;color:var(--gold)'''
# Not yet there — let me add it after the badge span instead

# Actually, add delivery note after the header block
OLD_DETAIL_FLEX_END = '''<span class="badge ${assetVerdict(a,c).cls}" style="font-size:10px">${assetVerdict(a,c).label}</span>
        </div>'''

NEW_DETAIL_FLEX_END = '''<span class="badge ${assetVerdict(a,c).cls}" style="font-size:10px">${assetVerdict(a,c).label}</span>
        </div>
        ${c.deliveryNote ? `<div style="font-size:11px;color:var(--gold);margin-bottom:6px;padding:3px 8px;background:rgba(212,175,55,0.08);border-radius:4px;border-left:2px solid var(--gold)">⏳ ${c.deliveryNote}</div>` : ''}'''

rep(OLD_DETAIL_FLEX_END, NEW_DETAIL_FLEX_END, 'deliveryNote block in diag-details')

# ══ 6: Quick Scan — add ROE to result ══
OLD_QS_DISPLAY = '''      Lãi vốn: <strong style="color:${gainPct>=0?'var(--emerald)':'var(--red)'}">${gainPct>=0?'+':''}${gainPct.toFixed(1)}%</strong>
      ${cycle ? `&nbsp;|&nbsp; Cycle: <strong>${cycle}/100</strong>` : ''}
      ${viewsTin ? `&nbsp;|&nbsp; Views/Tin: <strong>${viewsTin}</strong>` : ''}'''

NEW_QS_DISPLAY = '''      Lãi vốn: <strong style="color:${gainPct>=0?'var(--emerald)':'var(--red)'}">${gainPct>=0?'+':''}${gainPct.toFixed(1)}%</strong>
      &nbsp;|&nbsp; ROE/vốn: <strong style="color:${roeAnn>=18?'var(--emerald)':roeAnn>=8?'var(--yellow)':'var(--red)'}">${roeAnn.toFixed(1)}%/năm</strong>
      ${cycle ? `&nbsp;|&nbsp; Cycle: <strong>${cycle}/100</strong>` : ''}
      ${viewsTin ? `&nbsp;|&nbsp; Views/Tin: <strong>${viewsTin}</strong>` : ''}'''

rep(OLD_QS_DISPLAY, NEW_QS_DISPLAY, 'ROE in Quick Scan')

# ══ 7: renderDiagnosis — CF card breakdown ══
rep(
    "  const cfColor  = totalCF >= 0 ? 'ok' : 'danger';",
    """  const cfBreakdown = calcs.slice(0,4).map(({a,c}) =>
    `<span style="white-space:nowrap">${(a.name||'').split(' ')[0]}: <strong style="color:${c.cashflow>=0?'var(--emerald)':'var(--red)'}">${c.cashflow>=0?'+':''}${c.cashflow.toFixed(0)}Tr</strong></span>`
  ).join(' | ') + (n>4?' …':'');
  const cfColor  = totalCF >= 0 ? 'ok' : 'danger';""",
    'CF breakdown variable in renderDiagnosis'
)

rep(
    '<div class="stat-sub">${n} tài sản gộp lại</div>',
    '<div class="stat-sub" style="font-size:10px;line-height:1.5">${cfBreakdown}</div>',
    'CF stat-sub breakdown display'
)

# ══ 8: CSS — add badge classes if not already present ══
BADGE_CSS = '''\n/* ── Sprint 3 Badge Classes ─────────────────────────── */
.badge-danger { background:rgba(239,68,68,.15);  color:#EF4444; border:1px solid rgba(239,68,68,.3);  padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;display:inline-block; }
.badge-warn   { background:rgba(234,179,8,.12);  color:#EAB308; border:1px solid rgba(234,179,8,.25); padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;display:inline-block; }
.badge-ok     { background:rgba(16,185,129,.12); color:#10B981; border:1px solid rgba(16,185,129,.25);padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;display:inline-block; }
.badge-gold   { background:rgba(212,175,55,.12); color:#D4AF37; border:1px solid rgba(212,175,55,.25);padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;display:inline-block; }
.badge-muted  { background:rgba(255,255,255,.06);color:#9CA3AF; border:1px solid rgba(255,255,255,.1); padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;display:inline-block; }
\n'''

if 'badge-danger {' not in content and '.badge-danger' not in content:
    rep('</style>', BADGE_CSS + '</style>', 'Badge CSS classes')
else:
    results.append('⏭️  Badge CSS đã tồn tại')

# ══ WRITE ══
content = content.replace('\n', '\r\n')
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print('\n=== SPRINT 3 KẾT QUẢ ===')
for r in results: print(r)

with open(FILE, 'r', encoding='utf-8') as f:
    v = f.read()
print('\n=== VERIFY ===')
checks = [
    ('f-delivery field',    'id="f-delivery"'),
    ('delivery in getForm', "delivery: n('f-delivery')"),
    ('deliveryNote calc',   'deliveryNote = (a.rentstatus'),
    ('deliveryNote return', 'deliveryNote, cycle'),
    ('ROE Quick Scan',      'ROE/vốn'),
    ('cfBreakdown',         'const cfBreakdown'),
    ('CF stat-sub',         'cfBreakdown}</div>'),
    ('badge CSS',           'badge-danger {'),
]
ok = err = 0
for name, pat in checks:
    if pat in v:
        print(f'✅ {name}'); ok += 1
    else:
        print(f'❌ {name}'); err += 1
print(f'\n{ok} OK / {err} lỗi')
