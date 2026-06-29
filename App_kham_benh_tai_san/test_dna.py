def classifyProfile(n, totalMarket, totalDebt, totalCF, avgLoan, ph1_pct, ph2_pct, ph3_pct, hasPh1, hasPh2, hasPh3):
    debtR = totalDebt / totalMarket if totalMarket > 0 else 0
    if not n: return 'guardian'
    if totalDebt < 0.1 and avgLoan < 5:
        if hasPh1 and hasPh2 and hasPh3 and n >= 3: return 'sage'
        if not hasPh1 and hasPh2 and hasPh3: return 'planter'
        if not hasPh1 and hasPh2 and not hasPh3 and n >= 3: return 'planter'
        if ph1_pct >= 0.5: return 'predator'
        return 'ruler' if (ph3_pct >= 0.4 and n >= 3) else 'guardian'
    if totalCF < -15 and avgLoan > 55 and ph3_pct < 0.2: return 'prey'
    if hasPh1 and hasPh2 and hasPh3 and n >= 3 and debtR < 0.65 and totalCF > -20: return 'sage'
    if hasPh1 and ph3_pct >= 0.4 and debtR < 0.4 and totalCF > -10: return 'ruler'
    if not hasPh1 and hasPh2 and hasPh3 and n >= 2 and debtR < 0.7: return 'planter'
    if (ph1_pct + ph2_pct) >= 0.6 and avgLoan > 40: return 'predator'
    if ph3_pct >= 0.35 or (ph3_pct > 0 and avgLoan < 35): return 'guardian'
    if (ph1_pct + ph2_pct) >= 0.5: return 'predator'
    return 'prey' if avgLoan > 50 else 'predator'

ICON = {
    'ruler':   '👑 NHÀ CAI TRỊ',
    'guardian':'🏗️ NGƯỜI GIỮ KHO',
    'predator':'🏹 NGƯỜI THỢ SĂN',
    'prey':    '🎲 KẺ CỜ BẠC',
    'sage':    '🦉 NHÀ THÔNG THÁI',
    'planter': '🌱 NGƯỜI GIEO HẠT',
}

