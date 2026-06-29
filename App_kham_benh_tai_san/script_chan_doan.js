/**
 * SCRIPT CHẨN ĐOÁN - Chạy trên trang nhà riêng bất kỳ
 * =====================================================
 * Mục đích: Tìm encryptedParams trên trang hiện tại
 * 
 * 1. Mở Chrome → vào https://batdongsan.com.vn/ban-nha-rieng-ba-dinh?vrs=1
 * 2. ĐỢI TRANG LOAD XONG (thấy danh sách nhà, không phải Cloudflare)
 * 3. F12 → Console → paste code → Enter
 */

// Bước 1: Kiểm tra __NEXT_DATA__
console.log("=== CHẨN ĐOÁN TRANG ===");
const nd = document.getElementById("__NEXT_DATA__");
if (nd) {
    console.log("✅ Tìm thấy __NEXT_DATA__");
    const data = JSON.parse(nd.textContent);

    // Tìm tất cả key chứa "encrypt" hoặc "pricing"
    function findAllKeys(obj, path, results, depth) {
        if (!obj || typeof obj !== "object" || depth > 12) return;
        for (const k of Object.keys(obj)) {
            const fullPath = path ? `${path}.${k}` : k;
            if (k.toLowerCase().includes("encrypt") || k.toLowerCase().includes("pricing")) {
                results.push({ path: fullPath, value: obj[k] });
            }
            findAllKeys(obj[k], fullPath, results, depth + 1);
        }
    }

    const results = [];
    findAllKeys(data, "", results, 0);

    if (results.length > 0) {
        console.log(`✅ Tìm thấy ${results.length} key liên quan:`);
        results.forEach(r => console.log(`  ${r.path} = ${JSON.stringify(r.value).substring(0, 80)}`));
    } else {
        console.log("❌ Không tìm thấy key encrypt/pricing trong __NEXT_DATA__");
        console.log("📝 Các top-level keys:", Object.keys(data));
        if (data.props) console.log("📝 props keys:", Object.keys(data.props));
        if (data.props?.pageProps) console.log("📝 pageProps keys:", Object.keys(data.props.pageProps));
    }
} else {
    console.log("❌ Không có __NEXT_DATA__ trong DOM");
}

// Bước 2: Tìm trong toàn bộ HTML
console.log("\n=== TÌM TRONG HTML ===");
const html = document.documentElement.innerHTML;
const idx1 = html.indexOf("encryptedParams");
const idx2 = html.indexOf("pricingEncrypted");
const idx3 = html.indexOf("GetPricingHistory");
const idx4 = html.indexOf("countOfYears");

console.log("encryptedParams tại:", idx1 > -1 ? `vị trí ${idx1}` : "KHÔNG TÌM THẤY");
console.log("pricingEncrypted tại:", idx2 > -1 ? `vị trí ${idx2}` : "KHÔNG TÌM THẤY");
console.log("GetPricingHistory tại:", idx3 > -1 ? `vị trí ${idx3}` : "KHÔNG TÌM THẤY");
console.log("countOfYears tại:", idx4 > -1 ? `vị trí ${idx4}` : "KHÔNG TÌM THẤY");

if (idx1 > -1) {
    console.log("📝 Context:", html.substring(Math.max(0, idx1 - 50), idx1 + 150));
}
if (idx2 > -1) {
    console.log("📝 Context:", html.substring(Math.max(0, idx2 - 50), idx2 + 150));
}

// Bước 3: Tìm trong window/global
console.log("\n=== TÌM TRONG WINDOW ===");
if (window.__NEXT_DATA__) {
    console.log("✅ window.__NEXT_DATA__ tồn tại");
    const wr = [];
    findAllKeys(window.__NEXT_DATA__, "", wr, 0);
    wr.forEach(r => console.log(`  ${r.path} = ${JSON.stringify(r.value).substring(0, 80)}`));
}

// Kiểm tra React fiber
console.log("\n=== GỢI Ý ===");
console.log("Nếu không tìm thấy encryptedParams, hãy thử:");
console.log("1. Scroll xuống phần 'Biểu đồ giá' và click 'Xem lịch sử giá'");
console.log("2. Sau đó chạy lại script này để xem dữ liệu mới");
console.log("3. Hoặc mở tab Network (F12), click '5 năm', tìm request GetPricingHistory");
