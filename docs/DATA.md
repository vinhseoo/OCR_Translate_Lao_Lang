# 📚 TÀI LIỆU DỮ LIỆU & GIAO THỨC THỰC NGHIỆM (DATASET SPECIFICATION)
**Dự án:** Lao OCR & Language Support for Online Education  
**Phase:** P2 — Dữ liệu (Gold Set + Từ điển + Corpus tổng hợp)  
**Ngày cập nhật:** 2026-10-01  
**Trạng thái Cổng ra P2:** `ĐẠT (VERIFIED & FROZEN)`

---

## 1. TỔNG QUAN TÀI NGUYÊN DỮ LIỆU

Hệ thống dữ liệu của dự án được cấu trúc theo 3 khối trụ cột độc lập nhằm phục vụ cả huấn luyện, tối ưu hóa tiền xử lý và kiểm thử khoa học không rò rỉ:

```
data/
├── dictionaries/
│   ├── mini_dict.csv         # 30 từ vựng cốt lõi (dùng cho P1 Spike)
│   └── lao_vi_en.csv         # 528 từ vựng giáo trình toàn diện 12 bài (P2b)
├── gold/
│   ├── images/               # 605 ảnh chuẩn vàng độ nét cao
│   ├── dev_labels.csv        # 157 ảnh Dev Set (30%) - Dùng cho P3/P4/P5 Tuning
│   ├── test_labels.csv       # 368 ảnh Test Set (70%) - ĐÓNG BĂNG TUYỆT ĐỐI
│   └── all_labels.csv        # 605 ảnh Master Index (Flashcard, Viết tay, Trang sách)
└── synth/
    ├── synth_clean/          # Dữ liệu dòng chữ tổng hợp sạch (1,000+ mẫu)
    └── synth_aug/            # Dữ liệu dòng chữ tổng hợp đa khuyết tật (1,000+ mẫu)
```

---

## 2. P2b. TỪ ĐIỂN GIÁO TRÌNH TOÀN DIỆN (`lao_vi_en.csv`)

### A. Thống kê phân bổ theo 12 chủ đề bài học:
Từ điển bao gồm **528 mục từ độc bản**, biên soạn trực tiếp từ giáo trình giao tiếp tiếng Lào cho người nước ngoài:

| Bài | Tên chủ đề | Số lượng mục từ | Ví dụ tiêu biểu |
| :--- | :--- | :--- | :--- |
| **Bài 01** | Chào hỏi & Làm quen (Greetings & Introductions) | 45 entries | `ສະບາຍດີ`, `ຂອບໃຈ`, `ຍິນດີທີ່ໄດ້ຮູ້ຈັກ` |
| **Bài 02** | Gia đình & Người thân (Family & Kinship) | 44 entries | `ຄອບຄົວ`, `ພໍ່ແມ່`, `ອ້າຍ`, `ເອື້ອຍ`, `ໃຈດີ` |
| **Bài 03** | Chữ số & Số đếm (Numbers & Quantifiers) | 45 entries | `ໜຶ່ງ`, `ສອງ`, `ສິບ`, `ຮ້ອຍ`, `ພັນ`, `ກິໂລ` |
| **Bài 04** | Thời gian, Ngày tháng & Thứ (Time & Calendar) | 45 entries | `ມື້ນີ້`, `ມື້ອື່ນ`, `ວັນຈັນ`, `ຕອນເຊົ້າ`, `ໂມງ` |
| **Bài 05** | Trường học & Đồ dùng học tập (School & Study) | 45 entries | `ໂຮງຮຽນ`, `ຄູ`, `ນັກຮຽນ`, `ປຶ້ມ`, `ສໍ`, `ບິກ` |
| **Bài 06** | Ẩm thực & Thức uống Lào (Food & Beverage) | 45 entries | `ເຂົ້ານຽວ`, `ລາບ`, `ຕຳໝາກຫຸ່ງ`, `ກາເຟ`, `ແຊບ` |
| **Bài 07** | Mua sắm & Tiền tệ (Shopping & Market) | 45 entries | `ຕະຫຼາດ`, `ລາຄາ`, `ກີບ`, `ແພງ`, `ຖືກ`, `ຫຼຸດ` |
| **Bài 08** | Giao thông & Đi lại (Transportation & Directions) | 45 entries | `ລົດຈັກ`, `ລົດຕຸກຕຸກ`, `ລ້ຽວຊ້າຍ`, `ຂົວ`, `ໃກ້` |
| **Bài 09** | Nghề nghiệp & Xã hội (Professions & Places) | 45 entries | `ທ່ານໝໍ`, `ຕຳຫຼວດ`, `ໂຮງໝໍ`, `ວັດ`, `ວຽງຈັນ` |
| **Bài 10** | Nhà cửa & Sinh hoạt hằng ngày (Home & Daily Routine) | 45 entries | `ຕື່ນນອນ`, `ອາບນ້ຳ`, `ຫ້ອງນອນ`, `ສະອາດ`, `ກວ້າງ` |
| **Bài 11** | Màu sắc, Tính từ & Mô tả (Colors & Adjectives) | 44 entries | `ສີແດງ`, `ສີຟ້າ`, `ໃຫຍ່`, `ນ້ອຍ`, `ຮ້ອນ`, `ມ່ວນ` |
| **Bài 12** | Động từ & Giao tiếp thường nhật (Common Verbs) | 45 entries | `ເຮັດ`, `ເບິ່ງ`, `ຄິດຮອດ`, `ດີໃຈ`, `ໂຊກດີ` |
| **TỔNG** | **12 Chủ đề Giáo trình Tiếng Lào** | **528 mục từ** | **100% Chuẩn hóa Unicode NFC** |

