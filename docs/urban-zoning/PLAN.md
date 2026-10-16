# URBAN-PLAN-002 — masterplan tinh chỉnh để duyệt

**Bạn đã chấp nhận sơ bộ ý tưởng phân khu4096×3072. Bản tinh chỉnh này đang chờ duyệt; chưa được phép sản xuất công trình cuối hoặc dựng lại map chơi được.** Yêu cầu mới đầy đủ: [URBAN_PLANNING_REFINEMENT.md](../current/URBAN_PLANNING_REFINEMENT.md).

- [Masterplan PNG](district-zoning-plan.png) / [SVG có nhóm chỉnh sửa](district-zoning-plan.svg) / [JSON nguồn](zoning-plan.json).
- [15 khối nền/mái/cửa/sân cùng tỉ lệ](building-footprints.png) / [SVG chi tiết](building-footprints.svg) / [lịch công trình](BUILDING_SCHEDULE.md).
- [Tham khảo lịch sử thực đã đọc](HISTORICAL_REFERENCES.md) / [góc khám phá & đất sử dụng](DISCOVERY_DENSITY.md) / [quy tắc bố trí](placement-rules.md).

## Đã sửa theo tám điểm review

| Điểm | Quy hoạch tinh chỉnh |
| --- | --- |
| Cung và tường | Khu cung riêng x1280–2816,y64–704: tường phía bắc, hai tường hồi, mặt tường trước nối đúng cổng chính, hai cổng phục vụ, cổng trong và hai sân. Nhà dân/chợ nằm ngoài; không có tường thành bao phố ở. |
| Phố và ngõ | Giữ đại lộ nghi lễ thẳng tại x2048. Thay đường ngang và vòng chữ nhật bằng phố men sân học viện, sân xưởng/bảo tàng, ngõ theo bếp/hiên/ranh đất, đường vườn theo bờ và cây. Có vòng phụ chợ, phố danh nhân và sân hội họa. |
| Công trình đa dạng | Thể hiện khối cánh nhà thực trong JSON/PNG thay cho15rectangle đơn giản. Học viện sân U, xưởng L + bệ dụng cụ, nhà sử liệu dài + tiền sảnh lệch, cửa hàng sâu có hốc đọc, kho giấy giật cấp, trà hiên mở, xưởng nghề, đình có bệ không mái, nhà U/L/hai nếp/giếng chung. |
| Phối cảnh | Chính diện chủ yếu đông–tây, hướng nam; mái chính nằm ngang và cánh hồi vuông góc. Đường có thể uốn nhưng không xoay cả ngôi nhà theo đường. Giữ top-down/3⁄4 nhẹ, không kim cương isometric. Sơ đồ mái không chứng minh artwork cuối có chiều sâu. |
| Nước | Một dòng liên tục từ mép tây sang đông, hồ bờ bất quy tắc thông với dòng, bờ24px mỗi bên. Cầu tây ở(1472,2352), cầu đông(2720,2352); mỗi cầu96×160px nối đoạn tiếp cận thẳng và phủ cả bờ. |
| Mật độ | 22điểm tiếp cận/khám phá dự kiến, bảy khoảnh xanh có chức năng, sân học/sân nghề/sân ở riêng. Cửa, hốc đọc, sân nghề, hiên trà, bờ hồ và ngã rẽ tạo nhịp; không mở thêm đất chỉ để kéo dài thời gian đi. |
| Tham khảo | KHS/Gyeongbokgung: cổng chính và đại lộ Yukjo; UNESCO/Changdeokgung: thứ bậc sân và thích ứng địa hình; Seowon: học–sân–cảnh quan; Hahoe/Yangdong: cụm nhà/sân/ngõ/nước. Mỗi công trình gắn mã nguồn và cách chuyển hóa riêng. |
| Skill bền vững | Đọc AGENTS/registry và skill Forge thực tại pin5324342; giữ nguyên Juni144frames và workflow đã chứng minh. Vòng này chỉ vẽ sơ đồ quy hoạch/kiểm hình học, không gọi pipeline sinh art hay nhận đã export map/nav/Tiled mới. |

## Cung thành: giới hạn rõ, quan hệ bên trong rõ

Đường bao gồm các đoạn tường **và các khoảng cổng có tên**, tạo một vòng kín duy nhất. Tường hồi phía tây/đông chạy trở lại tường bắc; tường trước nối hai bên cổng chính. Hai cổng phụ phục vụ khu cung, không biến thành lối xuyên ngõ dân cư. Lối ngoài tường phía tây đến điểm xem cổng phục vụ, không tự đưa người chơi vào cung. Sảnh bắc/cổng trong/hai sân chỉ là bối cảnh đặt chỗ để hiểu thứ bậc, **không phải một cung điện chơi được mới**.

Cổng chính quay nam ra sân trước và đại lộ. Điểm đến gặp gỡ lệch khỏi tim trục. Tượng Sejong lệch trục; Sejong giáo dục thuộc sân học viện, không phải tượng thứ hai. Khu cung trong và cổng phụ ở trạng thái đóng/dự trữ. Nhà ở dùng ranh sân dân dụng thấp khi cần, không dùng tường phòng thủ. Đây là khu phố hư cấu, không tái dựng Gyeongbokgung theo tỉ lệ hoặc gộp các di tích thành một lịch sử thật.

## Phố có lý do, không là ô lưới trang trí

