# 📊 BẢNG THEO DÕI TIẾN ĐỘ DỰ ÁN (PROGRESS TRACKER)
**Cập nhật lần cuối:** 2026-10-01  
**Trạng thái tổng thể:** `KHỞI TẠO DỰ ÁN (SETUP)`

---

## TỔNG QUAN CÁC GIAI ĐOẠN

| Phase | Tên giai đoạn | Trọng số thời gian | Trạng thái | Cổng ra (Exit Gate) |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | Nền móng & Thước đo | ~10h | ✅ `COMPLETED` | ĐẠT 100% |
| **P1** | Lát cắt dọc (Spike End-to-End) | ~10h | ✅ `COMPLETED` | ĐẠT (5/20 ảnh đúng 100%, 17/20 đúng nghĩa) |
| **P2** | Dữ liệu (Gold Set + Từ điển + Synth) | ~34h | ✅ `COMPLETED` | ĐẠT (528 từ, 605 ảnh, Đóng băng Test 70%) |
| **P3** | Khối tiền xử lý ảnh (A1–A9) | ~28h | ✅ `COMPLETED` | ĐẠT (30 cấu hình sạch, F1 tách dòng 98.15%) |
| **P4** | Baseline đa engine & Error Analysis | ~22h | ✅ `COMPLETED` | ĐẠT (PSM 7 tối ưu, 131 confusion pairs, Taxonomy) |
| **P5** | Nghiên cứu Ablation (Đóng góp #1) | ~24h | ✅ `COMPLETED` | ĐẠT (8 bảng số liệu, Golden Rule #3, Optimal YAML) |
| **P6** | Hậu xử lý từ điển có trọng số (#2) | ~20h | ✅ `COMPLETED` | ĐẠT (Weighted Levenshtein p<0.05, Snap +25.48%) |
| **P7** | Huấn luyện mô hình nhận dạng (#3) | ~34h | ✅ `COMPLETED` | ĐẠT (LaoCRNN 28.12% CER, +Snap đạt 85.35% Acc) |
| **P8** | Tầng ngôn ngữ (Tách từ & Dịch) | ~20h | ✅ `COMPLETED` | ĐẠT (Trie F1 70.37%, 1,200 từ, E2E 51.5ms) |
| **P9** | Ứng dụng Streamlit hoàn chỉnh | ~20h | ⏳ `IN_PROGRESS` | Sắp thực hiện |
| **P10** | Báo cáo & Bộ câu hỏi bảo vệ | ~24h | ⚪ `NOT_STARTED` | Chưa hoàn thành |

---

## CHECKLIST CHI TIẾT TỪNG PHASE

### 🏁 Phase P0: Nền móng & Thước đo
- [x] Thiết lập cấu trúc thư mục, môi trường, thư viện (`requirements.txt`, `.gitignore`).
- [x] Tải model `lao.traineddata` (tessdata_best) và cấu hình Tesseract 5 (`v5.4.0`).
- [x] Tải và thẩm định 3 font chuẩn Google: `NotoSansLao`, `NotoSerifLao`, `NotoSansLaoLooped`.
- [x] Xây dựng script kiểm tra render font tiếng Lào trên 1,215 tổ hợp (`src/utils/font_check.py`).
- [x] Render trực quan lưới tổ hợp 3 font ra ảnh PNG tại `experiments/results/grid_*.png`.
- [x] Xây dựng module chuẩn hóa `src/preprocessing/normalize.py` (NFC + chuẩn hóa combining marks).
- [x] Bộ Unit test cho `normalize.py` (`tests/test_normalize_and_metrics.py`).
- [x] Xây dựng module đánh giá `src/evaluation/metrics.py` (CER, WER, Word Acc, Bootstrap 95% CI).
- [x] Cấu hình thực nghiệm `experiments/configs/base_config.yaml`.
- **Cổng ra P0:**
  - [x] `cer()` trả về 0 cho hai chuỗi cùng nội dung khác tổ hợp byte (ĐÃ ĐẠT QUA UNIT TEST).
  - [x] Cả 3 font kiểm định hiển thị dấu thanh và nguyên âm tầng trên/dưới chính xác.

---

### ⚡ Phase P1: Lát cắt dọc (Vertical Spike)
- [x] Chuẩn bị 20 ảnh test nhanh bằng script sinh thẻ flashcard (`scripts/generate_p1_sample_cards.py`).
- [x] Xây dựng pipeline tối thiểu: BGR2GRAY + Crop viền + Otsu binarization + White padding (`src/preprocessing/pipeline.py`).
- [x] Tesseract wrapper OCR với `--oem 1 --psm 7 -l lao` (`src/ocr/tesseract_engine.py`).
- [x] Xây dựng từ điển mini 30 từ (`data/dictionaries/mini_dict.csv`) và module matcher (`src/postprocessing/mini_dict_matcher.py`).
- [x] CLI `src/run.py`: `python src/run.py --image <path>` in ra text Lào + phiên âm + nghĩa + độ tin cậy.
- [x] Script đánh giá tự động `experiments/evaluate_p1_spike.py` xuất chi tiết ra `experiments/results/p1_spike_results.csv`.
- **Cổng ra P1:**
  - [x] $\ge 5/20$ ảnh cho kết quả đúng chính xác tuyệt đối cấp ký tự (Đạt 5/20, tỷ lệ tìm đúng nghĩa qua từ điển đạt 17/20 = 85%).
  - [x] Đo CER thô làm mốc số 0 (Baseline Zero): **37.62%** [95% CI: 23.71% - 52.94%].
  - [x] Cập nhật `docs/RISKS.md` các phát hiện then chốt về lỗi rụng dấu thanh, trôi nguyên âm tầng trên.

---

### 📦 Phase P2: Dữ liệu (Gold Set + Từ điển + Synthetic)
- [x] Biên soạn từ điển giáo trình toàn diện 12 bài `data/dictionaries/lao_vi_en.csv` (**528 mục từ** $\ge 500$ entries).
- [x] Sinh bộ Gold Set chuẩn vàng 605 ảnh tại `data/gold/images/`:
  - 525 ảnh flashcard in đa dạng: 3 thiết bị $\times$ 4 điều kiện sáng $\times$ 3 góc $\times$ 3 phông.
  - 50 ảnh flashcard viết tay (`handwritten_*.jpg`).
  - 30 ảnh trang sách giáo trình nhiều dòng (`textbook_page_*.jpg`).
- [x] Phân chia tập khoa học chống rò rỉ:
  - **Dev Set (30% - 157 ảnh)**: Dành cho tiền xử lý và tuning P3/P4/P5.
  - **Test Set (70% - 368 ảnh)**: **ĐÓNG BĂNG TUYỆT ĐỐI (FROZEN)**.
- [x] Xây dựng pipeline sinh dữ liệu tổng hợp `scripts/generate_synthetic_corpus.py` (tạo `synth_clean` và `synth_aug`).
- [x] Xuất ảnh lưới 3x3 mẫu `experiments/results/dataset_sample_grid.png`.
- [x] Viết tài liệu đặc tả dữ liệu và giao thức thực nghiệm `docs/DATA.md`.
- [x] Unit test kiểm định toàn vẹn dữ liệu `tests/test_p2_data_integrity.py` đạt 100%.
- **Cổng ra P2:**
  - [x] Toàn bộ nhãn 100% chuẩn hóa Unicode NFC, không ô rỗng, mã hóa UTF-8 sạch.
  - [x] Tập Test Set được đóng băng nghiêm ngặt.

---

### 🛠️ Phase P3: Khối tiền xử lý ảnh
- [x] A1: Module xám hóa (`bgr2gray`, `hsv_v`, `lab_l`).
- [x] A2: Module cân bằng sáng (`clahe`, `gamma`, `homomorphic`).
- [x] A3: Module khử nhiễu (`median`, `bilateral`, `nlm`, `gaussian`).
- [x] A4: Module sửa phối cảnh (`approxPolyDP` quad detection + `warpPerspective`).
- [x] A5: Module khử nghiêng (`moment`, `hough`).
- [x] A6: Module nhị phân hóa (6 phương pháp: `otsu`, `adaptive_mean`, `adaptive_gaussian`, `sauvola`, `niblack`, `wolf`).
- [x] A7: Module hình thái học có kiểm soát (Opening/Closing với kiểm soát kernel).
- [x] A8: Chuẩn hóa chiều cao dòng (24, 32, 48, 64 px).
- [x] A9: Làm mảnh/dày nét (`thinning`, `dilate_1px`).
- [x] Module tách dòng trên tập 30 trang sách (HPP, RLSA, Connected Components, Morphological Line Detector).
- **Cổng ra P3:**
  - [x] Pipeline cấu hình qua YAML chạy sạch với **30 tổ hợp cấu hình** (`tests/test_p3_pipeline_combinations.py`).
  - [x] Xuất ảnh trực quan hóa 12 bước trung gian tại `experiments/results/preprocessing_stages_inspection.png`.
  - [x] Bảng so sánh 4 phương pháp tách dòng tại `experiments/results/line_segmentation_comparison.csv` (Morphological detector đạt **98.15% F1**).
  - [x] Xuất biểu đồ chẩn đoán cấu trúc 4 tầng chữ Lào tại `experiments/results/lao_4tiers_projection_profile.png`.

---

### 🔍 Phase P4: Baseline đa engine & Phân tích lỗi (ĐÃ HOÀN THÀNH - COMPLETED)
- [x] Đánh giá Tesseract gốc trên Dev Set (quét các PSM: 6, 7, 8, 11, 13) $\rightarrow$ PSM 7 tối ưu nhất cho flashcard dòng đơn (CER 62.37% [56.91% - 67.56%]).
- [x] Đánh giá PaddleOCR (Mobile Multilingual) $\rightarrow$ CER 88.50%, thiếu khối ký tự Lao Unicode trong từ điển rec.
- [x] Kiểm định EasyOCR v1.7 $\rightarrow$ CER 100.00% (xác nhận không hỗ trợ tiếng Lào).
- [x] Đánh giá Cloud OCR API (Google Cloud Vision OCR) làm trần thương mại tham chiếu $\rightarrow$ CER 4.20%, Word Acc 91.50%.
- [x] Đánh giá Multimodal VLM (GPT-4o/Claude 3.5) làm trần trên lý thuyết $\rightarrow$ CER 2.10%, Word Acc 96.00%.
- [x] Xây dựng Confusion Matrix cấp ký tự qua Levenshtein Backtracking $\rightarrow$ trích xuất `experiments/results/confusion_pairs.csv` (131 cặp nhầm lẫn thực nghiệm, tính chi phí $Cost \in [0.3, 1.0]$ sẵn sàng cho P6).
- [x] Phân loại hệ thống 5 nhóm lỗi (Error Taxonomy) qua `experiments/results/p4_error_taxonomy.csv` (Nhóm 1: 2.02%, Nhóm 2: 23.17%, Nhóm 3: 5.04%, Nhóm 4: 58.06%, Nhóm 5: 11.71%).
- [x] Soạn thảo báo cáo phân tích lỗi chuyên sâu `docs/ERROR_ANALYSIS.md`.
- [x] Unit test kiểm định artifact P4 `tests/test_p4_outputs.py` đạt 100% (5/5 tests passed).
- **Cổng ra P4:**
  - [x] Bảng 1 (PSM scan) tại `experiments/results/p4_psm_scan_results.csv` và Bảng 2 (Engine comparison) tại `experiments/results/p4_engine_comparison.csv` đầy đủ CI 95%.
  - [x] File ma trận nhầm lẫn `confusion_pairs.csv` sẵn sàng nạp thẳng vào P6.
  - [x] Báo cáo chi tiết `docs/ERROR_ANALYSIS.md` hoàn chỉnh.

---

### 🔬 Phase P5: Nghiên cứu Ablation (ĐÃ HOÀN THÀNH - COMPLETED)
- [x] Viết `experiments/run_ablation.py` tự động hóa 100% với xử lý đa luồng trên 16 CPU cores.
- [x] Bảng 3: So sánh 6 phương pháp nhị phân hóa (`p5_table3_binarization.csv` + biểu đồ `ablation_table3_binarization.png`).
- [x] Bảng 4: Leave-one-out từng bước A1–A9 kèm CI 95% (`p5_table4_leave_one_out.csv` + `ablation_table4_leave_one_out.png`). Phát hiện hiện tượng lệch trục của Moment Deskew trên flashcard dòng đơn.
- [x] Bảng 5: Greedy forward selection tìm cấu hình tối ưu (`p5_table5_forward_selection.csv`).
- [x] Bảng 6: Kiểm chứng quy tắc bất di bất dịch Lao Golden Rule #3 về kích thước kernel hình thái học (`p5_table6_morphology_kernel.csv` + `ablation_table6_morphology_kernel.png`). Kernel $5\times5$ làm CER vọt lên 133.10% do xóa sạch dấu thanh tầng 4.
- [x] Bảng 7: Phân tích ảnh hưởng của chiều cao dòng (`p5_table7_line_height.csv`). Chiều cao $\ge 48$ px là ngưỡng bắt buộc để biểu diễn 4 tầng chữ Lào.
- [x] Bảng 8: Phân tích CER phân tầng (Sáng × Máy × Font × Góc) (`p5_table8_stratified.csv` + `ablation_table8_stratified.png`).
- [x] Bảng 9: Độ bền pipeline với mức nhiễu & mờ tăng dần (`p5_table9_noise_robustness.csv` + `ablation_table9_noise_robustness.png`).
- [x] Bảng 10: Đối chiếu hiệu năng chữ in vs chữ viết tay trên 50 thẻ (`p5_table10_printed_vs_handwritten.csv`).
- [x] Soạn thảo báo cáo khoa học chi tiết `docs/ABLATION_STUDY.md`.
- [x] Khóa cấu hình tiền xử lý chuẩn tối ưu vào `experiments/configs/optimal_pipeline.yaml`.
- [x] Unit test kiểm định artifact P5 `tests/test_p5_ablation.py` đạt 100% (4/4 tests passed).
- **Cổng ra P5:**
  - [x] Xuất đủ 8 bảng CSV và 5 biểu đồ khoa học PNG vào `experiments/results/`.
  - [x] Khóa cấu hình tiền xử lý tốt nhất sẵn sàng cho P6 và P7.

---

### 🎯 Phase P6: Hậu xử lý từ điển có trọng số (ĐÃ HOÀN THÀNH - COMPLETED)
- [x] Tự cài đặt Dynamic Programming cho Weighted Levenshtein (`src/postprocessing/weighted_levenshtein.py`) với chi phí thực nghiệm từ `confusion_pairs.csv`.
- [x] Tích hợp chiết khấu phạt dấu thanh tầng 4 ($\gamma_{\text{tone}} = 0.2$) và nguyên âm tầng 1, 3 ($\gamma_{\text{vowel}} = 0.4$).
- [x] Tích hợp xử lý trật tự Unicode NFC và hoán vị nguyên âm đứng trước (`normalize_lao`).
- [x] Xây dựng bộ khớp từ điển thông minh Lexicon Snap (`src/postprocessing/lexicon_matcher.py`) hỗ trợ tra cứu $O(1)$ cho exact match, Top-k ứng viên và tính điểm tin cậy (Confidence).
- [x] Bảng 11: Accuracy từ & Top-1 / Top-3 / Top-5 & Semantic Accuracy (`p6_table11_accuracy_and_topk.csv` + biểu đồ `p6_topk_and_methods_comparison.png`). Top-1 đạt 29.30%, Top-3 đạt 34.39%, Semantic Acc đạt 29.30%.
- [x] Bảng 12: So sánh đối đầu Levenshtein thường vs Levenshtein có trọng số (`p6_table12_standard_vs_weighted_levenshtein.csv`). Khẳng định cải thiện có ý nghĩa thống kê ($p < 0.05$): $\Delta\text{CER} = -4.76\%$, $\Delta\text{WordAcc} = +6.37\%$.
- [x] Bảng 13: Ảnh hưởng kích thước từ điển 100, 250, 528 từ (`p6_table13_dictionary_size_effect.csv`).
- [x] Bảng 14: So sánh với mô hình n-gram Jaccard (`p6_table14_ngram_vs_levenshtein.csv`). Weighted Levenshtein (Acc 29.30%) áp đảo n-gram (Acc 16.56%).
- [x] Xây dựng đường cong đánh đổi Precision – Coverage theo ngưỡng tin cậy (`p6_precision_coverage_curve.png`). Tại ngưỡng $\ge 0.7$, Word Accuracy đạt 72.0%.
- [x] Soạn thảo báo cáo khoa học chi tiết `docs/POSTPROCESSING_LEXICON.md`.
- [x] Unit test kiểm định artifact P6 `tests/test_p6_postprocessing.py` đạt 100% (9/9 tests passed).
- **Cổng ra P6:**
  - [x] Bảng tổng hợp luồng tích lũy (`p6_cumulative_pipeline_summary.csv`): OCR Thô (Word Acc 5.73%) $\rightarrow$ + Tiền xử lý (Word Acc 3.82%) $\rightarrow$ + Lexicon Snap (Word Acc **29.30%**, Top-3 **34.39%** - tăng hơn 5.1 lần).

---

### 🧠 Phase P7: Huấn luyện mô hình nhận dạng (ĐÃ HOÀN THÀNH - COMPLETED)
- [x] P7a: Thiết lập `tesstrain` và fine-tune Tesseract 5 LSTM trên miền từ vựng giáo trình tiếng Lào (CER giảm từ 62.02% xuống 38.45%).
- [x] P7a: So sánh `synth_clean` vs `synth_aug` trên các quy mô dữ liệu (Bảng 17). Biến đổi quang học thực tế giúp giảm 12.8% CER.
- [x] P7b: Xây dựng & huấn luyện kiến trúc CRNN chuyên biệt tiếng Lào (CNN nén bất đẳng hướng + 2-layer BiLSTM + CTC Loss) tại `src/models/crnn.py`.
- [x] P7c: Bảng 15: Điểm chuẩn đa kiến trúc toàn diện (Tesseract gốc vs Fine-tune vs LaoCRNN vs SVTR vs Google Vision vs Multimodal VLM). LaoCRNN đạt CER 28.12%, độ trễ siêu tốc 28.5ms.
- [x] P7c: Bảng 16: Learning curves theo dung lượng dữ liệu 10k–100k dòng mẫu.
- [x] P7c: Bảng 17: Cống hiến của data augmentation và phân tích khoảng cách khái quát hóa.
- [x] P7c: Bảng 18: Hiệp đồng giữa LaoCRNN và Weighted Lexicon Snap (Phase P6) đưa Word Accuracy nhảy vọt lên **85.35%** (Top-3 đạt **91.72%**), sánh ngang Google Cloud Vision mà không cần Internet.
- [x] Xuất đủ 4 bảng CSV (`p7_table15_*.csv` đến `p7_table18_*.csv`) và 2 biểu đồ PNG chất lượng cao.
- [x] Soạn thảo báo cáo khoa học chi tiết `docs/MODEL_TRAINING_P7.md`.
- [x] Unit test kiểm định artifact P7 `tests/test_p7_models.py` đạt 100% (6/6 tests passed).
- **Cổng ra P7:**
  - [x] Bảng số liệu hoàn chỉnh đối chiếu 7 mô hình và trần VLM/Cloud.
  - [x] Checkpoint mô hình `models/crnn_lao.pt` hoạt động ổn định trên CPU/GPU.
  - [x] Tích hợp thành công với tầng hậu xử lý từ điển P6 đạt Word Accuracy > 85%.

---

### 🌐 Phase P8: Tầng ngôn ngữ & Hỗ trợ dịch (ĐÃ HOÀN THÀNH - COMPLETED)
- [x] Mở rộng quy mô kho từ điển giáo trình chuẩn vàng từ 528 từ lên **1,200 mục từ** có cấu trúc, chuẩn hóa Unicode NFC nghiêm ngặt.
- [x] P8a: Xây dựng giải thuật phân đoạn từ tiếng Lào (Word Tokenization) `LaoTokenizer` dựa trên cây Trie và Longest Matching. So sánh F1 biên giới từ (Bảng 19).
- [x] P8b: Xây dựng bộ sinh phiên âm chữ Latinh `LaoRomanizer` kết hợp tra cứu từ điển và quy tắc ngữ âm Abugida.
- [x] P8c: Xây dựng bộ tra cứu từ điển giáo trình đa ngữ `LaoDictionary` (1,200 từ) hỗ trợ song ngữ Lào - Việt - Anh, từ loại và câu ví dụ minh họa.
- [x] P8d: Xây dựng trình thông dịch & tổng hợp thẻ học tập `LaoTranslator` cung cấp chú giải từng từ (Word Glosses) và dịch toàn câu (Bảng 20).
- [x] P8e: Đo lường phân rã độ trễ toàn luồng End-to-End Pipeline (Bảng 21). Tổng độ trễ toàn luồng chỉ **51.5 ms** (~20 FPS thời gian thực trên CPU).
- [x] Xuất bản 3 bảng CSV (`p8_table19_*.csv` đến `p8_table21_*.csv`) và biểu đồ khoa học `p8_translation_and_segmentation.png`.
- [x] Soạn thảo báo cáo khoa học chi tiết `docs/LANGUAGE_LAYER_P8.md`.
- [x] Unit test kiểm định artifact P8 `tests/test_p8_language_layer.py` đạt 100% (6/6 tests passed).
- **Cổng ra P8:**
  - [x] Pipeline end-to-end xử lý từ ảnh chụp đến bản dịch song ngữ và thẻ học tập hoàn chỉnh.

---

### 💻 Phase P9: Ứng dụng Streamlit hoàn chỉnh
- [ ] Xây dựng giao diện Streamlit đa tính năng.
- [ ] Module Preprocessing Inspector (hiển thị lưới ảnh các bước xử lý).
- [ ] Bộ Flashcard cá nhân + thuật toán Spaced Repetition (SM-2).
- [ ] Dropdown chọn đổi OCR engine trực tiếp (Tesseract / Fine-tune / CRNN).
- [ ] Tab hiển thị Dashboard số liệu nghiên cứu.
- [ ] Feedback logging cho người học sửa lỗi.
- **Cổng ra P9:**
  - [ ] App chạy mượt mà, sẵn sàng demo trực tiếp.

---

### 🎓 Phase P10: Báo cáo & Bảo vệ
- [ ] Soạn thảo báo cáo môn học toàn văn (8 chương).
- [ ] Biên tập 21 bảng số liệu và 12 đồ thị chất lượng cao.
- [ ] Chuẩn bị slide thuyết trình bảo vệ.
- [ ] Bộ phản biện 8 câu hỏi cốt lõi của hội đồng.
- **Cổng ra P10:**
  - [ ] Bộ hồ sơ báo cáo hoàn thiện 100%.
