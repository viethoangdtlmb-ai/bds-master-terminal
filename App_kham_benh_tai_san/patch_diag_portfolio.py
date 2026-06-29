#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Nhan ban Danh Muc Tai San tu Triage sang Chan Doan
"""
import sys, os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File loaded: {len(content)} chars")

# ─────────────────────────────────────────────────────────────────────────────
# Markers
CALL_MARKER = "list.innerHTML = PORTFOLIO.map((a, i) => generateAssetCardHTML(a, i, false)).join('');"
FUNC_START  = "function generateAssetCardHTML(a, i, isReadOnly = false) {"
DIAG_PANEL  = '<div id="diag-content" style="display:none">'
DIAG_RENDER = "document.getElementById('diag-content').style.display = 'block';"
RENDER_BEFORE_ASSET = "function renderAssetList() {"

assert CALL_MARKER in content, "FAIL: call marker not found"
assert FUNC_START  in content, "FAIL: func start not found"
assert DIAG_PANEL  in content, "FAIL: diag-content not found"
assert DIAG_RENDER in content, "FAIL: diag render marker not found"
print("All markers found OK")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Extract generateAssetCardHTML body
# ─────────────────────────────────────────────────────────────────────────────
func_start_idx = content.index(FUNC_START)
call_idx       = content.index(CALL_MARKER)

between = content[func_start_idx:call_idx]

depth = 0; closing_pos = -1; i = 0
in_str = False; str_c = ''; in_sl = False; in_ml = False

while i < len(between):
    c = between[i]
    if in_sl:
        if c == '\n': in_sl = False
    elif in_ml:
        if c == '*' and i+1 < len(between) and between[i+1] == '/':
            in_ml = False; i += 1
    elif in_str:
        if c == '\\': i += 1
        elif c == str_c: in_str = False
    else:
        if c == '/' and i+1 < len(between):
            if between[i+1] == '/': in_sl = True; i += 2; continue
            if between[i+1] == '*': in_ml = True; i += 2; continue
        if c in ('"',"'",'`'): in_str = True; str_c = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: closing_pos = i; break
    i += 1

assert closing_pos != -1, "FAIL: cannot find closing brace"
gen_func_body = between[:closing_pos+1]
after_func    = between[closing_pos+1:]
print(f"Extracted generateAssetCardHTML: {len(gen_func_body)} chars")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Remove from renderAssetList, insert comment
# ─────────────────────────────────────────────────────────────────────────────
old_inside = gen_func_body + after_func
new_inside = "\r\n  // generateAssetCardHTML is now a global function (see below)\r\n" + after_func
content = content.replace(old_inside, new_inside, 1)
print("Step 2 done: removed from renderAssetList")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Make clean global version (dedent)
# ─────────────────────────────────────────────────────────────────────────────
lines = gen_func_body.split('\n')
first_line = lines[0]
indent = len(first_line) - len(first_line.lstrip())
dedented = []
for ln in lines:
    if ln[:indent] == ' ' * indent:
        dedented.append(ln[indent:])
    else:
        dedented.append(ln.lstrip())
global_func_clean = '\n'.join(dedented)

insert_text = (
    "\n// === GLOBAL: generateAssetCardHTML ===\n"
    "// Dung chung cho Triage va Chan Doan\n"
    + global_func_clean
    + "\n\n"
)

content = content.replace(RENDER_BEFORE_ASSET, insert_text + RENDER_BEFORE_ASSET, 1)
print("Step 3 done: inserted global generateAssetCardHTML")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Add HTML to diag-content
# ─────────────────────────────────────────────────────────────────────────────
new_diag_open = '''<div id="diag-content" style="display:none">

      <!-- DANH MUC TAI SAN Mirror from Triage read-only -->
      <div id="diag-portfolio-section" style="margin-bottom:24px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
          <div style="font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-3)">
            \U0001f3e0 Danh M\u1ee5c T\u00e0i S\u1ea3n
          </div>
          <span id="diag-asset-count-badge" style="font-size:11px;color:var(--text-2);background:var(--bg-border);padding:2px 10px;border-radius:12px;font-family:var(--mono)"></span>
        </div>
        <div id="diag-portfolio-summary"
             style="display:none;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;
                    background:var(--bg-card);border:1px solid var(--bg-border);
                    border-radius:var(--r-md);padding:14px 16px"></div>
        <div id="diag-asset-list"></div>
      </div>
      <!-- END DANH MUC TAI SAN -->'''

content = content.replace(DIAG_PANEL, new_diag_open, 1)
print("Step 4 done: added diag-portfolio-section HTML")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: Add rendering code to renderDiagnosis
# ─────────────────────────────────────────────────────────────────────────────
portfolio_render_code = r"""document.getElementById('diag-content').style.display = 'block';

  // -- Render portfolio panel (mirror Triage, read-only) ---------------
  (() => {
    const cntBadge = document.getElementById('diag-asset-count-badge');
    if (cntBadge) cntBadge.textContent = portfolio.length + ' tai san';

    const sumDiv = document.getElementById('diag-portfolio-summary');
    if (sumDiv && portfolio.length > 0) {
      const tMkt  = portfolio.reduce((s,a) => s+(a.market||0), 0);
      const tCost = portfolio.reduce((s,a) => s+(a.cost||0), 0);
      const tEq   = portfolio.reduce((s,a) => s+(a.cost||0)*(1-(a.loanpct||0)/100), 0);
      const tDebt = portfolio.reduce((s,a) => s+(calcAsset(a).autoDebt||0)/1000, 0);
      const tCF   = portfolio.reduce((s,a) => s+calcAsset(a).cashflow, 0);
      const gain  = tMkt - tCost;
      const mkStat = (label, val, sub, color) =>
        `<div style="text-align:center"><div style="font-size:10px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">${label}</div><div style="font-family:var(--mono);font-size:18px;font-weight:700;color:${color}">${val}</div><div style="font-size:11px;color:var(--text-2);margin-top:2px">${sub}</div></div>`;
      sumDiv.style.display = 'grid';
      sumDiv.innerHTML =
        mkStat('T\u1ed5ng Gi\u00e1 Tr\u1ecb', tMkt.toFixed(1)+' T\u1ef7', (gain>=0?'+':'')+gain.toFixed(1)+' T\u1ef7 so v\u1ed1n g\u1ed1c', 'var(--gold)') +
        mkStat('V\u1ed1n T\u1ef1 C\u00f3', tEq.toFixed(1)+' T\u1ef7', portfolio.length+' t\u00e0i s\u1ea3n', 'var(--text-1)') +
        mkStat('T\u1ed5ng D\u01b0 N\u1ee3', tDebt.toFixed(1)+' T\u1ef7', 'N\u1ee3 NH hi\u1ec7n t\u1ea1i', tDebt>0?'var(--yellow)':'var(--text-1)') +
        mkStat('D\u00f2ng Ti\u1ec1n/Th\u00e1ng', (tCF>=0?'+':'')+tCF.toFixed(1)+' Tr', '\u01af\u1edbc t\u00ednh l\u00e3i vay c\u01a1 b\u1ea3n', tCF>=0?'var(--emerald)':'var(--red)');
    }

    const diagList = document.getElementById('diag-asset-list');
    if (diagList) {
      diagList.innerHTML = portfolio.map((a, i) => generateAssetCardHTML(a, i, true)).join('');
    }
  })();
  // -- End portfolio panel ----------------------------------------------"""

content = content.replace(DIAG_RENDER, portfolio_render_code, 1)
print("Step 5 done: added rendering to renderDiagnosis()")

# ─────────────────────────────────────────────────────────────────────────────
# WRITE
# ─────────────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"DONE - File saved ({len(content)} chars)")
