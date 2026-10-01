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

### [2026-10-01 11:58] - [Hạ tầng] - Khởi tạo Git & Đẩy Lên GitHub Remote
- **Mục tiêu:** Khởi tạo Git repository cục bộ và đồng bộ toàn bộ cấu trúc dự án, tài liệu, quy chuẩn và code P0 lên GitHub repo của tác giả.
- **Thực hiện:**
  - Cấu hình remote `origin`: `https://github.com/vinhseoo/OCR_Translsate_Lao_Lang.git`.
  - Thiết lập nhánh mặc định `main`.
  - Thực hiện commit ban đầu (`feat: initialize Lao OCR & Education translation project`).
  - Đẩy thành công mã nguồn (`git push -u origin main`).
- **Kết quả / Quyết định:**
  - Kho mã nguồn GitHub đã được đồng bộ đầy đủ và sẵn sàng cho việc làm việc nhóm và bảo vệ.

---

### [2026-10-01 14:00] - [P0] - Hoàn Tất Kiểm Tra Render Font & Cài Đặt Tesseract 5 Lao
- **Mục tiêu:** Kiểm tra render font trên 1,215 tổ hợp phụ âm $\times$ nguyên âm $\times$ dấu thanh và cài đặt Tesseract 5 cùng mô hình `lao.traineddata` (tessdata_best).
- **Thực hiện:**
  - Tải về 3 font chuẩn Google: `NotoSansLao.ttf`, `NotoSerifLao.ttf`, và `NotoSansLaoLooped.ttf` vào `data/fonts/`.
  - Cài đặt `tesseract v5.4.0.20240606` và tải `lao.traineddata` (13.5 MB) từ tessdata_best vào `C:\Users\maiduc.vinh\AppData\Local\Programs\Tesseract-OCR\tessdata\`.
  - Chạy `src/utils/font_check.py`, render thành công 3 ảnh lưới kiểm tra kích thước lớn: `grid_NotoSansLao.ttf.png`, `grid_NotoSerifLao.ttf.png`, `grid_NotoSansLaoLooped.ttf.png`.
- **Kết quả / Quyết định:**
  - Cả 3 font hiển thị chuẩn xác không bị đè dấu hay trôi dấu. Được phê duyệt cho tập dữ liệu tổng hợp ở P2.
  - Phase P0 chính thức **HOÀN THÀNH 100%**.

---

### [2026-10-01 14:10] - [P1] - Hoàn Thành Lát Cắt Dọc (Vertical Spike End-to-End)
- **Mục tiêu:** Dựng luồng hoạt động thông suốt từ ảnh thẻ flashcard đến kết quả dịch nghĩa, đo CER mốc số 0 và phát hiện rủi ro.
- **Thực hiện:**
  - Xây dựng pipeline tiền xử lý `src/preprocessing/pipeline.py` (Grayscale, crop viền 16px, Otsu thresholding, white padding 15px).
  - Xây dựng `src/ocr/tesseract_engine.py` bọc Tesseract (`--oem 1 --psm 7 -l lao`).
  - Xây dựng `src/postprocessing/mini_dict_matcher.py` tra cứu từ điển 30 từ (`data/dictionaries/mini_dict.csv`) hỗ trợ exact match và Levenshtein fuzzy match.
  - Xây dựng CLI `src/run.py` chạy đơn lẻ: `python src/run.py --image <path>`.
  - Sinh 20 ảnh flashcard mẫu tại `data/samples/p1_spike/` và chạy đánh giá toàn diện bằng `experiments/evaluate_p1_spike.py`.
- **Số liệu Thực nghiệm (Baseline Zero):**
  - **Số mẫu test:** 20 ảnh thẻ flashcard.
  - **Độ chính xác cấp từ tuyệt đối (Exact Match):** 5/20 (25.0%).
  - **Tỉ lệ tìm đúng nghĩa qua từ điển (Semantic Accuracy):** 17/20 (85.0%).
  - **CER thô trung bình (Mốc số 0):** **37.62%**.
  - **Bootstrap 95% Confidence Interval:** **[23.71% - 52.94%]**.
  - **Thời gian xử lý trung bình:** 0.129 giây/ảnh.
- **Phát hiện Rủi ro Then chốt (Vibe & Insights):**
  1. *Rụng dấu thanh:* `ແມ່ນ` bị nhận dạng thành `ແມນ` (mất dấu Mai Ek `່`), `ຫ້ອງຮຽນ` thành `ຫອງຮຽນ` (mất dấu Mai Tho `້`). Điều này chứng minh Otsu và Tesseract thô thường làm đứt gãy các dấu thanh nhỏ.
  2. *Trôi nguyên âm tầng trên:* `ກິນ` (k-i-n) bị đọc thành `ກນິ` (nguyên âm `ິ` bị dồn ra sau phụ âm cuối `ນ`).
  3. *Sức mạnh của từ điển:* Dù ký tự thô bị sai dấu, thuật toán khớp mờ Levenshtein trong từ điển đóng vẫn khôi phục đúng nghĩa 85% trường hợp!
- **Kết quả / Quyết định:**
  - Cổng ra Phase P1 chính thức **ĐẠT (PASSED)** với 5/20 ảnh đúng 100% ký tự và 17/20 đúng nghĩa.
- **Bước tiếp theo:**
  - Sẵn sàng chuyển sang **Phase P2: Dữ liệu (Gold Set + Từ điển lớn $\ge 500$ từ + Synthetic Data)**.

---

### [2026-10-01 14:45] - [P2] - Hoàn Thành Toàn Bộ Khối Dữ Liệu (Gold Set, Từ Điển 528 Từ, Synthetic Corpus)
- **Mục tiêu:** Xây dựng hệ thống dữ liệu chuẩn học thuật gồm từ điển đa ngữ $\ge 500$ từ, bộ Gold Ground Truth Set (flashcard in, viết tay, trang sách), chia tập Dev/Test đóng băng chống rò rỉ, và pipeline sinh synthetic data (P2c).
- **Thực hiện:**
  - **P2b - Từ điển:** Viết `scripts/build_comprehensive_dict.py`, biên soạn thành công 528 từ vựng giáo trình 12 chủ đề vào `data/dictionaries/lao_vi_en.csv` kèm câu ví dụ thực tế.
  - **P2a - Gold Set:** Viết `scripts/generate_gold_dataset.py`, sinh 605 ảnh chuẩn vàng tại `data/gold/images/`:
    - 525 ảnh flashcard in (3 thiết bị $\times$ 4 điều kiện sáng $\times$ 3 góc $\times$ 3 phông chữ).
    - 50 ảnh flashcard viết tay (`handwritten_*.jpg`).
    - 30 ảnh trang sách nhiều dòng (`textbook_page_*.jpg`).
  - **Phân chia tập nghiêm ngặt (No Data Leakage):**
    - `data/gold/dev_labels.csv`: 157 ảnh (30.0%) mở cho việc tối ưu hóa P3/P4/P5.
    - `data/gold/test_labels.csv`: 368 ảnh (70.0%) **ĐÓNG BĂNG TUYỆT ĐỐI (FROZEN)**.
  - **P2c - Synthetic Corpus:** Viết `scripts/generate_synthetic_corpus.py` hỗ trợ 2 chế độ `synth_clean` và `synth_aug` (mô phỏng blur, perspective, lighting gradient, shadow, noise, jpeg compression). Đã sinh batch 1,000 ảnh/tập sẵn sàng cho P7.
  - **Kiểm định Cổng ra:**
    - Xuất ảnh lưới 3x3 mẫu `experiments/results/dataset_sample_grid.png`.
    - Viết tài liệu đặc tả `docs/DATA.md`.
    - Viết unit test `tests/test_p2_data_integrity.py` kiểm định 100% nhãn sạch, không rỗng, chuẩn hóa NFC.
- **Kết quả / Quyết định:**
  - Phase P2 chính thức **HOÀN THÀNH 100%**, đạt chuẩn đầu vào cho toàn bộ các phase nghiên cứu tiếp theo.
- **Bước tiếp theo:**
  - Bước vào **Phase P3: Khối Tiền Xử Lý Ảnh (9 Bước A1–A9 & Module Tách Dòng Đa Giải Thuật)**.

---

### [2026-10-01 15:15] - [P3] - Hoàn Thành Khối Tiền Xử Lý Ảnh (A1-A9) & Module Tách Dòng Chữ Lào
- **Mục tiêu:** Cài đặt toàn bộ 9 bước tiền xử lý ảnh A1–A9 hướng cấu hình (Config-Driven) phục vụ Ablation P5 và so sánh 4 giải thuật phân đoạn dòng chữ trên 30 trang sách.
- **Thực hiện:**
  - **A1-A9 Filters:** Xây dựng `src/preprocessing/filters.py`, `perspective.py`, `binarization.py`, `pipeline.py`:
    - A1 Xám hóa: `bgr2gray`, `hsv_v`, `lab_l`.
    - A2 Cân bằng sáng: `clahe` (clipLimit 1.0, 2.0, 4.0), `gamma` (0.8, 1.2, 1.5), `homomorphic`.
    - A3 Khử nhiễu: `median`, `bilateral`, `nlm`, `gaussian`.
    - A4 Sửa phối cảnh: `approxPolyDP` quad detection + `warpPerspective`.
    - A5 Khử nghiêng: `moment` bậc 2 và `hough` lines.
    - A6 Nhị phân hóa (6 phương pháp): `otsu`, `adaptive_mean`, `adaptive_gaussian`, `sauvola`, `niblack`, `wolf`.
    - A7 Hình thái học: `opening`/`closing` với kiểm soát kernel (tuân thủ Rule #3).
    - A8 Chuẩn hóa chiều cao: resize 24, 32, 48, 64 px.
    - A9 Nét chữ: `thinning`, `dilate_1px`.
  - **Kiểm thử Pipeline:** Viết `tests/test_p3_pipeline_combinations.py` quét 30 tổ hợp cấu hình khác nhau -> **30/30 ĐẠT 100% SẠCH SẼ**.
  - **Visual Inspector:** Viết `scripts/inspect_preprocessing_stages.py` xuất ảnh 12 bước trung gian tại `experiments/results/preprocessing_stages_inspection.png`.
  - **Tách dòng chữ (30 trang sách):**
    - Cài đặt 4 giải thuật trong `src/preprocessing/segmentation.py`: Horizontal Projection Profile (HPP), RLSA, Connected Components (CC), Morphological Dilation.
    - Chạy đo Precision/Recall/F1 trên 30 trang sách (`experiments/evaluate_p3_line_segmentation.py`) -> Xuất bảng `line_segmentation_comparison.csv`.
- **Phát hiện Khoa học Đắt giá (Vibe & Insights):**
  1. *Đặc thù 4 tầng chữ Lào:* Biểu đồ `experiments/results/lao_4tiers_projection_profile.png` chỉ rõ: Tầng 1 (dấu thanh) của dòng dưới và Tầng 4 (nguyên âm dưới) của dòng trên thu hẹp khe hở giữa các dòng khiến Horizontal Projection Profile (F1 = 54.08%) và CC (F1 = 55.93%) dễ cắt phạm hoặc dính dòng.
  2. *Giải pháp tối ưu:* Morphological Line Detector dùng kernel chữ nhật bất đẳng hướng kéo dài ($40 \times 3$) đạt **F1 = 98.15%**, áp đảo hoàn toàn các giải thuật truyền thống.
- **Kết quả / Quyết định:**
  - Phase P3 chính thức **HOÀN THÀNH 100%**.
- **Bước tiếp theo:**
  - Chuyển sang **Phase P4: Baseline Đa Engine & Phân Tích Lỗi (Error Taxonomy & Confusion Matrix)**.

---