Đại lộ160px là tuyến duy nhất cần thẳng trang trọng. Phố chính112px né sân công trình; nhánh80–96px theo ranh khu đất; ngõ/vườn64px. JSON lưu `reason` cho từng tuyến. Lối chợ vòng qua cánh bếp và kho, không cắt qua quầy. Ngõ hanok đổi hướng theo sân U và bếp nhà L; lối nhà vườn men hai nếp nhà khác nhau. Đường hồ đi vòng đình rồi nối lại vòng hai cầu.

Vòng khám phá nét vàng: quảng trường → phố xưởng/bảo tàng → cầu đông → đường vườn phía nam → cầu tây → phố sách/học viện → quảng trường. Có nhánh lựa chọn sang ngõ nhà, sân hội họa, hiên trà, đình hồ; ba vòng phụ tránh việc tất cả điểm đến là ngõ cụt. Các đoạn đổi hướng đi kèm thay đổi mặt tiền/sân/địa hình, không lượn ngẫu nhiên. Chiều rộng là khoảng phải giữ thông sau này; đạo cụ/người nói chuyện không chiếm tim tuyến.

## Kiến trúc và nước theo cùng một thế giới

Từng `masses[]` trong JSON là một cánh/khối nền riêng, có kiểu mái, hướng sống mái, số gian mặt trước. Rectangle bao ngoài chỉ giúp đặt chỗ, **không được dùng làm collider** khiến sân U/L bị lấp. Mỗi nhà có cửa ngoài, điểm tiếp cận, sân và chức năng; học viện/nhà U có thêm cửa phía trong sân. Hình mái là sơ đồ định hướng, chưa có texture hoặc final sprite. Thang tỉ lệ giữ Juni80px, tile32px, foot16×8, walk60/run100; sau duyệt phải kiểm cửa, hiên, mái và bóng ở camera1× trước khi chấp nhận art.

Suối vẫn là một dòng liên tục, chỉ rộng thành hồ ở vườn. Mặt phố chợ dùng mép đá thấp; bờ vườn chuyển sang đất, cây bờ và bậc đá; nhà ở lùi sau bờ cây. Những dải vật liệu nối nhau theo vùng sử dụng, không tô một đường viền cứng duy nhất. Hai điểm qua nước đã được kiểm sơ bộ: deck phủ64px dòng + hai bờ24px + dư tiếp cận, tuyến tới cầu thẳng theo trục cầu, không có đường lội thứ ba hoặc đường bị cắt bởi bờ.

## Mật độ và nhịp khám phá

Diện tích4096×3072 được giữ, không phình thêm. Có15khối kiến trúc/landmark, nhiều cánh phụ, sân riêng và22góc dùng được theo kế hoạch; vườn học viện, sân vật liệu xưởng, vườn bếp, sân hậu cửa hàng, vườn thảo mộc và bờ suối có chức năng cụ thể. Giữ chỗ mở đúng vai trò: quảng trường xã hội, sân học, sân trình diễn, đình nhìn nước. Số điểm không phải bằng chứng game đã thú vị; sau duyệt phải đi thật để đo nhịp nhìn–đi–dừng và sửa đoạn trống.

Các NPC chỉ là vị trí quy hoạch gắn công trình: Sejong/học viện, Jang/xưởng thiên văn, Yi/nhà sử liệu, Saimdang/sân hội họa. Không sản xuất hoặc thay nhân vật tại vòng này; không dùng artwork khách cũ bị từ chối để giả là NPC mới. Chương trình chợ, nhà ở và học tập là thiết kế RPG nguyên gốc, không khẳng định chúng đã tồn tại trong di tích tham khảo.

## Kiểm chứng và phạm vi còn chờ

Kiểm tra hình học lưới8px: **41/41điểm tiếp cận nối được,37.022/37.022ô đi bộ cùng thành phần,0khối công trình chồng nhau,0đường lấn nhà/bờ ngoài cầu,0tường cung trong khu chợ/ở**. Chuỗi tường+cổng là một vòng kín; hai cầu đúng dòng/tuyến. Đây là kiểm quy hoạch bảo thủ với bán kính8px, **không phải Forge nav/collision cuối hoặc Phaser của map đề xuất**. Lần thử đầu phát hiện năm đoạn lấn góc nhà và một bệ thiên văn cô lập; đã sửa vị trí/lối nối, không nới ngưỡng. [Báo cáo](planning-check.json), [sơ đồ khoảng đi](planning-clearance.png), raw lần đầu trong `history/`.

Bản chơi2048×768+phòng đọc, Juni/tài sản/source/tests/toolchain giữ nguyên; recovery trước chỉnh `recovery/before-urban-refinement-20261016`→ec520e3. Main và Pages không thay đổi. Phần đo khoảng đi bộ là ước tính trên tim đường trong báo cáo, không phải gameplay capture. Sau khi duyệt mới dùng workflow Forge thực để sinh/chiết art, layered map/nav/Tiled và tích hợp một ứng viên Phaser riêng, rồi kiểm movement/collision/occlusion/mobile và quay thực tế.

**Dừng để bạn duyệt masterplan tinh chỉnh. Không sinh buildings cuối, dựng lại playable map, làm PR/merge main hoặc deploy trước khi đủ các quyết định tương ứng.** Quy trình main tương lai trong [PROMOTION.md](PROMOTION.md) vẫn có hiệu lực.
