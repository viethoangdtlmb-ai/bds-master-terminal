/**
 * SCRIPT LẤY GIÁ NHÀ RIÊNG V3 - TỰ ĐỘNG NAVIGATE TỪNG QUẬN
 * ============================================================
 * CÁCH SỬ DỤNG:
 * 1. Mở Chrome → vào https://batdongsan.com.vn/ban-nha-rieng-ba-dinh?vrs=1
 * 2. Xác nhận Cloudflare nếu có
 * 3. Nhấn F12 → tab Console → paste script → Enter
 * 4. Script sẽ TỰ ĐỘNG chuyển trang qua từng quận
 * 5. Khi xong, file CSV sẽ tự tải về
 *
 * LƯU Ý: Script sẽ tự reload trang nhiều lần - ĐỪNG ĐÓNG TAB!
 */

(function () {
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

    const STORAGE_KEY = "NR_PRICE_COLLECTOR_V3";

    // Lấy trạng thái lưu từ localStorage
    let state = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");

    // ===== BƯỚC 0: Khởi tạo nếu chưa có state =====
    if (!state) {
        state = { currentIndex: 0, results: {}, status: "running" };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        console.log("%c🏠 BẮT ĐẦU THU THẬP GIÁ NHÀ RIÊNG - 22 KHU VỰC", "color: #00bcd4; font-size: 16px; font-weight: bold");
        console.log("Script sẽ tự động navigate qua từng quận. ĐỪNG ĐÓNG TAB!");
        console.log("=".repeat(55));
    }

    // ===== Kiểm tra nếu đã hoàn thành =====
    if (state.status === "done") {
        console.log("%c✅ ĐÃ HOÀN THÀNH! Đang xuất CSV...", "color: #4caf50; font-size: 14px");
        exportCSV(state.results);
        localStorage.removeItem(STORAGE_KEY);
        return;
    }

    // ===== BƯỚC 1: Trích xuất dữ liệu từ trang hiện tại =====
    const idx = state.currentIndex;

    if (idx >= DISTRICTS.length) {
        // Tất cả quận đã xong
        state.status = "done";
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        console.log("%c✅ ĐÃ THU THẬP XONG TẤT CẢ! Đang xuất CSV...", "color: #4caf50; font-size: 16px; font-weight: bold");
        exportCSV(state.results);
        localStorage.removeItem(STORAGE_KEY);
        return;
    }

    const district = DISTRICTS[idx];
    console.log(`%c[${idx + 1}/22] Đang xử lý: ${district.name}`, "color: #ff9800; font-weight: bold");

    // Kiểm tra đúng trang chưa
    const currentPath = window.location.pathname;
    const expectedPath = `/${district.slug}`;

    if (!currentPath.startsWith(expectedPath)) {
        // Chưa đúng trang → navigate
        console.log(`  🔄 Đang chuyển tới trang ${district.name}...`);
        window.location.href = `https://batdongsan.com.vn/${district.slug}?vrs=1`;
        return; // Script sẽ chạy lại sau khi trang load
    }

    // Đúng trang rồi → tìm encryptedParams từ __NEXT_DATA__ trong DOM
    console.log(`  📝 Đang tìm dữ liệu trên trang...`);

    const nextDataEl = document.getElementById("__NEXT_DATA__");
    let encryptedParams = null;

    if (nextDataEl) {
        try {
            const nextData = JSON.parse(nextDataEl.textContent);
            encryptedParams = deepFind(nextData, "encryptedParams") ||
                deepFind(nextData, "pricingEncryptedParams");
        } catch (e) {
            console.warn("  ⚠️ Không parse được __NEXT_DATA__");
        }
    }

    // Cũng thử tìm trong toàn bộ HTML nếu không có trong __NEXT_DATA__
    if (!encryptedParams) {
        const htmlStr = document.documentElement.innerHTML;
        const patterns = [
            /"encryptedParams"\s*:\s*"([0-9a-f]{20,})"/,
            /"pricingEncryptedParams"\s*:\s*"([0-9a-f]{20,})"/,
            /encryptedParams['"]\s*:\s*['"]([\da-f]{20,})['"]/
        ];
        for (const p of patterns) {
            const m = htmlStr.match(p);
            if (m) { encryptedParams = m[1]; break; }
        }
    }

    if (!encryptedParams) {
        console.warn(`  ⚠️ Không tìm thấy encryptedParams cho ${district.name} → N/A`);
        state.results[district.name] = [{ month: "N/A", price: "N/A" }];
        state.currentIndex++;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        // Chuyển trang tiếp
        goToNext(state, DISTRICTS);
        return;
    }

    console.log(`  🔑 Tìm thấy encryptedParams: ${encryptedParams.substring(0, 25)}...`);

    // ===== BƯỚC 2: Gọi API lấy giá 5 năm =====
    callPricingAPI(encryptedParams, district.name, state, DISTRICTS);

    // ===== HÀM PHỤ TRỢ =====
    function deepFind(obj, key, depth) {
        if (!obj || typeof obj !== "object" || (depth || 0) > 15) return null;
        if (obj[key] && typeof obj[key] === "string" && obj[key].length > 15) return obj[key];
        for (const k of Object.keys(obj)) {
            const r = deepFind(obj[k], key, (depth || 0) + 1);
            if (r) return r;
        }
        return null;
    }

    async function callPricingAPI(ep, districtName, st, dists) {
        const API = "/Origins/CommonData/GetPricingHistory";
        let chartPoints = null;

        for (const pt of [1, 2, 4, 38]) {
            try {
                const resp = await fetch(API, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    credentials: "include",
                    body: JSON.stringify({ encryptedParams: ep, productType: pt, countOfYears: 5 })
                });
                if (resp.ok) {
                    const data = await resp.json();
                    const cp = data?.chartPoints || data?.data?.chartPoints;
                    if (cp && cp.length > 5) {
                        chartPoints = cp;
                        console.log(`  📊 productType=${pt} → ${cp.length} tháng`);
                        break;
                    }
                }
            } catch (e) { }
        }

        if (chartPoints && chartPoints.length > 0) {
            const rows = chartPoints.map(p => ({
                month: p.label || p.Label || "",
                price: p.avg || p.Avg || ""
            }));
            st.results[districtName] = rows;
            const first = rows[0]?.month || "";
            const last = rows[rows.length - 1]?.month || "";
            console.log(`  %c✅ ${districtName}: ${rows.length} tháng (${first} → ${last})`, "color: #4caf50; font-weight: bold");
        } else {
            console.warn(`  ❌ Không có dữ liệu giá cho ${districtName}`);
            st.results[districtName] = [{ month: "N/A", price: "N/A" }];
        }

        st.currentIndex++;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(st));
        // Delay 2s rồi chuyển trang
        setTimeout(() => goToNext(st, dists), 2000);
    }

    function goToNext(st, dists) {
        if (st.currentIndex >= dists.length) {
            st.status = "done";
            localStorage.setItem(STORAGE_KEY, JSON.stringify(st));
            exportCSV(st.results);
            localStorage.removeItem(STORAGE_KEY);
            return;
        }
        const next = dists[st.currentIndex];
        console.log(`  🔄 Chuyển tới ${next.name}...`);
        window.location.href = `https://batdongsan.com.vn/${next.slug}?vrs=1`;
    }

    function exportCSV(results) {
        let csv = "\uFEFFKhu_vuc,Thang,Gia_TB (tr/m2)\n";
        let totalRows = 0;
        let success = 0;
        let fail = 0;

        for (const [district, rows] of Object.entries(results)) {
            for (const r of rows) {
                csv += `${district},${r.month},${r.price}\n`;
                totalRows++;
            }
            if (rows.length > 1 || rows[0]?.month !== "N/A") success++;
            else fail++;
        }

        console.log("\n" + "=".repeat(55));
        console.log(`%c📊 KẾT QUẢ: ${success} thành công, ${fail} thất bại, ${totalRows} dòng`, "color: #00bcd4; font-size: 14px; font-weight: bold");

        // Download
        const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "gia_nha_rieng_22_quan_60thang.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        console.log("%c📥 File CSV đã tải: gia_nha_rieng_22_quan_60thang.csv", "color: #4caf50; font-size: 14px");
        console.log("\n--- BACKUP CSV ---");
        console.log(csv);
    }
})();

/**
 * QUAN TRỌNG: Script này dùng localStorage để lưu tiến trình.
 * Khi trang redirect sang quận mới, bạn phải PASTE LẠI script vào Console.
 * 
 * CÁCH ĐƠN GIẢN HƠN: Dùng Snippets trong Chrome DevTools:
 * 1. F12 → tab Sources → Snippets (bên trái)
 * 2. New snippet → paste code → Ctrl+Enter để chạy
 * 3. Mỗi khi trang load mới, click phải snippet → Run lại
 *
 * HOẶC: Dùng Tampermonkey extension để tự chạy trên mỗi trang batdongsan
 */
