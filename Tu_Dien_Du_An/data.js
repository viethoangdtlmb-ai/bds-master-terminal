// Dữ liệu Đánh giá Chủ Đầu Tư (Developer Insights)
const developerData = {
    'Vingroup': {
        pros: 'Hệ sinh thái ALL-IN-ONE số 1 VN. Tiến độ thi công thần tốc, pháp lý chuẩn chỉnh. Cư dân dọn về ở ngay tạo sinh khí cực tốt.',
        cons: 'Mật độ xây dựng tại một số phân khu cao. Nguồn cung thứ cấp khổng lồ khiến giá thứ cấp có xu hướng bão hòa nhanh.',
        target: 'Khách mua ở thực thích tiện ích đồng bộ, khách tỉnh mua cho con cái học đại học, nhà đầu tư mua để cho thuê (Dòng tiền).'
    },
    'Masterise Homes': {
        pros: 'Dịch vụ quản lý quốc tế tiêu chuẩn Marriott, thiết kế Full-Kính (Low-E) cực kỳ sang trọng. Định danh cộng đồng cư dân tinh hoa rào cản cao.',
        cons: 'Mức giá bán luôn "lập đỉnh" thiết lập mặt bằng mới của khu vực. Đòi hỏi vốn ban đầu cực mạnh.',
        target: 'Khách VIP, Việt kiều mua để giữ tiền (Tích sản), thích trải nghiệm sống xa xỉ, có quản gia riêng.'
    },
    'MIK Group': {
        pros: 'Cấu trúc sản phẩm thông minh tối ưu diện tích, giá bán "mềm" hơn Masterise nhưng tiện ích (hồ bơi, gym) vẫn rất cao cấp. Thanh khoản thứ cấp cực tốt.',
        cons: 'Mức độ nhận diện thương hiệu siêu sang chưa bằng Masterise/Sun Group. Quản lý vận hành ở mức khá.',
        target: 'Khách hàng trẻ cấp tiến (Gen Z/Millennials), chuyên gia IT, nhà đầu tư lướt sóng hoặc cho thuê.'
    },
    'Sun Group': {
        pros: 'Thiết kế mang tính biểu tượng (Iconic) thay đổi diện mạo khu vực. Chất lượng xây dựng 6 sao, vị trí thường là "đất vàng" độc bản.',
        cons: 'Quỹ căn thường rất hiếm, kén khách, giá trị cực kỳ đắt đỏ. Tiến độ ra sổ đôi khi phụ thuộc vào thiết kế điều chỉnh.',
        target: 'Giới siêu giàu mua sưu tầm tài sản truyền đời, nhà đầu tư chuộng các biểu tượng độc tôn.'
    },
    'Sunshine Group': {
        pros: 'Dẫn đầu công nghệ Smart Home 4.0 đồng bộ, kiến trúc dát vàng, không gian chuẩn hoàng gia.',
        cons: 'Quá khứ từng bị chậm tiến độ. Đang trong quá trình tái cấu trúc mạnh mẽ với quỹ đất vàng ở Ciputra.',
        target: 'Khách chuộng công nghệ, thích không gian sống lộng lẫy xa hoa khu vực Hồ Tây.'
    },
    'SJ Group': {
        pros: 'Chuyên trị đại đô thị ven đô (điển hình Nam An Khánh). Phát triển không gian sống xanh, hồ điều hòa khổng lồ, mật độ siêu thấp.',
        cons: 'Hạ tầng kết nối nội khu và dịch vụ thương mại đôi khi hoàn thiện chậm hơn tiến độ bàn giao nhà.',
        target: 'Khách mua biệt thự vùng ven nghỉ dưỡng cuối tuần, đầu tư gom đất chờ hạ tầng Vành đai 3.5.'
    },
    'Gamuda Land': {
        pros: 'Quy hoạch xanh chuẩn ESG quốc tế. Hệ thống cây xanh mặt nước thuộc top đẹp nhất Hà Nội (Công viên Yên Sở).',
        cons: 'Dự án trọng điểm thường ở khu Nam - nơi hạ tầng giao thông vẫn đang trong quá trình nâng cấp.',
        target: 'Gia đình đa thế hệ, người lớn tuổi cần không gian sống xanh sinh thái nghỉ dưỡng.'
    },
    'CapitaLand': {
        pros: 'Chủ đầu tư Ngoại (Singapore) uy tín toàn cầu. Tiêu chuẩn bàn giao khắt khe, phong cách nhiệt đới tinh tế.',
        cons: 'Rào cản tài chính lớn. Tiến độ thanh toán khắt khe hơn theo quy định vốn FDI.',
        target: 'Expat, chuyên gia nước ngoài, giới tinh hoa công nghệ khu phía Tây.'
    },
    'TSQ Việt Nam': {
        pros: 'Am hiểu sâu sắc văn hóa và quy hoạch khu vực Hà Đông (Việt Kiều Châu Âu). Thiết kế kiến trúc độc bản.',
        cons: 'Năng lực triển khai siêu dự án chưa được kiểm chứng nhiều như Vin/Sun.',
        target: 'Cư dân nội vùng Hà Đông muốn nâng cấp chất lượng sống.'
    }
};

