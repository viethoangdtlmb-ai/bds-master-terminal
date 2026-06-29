/**
 * SCRIPT LẤY GIÁ NHÀ RIÊNG 22 QUẬN HUYỆN - 60 THÁNG
 * =====================================================
 * CÁCH SỬ DỤNG:
 * 1. Mở Chrome, vào https://batdongsan.com.vn/ban-nha-rieng-ba-dinh
 * 2. Đăng nhập nếu cần (xác nhận Cloudflare nếu có)
 * 3. Nhấn F12 → chọn tab Console
 * 4. Copy toàn bộ code này, paste vào Console, nhấn Enter
 * 5. Chờ script chạy xong (~3-5 phút), kết quả sẽ tự download file CSV
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

    const API_URL = "/Origins/CommonData/GetPricingHistory";
    let allData = [];
    let successCount = 0;
    let failCount = 0;

    console.log("🏠 BẮT ĐẦU THU THẬP GIÁ NHÀ RIÊNG - 22 KHU VỰC");
    console.log("=".repeat(50));

    for (let i = 0; i < DISTRICTS.length; i++) {
        const d = DISTRICTS[i];
        console.log(`\n[${i + 1}/22] Đang lấy: ${d.name}...`);

        try {
            // Bước 1: Mở trang nhà riêng để lấy encryptedParams
            const pageUrl = `https://batdongsan.com.vn/ban-nha-rieng-${d.slug}?vrs=1`;
            const pageResp = await fetch(pageUrl);
            const html = await pageResp.text();

            // Bước 2: Tìm encryptedParams trong HTML source
            // Trang web nhúng dữ liệu này trong script __NEXT_DATA__ hoặc thuộc tính data-*
            let encryptedParams = null;

            // Phương pháp 1: Tìm trong __NEXT_DATA__
            const nextDataMatch = html.match(/__NEXT_DATA__.*?({.*?})\s*<\/script>/s);
            if (nextDataMatch) {
                try {
                    const nextData = JSON.parse(nextDataMatch[1]);
                    // Tìm encryptedParams trong cấu trúc __NEXT_DATA__
                    const findEncrypted = (obj) => {
                        if (!obj || typeof obj !== 'object') return null;
                        if (obj.encryptedParams) return obj.encryptedParams;
                        if (obj.pricingEncryptedParams) return obj.pricingEncryptedParams;
                        for (const key of Object.keys(obj)) {
                            const result = findEncrypted(obj[key]);
                            if (result) return result;
                        }
                        return null;
                    };
                    encryptedParams = findEncrypted(nextData);
                } catch (e) { }
            }

            // Phương pháp 2: Tìm trực tiếp bằng regex
            if (!encryptedParams) {
                const epMatch = html.match(/"encryptedParams"\s*:\s*"([a-f0-9]+)"/);
                if (epMatch) encryptedParams = epMatch[1];
            }

            // Phương pháp 3: Tìm pricingEncryptedParams
            if (!encryptedParams) {
                const pMatch = html.match(/"pricingEncryptedParams"\s*:\s*"([a-f0-9]+)"/);
                if (pMatch) encryptedParams = pMatch[1];
            }

            if (!encryptedParams) {
                console.warn(`  ⚠️ Không tìm thấy encryptedParams cho ${d.name} - có thể không có dữ liệu`);
                allData.push({ district: d.name, month: "N/A", price: "N/A" });
                failCount++;
                continue;
            }

            // Bước 3: Gọi API lấy lịch sử giá 5 năm
            // productType: 1 = Nhà riêng, 38 = Chung cư
            const apiResp = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    encryptedParams: encryptedParams,
                    productType: 1,
                    countOfYears: 5
                })
            });

            if (!apiResp.ok) {
                // Thử productType khác
                const apiResp2 = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        encryptedParams: encryptedParams,
                        productType: 2,
                        countOfYears: 5
                    })
                });
                if (!apiResp2.ok) {
                    console.warn(`  ❌ API trả lỗi cho ${d.name}: ${apiResp.status}`);
                    allData.push({ district: d.name, month: "N/A", price: "N/A" });
                    failCount++;
                    continue;
                }
                var data = await apiResp2.json();
            } else {
                var data = await apiResp.json();
            }

            // Bước 4: Trích xuất chartPoints
            let chartPoints = null;
            if (data && data.chartPoints) chartPoints = data.chartPoints;
            else if (data && data.data && data.data.chartPoints) chartPoints = data.data.chartPoints;
            else if (Array.isArray(data)) chartPoints = data;

            if (!chartPoints || chartPoints.length === 0) {
                console.warn(`  ⚠️ Không có chartPoints cho ${d.name}`);
                allData.push({ district: d.name, month: "N/A", price: "N/A" });
                failCount++;
                continue;
            }

            // Bước 5: Lưu tất cả các tháng
            for (const p of chartPoints) {
                allData.push({
                    district: d.name,
                    month: p.label || p.Label || "",
                    price: p.avg || p.Avg || p.price || ""
                });
            }
            console.log(`  ✅ ${d.name}: ${chartPoints.length} tháng (${chartPoints[0]?.label || ''} → ${chartPoints[chartPoints.length - 1]?.label || ''})`);
            successCount++;

            // Delay 1.5s giữa các request
            await new Promise(r => setTimeout(r, 1500));

        } catch (err) {
            console.error(`  ❌ Lỗi ${d.name}:`, err.message);
            allData.push({ district: d.name, month: "N/A", price: "N/A" });
            failCount++;
        }
    }

    // Bước 6: Xuất CSV
    console.log("\n" + "=".repeat(50));
    console.log(`✅ HOÀN THÀNH: ${successCount} thành công, ${failCount} thất bại`);
    console.log(`📊 Tổng dòng dữ liệu: ${allData.length}`);

    let csv = "Khu_vuc,Thang,Gia_TB (tr/m2)\n";
    for (const row of allData) {
        csv += `${row.district},${row.month},${row.price}\n`;
    }

    // Auto download file CSV
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "gia_nha_rieng_22_quan_60thang.csv";
    a.click();
    URL.revokeObjectURL(url);

    console.log("📥 File CSV đã tự động tải xuống: gia_nha_rieng_22_quan_60thang.csv");
    console.log("\n💡 Sau khi download, copy file vào thư mục:");
    console.log("   d:\\1. BDS\\AI-Assistant\\App_kham_benh_tai_san\\");

    // Cũng log dữ liệu vào console để backup
    console.log("\n📋 DỮ LIỆU THÔ (backup):");
    console.log(csv);

    return allData;
})();
