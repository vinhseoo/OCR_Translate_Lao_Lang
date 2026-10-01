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
| **P3** | Khối tiền xử lý ảnh (A1–A9) | ~28h | ⏳ `IN_PROGRESS` | Sắp thực hiện |
| **P4** | Baseline đa engine & Error Analysis | ~22h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
| **P5** | Nghiên cứu Ablation (Đóng góp #1) | ~24h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
| **P6** | Hậu xử lý từ điển có trọng số (#2) | ~20h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
| **P7** | Huấn luyện mô hình nhận dạng (#3) | ~34h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
| **P8** | Tầng ngôn ngữ (Tách từ & Dịch) | ~20h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
| **P9** | Ứng dụng Streamlit hoàn chỉnh | ~20h | ⚪ `NOT_STARTED` | Chưa hoàn thành |
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
- [ ] A1: Module xám hóa (BGR2GRAY, HSV-V, LAB-L).
- [ ] A2: Module cân bằng sáng (CLAHE, Gamma, Homomorphic).
- [ ] A3: Module khử nhiễu (Median, Bilateral, NLM, Gaussian).
- [ ] A4: Module sửa phối cảnh (Contour quad warp).
- [ ] A5: Module khử nghiêng (Deskew).
- [ ] A6: Module nhị phân hóa (Otsu, Adaptive Mean, Adaptive Gaussian, Sauvola, Niblack, Wolf).
- [ ] A7: Module hình thái học có kiểm soát.
- [ ] A8: Chuẩn hóa chiều cao dòng (24, 32, 48, 64 px).
- [ ] A9: Làm mảnh/dày nét.
- [ ] Module tách dòng trên tập 30 trang sách (Projection, RLSA, Connected Components, Deep detector).
- **Cổng ra P3:**
  - [ ] Pipeline cấu hình qua YAML chạy được $\ge 20$ tổ hợp.
  - [ ] Notebook demo trực quan các bước trung gian.
  - [ ] Bảng so sánh 4 phương pháp tách dòng theo IoU.

---

### 🔍 Phase P4: Baseline đa engine & Phân tích lỗi
- [ ] Đánh giá Tesseract gốc trên Dev Set (quét các PSM).
- [ ] Đánh giá PaddleOCR.
- [ ] Đánh giá Cloud OCR API (Google/Azure) làm trần tham chiếu.
- [ ] Đánh giá VLM (GPT-4o/Claude/Gemini).
- [ ] Xây dựng Confusion Matrix cấp ký tự $\rightarrow$ trích xuất `experiments/results/confusion_pairs.csv`.
- [ ] Phân tích 5 nhóm lỗi cơ bản với ảnh minh họa.
- **Cổng ra P4:**
  - [ ] Bảng 1 & 2: So sánh các engine.
  - [ ] File ma trận nhầm lẫn `confusion_pairs.csv` sẵn sàng cho P6.

---

### 🔬 Phase P5: Nghiên cứu Ablation (Đóng góp #1)
- [ ] Viết `experiments/run_ablation.py` tự động hóa 100%.
- [ ] Bảng 3: So sánh 6 phương pháp nhị phân hóa.
- [ ] Bảng 4: Leave-one-out từng bước A1–A9 (kèm CI 95%).
- [ ] Bảng 5: Greedy forward selection tìm cấu hình tối ưu.
- [ ] Bảng 6: Phân tích ảnh hưởng của kích thước kernel hình thái học.
- [ ] Bảng 7: Phân tích ảnh hưởng của chiều cao dòng.
- [ ] Bảng 8: Phân tích CER phân tầng (Sáng × Máy × Font × Góc).
- [ ] Bảng 9: Độ bền pipeline với mức nhiễu tăng dần.
- [ ] Bảng 10: Chữ in vs Chữ viết tay.
- **Cổng ra P5:**
  - [ ] Xuất 8 bảng và 5 biểu đồ khoa học vào `experiments/results/`.
  - [ ] Khóa cấu hình tiền xử lý tốt nhất.

---

### 🎯 Phase P6: Hậu xử lý từ điển có trọng số (Đóng góp #2)
- [ ] Tự cài đặt Dynamic Programming cho Weighted Levenshtein với chi phí từ `confusion_pairs.csv`.
- [ ] Tích hợp xử lý trật tự nguyên âm đứng trước (`ເ ແ ໂ ໃ ໄ`).
- [ ] Xây dựng bộ lọc Top-k ứng viên và tính điểm tin cậy.
- [ ] Bảng 11: Accuracy từ và Top-1/3/5.
- [ ] Bảng 12: So sánh Levenshtein thường vs Levenshtein có trọng số.
- [ ] Bảng 13: Ảnh hưởng kích thước từ điển (100, 250, 500 từ).
- [ ] Bảng 14: So sánh với n-gram Language Model.
- **Cổng ra P6:**
  - [ ] Bảng tổng hợp thô $\rightarrow$ +tiền xử lý $\rightarrow$ +lexicon snap.

---

### 🧠 Phase P7: Huấn luyện mô hình nhận dạng (Đóng góp #3)
- [ ] P7a: Thiết lập `tesstrain` và fine-tune Tesseract 5 LSTM trên GPU/CPU.
- [ ] P7a: So sánh `synth_clean` vs `synth_aug` trên các quy mô dữ liệu.
- [ ] P7b: Xây dựng & huấn luyện kiến trúc CRNN (ResNet + BiLSTM + CTC).
- [ ] P7c: Bảng 15: So sánh toàn diện Tesseract gốc vs Fine-tune vs CRNN.
- [ ] P7c: Bảng 16: Learning curves theo dung lượng dữ liệu.
- [ ] P7c: Bảng 17: Cống hiến của data augmentation.
- [ ] P7c: Bảng 18: Kết hợp mô hình tốt nhất với Lexicon Snap.
- **Cổng ra P7:**
  - [ ] Bảng số liệu hoàn chỉnh đối chiếu mọi mô hình và trần VLM/Cloud.

---

### 🌐 Phase P8: Tầng ngôn ngữ & Hỗ trợ dịch
- [ ] Tích hợp LaoNLP tokenizer và so sánh F1 biên giới từ với ICU / Chamkho (Bảng 19).
- [ ] Tra cứu nghĩa từ điển đa ngữ (Việt, Anh, từ loại, phiên âm).
- [ ] Tích hợp NLLB-200 distilled 600M (`lao_Laoo`) cho dịch câu/cụm từ.
- [ ] Đo lường chất lượng dịch BLEU / chrF++ (Bảng 20).
- [ ] Đo lường độ trễ từng module (Bảng 21).
- **Cổng ra P8:**
  - [ ] Pipeline end-to-end xử lý từ ảnh đến bản dịch hoàn chỉnh.

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