const projectsData = [
{
        id: 'lumiere-hanoi-seasons-garden',
        verified: true,
        name: 'LUMIÈRE HANOI SEASONS GARDEN ( CAO XÀ LÁ )',
        location: 'Thanh Xuân, Hà Nội',
        lat: 20.995454,
        lng: 105.809153,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/lumiere-hanoi-seasons-garden',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'vinhomes-ocean-park-2',
        verified: true,
        name: 'VINHOMES OCEAN PARK 2 (OCP2)',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9448735,
        lng: 105.9753818,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/vinhomes-ocean-park-2',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'vinhomes-ocean-park-3',
        verified: true,
        name: 'VINHOMES OCEAN PARK 3',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.957655,
        lng: 105.9760955,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/vinhomes-ocean-park-3',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'vinhomes-wonder-city',
        verified: true,
        name: 'VINHOMES WONDER CITY (VIN ĐAN PHƯỢNG)',
        location: 'Đan Phượng, Hà Nội',
        lat: 21.092773,
        lng: 105.7081971,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/vinhomes-wonder-city',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-era-landmark',
        verified: true,
        name: 'MASTERI ERA LANDMARK',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9571684,
        lng: 105.969864,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-era-landmark',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'imperia-ocean-city-the-parkland',
        verified: true,
        name: 'IMPERIA OCEAN CITY - THE PARKLAND',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9388356,
        lng: 105.9831526,
        developer: 'MIK',
        link: 'https://salepro.com/project-detail/imperia-ocean-city-the-parkland',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-grand-coast',
        verified: true,
        name: 'MASTERI GRAND COAST',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9507038,
        lng: 105.9853787,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-grand-coast',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masterise-homes-co-loa-lumiere-essence-peak',
        verified: true,
        name: 'MASTERISE HOMES CỔ LOA - LUMIÈRE ESSENCE PEAK',
        location: 'Đông Anh, Hà Nội',
        lat: 21.0946864,
        lng: 105.8595069,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masterise-homes-co-loa-lumiere-essence-peak',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'lumiere-springbay',
        verified: true,
        name: 'LUMIÈRE SPRINGBAY',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9519293,
        lng: 105.9810523,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/lumiere-springbay',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'vinhomes-global-gate',
        verified: true,
        name: 'VINHOMES GLOBAL GATE',
        location: 'Đông Anh, Hà Nội',
        lat: 21.0946088,
        lng: 105.8600959,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/vinhomes-global-gate',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'imperia-sky-park',
        verified: true,
        name: 'IMPERIA SKY PARK',
        location: 'Hoài Đức, Hà Nội',
        lat: 21.0101417,
        lng: 105.723883,
        developer: 'MIK',
        link: 'https://salepro.com/project-detail/imperia-sky-park',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-fullton',
        verified: true,
        name: 'THE FULLTON',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9720833,
        lng: 105.98075,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/the-fullton',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'alluvia-city',
        verified: true,
        name: 'ALLUVIA CITY',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9412181,
        lng: 105.9196786,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/alluvia-city',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'sun-feliza-suites',
        verified: true,
        name: 'SUN FELIZA SUITES',
        location: 'Cầu Giấy, Hà Nội',
        lat: 21.0363744,
        lng: 105.781661,
        developer: 'SUN GROUP',
        link: 'https://salepro.com/project-detail/sun-feliza-suites',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-sky-quarter',
        verified: true,
        name: 'MASTERI SKY QUARTER',
        location: 'Đan Phượng, Hà Nội',
        lat: 21.098768,
        lng: 105.713231,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-sky-quarter',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'alumi',
        verified: true,
        name: 'ALUMI',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9421598,
        lng: 105.9198312,
        developer: 'XUÂN CẦU HOLDINGS',
        link: 'https://salepro.com/project-detail/alumi',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'iconia-lakeside',
        verified: true,
        name: 'ICONIA LAKESIDE',
        location: 'Nam Từ Liêm, Hà Nội',
        lat: 20.9947699,
        lng: 105.7890319,
        developer: 'MIPEC',
        link: 'https://salepro.com/project-detail/iconia-lakeside',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-vista-van-la',
        verified: true,
        name: 'THE VISTA VAN LA',
        location: 'Hà Đông, Hà Nội',
        lat: 20.9578914,
        lng: 105.7594948,
        developer: 'SJ GROUP',
        link: 'https://salepro.com/project-detail/the-vista-van-la-1',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'noble-palace-tay-thang-long',
        verified: true,
        name: 'NOBLE PALACE TÂY THĂNG LONG',
        location: 'Đan Phượng, Hà Nội',
        lat: 21.0812471,
        lng: 105.7011016,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/noble-palace-tay-thang-long',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-flame-vine',
        verified: true,
        name: 'THE FLAME VINE',
        location: 'Hoài Đức, Hà Nội',
        lat: 21.0523125,
        lng: 105.7241875,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/the-flame-vine',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'rivea-hanoi',
        verified: true,
        name: 'RIVEA HANOI',
        location: 'Hoàng Mai, Hà Nội',
        lat: 20.9950133,
        lng: 105.8770392,
        developer: 'TÂN Á ĐẠI THÀNH',
        link: 'https://salepro.com/project-detail/rivea-hanoi',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-queen',
        verified: true,
        name: 'THE QUEEN',
        location: 'Thanh Xuân, Hà Nội',
        lat: 20.986139,
        lng: 105.839028,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/the-queen',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'noble-crystal-tay-ho',
        verified: true,
        name: 'NOBLE CRYSTAL TÂY HỒ',
        location: 'Tây Hồ, Hà Nội',
        lat: 21.050529,
        lng: 105.8991377,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/noble-crystal-tay-ho',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'sunshine-legend-city',
        verified: true,
        name: 'SUNSHINE LEGEND CITY',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9437673,
        lng: 105.9650086,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/sunshine-legend-city',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'tmdv-smart-city',
        verified: true,
        name: 'TMDV SMART CITY',
        location: 'Nam Từ Liêm, Hà Nội',
        lat: 21.003813,
        lng: 105.756527,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/tmdv-smart-city',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'noble-crystal-long-bien',
        verified: true,
        name: 'NOBLE CRYSTAL LONG BIÊN',
        location: 'Long Biên, Hà Nội',
        lat: 21.0474593,
        lng: 105.901455,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/noble-crystal-long-bien',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'tmdv-vinhomes-ocean-park-1',
        verified: false,
        name: 'TMDV VINHOMES OCEAN PARK 1',
        location: 'Gia Lâm, Hà Nội',
        lat: 21.001852,
        lng: 105.943216,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/tmdv-vinhomes-ocean-park-1',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'metropoli5',
        verified: true,
        name: 'METROPOLI5',
        location: 'Hoài Đức, Hà Nội',
        lat: 21.005374,
        lng: 105.7309939,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/metropoli5',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'noble-palace-long-bien',
        verified: true,
        name: 'NOBLE PALACE LONG BIÊN',
        location: 'Long Biên, Hà Nội',
        lat: 21.050529,
        lng: 105.8991377,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/noble-palace-long-bien',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'him-lam-thuong-phuc-legend',
        verified: true,
        name: 'HIM LAM THƯỢNG PHÚC LEGEND',
        location: 'Thường Tín, Hà Nội',
        lat: 20.8734448,
        lng: 105.8569501,
        developer: 'HIM LAM',
        link: 'https://salepro.com/project-detail/him-lam-thuong-phuc-legend',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'dong-luc-tower',
        verified: true,
        name: 'ĐỘNG LỰC TOWER',
        location: 'Thanh Xuân, Hà Nội',
        lat: 20.9899781,
        lng: 105.8100309,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/dong-luc-tower',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'hado-charm-villas',
        verified: true,
        name: 'HADO CHARM VILLAS',
        location: 'Hoài Đức, Hà Nội',
        lat: 21.0017727,
        lng: 105.7077968,
        developer: 'HÀ ĐÔ',
        link: 'https://salepro.com/project-detail/hado-charm-villas',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
    {
        id: 'reflection-west-lake',
        verified: true,
        name: 'The Reflection West Lake',
        location: 'Tây Hồ, Hà Nội',
        lat: 21.072772994119056,
        lng: 105.82515284216367,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/the-reflection-west-lake',
        status: 'Sắp nhận Booking (Rumor)',
        overview: [
            { label: 'Giá rumo', value: '150 - 250 tr/m²' },
            { label: 'Bàn giao', value: 'Dự kiến 2028' }
        ],
        targetCustomers: [
            'Khách hàng VVIP, chuyên gia ngoại cấp cao.'
        ],
        usps: [
            'Vị trí lõi Tây Hồ, thiết kế Boutique Luxury chỉ giới hạn vài chục căn hộ.',
            'Mỗi căn hộ là một tác phẩm nghệ thuật có quản gia riêng.'
        ],
        catalysts: [
            { title: 'Quỹ đất vàng', desc: 'Bất động sản ven hồ Tây không bao giờ sinh ra thêm.' }
        ],
        priceGap: `
            <div class="price-gap-box">
                <div class="title">Đánh giá chung</div>
                <div class="value">Tài sản phòng thủ tuyệt đối chống lạm phát. Tăng trưởng giá trị bằng tính độc tôn.</div>
            </div>
        `,
        warnings: `<p><strong>Rủi ro:</strong> Nguồn thông tin rumor chưa chính thức, cần chờ sự kiện kick-off để xác minh pháp lý.</p>`
    },
{
        id: 'eurowindow-twin-parks',
        verified: true,
        name: 'EUROWINDOW TWIN PARKS',
        location: 'Gia Lâm, Hà Nội',
        lat: 21.0078191,
        lng: 105.9455553,
        developer: 'EUROWINDOW HOLDING',
        link: 'https://salepro.com/project-detail/eurowindow-twin-parks',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'hanoi-signature-by-swiss-belhotel',
        verified: true,
        name: 'HANOI SIGNATURE',
        location: 'Cầu Giấy, Hà Nội',
        lat: 21.0415945,
        lng: 105.7987368,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/hanoi-signature-by-swiss-belhotel',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-trinity-square-ocp2',
        verified: true,
        name: 'MASTERI TRINITY SQUARE (OCP2)',
        location: 'Văn Giang, Hưng Yên',
        lat: 20.9456807,
        lng: 105.972215,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-trinity-square-ocp2',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'vinhomes-ocean-park-1',
        verified: true,
        name: 'VINHOMES OCEAN PARK 1',
        location: 'Gia Lâm, Hà Nội',
        lat: 20.9947937,
        lng: 105.9358326,
        developer: 'VINHOMES',
        link: 'https://salepro.com/project-detail/vinhomes-ocean-park-1',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-lakeside-ocp1',
        verified: true,
        name: 'MASTERI LAKESIDE (OCP1)',
        location: 'Gia Lâm, Hà Nội',
        lat: 21.0034851,
        lng: 105.9475821,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-lakeside-ocp1',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'lumiere-orient-pearl',
        verified: true,
        name: 'LUMIÈRE ORIENT PEARL',
        location: 'Gia Lâm, Hà Nội',
        lat: 21.0005376,
        lng: 105.9458919,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/lumiere-orient-pearl',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-matrix-one-premium',
        verified: true,
        name: 'THE MATRIX ONE PREMIUM',
        location: 'Nam Từ Liêm, Hà Nội',
        lat: 21.0104375,
        lng: 105.7733125,
        developer: 'MIK',
        link: 'https://salepro.com/project-detail/the-matrix-one-premium',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'masteri-grand-avenue',
        verified: true,
        name: 'MASTERI GRAND AVENUE',
        location: 'Đông Anh, Hà Nội',
        lat: 21.1011721,
        lng: 105.856156,
        developer: 'MASTERISE HOMES',
        link: 'https://salepro.com/project-detail/masteri-grand-avenue',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'imperia-signature-co-loa',
        verified: true,
        name: 'IMPERIA SIGNATURE (CỔ LOA)',
        location: 'Đông Anh, Hà Nội',
        lat: 21.0948135,
        lng: 105.8609288,
        developer: 'MIK',
        link: 'https://salepro.com/project-detail/imperia-signature-co-loa',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-senique-ha-noi-ocp1',
        verified: true,
        name: 'THE SENIQUE HÀ NỘI (OCP1)',
        location: 'Gia Lâm, Hà Nội',
        lat: 21.0017184,
        lng: 105.9493012,
        developer: 'CAPITALAND',
        link: 'https://salepro.com/project-detail/the-senique-ha-noi-ocp1',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'the-magnolia-private-residences',
        verified: false,
        name: 'THE MAGNOLIA PRIVATE RESIDENCES',
        location: 'Cầu Giấy, Hà Nội',
        lat: 21.0607675,
        lng: 105.8700045,
        developer: 'MIK',
        link: 'https://salepro.com/project-detail/the-magnolia-private-residences',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'iconia-lakesidett',
        verified: true,
        name: 'ICONIA LAKESIDE_TT',
        location: 'Nam Từ Liêm, Hà Nội',
        lat: 21.0285,
        lng: 105.8048,
        developer: 'MIPEC',
        link: 'https://salepro.com/project-detail/iconia-lakesidett',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'noble-palace-tay-ho',
        verified: true,
        name: 'NOBLE PALACE TÂY HỒ',
        location: 'Tây Hồ, Hà Nội',
        lat: 21.0845625,
        lng: 105.7933125,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/noble-palace-tay-ho',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'sunshine-river-park',
        verified: true,
        name: 'SUNSHINE RIVER PARK',
        location: 'Tây Hồ, Hà Nội',
        lat: 21.0871739,
        lng: 105.7921934,
        developer: 'SUNSHINE GROUP',
        link: 'https://salepro.com/project-detail/sunshine-river-park',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    },
{
        id: 'malibu-walk',
        verified: true,
        name: 'MALIBU WALK',
        location: 'Gia Lâm, Hà Nội',
        lat: 20.9938704,
        lng: 105.9448548,
        developer: 'KHÁC',
        link: 'https://salepro.com/project-detail/malibu-walk',
        status: 'Đang mở bán',
        overview: [
            { label: 'Phân khúc', value: 'Đang cập nhật' },
            { label: 'Giá dự kiến', value: 'Liên hệ tư vấn' }
        ],
        financials: {
            price: 'Liên hệ tư vấn',
            yield: 'Đang cập nhật',
            payment: 'Theo chính sách CĐT',
            legal: 'Sở hữu lâu dài'
        },
        targetCustomers: ['Khách hàng quan tâm dự án này'],
        usps: ['Đang cập nhật'],
        catalysts: [{ title: 'Tiềm năng', desc: 'Đang đánh giá' }],
        priceGap: `<div class="price-gap-box"><div class="title">Tư vấn</div><div class="value">Dữ liệu đang được đồng bộ chi tiết.</div></div>`,
        warnings: `<p>Dự án mới đồng bộ từ Excel.</p>`
    }
];
