# Công trình — khối nền, mái, mặt tiền, cửa và sân

Xem [bảng hình cùng tỉ lệ](building-footprints.png). Tất cả là đặt chỗ quy hoạch; chưa tạo sprites/buildings cuối. Tọa độ world px, y hướng nam.

## G01 — Cổng chính

Chức năng: Ceremonial palace threshold; forecourt view only, palace entry closed

Mặt tiền: South-facing three-bay gate on masonry podium; side wall junctions, closed leaves

Mái: One double-tier east-west gate roof; not a residential roof

Cửa/sân ngoài: [2048, 768]; điểm tiếp cận: [2048, 832].

Nguồn định hướng: R1, R2. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## A01 — Học viện Hangul

Chức năng: Quiet Hangul learning / reading court; preserves existing lesson as future integration target

Mặt tiền: Five-bay lecture facade plus recessed study/library wings; open south court

Mái: Broad horizontal main ridge; two short perpendicular wing roofs enclosing a U court

Cửa/sân ngoài: [672, 1136]; điểm tiếp cận: [672, 1200]; cửa giảng đường bên trong sân: [672, 800].

Nguồn định hướng: R1, R3. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## P01 — Mốc Sejong

Chức năng: Public orientation landmark, distinct from the educational Sejong guest

Mặt tiền: Seated bronze scholar on a low plinth, outside ceremonial centerline

Mái: No building roof; open view and readable silhouette

Cửa/sân ngoài: None; điểm tiếp cận: [2280, 1248].

Nguồn định hướng: R1. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## H01 — Xưởng thiên văn

Chức năng: Jang Yeong-sil invention / number learning; educational workshop, not a claimed reconstruction

Mặt tiền: Asymmetric work bays with tool storage on east, demonstration court and open instrument platform

Mái: L footprint: horizontal workshop ridge, lower north-south tool wing; separate uncovered instrument platform

Cửa/sân ngoài: [3168, 1120]; điểm tiếp cận: [3168, 1184]; cửa giảng đường bên trong sân: [3232, 672].

Nguồn định hướng: R1, R3. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## H02 — Nhà sử liệu

Chức năng: Yi Sun-sin naval history and strategy pavilion; no invented waterfront harbor

Mặt tiền: Six-bay long display facade, offset west vestibule and front strategy terrace

Mái: Low long hipped roof with small separate vestibule ridge, not academy-U or workshop-L

Cửa/sân ngoài: [3552, 1280]; điểm tiếp cận: [3552, 1392].

Nguồn định hướng: R1, R2. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## M01 — Hiệu sách

Chức năng: Book browsing, reading discovery and future vocabulary hooks

Mặt tiền: Narrow deep shop with two display bays and recessed side reading nook

Mái: Deep gable plus short low nook roof; frontage follows the bending book lane

Cửa/sân ngoài: [416, 1792]; điểm tiếp cận: [416, 1872].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## M02 — Giấy & bút

Chức năng: Stationery, hanji paper and writing-tool discovery

Mặt tiền: Three shallow paper-display bays, stepped east dry-store and protected loading nook

Mái: Two offset gable roofs of different depth; no duplicate of the bookshop footprint

Cửa/sân ngoài: [864, 1696]; điểm tiếp cận: [864, 1792].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## M03 — Trà quán

Chức năng: Tea rest, small social groups and a shaded view toward the stream

Mặt tiền: Low open four-bay maru veranda, side kitchen and small bank-facing tea court

Mái: Shallow main roof with separate kitchen return; outward-facing veranda, not a big civic hall

Cửa/sân ngoài: [544, 2080]; điểm tiếp cận: [576, 2112].

Nguồn định hướng: R2, R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## M04 — Xưởng thủ công

Chức năng: Craft demonstration, original small-item vocabulary and drying-rack discovery

Mặt tiền: Three open work bays with tall east tool store; drying court distinct from sales frontage

Mái: Stepped two-height roof with open work side, not another shallow paper shop

Cửa/sân ngoài: [992, 2080]; điểm tiếp cận: [992, 2112].

Nguồn định hướng: R3, R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## V01 — Đình ven hồ

Chức năng: Quiet gathering and framed pond view; pavilion floor/collider to be art-reviewed later

Mặt tiền: Open-sided pavilion with broad view, low terrace and no shop windows

Mái: Single compact hipped roof; south platform remains uncovered, lower than all halls

Cửa/sân ngoài: [2080, 2144]; điểm tiếp cận: [2080, 2176].

Nguồn định hướng: R2, R3. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## R01 — Nhà sân U

Chức năng: Residential quiet court; no public route through private rooms

Mặt tiền: Small inward-looking U house, asymmetrical room lengths and recessed courtyard entry

Mái: Three modest gables enclosing a small court, well below academy scale

Cửa/sân ngoài: [3088, 2016]; điểm tiếp cận: [3088, 2112]; cửa giảng đường bên trong sân: [3088, 1872].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## R02 — Nhà góc L

Chức năng: Residential family courtyard with working kitchen garden

Mặt tiền: Long horizontal house and east kitchen return, sheltered west garden entry

Mái: Unequal L roof: broad hip/gable main roof and narrow lower kitchen roof

Cửa/sân ngoài: [3568, 2064]; điểm tiếp cận: [3568, 2128].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## S01 — Xưởng hội họa

Chức năng: Saimdang art / color / nature vocabulary, drying and painting discoveries

Mặt tiền: Long low studio, stepped east display gallery, west washing room; outdoor painting court

Mái: Three different-height roof parts around an off-center art court; mostly horizontal display facade

Cửa/sân ngoài: [640, 2672]; điểm tiếp cận: [640, 2784].

Nguồn định hướng: R3, R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## R03 — Nhà hai nếp

Chức năng: Garden residence and shared herb tending, not a shop

Mặt tiền: Two offset small pavilions with a narrow covered connector; west shared garden entry

Mái: Separated east-west ridges linked at one end; zigzag compound distinct from U and L houses

Cửa/sân ngoài: [3056, 2784]; điểm tiếp cận: [3024, 2848].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.

## R04 — Nhà giếng chung

Chức năng: Small dwelling with shared-well discovery off the lane

Mặt tiền: Deep two-bay house with long low front porch and east shared-well apron

Mái: One deep gable plus shallow veranda roof, no side-wing clone

Cửa/sân ngoài: [3672, 2784]; điểm tiếp cận: [3648, 2880].

Nguồn định hướng: R4. Sân và từng khối cánh nhà được lưu riêng trong JSON, không dùng rectangle bao ngoài làm collider.
