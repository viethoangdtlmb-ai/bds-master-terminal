"""
Fix bug: runQuickScan() bị merge lỗi trong index.html
"""
import re

FILE = 'index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

PATTERN = r'function runQuickScan\(\).*?(?=\n// ── Loan Branch)'

# Emoji 🟢🟡🔴 dùng trực tiếp
REPLACEMENT = """function runQuickScan() {
  const district = document.getElementById('qs-district').value;
  const buyPrice  = parseFloat(document.getElementById('qs-buy').value)  || 0;
  const nowPrice  = parseFloat(document.getElementById('qs-now').value)  || 0;
  const loanPct   = parseFloat(document.getElementById('qs-loan').value) || 0;
  const buyYear   = parseInt(document.getElementById('qs-year').value)   || (new Date().getFullYear() - 2);

  if (!buyPrice || !nowPrice) { alert('Vui lòng nhập giá mua và giá hiện tại.'); return; }

  const years    = Math.max(0.5, new Date().getFullYear() - buyYear);
  const gainPct  = (nowPrice - buyPrice) / buyPrice * 100;
  const equity   = buyPrice * (1 - loanPct / 100);
  const roeAnn   = equity > 0 ? (gainPct / years) * (buyPrice / equity) : 0;
  const md       = window.MARKET_DATA;
  const distData = md ? md.districts.find(d => d.name === district) : null;
  const cycle    = distData ? distData.cycle : null;
  const viewsTin = distData ? distData.views_tin : null;

  let health = 50;
  if (gainPct > 30) health += 20;
  else if (gainPct > 15) health += 10;
  else if (gainPct < 0) health -= 20;
  if (roeAnn > 18) health += 10;
  else if (roeAnn < 4 && loanPct > 0) health -= 10;
  if (cycle && cycle > 70) health += 10;
  if (cycle && cycle < 35) health -= 15;
  if (viewsTin && viewsTin < 3) health -= 10;
  health = Math.max(10, Math.min(95, health));

  const color = health >= 70 ? 'var(--emerald)' : health >= 45 ? 'var(--yellow)' : 'var(--red)';
  const icon  = health >= 70 ? '\U0001F7E2' : health >= 45 ? '\U0001F7E1' : '\U0001F534';

  const res = document.getElementById('qs-result');
  res.style.display = 'flex';
  res.style.gap = '12px';
  res.style.alignItems = 'center';
  res.style.flexWrap = 'wrap';
  res.innerHTML = `
    <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:${color}">${icon} ${health}/100</div>
    <div style="font-size:12px;color:var(--text-2)">
      Lãi vốn: <strong style="color:${gainPct>=0?'var(--emerald)':'var(--red)'}">${gainPct>=0?'+':''}${gainPct.toFixed(1)}%</strong>
      ${cycle ? `&nbsp;|&nbsp; Cycle: <strong>${cycle}/100</strong>` : ''}
      ${viewsTin ? `&nbsp;|&nbsp; Views/Tin: <strong>${viewsTin}</strong>` : ''}
    </div>
    <button class="btn btn-secondary btn-sm" onclick="switchTab('triage');toggleQuickScan()">→ Khám đầy đủ</button>
  `;
}"""

match = re.search(PATTERN, content, re.DOTALL)
if match:
    original = match.group(0)
    print(f"Tìm thấy function. Length gốc: {len(original)} chars")
    print(f"Preview (80 chars lỗi): ...{repr(original[500:600])}")

    new_content = content[:match.start()] + REPLACEMENT + content[match.end():]

    # Chuẩn hóa về CRLF
    new_content = new_content.replace('\r\n', '\n').replace('\r', '\n')
    new_content = new_content.replace('\n', '\r\n')

    with open(FILE, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)

    # Verify
    with open(FILE, 'r', encoding='utf-8') as f:
        verify = f.read()

    count_fn  = verify.count('function runQuickScan()')
    broken1   = 'toggleQuickScan()"> →' in verify
    broken2   = '}d)' in verify
    dup_health = verify.count('let health = 50;')

    print(f"\n=== KẾT QUẢ ===")
    print(f"Số function runQuickScan(): {count_fn}  {'✅' if count_fn==1 else '❌'}")
    print(f"Pattern lỗi còn không:     {'❌ CÒN' if broken1 or broken2 else '✅ SẠCH'}")
    print(f"Số 'let health = 50;':     {dup_health}  {'✅' if dup_health==1 else '⚠️ duplicate!'}")
    if count_fn == 1 and not broken1 and not broken2 and dup_health == 1:
        print("\n🎉 FIX HOÀN TẤT — File sạch!")
    else:
        print("\n⚠️ Cần kiểm tra lại.")
else:
    print("❌ Không tìm thấy pattern! Thử debug...")
    print(f"  'function runQuickScan' có trong file: {'function runQuickScan' in content}")
