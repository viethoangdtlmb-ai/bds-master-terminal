/**
 * script_lay_gia_nha_rieng_auto.js
 * ==================================
 * Crawl giá NHÀ RIÊNG (tr/m²) lịch sử 60 tháng cho 22 quận Hà Nội.
 * Chạy tự động trong Console Chrome (giống script_lay_gia_thue_cc.js).
 *
 * Hướng dẫn:
 * 1. Mở Chrome → vào batdongsan.com.vn (đợi trang load, bypass Cloudflare)
 * 2. F12 → Console → Paste toàn bộ script → Enter
 * 3. Chờ ~5-7 phút, script tự lặp qua 22 quận
 * 4. File CSV (gia_nha_rieng_ha_noi_60thang.csv) tự động download
 */

(async () => {
    const DISTRICTS = {
        "Ba Dinh": "ba-dinh",
        "Bac Tu Liem": "bac-tu-liem",
        "Cau Giay": "cau-giay",
        "Dan Phuong": "dan-phuong",
        "Dong Anh": "dong-anh",
        "Dong Da": "dong-da",
        "Gia Lam": "gia-lam",
        "Ha Dong": "ha-dong",
        "Hai Ba Trung": "hai-ba-trung",
        "Hoai Duc": "hoai-duc",
        "Hoan Kiem": "hoan-kiem",
        "Hoang Mai": "hoang-mai",
        "Long Bien": "long-bien",
        "Nam Tu Liem": "nam-tu-liem",
        "Tay Ho": "tay-ho",
        "Thanh Tri": "thanh-tri",
        "Thanh Xuan": "thanh-xuan",
        "Van Giang (HY)": "van-giang",
        "Soc Son": "soc-son",
        "Me Linh": "me-linh",
        "Thach That": "thach-that",
        "Tu Son (BN)": "tu-son-bn",
    };

    const BASE_URL = "https://batdongsan.com.vn/ban-nha-rieng-";
    const delay = ms => new Promise(r => setTimeout(r, ms));

    // Lưu dữ liệu: { "Ba Dinh": [{ thang: "2021-03", gia: 56.7 }, ...], ... }
    const allData = {};
    const allMonths = new Set();
    let successCount = 0;

    console.log("🏠 BẮT ĐẦU CRAWL GIÁ NHÀ RIÊNG — 22 QUẬN HÀ NỘI — 60 THÁNG");
    console.log("=".repeat(65));

    for (const [name, slug] of Object.entries(DISTRICTS)) {
        const url = `${BASE_URL}${slug}`;
        console.log(`\n📍 [${Object.keys(DISTRICTS).indexOf(name) + 1}/${Object.keys(DISTRICTS).length}] ${name} → ${url}`);

        try {
            const resp = await fetch(url, {
                credentials: "include",
                headers: {
                    "Accept": "text/html,application/xhtml+xml",
                    "User-Agent": navigator.userAgent,
                }
            });
            const html = await resp.text();

            // Kiểm tra Cloudflare block
            if (html.includes("Just a moment") || html.length < 50000) {
                if (html.includes("Just a moment")) {
                    console.log(`  ⛔ Bị Cloudflare chặn! Dừng script.`);
                    console.log(`  💡 Hãy reload trang batdongsan.com.vn, vượt Cloudflare, rồi chạy lại script.`);
                    break;
                }
            }

            // Extract giá từ chart data: {"month":"2021-03","value":56.7}
            const chartPattern = /\{"month"\s*:\s*"([2]\d{3}-\d{2})"\s*,\s*"value"\s*:\s*([\d.]+)\}/g;
            const prices = [];
            let match;
            while ((match = chartPattern.exec(html)) !== null) {
                const monthKey = match[1]; // "2021-03"
                const value = parseFloat(match[2]);
                prices.push({ thang: monthKey, gia: value });
                allMonths.add(monthKey);
            }

            // Deduplicate by month (keep last occurrence)
            const uniquePrices = {};
            for (const p of prices) {
                uniquePrices[p.thang] = p.gia;
            }

            const sortedPrices = Object.entries(uniquePrices)
                .sort(([a], [b]) => a.localeCompare(b))
                .map(([thang, gia]) => ({ thang, gia }));

            allData[name] = sortedPrices;

            if (sortedPrices.length > 0) {
                const first = sortedPrices[0];
                const last = sortedPrices[sortedPrices.length - 1];
                console.log(`  ✅ ${sortedPrices.length} data points | ${first.thang} (${first.gia}) → ${last.thang} (${last.gia})`);
                successCount++;
            } else {
                console.log(`  ⚠️ Không tìm thấy chart data (HTML = ${(html.length / 1024).toFixed(0)}KB)`);
            }

        } catch (e) {
            console.log(`  ❌ Lỗi: ${e.message}`);
            allData[name] = [];
        }

        // Delay ngẫu nhiên 5-10s (dài hơn để tránh chặn)
        const waitMs = 5000 + Math.random() * 5000;
        console.log(`  ⏳ Chờ ${(waitMs / 1000).toFixed(1)}s...`);
        await delay(waitMs);
    }

    // ============================================================
    // EXPORT CSV — Format giống gia_chung_cu_ha_noi_22_quan_60thang.csv
    // ============================================================

    if (successCount === 0) {
        console.log("\n❌ Không có dữ liệu nào được crawl. Kiểm tra Cloudflare.");
        return;
    }

    // Chuyển month key "2021-03" → "T3/21"
    function formatMonth(monthKey) {
        const [y, m] = monthKey.split("-");
        return `T${parseInt(m)}/${y.slice(2)}`;
    }

    // Sort months
    const sortedMonths = Array.from(allMonths).sort();

    // CSV format: Khu_vuc,Thang,Gia_TB (tr/m2)
    let csv = "Khu_vuc,Thang,Gia_TB (tr/m2)\n";
    for (const [name, prices] of Object.entries(allData)) {
        if (prices.length === 0) {
            csv += `${name},T3/21,N/A\n`;
            csv += `${name},T3/26,N/A\n`;
        } else {
            for (const p of prices) {
                csv += `${name},${formatMonth(p.thang)},${p.gia}\n`;
            }
        }
    }

    // Auto-download CSV
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "gia_nha_rieng_ha_noi_22_quan_60thang.csv";
    link.click();

    // Console summary
    console.log("\n" + "=".repeat(65));
    console.log("📊 KẾT QUẢ CRAWL GIÁ NHÀ RIÊNG HÀ NỘI");
    console.log("=".repeat(65));
    console.log(`✅ Thành công: ${successCount}/${Object.keys(DISTRICTS).length} quận`);
    console.log(`📅 Phạm vi: ${sortedMonths[0]} → ${sortedMonths[sortedMonths.length - 1]}`);

    // Bảng tóm tắt giá hiện tại
    const summary = [];
    for (const [name, prices] of Object.entries(allData)) {
        if (prices.length > 0) {
            const last = prices[prices.length - 1];
            const first = prices[0];
            const growth = (((last.gia - first.gia) / first.gia) * 100).toFixed(1);
            summary.push({
                "Quận": name,
                "Giá đầu": first.gia,
                "Giá cuối": last.gia,
                "Tăng 5Y (%)": growth + "%",
                "Số tháng": prices.length,
            });
        }
    }
    console.table(summary);
    console.log("✅ File CSV đã tự động download: gia_nha_rieng_ha_noi_22_quan_60thang.csv");
})();
