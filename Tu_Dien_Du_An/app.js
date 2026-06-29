// Khởi tạo Bản đồ Leaflet
let map;
let markers = [];
let planningLayer;
let isPlanningVisible = false;

document.addEventListener('DOMContentLoaded', () => {
    console.log("HỆ THỐNG GIÁM SÁT LỖI (DEBUG MODE) ĐÃ KÍCH HOẠT");
    
    try {
        initMap();
        console.log("✓ Khởi tạo bản đồ thành công.");
    } catch (e) {
        console.error("❌ LỖI NGHIÊM TRỌNG (initMap): Không thể tải bản đồ.", e);
    }

    try {
        renderProjectList(projectsData);
        console.log("✓ Render danh sách dự án thành công.");
    } catch (e) {
        console.error("❌ LỖI DỮ LIỆU (renderProjectList): Cấu trúc data.js bị sai định dạng (có thể thiếu trường overview, name...).", e);
    }

    try {
        setupSearch();
        console.log("✓ Thiết lập tìm kiếm thành công.");
    } catch (e) {
        console.error("❌ LỖI UI (setupSearch): Không tìm thấy ô nhập tìm kiếm.", e);
    }

    try {
        setupFilters();
        console.log("✓ Thiết lập Dropdown bộ lọc thành công.");
    } catch (e) {
        console.error("❌ LỖI DROPDOWN (setupFilters): Dữ liệu CĐT hoặc Quận Huyện có vấn đề.", e);
    }

    try {
        setupPlanningToggle();
        setupSidebarToggle();
        console.log("✓ Thiết lập hiệu ứng UI thành công.");
    } catch (e) {
        console.error("❌ LỖI GIAO DIỆN: Nút toggle sidebar hoặc quy hoạch bị lỗi.", e);
    }
});

function setupSidebarToggle() {
    const btn = document.getElementById('toggleSidebarBtn');
    const sidebar = document.getElementById('sidebar');
    
    if (btn && sidebar) {
        // Ngăn sự kiện click lan xuống bản đồ
        L.DomEvent.disableClickPropagation(btn);
        
        btn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            
            // Đổi icon
            if (sidebar.classList.contains('collapsed')) {
                btn.innerHTML = '<i class="fa-solid fa-list"></i>';
            } else {
                btn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            }
            
            // Cập nhật lại kích thước bản đồ sau khi animation kết thúc
            setTimeout(() => {
                if (map) map.invalidateSize();
            }, 300);
        });
    }
}

function initMap() {
    // Tọa độ trung tâm Hà Nội
    map = L.map('map').setView([21.0285, 105.8048], 11);

    // Đã thay thế hoàn toàn sang dữ liệu của GOOGLE MAPS (Phiên bản Việt Nam - gl=VN)
    // Đảm bảo tuyệt đối chủ quyền biển đảo Hoàng Sa, Trường Sa hiển thị tiếng Việt và thuộc Việt Nam.
    
    // 1. Google Maps Tiêu chuẩn (Giao thông đường phố)
    const googleStreets = L.tileLayer('https://mt1.google.com/vt/lyrs=m&hl=vi&gl=VN&x={x}&y={y}&z={z}', {
        attribution: '&copy; Google Maps',
        maxZoom: 20
    });

    // 2. Google Maps Vệ tinh (Lai - Có tên đường)
    const googleHybrid = L.tileLayer('https://mt1.google.com/vt/lyrs=y&hl=vi&gl=VN&x={x}&y={y}&z={z}', {
        attribution: '&copy; Google Maps',
        maxZoom: 20
    });

    // 3. Google Maps Địa hình
    const googleTerrain = L.tileLayer('https://mt1.google.com/vt/lyrs=p&hl=vi&gl=VN&x={x}&y={y}&z={z}', {
        attribution: '&copy; Google Maps',
        maxZoom: 20
    });

    // Gắn Google Streets làm mặc định
    googleStreets.addTo(map);

    // Thêm bộ chuyển đổi bản đồ (Layer Control) ở góc dưới bên phải
    const baseMaps = {
        "Google Tiêu Chuẩn": googleStreets,
        "Google Vệ Tinh": googleHybrid,
        "Google Địa Hình": googleTerrain
    };

    const layerControl = L.control.layers(baseMaps, null, {position: 'bottomright'}).addTo(map);

    // --- HIỂN THỊ LỚP QUY HOẠCH GIAO THÔNG TỪ GULAND ---
    // Tạo Pane riêng với zIndex cực cao (500) để không bao giờ bị đè
    map.createPane('metroPane');
    map.getPane('metroPane').style.zIndex = 500;
    map.getPane('metroPane').style.pointerEvents = 'none'; // Không cản trở click chuột vào các marker

    const gulandMetroLayer = L.tileLayer('https://s3.hn-1.cloud.cmctelecom.vn/guland6/hn-road-metro/{z}/{x}/{y}.png', {
        maxZoom: 20,
        opacity: 0.9,
        pane: 'metroPane',
        attribution: 'Dữ liệu Quy hoạch Giao thông'
    });
    
    // Thêm tùy chọn bật/tắt lớp Quy hoạch vào bảng điều khiển (Mặc định TẮT)
    layerControl.addOverlay(gulandMetroLayer, "<span style='color:#00d2ff; font-weight:600;'>🚇 Quy hoạch Giao thông & Metro</span>");

    // Khởi tạo biến planningLayer (sẽ được tạo khi người dùng bật)
    planningLayer = null;

    renderMarkers(projectsData);
}

