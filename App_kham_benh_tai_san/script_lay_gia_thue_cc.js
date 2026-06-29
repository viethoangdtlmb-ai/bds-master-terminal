/**
 * script_lay_gia_thue_cc.js
 * ===========================
 * Chạy trực tiếp trong Console trình duyệt Chrome (F12 > Console).
 * 
 * Hướng dẫn:
 * 1. Mở Chrome, đăng nhập batdongsan.com.vn (để bypass Cloudflare)
 * 2. Vào bất kỳ trang nào trên batdongsan.com.vn
 * 3. Nhấn F12 > Console > Paste toàn bộ script này > Enter
 * 4. Chờ ~3-5 phút, script sẽ tự lặp qua 18 quận
 * 5. Kết quả CSV sẽ tự động download về máy
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
    };

    // Giá bán T3/2026 (tr/m²) từ CSV gốc
    const GIA_BAN = {
        "Ba Dinh": 179.6, "Bac Tu Liem": 105.8, "Cau Giay": 110.5,
        "Dan Phuong": 67.8, "Dong Anh": 121.2, "Dong Da": 117.1,
        "Gia Lam": 73.8, "Ha Dong": 77.1, "Hai Ba Trung": 112.2,
        "Hoai Duc": 80.0, "Hoan Kiem": 473.1, "Hoang Mai": 87.3,
        "Long Bien": 89.2, "Nam Tu Liem": 95.7, "Tay Ho": 149.8,
        "Thanh Tri": 74.8, "Thanh Xuan": 108.6, "Van Giang (HY)": 72.2,
    };

    const delay = ms => new Promise(r => setTimeout(r, ms));
    const results = [];

    console.log("🚀 BẮT ĐẦU CRAWL GIÁ THUÊ CHUNG CƯ — 18 QUẬN HÀ NỘI");
    console.log("=".repeat(60));

    for (const [name, slug] of Object.entries(DISTRICTS)) {
        const url = `https://batdongsan.com.vn/cho-thue-can-ho-chung-cu-${slug}`;
        console.log(`\n📍 ${name} → ${url}`);

        try {
            const resp = await fetch(url, {
                credentials: "include",
                headers: {
                    "Accept": "text/html,application/xhtml+xml",
                    "User-Agent": navigator.userAgent,
                }
            });
            const html = await resp.text();

            // --- Extract giá thuê ---
            let giaThue = null;
            let soTin = null;
            let note = "";

            // Cách 1: Chart data từ __NEXT_DATA__
            const chartPattern = /\{"month"\s*:\s*"([2]\d{3}-\d{2})"\s*,\s*"value"\s*:\s*([\d.]+)\}/g;
            const chartData = [];
            let match;
            while ((match = chartPattern.exec(html)) !== null) {
                chartData.push({ month: match[1], value: parseFloat(match[2]) });
            }

            if (chartData.length > 0) {
                chartData.sort((a, b) => b.month.localeCompare(a.month));
                const recent3 = chartData.slice(0, 3);
                giaThue = recent3.reduce((s, d) => s + d.value, 0) / recent3.length;
                note = `Chart data (${chartData.length} pts, TB 3T gần nhất)`;
            }

            // Cách 2: Giá tổng từ listings / 70m² (fallback)
            if (!giaThue) {
                const pricePattern = /([\d.,]+)\s*(?:triệu|tr)\s*\/\s*th/gi;
                const totalPrices = [];
                while ((match = pricePattern.exec(html)) !== null) {
                    const val = parseFloat(match[1].replace(",", "."));
                    if (val > 3 && val < 100) totalPrices.push(val);
                }
                if (totalPrices.length > 0) {
                    const avgTotal = totalPrices.reduce((s, v) => s + v, 0) / totalPrices.length;
                    giaThue = avgTotal / 70; // Ước tính diện tích TB 70m²
                    soTin = totalPrices.length;
                    note = `Total price / 70m² (${totalPrices.length} mẫu)`;
                }
            }

            // Cách 3: Đếm tin đăng
            if (!soTin) {
                const tinMatch = html.match(/Hiện có\s*([\d.]+)\s*bất/);
                if (tinMatch) soTin = parseInt(tinMatch[1].replace(".", ""));
            }

            // Tính Yield
            const giaBan = GIA_BAN[name] || 0;
            let yieldPct = null;
            if (giaThue && giaBan > 0) {
                yieldPct = ((giaThue * 12) / giaBan * 100).toFixed(2);
            }

            if (giaThue) {
                console.log(`  ✅ Giá thuê: ${giaThue.toFixed(3)} tr/m²/tháng | Yield: ${yieldPct}% | ${note}`);
            } else {
                note = "Không tìm thấy dữ liệu giá thuê";
                console.log(`  ⚠️ ${note}`);
            }

            results.push({
                name, giaBan,
                giaThue: giaThue ? giaThue.toFixed(3) : "N/A",
                yieldPct: yieldPct || "N/A",
                soTin: soTin || "N/A",
                note
            });

        } catch (e) {
            console.log(`  ❌ Lỗi: ${e.message}`);
            results.push({
                name, giaBan: GIA_BAN[name] || 0,
                giaThue: "N/A", yieldPct: "N/A",
                soTin: "N/A", note: `Error: ${e.message}`
            });
        }

        // Delay ngẫu nhiên 3-6s
        const waitMs = 3000 + Math.random() * 3000;
        console.log(`  ⏳ Chờ ${(waitMs / 1000).toFixed(1)}s...`);
        await delay(waitMs);
    }

    // ============================================================
    // EXPORT CSV
    // ============================================================

    let csv = "Quận/Huyện,Giá Bán (tr/m²),Giá Thuê (tr/m²/tháng),Rental Yield (%),Số Tin Thuê,Ghi Chú\n";
    for (const r of results) {
        csv += `${r.name},${r.giaBan},${r.giaThue},${r.yieldPct},${r.soTin},"${r.note}"\n`;
    }

    // Auto-download CSV
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "rental_yield_ha_noi.csv";
    link.click();

    // Console summary
    console.log("\n" + "=".repeat(60));
    console.log("📊 BẢNG RENTAL YIELD — CHUNG CƯ HÀ NỘI T4/2026");
    console.log("=".repeat(60));
    console.table(results.map(r => ({
        "Quận": r.name,
        "Giá Bán": r.giaBan,
        "Giá Thuê": r.giaThue,
        "Yield (%)": r.yieldPct,
        "Ghi Chú": r.note,
    })));
    console.log("✅ File CSV đã tự động download!");
})();