cases = [
    # ═══════════════ NHÓM 1: EDGE CASES (6 cases) ═══════════════
    {'group':'NHÓM 1: Edge Cases','expect':'guardian',
     'name':'Chưa có tài sản (n=0)',
     'params':dict(n=0,totalMarket=0,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0,ph2_pct=0,ph3_pct=0,hasPh1=False,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 1: Edge Cases','expect':'guardian',
     'name':'1 TS Pha 3 duy nhất, không nợ → Người Giữ Kho (n<2)',
     'params':dict(n=1,totalMarket=5,totalDebt=0,totalCF=15,avgLoan=0,ph1_pct=0,ph2_pct=0,ph3_pct=1.0,hasPh1=False,hasPh2=False,hasPh3=True)},
    {'group':'NHÓM 1: Edge Cases','expect':'predator',
     'name':'1 TS Pha 1 duy nhất, không nợ',
     'params':dict(n=1,totalMarket=3,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 1: Edge Cases','expect':'guardian',
     'name':'1 TS Pha 2 duy nhất, không nợ',
     'params':dict(n=1,totalMarket=4,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0,ph2_pct=1.0,ph3_pct=0,hasPh1=False,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 1: Edge Cases','expect':'guardian',
     'name':'2 TS Pha 3, không nợ → Người Giữ Kho (n=2 < 3 chưa đủ Ruler)',
     'params':dict(n=2,totalMarket=10,totalDebt=0,totalCF=25,avgLoan=0,ph1_pct=0,ph2_pct=0,ph3_pct=1.0,hasPh1=False,hasPh2=False,hasPh3=True)},
    {'group':'NHÓM 1: Edge Cases','expect':'planter',
     'name':'10 TS toàn Pha 2, không nợ, n=10≥3 → Người Gieo Hạt (cash Ph2 thuần)',
     'params':dict(n=10,totalMarket=50,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0,ph2_pct=1.0,ph3_pct=0,hasPh1=False,hasPh2=True,hasPh3=False)},

    # ═══════════════ NHÓM 2: KẺ CỜ BẠC (8 cases) ═══════════════
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'prey',
     'name':'Đất vùng ven, vay 70%, CF âm -25Tr',
     'params':dict(n=2,totalMarket=10,totalDebt=7,totalCF=-25,avgLoan=70,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'prey',
     'name':'Toàn Ph1, vay 80%, CF -30Tr',
     'params':dict(n=3,totalMarket=15,totalDebt=12,totalCF=-30,avgLoan=80,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'prey',
     'name':'Ph1+Ph2, vay 60%, CF -20Tr, không có Ph3',
     'params':dict(n=3,totalMarket=15,totalDebt=10,totalCF=-20,avgLoan=65,ph1_pct=0.67,ph2_pct=0.33,ph3_pct=0,hasPh1=True,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'prey',
     'name':'avgLoan=56 (vừa qua ngưỡng 55), CF -16Tr, ph3=0',
     'params':dict(n=2,totalMarket=10,totalDebt=5.6,totalCF=-16,avgLoan=56,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'predator',
     'name':'CF=-14 (chưa đủ -15), vay 70%, ph3=0 → KHÔNG phải Cờ Bạc',
     'params':dict(n=2,totalMarket=10,totalDebt=7,totalCF=-14,avgLoan=70,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'prey',
     'name':'CF -16Tr, avgLoan=60>55, ph3=0 → Kẻ Cờ Bạc (step 1)',
     'params':dict(n=2,totalMarket=10,totalDebt=6,totalCF=-16,avgLoan=60,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'predator',
     'name':'CF -16Tr, vay 70%, ph3=33% cứu khỏi prey → Thợ Săn (step5)',
     'params':dict(n=3,totalMarket=15,totalDebt=10,totalCF=-16,avgLoan=65,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 2: KẺ CỜ BẠC 🎲','expect':'guardian',
     'name':'n=1, ph3=100%, vay, CF nhẹ → Guardian (ph3≥0.35 step 6)',
     'params':dict(n=1,totalMarket=5,totalDebt=3,totalCF=-5,avgLoan=60,ph1_pct=0,ph2_pct=0,ph3_pct=1.0,hasPh1=False,hasPh2=False,hasPh3=True)},

    # ═══════════════ NHÓM 3: NGƯỜI THỢ SĂN (8 cases) ═══════════════
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'3 TS Ph1+Ph2, vay 60%',
     'params':dict(n=3,totalMarket=30,totalDebt=18,totalCF=-5,avgLoan=60,ph1_pct=0.67,ph2_pct=0.33,ph3_pct=0,hasPh1=True,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'Cash buyer toàn đất nền Ph1=100%',
     'params':dict(n=3,totalMarket=12,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=1.0,ph2_pct=0,ph3_pct=0,hasPh1=True,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'Ph1=60%, Ph2=40%, vay 45%',
     'params':dict(n=5,totalMarket=40,totalDebt=18,totalCF=-8,avgLoan=45,ph1_pct=0.6,ph2_pct=0.4,ph3_pct=0,hasPh1=True,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'Đủ 3 pha nhưng debtR=80% → Thợ Săn (quá nợ, không đủ Thông Thái)',
     'params':dict(n=4,totalMarket=40,totalDebt=32,totalCF=-12,avgLoan=65,ph1_pct=0.5,ph2_pct=0.25,ph3_pct=0.25,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'Ph1=50%, Ph2=50%, không nợ (cash buyer Ph1 tấn công)',
     'params':dict(n=2,totalMarket=8,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0.5,ph2_pct=0.5,ph3_pct=0,hasPh1=True,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'sage',
     'name':'3 pha, n=3, debtR=0.35<0.65 → Nhà Thông Thái (step 2)',
     'params':dict(n=3,totalMarket=20,totalDebt=7,totalCF=-3,avgLoan=35,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'predator',
     'name':'Ph2 nhiều (70%), vay 50%, CF nhẹ âm',
     'params':dict(n=5,totalMarket=30,totalDebt=15,totalCF=-8,avgLoan=50,ph1_pct=0.3,ph2_pct=0.7,ph3_pct=0,hasPh1=True,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 3: NGƯỜI THỢ SĂN 🏹','expect':'sage',
     'name':'5 TS 3 pha, debtR=0.3<0.65 → Nhà Thông Thái dù ph3 chỉ 60%',
     'params':dict(n=5,totalMarket=30,totalDebt=9,totalCF=2,avgLoan=30,ph1_pct=0.2,ph2_pct=0.2,ph3_pct=0.6,hasPh1=True,hasPh2=True,hasPh3=True)},

    # ═══════════════ NHÓM 4: NHÀ CAI TRỊ (7 cases) ═══════════════
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'guardian',
     'name':'3 căn hộ cho thuê Ph3=100%, debtR=30% → Người Giữ Kho (không có Ph1)',
     'params':dict(n=3,totalMarket=30,totalDebt=9,totalCF=25,avgLoan=30,ph1_pct=0,ph2_pct=0,ph3_pct=1.0,hasPh1=False,hasPh2=False,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'planter',
     'name':'Ph3=50%, Ph2=50%, debtR=25%, CF dương, không Ph1 → Người Gieo Hạt',
     'params':dict(n=4,totalMarket=40,totalDebt=10,totalCF=15,avgLoan=25,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'planter',
     'name':'Ph3=40% tại ngưỡng, Ph2=60%, debtR=0.35, không Ph1 → Người Gieo Hạt',
     'params':dict(n=5,totalMarket=50,totalDebt=17.5,totalCF=0,avgLoan=32,ph1_pct=0,ph2_pct=0.6,ph3_pct=0.4,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'guardian',
     'name':'2 căn hộ cash, ph3=100%, không nợ → Người Giữ Kho (n=2 < 3)',
     'params':dict(n=2,totalMarket=12,totalDebt=0,totalCF=20,avgLoan=0,ph1_pct=0,ph2_pct=0,ph3_pct=1.0,hasPh1=False,hasPh2=False,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'planter',
     'name':'Ph3=45% nhưng debtR=0.55 → không đủ Ruler → Người Gieo Hạt',
     'params':dict(n=2,totalMarket=20,totalDebt=11,totalCF=5,avgLoan=53,ph1_pct=0,ph2_pct=0.55,ph3_pct=0.45,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'planter',
     'name':'Ph3=39%<40%, no Ph1, debtR=0.3<0.7 → Người Gieo Hạt (step4)',
     'params':dict(n=5,totalMarket=30,totalDebt=9,totalCF=5,avgLoan=28,ph1_pct=0,ph2_pct=0.61,ph3_pct=0.39,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 4: NHÀ CAI TRỊ 👑','expect':'planter',
     'name':'Ph3=50%, Ph2=50%, CF=-9, không Ph1, debtR=30% → Người Gieo Hạt',
     'params':dict(n=3,totalMarket=30,totalDebt=9,totalCF=-9,avgLoan=28,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},

    # ═══════════════ NHÓM 5: NGƯỜI GIỮ KHO (6 cases) ═══════════════
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'guardian',
     'name':'Cash buyer, Ph2=100%, không nợ',
     'params':dict(n=2,totalMarket=10,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0,ph2_pct=1.0,ph3_pct=0,hasPh1=False,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'planter',
     'name':'Ph3=35%, no Ph1, debtR=0.4<0.7 → Người Gieo Hạt (step4)',
     'params':dict(n=4,totalMarket=30,totalDebt=12,totalCF=3,avgLoan=40,ph1_pct=0,ph2_pct=0.65,ph3_pct=0.35,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'sage',
     'name':'3 pha, n=5, debtR=0.28<0.65 → Nhà Thông Thái (kể cả ph3=20%)',
     'params':dict(n=5,totalMarket=25,totalDebt=7,totalCF=2,avgLoan=28,ph1_pct=0.4,ph2_pct=0.4,ph3_pct=0.2,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'predator',
     'name':'Ph2=100%, avgLoan=40, no Ph3 → Thợ Săn (step7 fallback ph1+ph2≥50%)',
     'params':dict(n=2,totalMarket=10,totalDebt=4,totalCF=0,avgLoan=40,ph1_pct=0,ph2_pct=1.0,ph3_pct=0,hasPh1=False,hasPh2=True,hasPh3=False)},
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'predator',
     'name':'Không có pha nào, avgLoan=40%, n>0 → Người Thợ Săn (default predator)',
     'params':dict(n=2,totalMarket=10,totalDebt=4,totalCF=-3,avgLoan=40,ph1_pct=0,ph2_pct=0,ph3_pct=0,hasPh1=False,hasPh2=False,hasPh3=False)},
    {'group':'NHÓM 5: NGƯỜI GIỮ KHO 🏗️','expect':'sage',
     'name':'3 pha, n=3, debtR=0.2 → Nhà Thông Thái (kể cả ph3=10%)',
     'params':dict(n=3,totalMarket=20,totalDebt=4,totalCF=2,avgLoan=20,ph1_pct=0.3,ph2_pct=0.6,ph3_pct=0.1,hasPh1=True,hasPh2=True,hasPh3=True)},

    # ═══════════════ NHÓM 6: NGƯỜI GIEO HẠT (7 cases) ═══════════════
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'planter',
     'name':'Nhà phố cho thuê + biệt thự, không nợ, không Ph1',
     'params':dict(n=2,totalMarket=25,totalDebt=0,totalCF=20,avgLoan=0,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'planter',
     'name':'Ph2+Ph3, debtR=0.6, CF âm -16Tr (logic mới dùng debtR)',
     'params':dict(n=2,totalMarket=20,totalDebt=12,totalCF=-16,avgLoan=55,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'planter',
     'name':'Ph3=50%, Ph2=50%, debtR=55% < 70%, CF dương',
     'params':dict(n=4,totalMarket=40,totalDebt=22,totalCF=8,avgLoan=52,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'planter',
     'name':'Ph2+Ph3 cash buyer, không nợ, n=3',
     'params':dict(n=3,totalMarket=15,totalDebt=0,totalCF=10,avgLoan=0,ph1_pct=0,ph2_pct=0.33,ph3_pct=0.67,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'planter',
     'name':'n=2 tối thiểu, Ph2+Ph3, debtR=0.65 (sát ngưỡng 0.7)',
     'params':dict(n=2,totalMarket=20,totalDebt=13,totalCF=-5,avgLoan=60,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'guardian',
     'name':'Ph2+Ph3 nhưng debtR=0.75 ≥ 0.7 → KHÔNG Gieo Hạt → Guardian',
     'params':dict(n=2,totalMarket=20,totalDebt=15,totalCF=-5,avgLoan=70,ph1_pct=0,ph2_pct=0.5,ph3_pct=0.5,hasPh1=False,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 6: NGƯỜI GIEO HẠT 🌱','expect':'guardian',
     'name':'n=1, Ph2=100% cash, không Ph3 → Người Giữ Kho (1 TS trong cash branch)',
     'params':dict(n=1,totalMarket=5,totalDebt=0,totalCF=0,avgLoan=0,ph1_pct=0,ph2_pct=1.0,ph3_pct=0,hasPh1=False,hasPh2=True,hasPh3=False)},

    # ═══════════════ NHÓM 7: NHÀ THÔNG THÁI (8 cases) ═══════════════
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'sage',
     'name':'3 TS đủ 3 pha, debtR=50%, CF trong tầm',
     'params':dict(n=3,totalMarket=30,totalDebt=15,totalCF=-5,avgLoan=45,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'sage',
     'name':'5 TS: 2 Ph1 + 2 Ph2 + 1 Ph3, vay 50%',
     'params':dict(n=5,totalMarket=80,totalDebt=40,totalCF=10,avgLoan=43,ph1_pct=0.4,ph2_pct=0.4,ph3_pct=0.2,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'sage',
     'name':'3 TS đủ 3 pha, debtR=64% (sát ngưỡng 65%), CF -19',
     'params':dict(n=3,totalMarket=25,totalDebt=16,totalCF=-19,avgLoan=58,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'sage',
     'name':'7 TS đại gia, đủ 3 pha, nợ hợp lý',
     'params':dict(n=7,totalMarket=150,totalDebt=70,totalCF=30,avgLoan=42,ph1_pct=0.3,ph2_pct=0.4,ph3_pct=0.3,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'predator',
     'name':'Đủ 3 pha nhưng debtR=0.80 → không phải NTT',
     'params':dict(n=4,totalMarket=40,totalDebt=32,totalCF=-10,avgLoan=60,ph1_pct=0.5,ph2_pct=0.25,ph3_pct=0.25,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'predator',
     'name':'Đủ 3 pha nhưng CF=-21 → không phải NTT',
     'params':dict(n=3,totalMarket=20,totalDebt=10,totalCF=-21,avgLoan=48,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'ruler',
     'name':'n=2 (Ph1+Ph3), không Ph2 → không Sage (n<3) → Ruler (Ph3=50%, hasPh1, debtR<40%)',
     'params':dict(n=2,totalMarket=20,totalDebt=6,totalCF=5,avgLoan=28,ph1_pct=0.5,ph2_pct=0,ph3_pct=0.5,hasPh1=True,hasPh2=False,hasPh3=True)},
    {'group':'NHÓM 7: NHÀ THÔNG THÁI 🦉','expect':'sage',
     'name':'3 TS đủ 3 pha cash buyer (không vay)',
     'params':dict(n=3,totalMarket=30,totalDebt=0,totalCF=15,avgLoan=0,ph1_pct=0.33,ph2_pct=0.33,ph3_pct=0.33,hasPh1=True,hasPh2=True,hasPh3=True)},
]

# ── Chạy test ─────────────────────────────────────────────────────────────────
lines = ['# 🧬 BÁO CÁO KIỂM TRA DNA (50 TÌNH HUỐNG)\n']
current_group = ''
passed = failed = 0

for i, case in enumerate(cases):
    if case['group'] != current_group:
        current_group = case['group']
        lines.append(f'\n## {current_group}\n')
        lines.append('| # | Tình huống | Kết quả | Kỳ vọng | |\n')
        lines.append('|---|-----------|---------|---------|---|\n')

    result = classifyProfile(**case['params'])
    expected = case['expect']
    ok = result == expected
    if ok: passed += 1
    else: failed += 1
    status = '✅' if ok else f'❌ got:`{result}`'
    lines.append(f"| {i+1} | {case['name']} | `{result}` | `{expected}` | {status} |\n")

lines.append(f'\n---\n## 📊 Tổng kết: **{passed} PASS / {failed} FAIL** / {len(cases)} cases\n')
if failed == 0:
    lines.append('> ✅ **Tất cả 50 cases PASS. Logic DNA hoàn toàn chính xác.**\n')
else:
    lines.append(f'> ❌ **{failed} case cần xem xét lại.**\n')

with open('dna_test_report.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Result: {passed} pass, {failed} fail / {len(cases)} total")