function renderMarkers(projects) {
    // Xóa markers cũ
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    projects.forEach(proj => {
        if (!proj.lat || !proj.lng) return;

        // Custom Icon dựa trên phân khúc
        let iconColor = 'blue';
        if (proj.overview && proj.overview[0].value.toLowerCase().includes('siêu sang')) iconColor = 'gold';
        else if (proj.overview && proj.overview[0].value.toLowerCase().includes('thấp tầng')) iconColor = 'green';
        else if (proj.overview && proj.overview[0].value.toLowerCase().includes('noxh')) iconColor = 'red';

        const customIcon = L.divIcon({
            className: 'custom-div-icon',
            html: `<div style='background-color:${iconColor}; width:15px; height:15px; border-radius:50%; border:2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5);'></div>`,
            iconSize: [15, 15],
            iconAnchor: [7, 7]
        });

        const marker = L.marker([proj.lat, proj.lng], { icon: customIcon }).addTo(map);
        
        // Popup Tóm tắt
        const priceText = proj.financials ? proj.financials.price : (proj.overview.find(o => o.label.includes('Giá'))?.value || 'Đang cập nhật');
        
        const linkHtml = proj.link ? `<div style="margin-top: 12px; text-align: center;"><a href="${proj.link}" target="_blank" style="display: inline-block; width: 100%; padding: 8px; background: #0f172a; color: #b48c51; text-decoration: none; border-radius: 6px; font-size: 12px; font-weight: 600; transition: all 0.2s;">🔗 XEM TÀI LIỆU DỰ ÁN</a></div>` : '';

        const popupContent = `
            <div style="min-width: 250px;">
                <h3 style="margin: 0 0 5px 0; color: #1e293b; font-size:16px;">${proj.name}</h3>
                <p style="margin: 0 0 10px 0; font-size:12px; color: #64748b;">${proj.developer}</p>
                <div style="background: #f8fafc; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="font-size:12px;"><strong>Giá:</strong> <span style="color:#166534;">${priceText}</span></div>
                    <div style="font-size:12px;"><strong>Tình trạng:</strong> ${proj.status}</div>
                </div>
                <ul style="padding-left:15px; margin:0; font-size:12px; color: #475569;">
                    ${proj.usps.slice(0, 2).map(u => `<li>${u}</li>`).join('')}
                </ul>
                ${linkHtml}
            </div>
        `;
        
        marker.bindPopup(popupContent);
        marker.projectId = proj.id;
        markers.push(marker);
    });
}

