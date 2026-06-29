#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phuong an A:
1. Xoa diag-portfolio-summary (Summary Strip) khoi HTML
2. Di chuyen diag-portfolio-section xuong sau diag-kpi trong HTML
3. Xoa code render summary strip khoi renderDiagnosis()
4. Them card "Tong Du No" vao KPI Cards trong renderDiagnosis()
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Loaded: {len(content)} chars")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Trong HTML - xoa diag-portfolio-summary, giu diag-asset-list
# Va move diag-portfolio-section xuong sau diag-kpi
# ─────────────────────────────────────────────────────────────────────────────

# Old portfolio section (at top, with summary strip)
OLD_PORTFOLIO_SECTION = '''      <!-- DANH MUC TAI SAN Mirror from Triage read-only -->
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

assert OLD_PORTFOLIO_SECTION in content, "FAIL: portfolio section not found"

# Remove from top (replace with empty string)
content = content.replace(OLD_PORTFOLIO_SECTION, '', 1)
print("Step 1: Removed portfolio section from top")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Insert diag-portfolio-section AFTER diag-kpi div
# ─────────────────────────────────────────────────────────────────────────────

AFTER_KPI_MARKER = '      <!-- Alerts -->'

NEW_PORTFOLIO_SECTION = '''      <!-- DANH MUC TAI SAN Mirror from Triage read-only — below KPI Cards -->
      <div id="diag-portfolio-section" style="margin-bottom:24px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;margin-top:4px">
          <div style="font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-3)">
            \U0001f3e0 Danh M\u1ee5c T\u00e0i S\u1ea3n
          </div>
          <span id="diag-asset-count-badge" style="font-size:11px;color:var(--text-2);background:var(--bg-border);padding:2px 10px;border-radius:12px;font-family:var(--mono)"></span>
        </div>
        <div id="diag-asset-list"></div>
      </div>
      <!-- END DANH MUC TAI SAN -->

      <!-- Alerts -->'''

assert AFTER_KPI_MARKER in content, "FAIL: alerts marker not found"
content = content.replace(AFTER_KPI_MARKER, NEW_PORTFOLIO_SECTION, 1)
print("Step 2: Inserted portfolio section after KPI Cards")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Xoa code render summary strip khoi renderDiagnosis()
# Phan nay render diag-portfolio-summary
# ─────────────────────────────────────────────────────────────────────────────

OLD_SUMMARY_RENDER = '''    const sumDiv = document.getElementById('diag-portfolio-summary');
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

    const diagList'''

NEW_SUMMARY_RENDER = '''    const diagList'''

assert OLD_SUMMARY_RENDER in content, "FAIL: summary render code not found"
content = content.replace(OLD_SUMMARY_RENDER, NEW_SUMMARY_RENDER, 1)
print("Step 3: Removed summary strip render from renderDiagnosis()")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Them card "Tong Du No" vao KPI Cards trong renderDiagnosis()
# Tim doan render diag-kpi va them them 1 card
# ─────────────────────────────────────────────────────────────────────────────

# Tim vi tri them card - sau card Tong Gia Tri Tai San (card cuoi)
OLD_KPI_END = '''    <div class="stat-card ${mktColor}"><div class="stat-label">T\u1ed5ng Gi\u00e1 Tr\u1ecb T\u00e0i S\u1ea3n</div><div class="stat-value">${totalMarket.toFixed(1)}<small style="font-size:14px"> T\u1ef7</small></div><div class="stat-sub">V\u1ed1n g\u1ed1c: ${totalCost.toFixed(1)} T\u1ef7 &nbsp;|&nbsp; <span style="color:${mktGain>=0?'var(--emerald)':'var(--red)'}">${mktGain>=0?'+':''}${mktGain.toFixed(1)} T\u1ef7</span></div></div>`;'''

# Them card Tong Du No truoc dau backtick ket thuc
NEW_KPI_END = '''    <div class="stat-card ${mktColor}"><div class="stat-label">T\u1ed5ng Gi\u00e1 Tr\u1ecb T\u00e0i S\u1ea3n</div><div class="stat-value">${totalMarket.toFixed(1)}<small style="font-size:14px"> T\u1ef7</small></div><div class="stat-sub">V\u1ed1n g\u1ed1c: ${totalCost.toFixed(1)} T\u1ef7 &nbsp;|&nbsp; <span style="color:${mktGain>=0?'var(--emerald)':'var(--red)'}">${mktGain>=0?'+':''}${mktGain.toFixed(1)} T\u1ef7</span></div></div>

    <div class="stat-card ${totalDebtVal>0?'warn':''}"><div class="stat-label">T\u1ed5ng D\u01b0 N\u1ee3</div><div class="stat-value">${totalDebtVal.toFixed(1)}<small style="font-size:14px"> T\u1ef7</small></div><div class="stat-sub">N\u1ee3 NH hi\u1ec7n t\u1ea1i &mdash; ${n} t\u00e0i s\u1ea3n</div></div>`;'''

assert OLD_KPI_END in content, "FAIL: KPI end marker not found"
content = content.replace(OLD_KPI_END, NEW_KPI_END, 1)
print("Step 4a: Added Tong Du No card to KPI HTML template")

# Them bien totalDebtVal truoc doan render KPI (tim doan tinh totalCost)
OLD_DEBT_CALC = '''  const totalCost   = calcs.reduce((s,{a}) => s+(a.cost||0), 0);'''
NEW_DEBT_CALC = '''  const totalCost   = calcs.reduce((s,{a}) => s+(a.cost||0), 0);
  const totalDebtVal= calcs.reduce((s,{c}) => s+(c.autoDebt||0)/1000, 0);'''

assert OLD_DEBT_CALC in content, "FAIL: totalCost calc not found"
content = content.replace(OLD_DEBT_CALC, NEW_DEBT_CALC, 1)
print("Step 4b: Added totalDebtVal calculation")

# ─────────────────────────────────────────────────────────────────────────────
# WRITE
# ─────────────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"DONE - Saved ({len(content)} chars)")
print("Summary:")
print("  1. Removed Summary Strip from HTML (top of diag-content)")
print("  2. Moved Asset Cards section to BELOW KPI Cards (no strip)")
print("  3. Removed summary strip JS render from renderDiagnosis()")
print("  4. Added Tong Du No card to KPI Cards")
