"""
apply_phase_map.py
==================
Thay thế toàn bộ logic Phase 2-layer bằng HARDCODED lookup table.
Pha 4 vẫn là KH tự chọn (goal='tich-san').
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# ── NEW PHASE BLOCK ────────────────────────────────────────────
NEW_PHASE_BLOCK = '''
  // ============================================================
  // PHÂN LOẠI PHA — HARDCODED LOOKUP TABLE (Q2/2026)
  // Cập nhật thủ công theo thực tế thị trường
  // ============================================================
  const PHASE_MAP = {
    // Pha 1 — Chính Sách (vùng ven, hạ tầng sơ khai, ít dân)
    'Đan Phượng':   1, 'Sóc Sơn':     1, 'Mê Linh':      1,
    'Thạch Thất':   1, 'Từ Sơn (BN)': 1, 'Văn Giang (HY)': 1,
    // Pha 2 — Di Dân (hạ tầng đang lên, dân đang đổ về, yoy cao)
    'Hoài Đức':     2, 'Đông Anh':    2, 'Hoàng Mai':    2,
    'Thanh Trì':    2, 'Gia Lâm':     2,
    // Pha 3 — Dòng Tiền (khu trưởng thành, dân cư ổn định, thanh khoản tốt)
    'Đống Đa':      3, 'Cầu Giấy':   3, 'Hà Đông':      3,
    'Thanh Xuân':   3, 'Hai Bà Trưng':3, 'Ba Đình':      3,
    'Nam Từ Liêm':  3, 'Tây Hồ':     3, 'Bắc Từ Liêm':  3,
    'Hoàn Kiếm':   3, 'Long Biên':   3,
  };

  // Pha 4 (Tích Sản) = KH tự chọn mục tiêu
  let phase, phaseWarning = null;
  if (a.goal === 'tich-san') {
    phase = 4;
  } else {
    phase = PHASE_MAP[a.district] || 2;  // default Pha 2 nếu chưa phân loại
  }

  // Cảnh báo chiến lược lệch pha
  const isCashflow  = a.goal === 'cho-thue';
  const isShortTerm = a.goal === 'tang-gia' && (a.loanpct || 0) > 40;
  if (phase === 1 && isCashflow)
    phaseWarning = 'Khu vực Pha 1 chưa có dân cư — rất khó cho thuê. Chiến lược dòng tiền không phù hợp.';
  if (phase === 1 && isShortTerm)
    phaseWarning = 'Pha 1: Thanh khoản thấp, lướt sóng đòn bẩy cao = rủi ro kẹp hàng.';
  if (phase === 2 && isCashflow)
    phaseWarning = 'Pha 2: Dân đang về, thị trường cho thuê chưa ổn định. Nên chờ Pha 3.';
  if (phase === 3 && isShortTerm)
    phaseWarning = 'Pha 3: Khu trưởng thành, tăng giá chậm. Chiến lược lướt sóng không tối ưu.';'''

# ── TÌM VÀ THAY THẾ PHASE BLOCK CŨ ───────────────────────────
# Pattern: từ "// --- Layer 1: Market Signal ---" đến cuối block phase
# Tìm bằng anchors đặc trưng

START_ANCHOR = '  // --- Layer 1: Market Signal ---'
END_ANCHOR   = '  // Health Score'

idx_start = v.find(START_ANCHOR)
idx_end   = v.find(END_ANCHOR)

if idx_start == -1:
    print('❌ Không tìm thấy START_ANCHOR')
    sys.exit(1)
if idx_end == -1:
    print('❌ Không tìm thấy END_ANCHOR')
    sys.exit(1)

old_block = v[idx_start:idx_end]
print(f'Tìm thấy block cũ: {len(old_block)} chars ({old_block.count(chr(10))} dòng)')
print(f'  Từ char {idx_start} → {idx_end}')

v = v[:idx_start] + NEW_PHASE_BLOCK + '\n\n  ' + v[idx_end:]
print(f'✅ Đã thay thế phase block mới ({len(NEW_PHASE_BLOCK)} chars)')

# Ghi ra file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)

# Verify
with open('index.html', encoding='utf-8') as f:
    v2 = f.read()

checks = [
    ('PHASE_MAP exists',        'const PHASE_MAP = {' in v2),
    ('Pha 1: Đan Phượng',       "'Đan Phượng':   1" in v2),
    ('Pha 2: Hoài Đức',         "'Hoài Đức':     2" in v2),
    ('Pha 3: Long Biên',        "'Long Biên':   3" in v2),
    ('Pha 4: tich-san',         "a.goal === 'tich-san'" in v2),
    ('Old Layer1 gone',         '// --- Layer 1: Market Signal ---' not in v2),
    ('Old Layer2 gone',         '// --- Layer 2: Investor Intent ---' not in v2),
    ('Warning P1 cashflow',     'Pha 1 ch' in v2),
    ('Default Pha 2',           "PHASE_MAP[a.district] || 2" in v2),
]

ok = err = 0
for name, check in checks:
    status = '✅' if check else '❌'
    print(f'  {status} {name}')
    if check: ok += 1
    else: err += 1

# Syntax check
import re as re2
sc = re2.findall(r'<script>(.*?)</script>', v2, re2.DOTALL)
if sc:
    s = sc[0]
    ob, cb = s.count('{'), s.count('}')
    bt = s.count('`')
    print(f'\nSyntax: brace {ob}/{cb} {"✅" if ob==cb else "❌"}  backtick {bt} {"✅" if bt%2==0 else "❌ ODD"}')

print(f'\n{ok}/{len(checks)} verified')
if err == 0:
    print('🎉 DONE — Apply phase hardcode thành công!')
    print('🔄 Reload F5 tại http://localhost:8765')
else:
    print(f'⚠️  {err} lỗi cần kiểm tra')