function renderProjectList(projects) {
    const list = document.getElementById('projectList');
    list.innerHTML = '';
    
    projects.forEach(proj => {
        const li = document.createElement('li');
        li.className = 'project-item';
        
        // Trích xuất giá và phân khúc
        let priceText = 'Đang cập nhật';
        if (proj.financials && proj.financials.price) {
            priceText = proj.financials.price.split(' (')[0]; // Chỉ lấy phần giá rút gọn
        } else if (proj.overview) {
            const priceObj = proj.overview.find(o => o.label.toLowerCase().includes('giá'));
            if (priceObj) priceText = priceObj.value;
        }

        let segmentText = 'Sản phẩm tiêu chuẩn';
        let segmentClass = 'seg-standard';
        if (proj.overview) {
            const segObj = proj.overview.find(o => o.label.toLowerCase().includes('phân khúc') || o.label.toLowerCase().includes('sản phẩm'));
            if (segObj) segmentText = segObj.value;
        }
        
        const segLower = segmentText.toLowerCase();
        if (segLower.includes('siêu sang') || segLower.includes('hạng sang') || segLower.includes('vip') || segLower.includes('độc bản')) segmentClass = 'seg-luxury';
        else if (segLower.includes('cao cấp') || segLower.includes('thương mại')) segmentClass = 'seg-premium';
        else if (segLower.includes('noxh') || segLower.includes('xã hội')) segmentClass = 'seg-social';

        li.innerHTML = `
            <div class="p-header">
                <span class="p-developer">${proj.developer}</span>
                <span class="p-segment-badge ${segmentClass}" title="${segmentText}">
                    <i class="fa-solid fa-gem"></i>
                </span>
            </div>
            <div class="p-name">${proj.name}</div>
            <div class="p-info-grid">
                <div class="p-price"><i class="fa-solid fa-tags"></i> ${priceText}</div>
                <div class="p-area"><i class="fa-solid fa-location-dot"></i> ${proj.location}</div>
            </div>
            <div class="p-footer" style="justify-content: space-between; width: 100%;">
                <div class="p-status"><span class="status-dot"></span>${proj.status}</div>
                ${proj.link ? `<a href="${proj.link}" target="_blank" style="color: #2563eb; font-size: 11px; text-decoration: none; font-weight: 600; padding: 4px 8px; background: #eff6ff; border-radius: 4px; border: 1px solid #bfdbfe;" title="Xem trên SalePro" onclick="event.stopPropagation()">🔗 Chi tiết</a>` : ''}
            </div>
        `;
        
        li.addEventListener('click', () => {
            // Active state
            document.querySelectorAll('.project-list li').forEach(el => el.classList.remove('active'));
            li.classList.add('active');
            
            // Tìm marker và mở popup
            const marker = markers.find(m => m.projectId === proj.id);
            if (marker) {
                map.flyTo(marker.getLatLng(), 15);
                marker.openPopup();
            } else {
                alert("Dự án này chưa có tọa độ trên bản đồ!");
            }
        });
        
        list.appendChild(li);
    });
}

function setupPlanningToggle() {
    const btn = document.getElementById('togglePlanningBtn');
    const districtSelect = document.getElementById('planningDistrict');
    const opacitySlider = document.getElementById('opacitySlider');
    const mapControls = document.getElementById('mapControls');

    // Ngăn chặn thao tác kéo thanh trượt bị dính vào sự kiện kéo bản đồ của Leaflet
    if (mapControls) {
        L.DomEvent.disableClickPropagation(mapControls);
        L.DomEvent.disableScrollPropagation(mapControls);
    }

    // Cập nhật bản đồ ngay nếu thay đổi dropdown trong lúc đang bật
    districtSelect.addEventListener('change', () => {
        if (isPlanningVisible) {
            updatePlanningLayer();
        }
    });

    // Thay đổi độ mờ (opacity) trực tiếp
    opacitySlider.addEventListener('input', (e) => {
        if (planningLayer) {
            const opacity = parseFloat(e.target.value);
            if (planningLayer.setOpacity) {
                planningLayer.setOpacity(opacity);
            } else if (planningLayer.eachLayer) {
                planningLayer.eachLayer(layer => {
                    if (layer.setOpacity) layer.setOpacity(opacity);
                });
            }
        }
    });

    btn.addEventListener('click', () => {
        if (isPlanningVisible) {
            if (planningLayer) map.removeLayer(planningLayer);
            btn.innerHTML = '<i class="fa-solid fa-layer-group"></i> Bật Quy Hoạch';
            btn.style.background = 'white';
            btn.style.color = '#1e293b';
        } else {
            updatePlanningLayer();
            btn.innerHTML = '<i class="fa-solid fa-layer-group"></i> Tắt Quy Hoạch';
            btn.style.background = '#2563eb';
            btn.style.color = 'white';
        }
        isPlanningVisible = !isPlanningVisible;
    });

    const allDistricts = ['NamTuLiem', 'BacTuLiem', 'HoaiDuc', 'HaDong', 'ThanhXuan', 'CauGiay', 'TayHo', 'DongAnh', 'GiaLam', 'DanPhuong', 'HoangMai', 'LongBien', 'QuocOai', 'ThanhTri', 'ThachThat'];

    // =======================================================
    // HÀM TẠO URL TILE ONLINE TỪ SERVER SỞ TNMT HÀ NỘI
    // =======================================================
    function getOnlineTileUrl(districtKey) {
        return `https://qhkhsdd.hanoi.gov.vn/QuyHoachServices/rest/QuyHoach/gsv_data/hanoistnmt/tile/{z}/{x}/{y}?pathtms=hanoistnmt/HN-${districtKey}-KH2024/HN-${districtKey}-KH2024_Clip.tif`;
    }

    function updatePlanningLayer() {
        const district = districtSelect.value;
        const opacity = parseFloat(opacitySlider.value);
        
        if (planningLayer) map.removeLayer(planningLayer);
        
        if (district === 'all') {
            const layers = allDistricts.map(d => {
                return L.tileLayer(getOnlineTileUrl(d), {
                    maxZoom: 22,
                    maxNativeZoom: 18,
                    opacity: opacity,
                    zIndex: 10,
                    errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=',
                    attribution: 'Quy hoạch: Sở TNMT Hà Nội'
                });
            });
            planningLayer = L.layerGroup(layers);
        } else {
            planningLayer = L.tileLayer(getOnlineTileUrl(district), {
                maxZoom: 22,
                maxNativeZoom: 18,
                opacity: opacity,
                zIndex: 10,
                errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=',
                attribution: 'Quy hoạch: Sở TNMT Hà Nội'
            });
        }
        
        planningLayer.addTo(map);
    }
}

