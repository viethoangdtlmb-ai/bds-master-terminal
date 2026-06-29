# 🧬 BÁO CÁO KIỂM TRA DNA (50 TÌNH HUỐNG)

## NHÓM 1: Edge Cases
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 1 | Chưa có tài sản (n=0) | `guardian` | `guardian` | ✅ |
| 2 | 1 TS Pha 3 duy nhất, không nợ → Người Giữ Kho (n<2) | `guardian` | `guardian` | ✅ |
| 3 | 1 TS Pha 1 duy nhất, không nợ | `predator` | `predator` | ✅ |
| 4 | 1 TS Pha 2 duy nhất, không nợ | `guardian` | `guardian` | ✅ |
| 5 | 2 TS Pha 3, không nợ → Người Giữ Kho (n=2 < 3 chưa đủ Ruler) | `guardian` | `guardian` | ✅ |
| 6 | 10 TS toàn Pha 2, không nợ, n=10≥3 → Người Gieo Hạt (cash Ph2 thuần) | `planter` | `planter` | ✅ |

## NHÓM 2: KẺ CỜ BẠC 🎲
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 7 | Đất vùng ven, vay 70%, CF âm -25Tr | `prey` | `prey` | ✅ |
| 8 | Toàn Ph1, vay 80%, CF -30Tr | `prey` | `prey` | ✅ |
| 9 | Ph1+Ph2, vay 60%, CF -20Tr, không có Ph3 | `prey` | `prey` | ✅ |
| 10 | avgLoan=56 (vừa qua ngưỡng 55), CF -16Tr, ph3=0 | `prey` | `prey` | ✅ |
| 11 | CF=-14 (chưa đủ -15), vay 70%, ph3=0 → KHÔNG phải Cờ Bạc | `predator` | `predator` | ✅ |
| 12 | CF -16Tr, avgLoan=60>55, ph3=0 → Kẻ Cờ Bạc (step 1) | `prey` | `prey` | ✅ |
| 13 | CF -16Tr, vay 70%, ph3=33% cứu khỏi prey → Thợ Săn (step5) | `predator` | `predator` | ✅ |
| 14 | n=1, ph3=100%, vay, CF nhẹ → Guardian (ph3≥0.35 step 6) | `guardian` | `guardian` | ✅ |

## NHÓM 3: NGƯỜI THỢ SĂN 🏹
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 15 | 3 TS Ph1+Ph2, vay 60% | `predator` | `predator` | ✅ |
| 16 | Cash buyer toàn đất nền Ph1=100% | `predator` | `predator` | ✅ |
| 17 | Ph1=60%, Ph2=40%, vay 45% | `predator` | `predator` | ✅ |
| 18 | Đủ 3 pha nhưng debtR=80% → Thợ Săn (quá nợ, không đủ Thông Thái) | `predator` | `predator` | ✅ |
| 19 | Ph1=50%, Ph2=50%, không nợ (cash buyer Ph1 tấn công) | `predator` | `predator` | ✅ |
| 20 | 3 pha, n=3, debtR=0.35<0.65 → Nhà Thông Thái (step 2) | `sage` | `sage` | ✅ |
| 21 | Ph2 nhiều (70%), vay 50%, CF nhẹ âm | `predator` | `predator` | ✅ |
| 22 | 5 TS 3 pha, debtR=0.3<0.65 → Nhà Thông Thái dù ph3 chỉ 60% | `sage` | `sage` | ✅ |

## NHÓM 4: NHÀ CAI TRỊ 👑
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 23 | 3 căn hộ cho thuê Ph3=100%, debtR=30% → Người Giữ Kho (không có Ph1) | `guardian` | `guardian` | ✅ |
| 24 | Ph3=50%, Ph2=50%, debtR=25%, CF dương, không Ph1 → Người Gieo Hạt | `planter` | `planter` | ✅ |
| 25 | Ph3=40% tại ngưỡng, Ph2=60%, debtR=0.35, không Ph1 → Người Gieo Hạt | `planter` | `planter` | ✅ |
| 26 | 2 căn hộ cash, ph3=100%, không nợ → Người Giữ Kho (n=2 < 3) | `guardian` | `guardian` | ✅ |
| 27 | Ph3=45% nhưng debtR=0.55 → không đủ Ruler → Người Gieo Hạt | `planter` | `planter` | ✅ |
| 28 | Ph3=39%<40%, no Ph1, debtR=0.3<0.7 → Người Gieo Hạt (step4) | `planter` | `planter` | ✅ |
| 29 | Ph3=50%, Ph2=50%, CF=-9, không Ph1, debtR=30% → Người Gieo Hạt | `planter` | `planter` | ✅ |

