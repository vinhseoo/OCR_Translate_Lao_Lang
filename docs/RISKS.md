# ⚠️ BẢNG QUẢN TRỊ RỦI RO & BẪY KỸ THUẬT (RISKS & PITFALLS)
**Dự án:** Lao OCR & Language Support

Tài liệu này ghi nhận các rủi ro kỹ thuật nguy hiểm, nguyên nhân gốc rễ và giải pháp phòng ngừa được đúc kết cho dự án OCR tiếng Lào.

---

## 🚨 BẢNG THEO DÕI RỦI RO

| ID | Rủi ro kỹ thuật | Mức độ | Khả năng xảy ra | Nguyên nhân gốc rễ | Biện pháp kiểm soát & Phòng ngừa | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | **Font render sai dấu tổ hợp âm** | 🔴 Nghiêm trọng | Rất cao | Font chữ Lào không có bảng GPOS/GSUB chuẩn, render dấu thanh bị lệch hoặc biến mất. | Kiểm tra bảng ~400 tổ hợp tại P0 trên 12 font bằng `Pillow + libraqm`. Lập Blacklist loại bỏ font lỗi trước khi sinh data ở P2c. | `THEO DÕI P0` |
| **R2** | **Lỗi không đồng nhất byte Unicode (NFC vs NFD)** | 🔴 Nghiêm trọng | Chắc chắn | Thứ tự gõ ký tự kết hợp (phụ âm $\rightarrow$ nguyên âm $\rightarrow$ dấu thanh) khác nhau sinh ra mã byte khác nhau dù nhìn giống nhau. | Hàm `normalize_lao()` bắt buộc ép về NFC + Regex chuẩn hóa trật tự tổ hợp. Unit test xác nhận `cer(s1, s2) == 0`. | `CÀI ĐẶT P0` |
| **R3** | **Morphology xóa mất dấu thanh nhỏ** | 🟠 Cao | Rất cao | Dấu thanh tiếng Lào (như `່`, `້`) là các đốm nhỏ rời rạc. Dùng kernel $\ge 3 \times 3$ làm phép Opening xóa sổ dấu thanh. | Giới hạn kernel ở kích thước $1 \times 1$ hoặc $2 \times 2$ có điều kiện; kiểm chứng định lượng bằng Ablation ở P5. | `LƯU Ý P3` |
| **R4** | **Nhị phân hóa Otsu thất bại dưới bóng đổ** | 🟠 Cao | Cao | Flashcard chụp bằng điện thoại thường bị bóng tay hoặc nguồn sáng lệch góc, Otsu tìm ngưỡng toàn cục sẽ làm cháy/đen chữ. | Triển khai các giải thuật ngưỡng cục bộ (Sauvola, Wolf) có cửa sổ trượt thích ứng. | `LƯU Ý P3` |
| **R5** | **Rò rỉ dữ liệu (Data Leakage)** | 🟠 Cao | Trung bình | Tinh chỉnh siêu tham số tiền xử lý hoặc fine-tune trên toàn bộ dữ liệu khiến kết quả Test ảo tưởng. | Chia tập Dev (30%) và Test (70%) ngay tại P2a; Test set đóng băng tuyệt đối, chỉ dùng để báo cáo cuối cùng. | `LƯU Ý P2` |
| **R6** | **Tesseract chế độ PSM không phù hợp** | 🟡 Trung bình | Cao | Tesseract mặc định (PSM 3) cho cả trang văn bản, áp dụng cho ảnh từ đơn/dòng đơn gây nhận dạng rỗng hoặc sai layout. | Dùng PSM 7 (single line) hoặc PSM 8 (single word) cho ảnh flashcard. | `KIỂM TRA P1` |
| **R7** | **Chi phí huấn luyện mô hình sâu (CRNN/SVTR) quá lớn** | 🟡 Trung bình | Trung bình | Thiếu GPU cục bộ mạnh mẽ làm tắc nghẽn Phase P7. | Viết code tương thích Google Colab / Kaggle T4 GPU (free tier); giới hạn batch size hợp lý. | `DỰ PHÒNG P7` |

---

## 🔍 CHI TIẾT 3 ĐIỂM CHẾT NGƯỜI CẦN TUÂN THỦ

1. **Kiểm tra render font ở P0:** Nếu font dựng dấu sai mà không phát hiện, toàn bộ 60k–100k ảnh tổng hợp ở P2c và cả P7 sẽ huấn luyện trên chữ sai. Đây là lỗi âm thầm và đắt giá nhất.
2. **Gold test set phải xong ở P2 và đóng băng:** Không có bộ kiểm thử sạch, mọi con số cải thiện ở P3, P4, P5, P6 đều vô nghĩa.
3. **Normalize NFC ở mọi điểm tính CER:** Thiếu bước này, CER sẽ cao bất thường do khác mã byte dù chữ nhận dạng đúng 100%.