function setupSearch() {
    document.getElementById('searchProject').addEventListener('input', applyFilters);
}

function setupFilters() {
    const devSelect = document.getElementById('filterDeveloper');
    const distSelect = document.getElementById('filterDistrict');
    const hnDistricts = ['Tây Hồ', 'Nam Từ Liêm', 'Bắc Từ Liêm', 'Hà Đông', 'Hoài Đức', 'Cầu Giấy', 'Thanh Xuân', 'Đông Anh', 'Gia Lâm', 'Long Biên', 'Hoàng Mai', 'Đan Phượng', 'Thường Tín', 'Văn Giang'];

    // Hàm cập nhật 2 chiều
    function updateDropdowns(trigger) {
        const selectedDev = devSelect.value;
        const selectedDist = distSelect.value;

        // Nếu thay đổi Chủ đầu tư -> Lọc lại danh sách Quận/Huyện
        if (trigger === 'dev' || trigger === 'init') {
            distSelect.innerHTML = '<option value="">Quận / Huyện</option>';
            const validDistricts = new Set();
            projectsData.forEach(p => {
                if (!selectedDev || (p.developer && p.developer === selectedDev)) {
                    const locLower = p.location.toLowerCase();
                    hnDistricts.forEach(d => {
                        if (locLower.includes(d.toLowerCase())) {
                            validDistricts.add(d);
                        }
                    });
                }
            });
            [...validDistricts].sort().forEach(dist => {
                const option = document.createElement('option');
                option.value = dist;
                option.textContent = dist;
                if (dist === selectedDist) option.selected = true; // Giữ lại lựa chọn hiện tại nếu vẫn hợp lệ
                distSelect.appendChild(option);
            });
        }

        // Nếu thay đổi Quận/Huyện -> Lọc lại danh sách Chủ đầu tư
        if (trigger === 'dist' || trigger === 'init') {
            devSelect.innerHTML = '<option value="">Chủ đầu tư</option>';
            const validDevs = new Set();
            projectsData.forEach(p => {
                const locLower = p.location.toLowerCase();
                const isInDistrict = !selectedDist || locLower.includes(selectedDist.toLowerCase());
                
                if (isInDistrict && p.developer && p.developer !== 'Đang cập nhật') {
                    validDevs.add(p.developer);
                }
            });
            [...validDevs].sort().forEach(dev => {
                const option = document.createElement('option');
                option.value = dev;
                option.textContent = dev;
                if (dev === selectedDev) option.selected = true; // Giữ lại lựa chọn hiện tại nếu vẫn hợp lệ
                devSelect.appendChild(option);
            });
        }
    }

    // Khởi tạo ban đầu (chưa chọn gì cả)
    updateDropdowns('init');

    // Bắt sự kiện
    devSelect.addEventListener('change', () => {
        updateDropdowns('dev'); // Update Quận/Huyện
        applyFilters();
    });
    
    distSelect.addEventListener('change', () => {
        updateDropdowns('dist'); // Update Chủ đầu tư
        applyFilters();
    });
}

function applyFilters() {
    const term = document.getElementById('searchProject').value.toLowerCase();
    const dev = document.getElementById('filterDeveloper').value.toLowerCase();
    const dist = document.getElementById('filterDistrict').value.toLowerCase();

    const filtered = projectsData.filter(p => {
        const matchName = p.name.toLowerCase().includes(term) || p.location.toLowerCase().includes(term);
        
        let matchDev = true;
        if (dev) {
            matchDev = p.developer && p.developer.toLowerCase().includes(dev);
        }

        let matchDist = true;
        if (dist) {
            matchDist = p.location.toLowerCase().includes(dist);
        }

        return matchName && matchDev && matchDist;
    });

    renderProjectList(filtered);
    renderMarkers(filtered);
}
