/**
 * SCRIPT LẤY GIÁ NHÀ RIÊNG V4 - INTERCEPT FETCH + AUTO CLICK
 * =============================================================
 * 
 * CÁCH DÙNG (Chrome Snippet - chỉ cần setup 1 lần):
 * 
 * 1. Mở Chrome → vào https://batdongsan.com.vn/ban-nha-rieng-ba-dinh?vrs=1
 * 2. Nhấn F12 → tab "Sources" → bên trái chọn "Snippets"
 *    (nếu không thấy, click ">>" để mở thêm tab)
 * 3. Click "+ New snippet" → đặt tên "nha_rieng"
 * 4. Paste TOÀN BỘ code này vào snippet
 * 5. Nhấn Ctrl+Enter hoặc click phải → Run
 * 6. Script sẽ tự động:
 *    - Click "Xem lịch sử giá" → "5 năm"
 *    - Bắt dữ liệu từ API response
 *    - Chuyển sang quận tiếp theo
 *    - Mỗi khi trang mới load xong → BẠN CHẠY LẠI Snippet (Ctrl+Enter)
 * 7. Khi đủ 22 quận → file CSV tự download
 *
 * RESET: Nếu muốn chạy lại từ đầu, paste vào Console:
 *   localStorage.removeItem("NR_V4")
 */

