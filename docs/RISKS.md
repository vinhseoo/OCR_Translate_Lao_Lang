# ⚠️ BẢNG QUẢN TRỊ RỦI RO & BẪY KỸ THUẬT (RISKS & PITFALLS)
**Dự án:** Lao OCR & Language Support

Tài liệu này ghi nhận các rủi ro kỹ thuật nguy hiểm, nguyên nhân gốc rễ và giải pháp phòng ngừa được đúc kết cho dự án OCR tiếng Lào.

---

## 🚨 BẢNG THEO DÕI RỦI RO

| ID | Rủi ro kỹ thuật | Mức độ | Khả năng xảy ra | Nguyên nhân gốc rễ | Biện pháp kiểm soát & Phòng ngừa | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | **Font render sai dấu tổ hợp âm** | 🔴 Nghiêm trọng | Rất cao | Font chữ Lào không có bảng GPOS/GSUB chuẩn, render dấu thanh bị lệch hoặc biến mất. | Đã tải & thẩm định 3 font Google: `NotoSansLao`, `NotoSerifLao`, `NotoSansLaoLooped` qua 1,215 tổ hợp (P0). | `ĐÃ GIẢI QUYẾT (P0)` |
| **R2** | **Lỗi không đồng nhất byte Unicode (NFC vs NFD)** | 🔴 Nghiêm trọng | Chắc chắn | Thứ tự gõ ký tự kết hợp (phụ âm $\rightarrow$ nguyên âm $\rightarrow$ dấu thanh) khác nhau sinh ra mã byte khác nhau dù nhìn giống nhau. | Hàm `normalize_lao()` ép NFC + hoán vị trật tự. Đạt CER = 0.0 qua bài test P0. | `ĐÃ GIẢI QUYẾT (P0)` |
| **R3** | **Morphology & Otsu làm rụng dấu thanh** | 🟠 Cao | Rất cao | Dấu thanh tiếng Lào (như `່`, `້`) là các đốm nhỏ rời rạc. Quan sát ở P1: `ແມ່ນ` bị nhận dạng thành `ແມນ`, `ຫ້ອງຮຽນ` thành `ຫອງຮຽນ`. | Cần Sauvola/Wolf ở P3, cấm kernel opening lớn; P6 bù trừ bằng Weighted Levenshtein. | `XÁC NHẬN TẠI P1` |
| **R4** | **Trôi nguyên âm tầng trên sang phụ âm cuối** | 🟠 Cao | Rất cao | Chữ có cấu trúc CVC như `ກິນ` (k-i-n) bị Tesseract đẩy nguyên âm `ິ` ra sau `ນ` thành `ກນິ`. | Cần quy tắc n-gram / lexicon snap hoặc fine-tune Tesseract ở P7. | `PHÁT HIỆN TẠI P1` |
| **R5** | **Nhiễu khung viền thẻ đánh lừa Tesseract** | 🟡 Trung bình | Cao | Khung viền đen của flashcard bị nhầm thành ký tự. | Thêm bước cắt viền (crop margin) và bổ sung padding trắng trong `pipeline.py`. | `ĐÃ XỬ LÝ (P1)` |
| **R6** | **Tesseract chế độ PSM không phù hợp** | 🟡 Trung bình | Cao | Tesseract mặc định (PSM 3) cho trang văn bản; từ ngắn (như `ຄູ`, `ບໍ່`) rất nhạy cảm với PSM. | Đã chốt PSM 7 (single line) có padding trắng. | `ĐÃ XỬ LÝ (P1)` |
| **R7** | **Chi phí huấn luyện mô hình sâu (CRNN/SVTR) quá lớn** | 🟡 Trung bình | Trung bình | Thiếu GPU cục bộ mạnh mẽ làm tắc nghẽn Phase P7. | Viết code tương thích Google Colab / Kaggle T4 GPU (free tier); giới hạn batch size hợp lý. | `DỰ PHÒNG P7` |

---

## 🔍 CHI TIẾT 3 ĐIỂM CHẾT NGƯỜI CẦN TUÂN THỦ

1. **Kiểm tra render font ở P0:** Nếu font dựng dấu sai mà không phát hiện, toàn bộ 60k–100k ảnh tổng hợp ở P2c và cả P7 sẽ huấn luyện trên chữ sai. Đây là lỗi âm thầm và đắt giá nhất.
2. **Gold test set phải xong ở P2 và đóng băng:** Không có bộ kiểm thử sạch, mọi con số cải thiện ở P3, P4, P5, P6 đều vô nghĩa.
3. **Normalize NFC ở mọi điểm tính CER:** Thiếu bước này, CER sẽ cao bất thường do khác mã byte dù chữ nhận dạng đúng 100%.
