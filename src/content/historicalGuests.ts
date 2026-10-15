export const historicalGuests = [
  {
    id: "sejong",
    name: "Vua Sejong",
    ko: "세종대왕",
    home: [450, 525],
    theme: "Hangul · Ngôn ngữ",
    gesture: "think",
    dialogue:
      "Chào bạn! Tôi là hình chiếu kể chuyện của vua Sejong (1397–1450). Hunminjeongeum được công bố năm 1446, dưới triều của tôi. Cùng nhìn một chữ trước nhé: 글자 — chữ viết. Bạn thấy nét nào lặp lại?",
    hook: "Ý tưởng nhiệm vụ · Tìm ba nét trên bảng chữ, rồi ghép một âm tiết. Chưa triển khai nhiệm vụ hay phần thưởng.",
    vocabulary: { ko: "글자", vi: "chữ viết" },
    source: "https://en.wikipedia.org/wiki/Sejong_the_Great",
  },
  {
    id: "jang",
    name: "Jang Yeong-sil",
    ko: "장영실",
    home: [595, 528],
    theme: "Khoa học · Khám phá",
    gesture: "pose",
    dialogue:
      "Xin chào! Tôi là khách lịch sử mô phỏng Jang Yeong-sil, người thợ và nhà phát minh thời Joseon, làm việc dưới triều Sejong. Quan sát và đo đạc giúp ta hiểu thiên nhiên. 물 — nước. Một giọt nước có thể giúp ta nghĩ về thời gian!",
    hook: "Ý tưởng nhiệm vụ · So sánh mực nước để tìm chi tiết còn thiếu của mô hình đồng hồ nước. Chưa mở trò chơi hay chấm điểm.",
    vocabulary: { ko: "물", vi: "nước" },
    source: "https://en.wikipedia.org/wiki/Jang_Yeong-sil",
  },
  {
    id: "saimdang",
    name: "Shin Saimdang",
    ko: "신사임당",
    home: [426, 607],
    theme: "Hội họa · Thiên nhiên",
    gesture: "wave",
    dialogue:
      "Chào bạn! Tôi là hình chiếu kể chuyện của Shin Saimdang (1504–1551), một nghệ sĩ và nhà thư pháp thời Joseon. Hãy chậm lại để nhìn chiếc lá. 나무 — cây. Thiên nhiên quanh ta có rất nhiều từ mới để ghi vào sổ vẽ.",
    hook: "Ý tưởng nhiệm vụ · Ghép nhãn cây và hoa với một trang sổ thiên nhiên. Chưa có tuyến nhiệm vụ hoàn chỉnh.",
    vocabulary: { ko: "나무", vi: "cây" },
    source: "https://en.wikipedia.org/wiki/Shin_Saimdang",
  },
  {
    id: "yi",
    name: "Đô đốc Yi Sun-sin",
    ko: "이순신",
    home: [650, 574],
    theme: "Chiến lược · Đồng đội",
    gesture: "wave",
    dialogue:
      "Xin chào! Tôi là khách lịch sử mô phỏng Yi Sun-sin (1545–1598), một đô đốc Joseon trong chiến tranh Imjin. Lập kế hoạch và phối hợp rất quan trọng. 함께 — cùng nhau. Ta hãy cùng đọc bản đồ trước khi chọn đường đi.",
    hook: "Ý tưởng nhiệm vụ · Cùng một người bạn chọn đường đưa thư an toàn trên bản đồ. Hiện chỉ là ý tưởng, chưa có multiplayer hay chiến đấu.",
    vocabulary: { ko: "함께", vi: "cùng nhau" },
    source: "https://en.wikipedia.org/wiki/Yi_Sun-sin",
  },
] as const;
export const historicalDisclaimer =
  "Khách lịch sử trong thị trấn hư cấu: các nhân vật thuộc những thời kỳ khác nhau, không phải đã sống cùng nhau. Lời thoại được sáng tác cho bản học thử.";
