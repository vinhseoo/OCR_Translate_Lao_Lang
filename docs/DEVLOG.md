# 📝 NHẬT KÝ PHÁT TRIỂN & TRUY VẾT DỰ ÁN (DEVLOG & VIBE LOG)
**Dự án:** Lao OCR & Language Support for Online Education  
**Mục đích:** Ghi lại dòng suy nghĩ, quyết định kỹ thuật, thử nghiệm thất bại/thành công, nhật ký từng bước thực hiện và truy vết toàn diện quá trình xây dựng hệ thống.

---

## 📌 QUY ƯỚC VIẾT LOG
Mỗi khi bắt đầu hoặc hoàn thành một công việc, thêm một entry theo cấu trúc:
```markdown
### [YYYY-MM-DD HH:MM] - [Phase Px] - [Tiêu đề công việc]
- **Mục tiêu:** ...
- **Thực hiện:** ...
- **Vấn đề / Phát hiện (Vibe & Insights):** ...
- **Kết quả / Quyết định:** ...
- **Bước tiếp theo:** ...
```

---

## 📜 CÁC BẢN GHI (ENTRIES)

### [2026-10-01 11:35] - [P0] - Khởi tạo Cấu trúc Dự án & Bộ Quy chuẩn
- **Mục tiêu:** Thiết lập nền móng dự án với đầy đủ tài liệu quy chuẩn (`AGENTS.md`), kế hoạch tổng thể 11 phase (`docs/PROJECT_PLAN.md`), bảng tiến độ (`docs/PROGRESS_TRACKER.md`), và nhật ký truy vết (`docs/DEVLOG.md`).
- **Thực hiện:**
  - Soạn thảo bộ quy tắc vàng về tiếng Lào: Bắt buộc chuẩn hóa Unicode NFC, xử lý tổ hợp phụ âm + nguyên âm + dấu thanh, xử lý 5 nguyên âm đứng trước (`ເ ແ ໂ ໃ ໄ`), tuyệt đối kiểm tra font trước khi sinh dữ liệu.
  - Định hình quy chuẩn thực nghiệm: Seed cố định, bootstrap 95% CI cho CER, không data leakage.
  - Phác thảo cấu trúc thư mục chuẩn hóa: `src/`, `data/`, `experiments/`, `docs/`, `app/`, `tests/`.
- **Vấn đề / Phát hiện (Vibe & Insights):**
  - Chữ Lào là ngôn ngữ có tài nguyên số tương đối hạn chế (low-resource language) so với tiếng Thái và Việt. Tesseract mô hình chuẩn thường rất dễ nhầm giữa các phụ âm có nét tương đồng (như `ດ` và `ຄ`, `ບ` và `ປ`).
  - Hậu xử lý từ điển với Weighted Levenshtein là chìa khóa vàng cho bài toán flashcard từ vựng.
- **Kết quả / Quyết định:**
  - Khởi tạo thành công bộ tài liệu quản trị và quy chuẩn dự án.
### [2026-10-01 11:42] - [P0] - Hoàn thành Chuẩn hóa Unicode Lao, Metrics CER & Unit Tests
- **Mục tiêu:** Cài đặt module `normalize_lao` xử lý combining marks và module `metrics.py` (CER, WER, Word Acc, Bootstrap CI), đạt Cổng ra P0.
- **Thực hiện:**
  - Viết `src/preprocessing/normalize.py`: Ép Unicode NFC 2 lớp, xử lý hoán vị dấu thanh đứng trước nguyên âm (lỗi gõ phổ biến ở tiếng Lào), loại bỏ Zero-Width Space.
  - Viết `src/evaluation/metrics.py`: Cài đặt Levenshtein Distance thuần túy (không phụ thuộc thư viện ngoài), CER, WER, Word Accuracy, và thuật toán Bootstrap Resampling 95% Confidence Interval (hỗ trợ fallback pure Python khi chưa có NumPy).
  - Viết `tests/test_normalize_and_metrics.py`: Test trường hợp 2 chuỗi cùng ký tự nhưng khác trật tự byte Unicode do gõ dấu ngược.
  - Chạy kiểm thử thành công: `✅ MỌI BÀI TEST P0 ĐÃ ĐẠT 100%! CỔNG RA P0 CHUẨN XÁC.`
  - Sinh từ điển mini 30 từ tại `data/dictionaries/mini_dict.csv` và script `src/utils/font_check.py` sinh ~400 tổ hợp phụ âm x nguyên âm x dấu thanh.
- **Vấn đề / Phát hiện (Vibe & Insights):**
  - Môi trường Windows console mặc định dùng `cp1252`, khi in ký tự Unicode (emoji hoặc tiếng Việt) sẽ gây lỗi `UnicodeEncodeError`. Đã xử lý chủ động bằng `sys.stdout.reconfigure(encoding="utf-8")`.
  - Hàm `metrics.py` được thiết kế có fallback thư viện chuẩn, giúp code chạy được ngay cả trên môi trường Python tối giản mà không bị crash.
- **Kết quả / Quyết định:**
  - Cổng ra số 1 của P0 (`cer() == 0` cho 2 chuỗi khác tổ hợp byte) chính thức **ĐẠT (PASSED)**.
- **Bước tiếp theo:**
  - Tiếp tục hoàn thiện P0 (chuẩn bị file font Lao và tải `lao.traineddata`), sau đó tiến hành Phase P1 (Spike End-to-End với 20 ảnh mẫu).

---
