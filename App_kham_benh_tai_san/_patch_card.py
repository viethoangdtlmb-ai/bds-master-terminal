import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines are 1-indexed; Python list is 0-indexed
# Replace lines 5961-6023 (indices 5960-6022) with clean Row 2 + HEALTH column
START = 5960  # 0-indexed = line 5961
END   = 6023  # 0-indexed end (exclusive) = up to and including line 6023

new_block = r"""      ${isReadOnly ? `
      <!-- Row 2: Ph\u00e2n T\u00edch + HEALTH column -->
      <div style="width:100%;margin-top:8px;display:flex;gap:12px;align-items:stretch">

        <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:7px">

          <div style="display:flex;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;padding-top:8px;border-top:1px solid var(--bg-border)">
            <div>
              <div style="color:var(--text-3);font-size:10px">GI\u00c1 HI\u1ec6N T\u1ea0I</div>
              <div style="color:var(--text-1);font-weight:600">${a.market} T\u1ef7</div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">\u0110\u01a0N GI\u00c1</div>
              <div><strong style="color:var(--text-1)">${c_q.unitPrice > 0 ? c_q.unitPrice.toFixed(1) : '?'}</strong> <span style="font-size:10px;color:var(--text-3)">Tr/m\u00b2</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">L\u00c3I V\u1ed0N</div>
              <div style="color:${gainColor}">${gainSign}${gain.toFixed(1)}%</div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="ROE To\u00e0n Kh\u00f3a: (L\u1ee3i nhu\u1eadn \u0111\u1ea7u t\u01b0 / V\u1ed1n t\u1ef1 c\u00f3)*100">ROE NG\u1ea6M</div>
              <div><strong style="color:${c_q.roeTotal>=0?'var(--emerald)':'var(--red)'}">${c_q.roeTotal.toFixed(1)}%</strong></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px;cursor:help" title="ROE trung b\u00ecnh m\u1ed7i n\u0103m">ROE/N\u0102M</div>
              <div><strong style="color:${c_q.roeAnnual>=15?'var(--emerald)':c_q.roeAnnual>=8?'var(--yellow)':'var(--red)'}">${c_q.roeAnnual.toFixed(1)}%</strong></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">D\u00d2NG TI\u1ec0N</div>
              <div><strong style="color:${c_q.cashflow>=0?'var(--emerald)':'var(--red)'}">${c_q.cashflow>0?'+':''}${c_q.cashflow.toFixed(1)}</strong> <span style="font-size:10px;color:var(--text-3)">Tr</span></div>
            </div>
            <div>
              <div style="color:var(--text-3);font-size:10px">DSCR</div>
              <div style="color:${dscrColor}">${dscr}</div>
            </div>
          </div>

          <!-- Row 3: Verdict + alerts -->
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-top:7px;border-top:1px solid var(--bg-border)">
            <span class="badge ${assetVerdict(a,c_q).cls}" style="font-size:10px;padding:3px 10px">${assetVerdict(a,c_q).label}</span>
            ${c_q.deliveryNote?`<span style="font-size:11px;color:var(--gold);background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);padding:2px 8px;border-radius:4px">\u23f3 ${c_q.deliveryNote}</span>`:''}
            ${(a.grace||0)>0&&(a.grace||0)<=3?`<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">\ud83d\udca3 \u00c2n h\u1ea1n g\u1ed1c c\u00f2n <strong>${a.grace} th\u00e1ng</strong></span>`:''}
            ${(a.prefmonths||0)>0&&(a.prefmonths||0)<=3?`<span style="font-size:11px;color:var(--yellow);background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.2);padding:2px 8px;border-radius:4px">\u26a1 \u01af\u u \u0111\u00e3i h\u1ebft trong <strong>${a.prefmonths} th\u00e1ng</strong></span>`:''}
          </div>

        </div>

        <!-- HEALTH column -->
        <div style="min-width:70px;width:70px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:${c_q.health>=65?'rgba(16,185,129,.08)':c_q.health>=40?'rgba(234,179,8,.08)':'rgba(239,68,68,.08)'};border:1px solid ${c_q.health>=65?'rgba(16,185,129,.25)':c_q.health>=40?'rgba(234,179,8,.25)':'rgba(239,68,68,.25)'};border-radius:8px;padding:10px 6px;text-align:center">
          <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px">Health</div>
          <div style="font-size:26px;font-weight:800;font-family:var(--mono);color:${c_q.health>=65?'var(--emerald)':c_q.health>=40?'var(--yellow)':'var(--red)'};line-height:1">${c_q.health}</div>
          <div style="font-size:9px;color:var(--text-3)">/100</div>
          <div style="font-size:13px;margin-top:4px">${c_q.health>=70?'\U0001f7e2':c_q.health>=45?'\U0001f7e1':'\U0001f534'}</div>
        </div>

      </div>
      ` : ''}

"""

lines[START:END] = [new_block]

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Done. Replaced lines {START+1}-{END} with clean Row 2 + HEALTH column block.")
print(f"File now has {len(lines)} lines.")