(function () {
    const STORAGE_KEY = "NR_V4";
    const DISTRICTS = [
        { name: "Ba Dinh", slug: "ban-nha-rieng-ba-dinh" },
        { name: "Bac Tu Liem", slug: "ban-nha-rieng-bac-tu-liem" },
        { name: "Cau Giay", slug: "ban-nha-rieng-cau-giay" },
        { name: "Dan Phuong", slug: "ban-nha-rieng-dan-phuong" },
        { name: "Dong Anh", slug: "ban-nha-rieng-dong-anh" },
        { name: "Dong Da", slug: "ban-nha-rieng-dong-da" },
        { name: "Gia Lam", slug: "ban-nha-rieng-gia-lam" },
        { name: "Ha Dong", slug: "ban-nha-rieng-ha-dong" },
        { name: "Hai Ba Trung", slug: "ban-nha-rieng-hai-ba-trung" },
        { name: "Hoai Duc", slug: "ban-nha-rieng-hoai-duc" },
        { name: "Hoan Kiem", slug: "ban-nha-rieng-hoan-kiem" },
        { name: "Hoang Mai", slug: "ban-nha-rieng-hoang-mai" },
        { name: "Long Bien", slug: "ban-nha-rieng-long-bien" },
        { name: "Me Linh", slug: "ban-nha-rieng-me-linh" },
        { name: "Nam Tu Liem", slug: "ban-nha-rieng-nam-tu-liem" },
        { name: "Soc Son", slug: "ban-nha-rieng-soc-son" },
        { name: "Tay Ho", slug: "ban-nha-rieng-tay-ho" },
        { name: "Thach That", slug: "ban-nha-rieng-thach-that" },
        { name: "Thanh Tri", slug: "ban-nha-rieng-thanh-tri" },
        { name: "Thanh Xuan", slug: "ban-nha-rieng-thanh-xuan" },
        { name: "Van Giang (HY)", slug: "ban-nha-rieng-van-giang" },
        { name: "Tu Son (BN)", slug: "ban-nha-rieng-tu-son-bn" }
    ];

    // ===== Load state =====
    let state = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (!state) {
        state = { idx: 0, data: {} };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        console.log("%c🏠 NHÀ RIÊNG COLLECTOR V4 - BẮT ĐẦU", "color:#00bcd4;font-size:16px;font-weight:bold");
    }

    // ===== Check if done =====
    if (state.idx >= DISTRICTS.length) {
        console.log("%c✅ ĐÃ XONG TẤT CẢ 22 QUẬN!", "color:#4caf50;font-size:16px;font-weight:bold");
        downloadCSV(state.data);
        localStorage.removeItem(STORAGE_KEY);
        return;
    }

    const d = DISTRICTS[state.idx];
    console.log(`%c[${state.idx + 1}/22] ${d.name}`, "color:#ff9800;font-size:14px;font-weight:bold");

    // ===== Check correct page =====
    if (!window.location.pathname.includes(d.slug.replace("ban-nha-rieng-", ""))) {
        console.log(`🔄 Đang chuyển tới ${d.name}...`);
        window.location.href = `https://batdongsan.com.vn/${d.slug}?vrs=1`;
        return;
    }

    // ===== STEP 1: Intercept fetch =====
    console.log("  🔌 Đang chặn fetch API...");
    const _origFetch = window.fetch;
    let captured = false;

    window.fetch = async function (...args) {
        const resp = await _origFetch.apply(this, args);
        const url = typeof args[0] === "string" ? args[0] : args[0]?.url || "";

        if (url.includes("GetPricingHistory") && !captured) {
            captured = true;
            try {
                const clone = resp.clone();
                const json = await clone.json();
                const cp = json?.chartPoints || json?.data?.chartPoints || [];

                if (cp.length > 0) {
                    state.data[d.name] = cp.map(p => ({
                        m: p.label || p.Label || "",
                        p: p.avg || p.Avg || ""
                    }));
                    console.log(`  %c✅ ${d.name}: ${cp.length} tháng (${cp[0]?.label} → ${cp[cp.length - 1]?.label})`, "color:#4caf50;font-weight:bold");
                } else {
                    state.data[d.name] = [{ m: "N/A", p: "N/A" }];
                    console.log(`  ⚠️ ${d.name}: Không có chartPoints`);
                }
            } catch (e) {
                state.data[d.name] = [{ m: "N/A", p: "N/A" }];
                console.warn(`  ❌ Lỗi parse:`, e);
            }

            // Save & go next
            state.idx++;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));

            if (state.idx >= DISTRICTS.length) {
                console.log("%c\n✅ XONG! Đang tải CSV...", "color:#4caf50;font-size:16px");
                setTimeout(() => {
                    downloadCSV(state.data);
                    localStorage.removeItem(STORAGE_KEY);
                }, 1000);
            } else {
                const next = DISTRICTS[state.idx];
                console.log(`  🔄 3s nữa chuyển sang ${next.name}...`);
                console.log(`  ⚡ CHẠY LẠI Snippet khi trang mới load (Ctrl+Enter trong Sources > Snippets)`);
                setTimeout(() => {
                    window.location.href = `https://batdongsan.com.vn/${next.slug}?vrs=1`;
                }, 3000);
            }
        }
        return resp;
    };

    // ===== STEP 2: Tìm và click "Xem lịch sử giá" =====
    console.log("  🔍 Đang tìm nút 'Xem lịch sử giá'...");

    setTimeout(() => {
        // Tìm tất cả link/button có text "Xem lịch sử giá" hoặc "lịch sử giá"
        const allEls = document.querySelectorAll("a, button, span, div, p");
        let priceBtn = null;

        for (const el of allEls) {
            const text = el.textContent?.trim() || "";
            if (text.includes("Xem lịch sử giá") || text === "Xem lịch sử giá") {
                // Ưu tiên element nhỏ nhất (most specific)
                if (!priceBtn || el.textContent.length < priceBtn.textContent.length) {
                    priceBtn = el;
                }
            }
        }

        if (!priceBtn) {
            // Thử scroll xuống trước
            console.log("  📜 Đang scroll tìm...");
            window.scrollTo(0, document.body.scrollHeight * 0.6);

            setTimeout(() => {
                for (const el of document.querySelectorAll("a, button, span, div, p")) {
                    const text = el.textContent?.trim() || "";
                    if (text.includes("Xem lịch sử giá")) {
                        if (!priceBtn || el.textContent.length < priceBtn.textContent.length) {
                            priceBtn = el;
                        }
                    }
                }

                if (priceBtn) {
                    clickPriceButton(priceBtn);
                } else {
                    console.warn(`  ⚠️ Không tìm thấy nút 'Xem lịch sử giá' cho ${d.name}`);
                    state.data[d.name] = [{ m: "N/A", p: "N/A" }];
                    state.idx++;
                    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
                    goNext();
                }
            }, 2000);
            return;
        }

        clickPriceButton(priceBtn);
    }, 2000);

    function clickPriceButton(btn) {
        console.log("  👆 Click 'Xem lịch sử giá'");
        btn.click();

        // Wait for modal/section to appear, then click "5 năm"
        setTimeout(() => {
            const allBtns = document.querySelectorAll("button, span, div, a, li");
            let fiveYearBtn = null;

            for (const el of allBtns) {
                const text = el.textContent?.trim() || "";
                if (text === "5 năm") {
                    fiveYearBtn = el;
                    break;
                }
            }

            if (fiveYearBtn) {
                console.log("  👆 Click '5 năm'");
                fiveYearBtn.click();
                console.log("  ⏳ Đợi API response...");
                // API call sẽ bị intercept bởi fetch override ở trên
                // Timeout nếu không có response sau 10s
                setTimeout(() => {
                    if (!captured) {
                        console.warn(`  ⚠️ Không nhận được API response cho ${d.name} sau 10s`);
                        state.data[d.name] = [{ m: "N/A", p: "N/A" }];
                        state.idx++;
                        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
                        goNext();
                    }
                }, 10000);
            } else {
                console.warn("  ⚠️ Không tìm thấy nút '5 năm'");
                // Thử click trực tiếp các tab khác
                console.log("  🔍 Đang tìm các tab thời gian...");
                for (const el of allBtns) {
                    const t = el.textContent?.trim();
                    if (t && (t.includes("năm") || t.includes("5"))) {
                        console.log(`    Tìm thấy: "${t}"`);
                    }
                }
                state.data[d.name] = [{ m: "N/A", p: "N/A" }];
                state.idx++;
                localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
                goNext();
            }
        }, 3000);
    }

    function goNext() {
        if (state.idx >= DISTRICTS.length) {
            downloadCSV(state.data);
            localStorage.removeItem(STORAGE_KEY);
            return;
        }
        const next = DISTRICTS[state.idx];
        console.log(`  🔄 Chuyển sang ${next.name}... Nhớ chạy lại Snippet!`);
        setTimeout(() => {
            window.location.href = `https://batdongsan.com.vn/${next.slug}?vrs=1`;
        }, 2000);
    }

    function downloadCSV(data) {
        let csv = "\uFEFFKhu_vuc,Thang,Gia_TB (tr/m2)\n";
        let total = 0, ok = 0, fail = 0;

        for (const [name, rows] of Object.entries(data)) {
            for (const r of rows) {
                csv += `${name},${r.m},${r.p}\n`;
                total++;
            }
            if (rows.length > 1 || rows[0].m !== "N/A") ok++; else fail++;
        }

        console.log(`\n${"=".repeat(50)}`);
        console.log(`%c📊 ${ok} thành công, ${fail} thất bại, ${total} dòng`, "color:#00bcd4;font-size:14px;font-weight:bold");

        const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = "gia_nha_rieng_22_quan_60thang.csv";
        document.body.appendChild(a); a.click();
        document.body.removeChild(a); URL.revokeObjectURL(url);

        console.log("%c📥 File CSV đã tải!", "color:#4caf50;font-size:14px");
        console.log("\n--- BACKUP ---\n" + csv);
    }
})();