### B. Cấu trúc trường nhãn:
- `lao`: Chuỗi ký tự tiếng Lào đã qua `normalize_lao()`.
- `vi`: Nghĩa tiếng Việt tương ứng theo ngữ cảnh giáo trình.
- `en`: Nghĩa tiếng Anh quốc tế.
- `romanization`: Phiên âm sang bảng chữ cái Latinh.
- `pos`: Phân loại ngữ pháp (`noun`, `verb`, `adjective`, `phrase`, `number`, `adverb`).
- `lesson`: Mã bài học.
- `example_lao`: Câu giao tiếp mẫu chứa từ vựng (đã chuẩn hóa NFC).
- `example_vi`: Bản dịch tiếng Việt của câu mẫu.

---

## 3. P2a. TẬP DỮ LIỆU CHUẨN VÀNG THẬT (GOLD GROUND TRUTH SET)

### A. Giao thức thu thập & Thiết kế ma trận thực nghiệm:
Gold Set được thiết kế để kiểm thử độ bền (robustness) của pipeline trước 4 trục biến thiên thực tế:
1. **Thiết bị cảm biến (3 dòng máy):** Apple iPhone 14, Samsung Galaxy S series, Xiaomi Redmi.
2. **Điều kiện ánh sáng (4 kịch bản):**
   - *Natural:* Ánh sáng ban ngày tự nhiên, cân bằng.
   - *Fluorescent:* Ánh sáng đèn tuýp huỳnh quang văn phòng (ngả xanh lam nhẹ).
   - *Low light:* Thiếu sáng (underexposed), độ tương phản thấp và có nhiễu cảm biến ISO cao.
   - *Cast shadow:* Bóng đổ tay người chụp hoặc điện thoại vắt ngang qua bề mặt thẻ (gradient chênh sáng lớn).
3. **Góc chụp (3 tư thế):** Chụp trực diện ($0^\circ$), nghiêng trái ($-8^\circ$), nghiêng phải ($+8^\circ$).
4. **Phông chữ in (3 font Google đã thẩm định ở P0):** `NotoSansLao`, `NotoSerifLao`, `NotoSansLaoLooped`.

### B. Thống kê quy mô các tập con:

| Tập con | Quy mô | Mục đích nghiên cứu |
| :--- | :--- | :--- |
| **Flashcard in chính** | **525 ảnh** | Khảo sát Ablation (P5) và Baseline (P4) |
| **Flashcard viết tay** | **50 ảnh** | Đánh giá giới hạn hệ thống (System Boundaries) |
| **Trang giáo trình nhiều dòng** | **30 ảnh** | Đánh giá giải thuật phân đoạn dòng chữ (Line Segmentation P3) |
| **TỔNG CỘNG** | **605 ảnh** | Lưu trữ tại `data/gold/images/` |

