import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:/1. BDS/AI-Assistant/App_kham_benh_tai_san/index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the switchTab hook we added for Surgery and add Diagnosis hook too
old = """// Hook: mở simulator khi chuyển sang tab Surgery
const _origSwitchTab = switchTab;
function switchTab(id) {
  _origSwitchTab(id);
  if (id === 'surgery') {
    const p = window.SESSION_PORTFOLIO || PORTFOLIO;
    openSimulator(p);
  }
}"""

new = """// Hook: auto-render khi chuyển tab nếu đã có dữ liệu
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

if old in html:
    html = html.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Done! Tab hook updated.')
else:
    print('String not found')
