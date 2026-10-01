# 🇱🇦 Lao OCR & Educational Translation System
> **Bài tập lớn môn Xử lý ảnh (Digital Image Processing)**  
> **Đề tài:** Nhận dạng ký tự quang học (OCR) và Hỗ trợ Dịch tiếng Lào dựa trên ảnh văn bản phục vụ hệ thống giảng dạy trực tuyến.

---

## 🎯 Mục tiêu Dự án
Xây dựng một hệ thống xử lý ảnh và nhận dạng ký tự hoàn chỉnh dành riêng cho tiếng Lào:
1. **Tiền xử lý ảnh thích nghi:** Khắc phục các điều kiện thực tế (chụp nghiêng, bóng đổ, nhiễu sáng, mờ nét).
2. **Nhận dạng chữ in tiếng Lào:** Từ flashcard, giáo trình, từ vựng trực quan.
3. **Hậu xử lý từ điển có trọng số:** Ứng dụng ma trận nhầm lẫn ký tự thực nghiệm vào Dynamic Programming Levenshtein.
4. **Hỗ trợ học tập:** Phiên âm Latinh, tra cứu nghĩa đa ngữ (Việt - Anh), flashcard tương tác với thuật toán lặp lại ngắt quãng (SM-2).

---

## 📁 Tài liệu Dự án
- [📜 Quy chuẩn Dự án (AGENTS.md)](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/AGENTS.md) — Các nguyên tắc cốt lõi về tiếng Lào, Unicode, mã nguồn và thực nghiệm.
- [🗺️ Kế hoạch Dự án Chi tiết (PROJECT_PLAN.md)](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/docs/PROJECT_PLAN.md) — Toàn bộ roadmap 11 phase (P0 đến P10) với mốc giờ, deliverables và cổng ra.
- [📊 Bảng Theo dõi Tiến độ (PROGRESS_TRACKER.md)](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/docs/PROGRESS_TRACKER.md) — Cập nhật trạng thái từng đầu việc và cổng ra.
- [📝 Nhật ký Phát triển & Truy vết (DEVLOG.md)](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/docs/DEVLOG.md) — Ghi chép chi tiết quá trình làm, suy nghĩ, vibe và bài học rút ra.
- [⚠️ Quản trị Rủi ro (RISKS.md)](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/docs/RISKS.md) — Danh sách bẫy kỹ thuật và giải pháp xử lý.

---

## 🏗️ Cấu trúc Thư mục

```text
├── AGENTS.md                  # Quy chuẩn dự án, quy tắc tiếng Lào & Unicode
├── README.md                  # Giới thiệu dự án
├── requirements.txt           # Thư viện phụ thuộc
├── docs/                      # Tài liệu dự án
│   ├── PROJECT_PLAN.md        # Kế hoạch chi tiết 11 phase
│   ├── PROGRESS_TRACKER.md    # Bảng trạng thái tiến độ
│   ├── DEVLOG.md              # Nhật ký phát triển (Vibe log)
│   ├── RISKS.md               # Bảng quản lý rủi ro
│   └── DATA.md                # Giao thức thu thập và thống kê dữ liệu
├── src/                       # Mã nguồn chính
│   ├── preprocessing/         # Xử lý ảnh: A1-A9, tách dòng, normalize
│   ├── ocr/                   # Tesseract wrapper, CRNN model
│   ├── postprocessing/        # Weighted Levenshtein, lexicon snap
│   ├── nlp/                   # Tokenizer, romanization, translation
│   ├── evaluation/            # CER, WER, accuracy, bootstrap CI
│   └── utils/                 # Font check, visualization helpers
├── experiments/               # Thực nghiệm khoa học
│   ├── configs/               # File cấu hình YAML
│   └── results/               # Bảng CSV, biểu đồ ablation study
├── data/                      # Dữ liệu
│   ├── raw/                   # Ảnh chụp thực tế thô
│   ├── gold/                  # Gold test set (dev 30% / test 70%)
│   ├── synth/                 # Dữ liệu tổng hợp (clean & augmented)
│   └── dictionaries/          # Từ điển tiếng Lào (>= 500 từ)
├── app/                       # Ứng dụng học tập Streamlit
└── tests/                     # Unit tests & integration tests
```

---

## 🚀 Lộ trình Thực hiện
Dự án được triển khai theo 11 phase có cổng ra (Exit Gate) nghiêm ngặt:
- **P0:** Nền móng & Thước đo (Font validation, NFC normalization, CER/WER metrics)
- **P1:** Lát cắt dọc (Vertical Spike End-to-End: 20 ảnh thử nhanh)
- **P2:** Dữ liệu chuẩn (Gold test set 450+ ảnh, Từ điển >=500 từ, Synth 60k+ dòng)
- **P3:** Khối tiền xử lý 9 bước (A1–A9) & Tách dòng đa giải thuật
- **P4:** Baseline đa engine & Phân tích ma trận nhầm lẫn
- **P5:** Nghiên cứu Ablation (Đóng góp #1 - 8 bảng thực nghiệm khoa học)
- **P6:** Hậu xử lý từ điển có trọng số (Đóng góp #2 - Weighted Levenshtein)
- **P7:** Huấn luyện mô hình nhận dạng (Đóng góp #3 - Fine-tune Tesseract vs CRNN)
- **P8:** Tầng ngôn ngữ (LaoNLP tokenization, Phiên âm Latinh, Dịch máy NLLB)
- **P9:** Ứng dụng học tập Streamlit (Preprocessing Inspector, SM-2 Flashcard)
- **P10:** Báo cáo khoa học & Bộ câu hỏi bảo vệ đồ án