## NHÓM 5: NGƯỜI GIỮ KHO 🏗️
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 30 | Cash buyer, Ph2=100%, không nợ | `guardian` | `guardian` | ✅ |
| 31 | Ph3=35%, no Ph1, debtR=0.4<0.7 → Người Gieo Hạt (step4) | `planter` | `planter` | ✅ |
| 32 | 3 pha, n=5, debtR=0.28<0.65 → Nhà Thông Thái (kể cả ph3=20%) | `sage` | `sage` | ✅ |
| 33 | Ph2=100%, avgLoan=40, no Ph3 → Thợ Săn (step7 fallback ph1+ph2≥50%) | `predator` | `predator` | ✅ |
| 34 | Không có pha nào, avgLoan=40%, n>0 → Người Thợ Săn (default predator) | `predator` | `predator` | ✅ |
| 35 | 3 pha, n=3, debtR=0.2 → Nhà Thông Thái (kể cả ph3=10%) | `sage` | `sage` | ✅ |

## NHÓM 6: NGƯỜI GIEO HẠT 🌱
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 36 | Nhà phố cho thuê + biệt thự, không nợ, không Ph1 | `planter` | `planter` | ✅ |
| 37 | Ph2+Ph3, debtR=0.6, CF âm -16Tr (logic mới dùng debtR) | `planter` | `planter` | ✅ |
| 38 | Ph3=50%, Ph2=50%, debtR=55% < 70%, CF dương | `planter` | `planter` | ✅ |
| 39 | Ph2+Ph3 cash buyer, không nợ, n=3 | `planter` | `planter` | ✅ |
| 40 | n=2 tối thiểu, Ph2+Ph3, debtR=0.65 (sát ngưỡng 0.7) | `planter` | `planter` | ✅ |
| 41 | Ph2+Ph3 nhưng debtR=0.75 ≥ 0.7 → KHÔNG Gieo Hạt → Guardian | `guardian` | `guardian` | ✅ |
| 42 | n=1, Ph2=100% cash, không Ph3 → Người Giữ Kho (1 TS trong cash branch) | `guardian` | `guardian` | ✅ |

## NHÓM 7: NHÀ THÔNG THÁI 🦉
| # | Tình huống | Kết quả | Kỳ vọng | |
|---|-----------|---------|---------|---|
| 43 | 3 TS đủ 3 pha, debtR=50%, CF trong tầm | `sage` | `sage` | ✅ |
| 44 | 5 TS: 2 Ph1 + 2 Ph2 + 1 Ph3, vay 50% | `sage` | `sage` | ✅ |
| 45 | 3 TS đủ 3 pha, debtR=64% (sát ngưỡng 65%), CF -19 | `sage` | `sage` | ✅ |
| 46 | 7 TS đại gia, đủ 3 pha, nợ hợp lý | `sage` | `sage` | ✅ |
| 47 | Đủ 3 pha nhưng debtR=0.80 → không phải NTT | `predator` | `predator` | ✅ |
| 48 | Đủ 3 pha nhưng CF=-21 → không phải NTT | `predator` | `predator` | ✅ |
| 49 | n=2 (Ph1+Ph3), không Ph2 → không Sage (n<3) → Ruler (Ph3=50%, hasPh1, debtR<40%) | `ruler` | `ruler` | ✅ |
| 50 | 3 TS đủ 3 pha cash buyer (không vay) | `sage` | `sage` | ✅ |

---
## 📊 Tổng kết: **50 PASS / 0 FAIL** / 50 cases
> ✅ **Tất cả 50 cases PASS. Logic DNA hoàn toàn chính xác.**
