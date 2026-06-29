/**
 * SCRIPT LẤY GIÁ NHÀ RIÊNG V2 - PHƯƠNG PHÁP INTERCEPT XHR
 * ===========================================================
 * CÁCH SỬ DỤNG:
 * 1. Mở Chrome → vào https://batdongsan.com.vn/ban-nha-rieng-ba-dinh?vrs=1
 * 2. Xác nhận Cloudflare nếu có, đăng nhập nếu cần
 * 3. Nhấn F12 → tab Console
 * 4. Copy TOÀN BỘ code này → paste vào Console → Enter
 * 5. Chờ ~5-8 phút, file CSV sẽ tự tải về
 *
 * NGUYÊN LÝ: Script mở từng trang quận trong iframe ẩn,
 * đợi trang load xong, tìm encryptedParams trong HTML,
 * gọi API GetPricingHistory trực tiếp.
 */

(async function () {
    const DISTRICTS = [
        { name: "Ba Dinh", slug: "ba-dinh" },
        { name: "Bac Tu Liem", slug: "bac-tu-liem" },
        { name: "Cau Giay", slug: "cau-giay" },
        { name: "Dan Phuong", slug: "dan-phuong" },
        { name: "Dong Anh", slug: "dong-anh" },
        { name: "Dong Da", slug: "dong-da" },
        { name: "Gia Lam", slug: "gia-lam" },
        { name: "Ha Dong", slug: "ha-dong" },
        { name: "Hai Ba Trung", slug: "hai-ba-trung" },
        { name: "Hoai Duc", slug: "hoai-duc" },
        { name: "Hoan Kiem", slug: "hoan-kiem" },
        { name: "Hoang Mai", slug: "hoang-mai" },
        { name: "Long Bien", slug: "long-bien" },
        { name: "Me Linh", slug: "me-linh" },
        { name: "Nam Tu Liem", slug: "nam-tu-liem" },
        { name: "Soc Son", slug: "soc-son" },
        { name: "Tay Ho", slug: "tay-ho" },
        { name: "Thach That", slug: "thach-that" },
        { name: "Thanh Tri", slug: "thanh-tri" },
        { name: "Thanh Xuan", slug: "thanh-xuan" },
        { name: "Van Giang (HY)", slug: "van-giang" },
        { name: "Tu Son (BN)", slug: "tu-son-bn" }
    ];

    const API_URL = "https://batdongsan.com.vn/Origins/CommonData/GetPricingHistory";
    let allData = [];
    let successCount = 0;
    let failCount = 0;

    console.log("%c🏠 BẮT ĐẦU THU THẬP GIÁ NHÀ RIÊNG - 22 KHU VỰC", "color: #00bcd4; font-size: 16px; font-weight: bold");
    console.log("=".repeat(55));

    // Hàm lấy HTML của trang
    async function getPageHtml(url) {
        try {
            const resp = await fetch(url, { credentials: 'include' });
            if (!resp.ok) return null;
            return await resp.text();
        } catch (e) {
            return null;
        }
    }

    // Hàm tìm encryptedParams từ HTML
    function findEncryptedParams(html) {
        if (!html) return null;

        // Cách 1: Tìm trong script __NEXT_DATA__
        const nextMatch = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
        if (nextMatch) {
            try {
                const nd = JSON.parse(nextMatch[1]);
                // Tìm đệ quy
                const find = (obj, depth) => {
                    if (!obj || typeof obj !== 'object' || depth > 10) return null;
                    // Ưu tiên tìm key chứa "encrypt" hoặc "pricing"
                    for (const k of Object.keys(obj)) {
                        if ((k === 'encryptedParams' || k === 'pricingEncryptedParams') && typeof obj[k] === 'string' && obj[k].length > 20) {
                            return obj[k];
                        }
                    }
                    for (const k of Object.keys(obj)) {
                        const r = find(obj[k], depth + 1);
                        if (r) return r;
                    }
                    return null;
                };
                const ep = find(nd, 0);
                if (ep) return ep;
            } catch (e) { }
        }

        // Cách 2: Regex trực tiếp trên toàn bộ HTML
        const patterns = [
            /"encryptedParams"\s*:\s*"([0-9a-f]{40,})"/,
            /"pricingEncryptedParams"\s*:\s*"([0-9a-f]{40,})"/,
            /encryptedParams['"]\s*:\s*['"]([\da-f]{40,})['"]/,
            /\\?"encryptedParams\\?"\s*:\s*\\?"([0-9a-f]{40,})\\?"/
        ];

        for (const p of patterns) {
            const m = html.match(p);
            if (m) return m[1];
        }
        return null;
    }

    for (let i = 0; i < DISTRICTS.length; i++) {
        const d = DISTRICTS[i];
        console.log(`%c[${i + 1}/22] Đang lấy: ${d.name}...`, "color: #ff9800");

        try {
            // Lấy HTML trang nhà riêng
            const url = `https://batdongsan.com.vn/ban-nha-rieng-${d.slug}?vrs=1`;
            const html = await getPageHtml(url);

            if (!html) {
                console.warn(`  ⚠️ Không tải được trang ${d.name}`);
                allData.push({ district: d.name, month: "N/A", price: "N/A" });
                failCount++;
                continue;
            }

            // Debug: log phần HTML chứa encrypt
            if (html.includes('encryptedParams') || html.includes('encrypted')) {
                console.log(`  📝 Tìm thấy "encrypted" trong HTML`);
            }

            const encryptedParams = findEncryptedParams(html);

            if (!encryptedParams) {
                console.warn(`  ⚠️ Không tìm thấy encryptedParams cho ${d.name}`);
                // Thử tìm bằng cách khác - debug HTML
                const idx = html.indexOf('encrypt');
                if (idx > -1) {
                    console.log(`  🔍 Vị trí "encrypt": ...${html.substring(Math.max(0, idx - 30), idx + 100)}...`);
                }
                allData.push({ district: d.name, month: "N/A", price: "N/A" });
                failCount++;
                continue;
            }

            console.log(`  🔑 encryptedParams: ${encryptedParams.substring(0, 30)}...`);

            // Gọi API - thử nhiều productType
            let chartPoints = null;

            for (const pt of [1, 2, 38, 4]) {
                try {
                    const apiResp = await fetch(API_URL, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            encryptedParams: encryptedParams,
                            productType: pt,
                            countOfYears: 5
                        })
                    });

                    if (apiResp.ok) {
                        const data = await apiResp.json();
                        const cp = data?.chartPoints || data?.data?.chartPoints;
                        if (cp && cp.length > 0) {
                            chartPoints = cp;
                            console.log(`  📊 productType=${pt} → ${cp.length} tháng`);
                            break;
                        }
                    }
                } catch (e) { }
            }

            if (!chartPoints || chartPoints.length === 0) {
                console.warn(`  ❌ Không có dữ liệu giá cho ${d.name}`);
                allData.push({ district: d.name, month: "N/A", price: "N/A" });
                failCount++;
                continue;
            }

            // Lưu tất cả tháng
            for (const p of chartPoints) {
                allData.push({
                    district: d.name,
                    month: p.label || p.Label || "",
                    price: p.avg || p.Avg || p.price || ""
                });
            }

            const first = chartPoints[0]?.label || "";
            const last = chartPoints[chartPoints.length - 1]?.label || "";
            console.log(`  %c✅ ${d.name}: ${chartPoints.length} tháng (${first} → ${last})`, "color: #4caf50; font-weight: bold");
            successCount++;

            // Delay 2s giữa các request
            await new Promise(r => setTimeout(r, 2000));

        } catch (err) {
            console.error(`  ❌ Lỗi ${d.name}:`, err.message);
            allData.push({ district: d.name, month: "N/A", price: "N/A" });
            failCount++;
        }
    }

    // KẾT QUẢ
    console.log("\n" + "=".repeat(55));
    console.log(`%c📊 KẾT QUẢ: ${successCount} thành công, ${failCount} thất bại`, "color: #00bcd4; font-size: 14px; font-weight: bold");
    console.log(`📋 Tổng dòng dữ liệu: ${allData.length}`);

    // Tạo CSV
    let csv = "\uFEFFKhu_vuc,Thang,Gia_TB (tr/m2)\n";
    for (const row of allData) {
        csv += `${row.district},${row.month},${row.price}\n`;
    }

    // Download CSV
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
    console.log("💡 Copy file vào: d:\\1. BDS\\AI-Assistant\\App_kham_benh_tai_san\\");

    // Log raw CSV thẳng để copy nếu download không hoạt động
    console.log("\n--- RAW CSV (Backup - copy nếu download lỗi) ---");
    console.log(csv);

    return { success: successCount, fail: failCount, total: allData.length };
})();