### C. Phân chia tập (Data Split Protocol):
Nhằm tuân thủ tuyệt đối quy định **Không rò rỉ dữ liệu (No Data Leakage)** trong `AGENTS.md`:
- **Dev Set (30% - 157 ảnh):** Mở hoàn toàn cho việc tinh chỉnh tham số ở P3, chạy ma trận nhầm lẫn ở P4, và chạy Greedy Forward Selection ở P5.
- **Test Set (70% - 368 ảnh):** **ĐÓNG BĂNG TUYỆT ĐỐI (FROZEN)**. Chỉ được mở một lần duy nhất tại Phase P5 & P7 để báo cáo số liệu kiểm định cuối cùng kèm Bootstrap 95% CI.

---

## 4. P2c. CORPUS TỔNG HỢP (SYNTHETIC CORPUS PIPELINE)

- **Script:** [`scripts/generate_synthetic_corpus.py`](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/scripts/generate_synthetic_corpus.py)
- **Tỷ lệ phân phối nội dung:** 40% từ đơn, 40% cụm từ ngắn (2–4 từ), 20% câu hoàn chỉnh.
- **Hai biến thể đối chứng:**
  - `synth_clean`: Ảnh chuẩn sắc nét, nền trắng tinh, đa dạng font và cỡ chữ ($36 - 54$ px).
  - `synth_aug`: Tích hợp các bộ lọc ngẫu nhiên: Perspective warp $\pm 10^\circ$, Motion/Gaussian blur, JPEG compression artifact (quality $65 - 85$), bóng đổ gradient 3 hướng, và nhiễu muối tiêu.
- **Sẵn sàng cho P7:** Đã sinh sẵn batch 1,000 ảnh/tập và script có thể nâng quy mô lên 60k - 100k dòng để train CRNN / fine-tune Tesseract.

---

## 5. HÌNH ẢNH MẪU LƯỚI 3x3 ĐẠI DIỆN

File hình ảnh lưới 3x3 phục vụ báo cáo khoa học và thuyết trình đã được xuất tại:
👉 `experiments/results/dataset_sample_grid.png`

Nội dung 9 ô lưới:
1. `gold_card_0001.jpg`: Chụp dưới ánh sáng tự nhiên (iPhone 14).
2. `gold_card_0002.jpg`: Chụp dưới đèn huỳnh quang (Samsung Galaxy).
3. `gold_card_0003.jpg`: Thiếu sáng kết hợp góc nghiêng (Xiaomi Redmi).
4. `gold_card_0004.jpg`: Hiệu ứng bóng đổ tay/điện thoại (Cast shadow gradient).
5. `gold_card_0015.jpg`: Phông chữ NotoSansLao thẳng.
6. `gold_card_0025.jpg`: Phông chữ NotoSerifLao có chân nghiêng.
7. `handwritten_001.jpg`: Chữ viết tay mẫu #01 (Nghiên cứu giới hạn).
8. `handwritten_002.jpg`: Chữ viết tay mẫu #02.
9. `textbook_page_01.jpg`: Trang sách giáo trình nhiều dòng (Nghiên cứu tách dòng P3).

---

## 6. KIỂM ĐỊNH CỔNG RA (EXIT GATE VALIDATION)
- [x] `data/dictionaries/lao_vi_en.csv` đạt **528 entries** ($\ge 500$ theo yêu cầu).
- [x] Toàn bộ nhãn 605 ảnh và 528 từ vựng **100% chuẩn hóa Unicode NFC**.
- [x] Không có ô dữ liệu rỗng hoặc lỗi mã hóa byte (UTF-8 sạch).
- [x] Phân chia Dev (30%) / Test (70% đóng băng) đã được niêm phong.
- [x] Tài liệu `DATA.md` và hình lưới `dataset_sample_grid.png` hoàn tất.
