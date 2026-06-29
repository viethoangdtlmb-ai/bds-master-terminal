import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:/1. BDS/AI-Assistant/App_kham_benh_tai_san/index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Step 1: Remove the broken hook (infinite loop source)
bad_hook = """// Hook: auto-render khi chuyển tab nếu đã có dữ liệu
const _origSwitchTab = switchTab;
function switchTab(id) {
  _origSwitchTab(id);
  const p = window.SESSION_PORTFOLIO || PORTFOLIO;
  if (id === 'diagnosis' && p && p.length > 0) {
    renderDiagnosis(p);
  }
  if (id === 'surgery') {
    openSimulator(p);
  }
}"""

if bad_hook in html:
    html = html.replace(bad_hook, '// [hook removed - merged into switchTab]', 1)
    print("Removed bad hook")
else:
    print("Bad hook not found - searching...")
    idx = html.find('_origSwitchTab')
    print(repr(html[max(0,idx-50):idx+200]))

# Step 2: Fix the ORIGINAL switchTab to include hooks inline
old_switch = """function switchTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  document.querySelector('[data-tab="' + id + '"]').classList.add('active');
}"""

new_switch = """function switchTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  document.querySelector('[data-tab="' + id + '"]').classList.add('active');
  // Auto-render hooks
  const _p = window.SESSION_PORTFOLIO || PORTFOLIO;
  if (id === 'diagnosis' && _p && _p.length > 0) {
    setTimeout(() => { if (typeof renderDiagnosis === 'function') renderDiagnosis(_p); }, 10);
  }
  if (id === 'surgery' && _p) {
    setTimeout(() => { if (typeof openSimulator === 'function') openSimulator(_p); }, 10);
  }
}"""

if old_switch in html:
    html = html.replace(old_switch, new_switch, 1)
    print("Original switchTab updated with hooks inline")
else:
    print("Original switchTab not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
