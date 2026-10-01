# 🗺️ KẾ HOẠCH DỰ ÁN CHI TIẾT (MASTER PROJECT PLAN)
**Đề tài:** OCR và Hỗ trợ Dịch Tiếng Lào Dựa Trên Ảnh Text Cho Giáo Dục Trực Tuyến  
**Môn học:** Xử lý ảnh (Digital Image Processing)  
**Phạm vi mục tiêu:** Nhận dạng chữ in tiếng Lào từ flashcard / từ vựng / giáo trình, trích xuất text, tra cứu từ điển học tập, phiên âm Latin và dịch nghĩa (Việt / Anh).

---

## TỔNG QUAN LỘ TRÌNH 11 PHASES (P0 → P10)

```
P0  Nền móng & Thước đo (Foundation & Metrics)
 │
P1  Lát cắt dọc (Vertical Spike End-to-End)
 │
P2  Dữ liệu (Gold Test Set + Từ điển đa ngữ + Corpus tổng hợp)
 │
 ├── P3 Khối tiền xử lý (Image Preprocessing Pipeline) ───────┐
 │                                                            │ (Chạy xen kẽ)
 ├── P4 Baseline đa engine & Ma trận nhầm lẫn (Error Analysis) ┘
 │
P5  Ablation Nghiên cứu (8 bảng thực nghiệm chuyên sâu)       ← Đóng góp khoa học #1
 │
P6  Hậu xử lý từ điển có trọng số (Weighted Levenshtein)      ← Đóng góp khoa học #2
 │
P7  Huấn luyện mô hình nhận dạng (Fine-tune vs CRNN/SVTR)     ← Đóng góp kỹ thuật #3
 │   P7a Fine-tune Tesseract 5 LSTM
 │   P7b Train CRNN / SVTR
 │   P7c So sánh đa chiều (Accuracy, Speed, Size)
 │
P8  Tầng ngôn ngữ (Tách từ, Phiên âm Latin, Dịch ngữ cảnh NLLB)
 │
P9  Ứng dụng học tập hoàn chỉnh (Streamlit App + Spaced Repetition SM-2)
 │
P10 Báo cáo & Bộ câu hỏi bảo vệ đồ án
```

---

## CHI TIẾT TỪNG PHASE

### 🏁 P0 — Nền móng & Thước đo (~10h)
- **Mục tiêu:** Thiết lập môi trường kỹ thuật không có "nợ công nghệ", đảm bảo thước đo chuẩn xác trước khi thử nghiệm.
- **Công việc chính:**
  1. Cài đặt môi trường: Tesseract 5 + `lao.traineddata` (tessdata_best, chạy `--oem 1`); PaddleOCR; PyTorch; Pillow; OpenCV; libraqm.
  2. ⚠️ **Kiểm tra render font:** Render bảng ~400 tổ hợp phụ âm × nguyên âm × dấu thanh trên 12 font Lào phổ biến (Saysettha, Phetsarath, v.v.). Soi trực quan từng font, lập danh sách đen các font dựng dấu lỗi.
  3. `src/preprocessing/normalize.py`: Chuẩn hóa Unicode NFC + chuẩn hóa thứ tự combining marks + bộ unit test.
  4. `src/evaluation/metrics.py`: CER, WER, Word Accuracy, Top-k Accuracy, Bootstrap Confidence Interval 95% cho CER.
  5. Hạ tầng thực nghiệm: `experiments/configs/` (YAML), logger ghi kết quả tự động ra CSV với seed cố định.
- **Cổng ra (Exit Gate):**
  - [ ] `cer(str1, str2) == 0` cho 2 chuỗi cùng nội dung nhưng khác thứ tự dấu Unicode.
  - [ ] Log thực nghiệm giả lập thành công ra CSV.
  - [ ] Danh sách font an toàn sẵn sàng cho P2.

---

### ⚡ P1 — Lát cắt dọc (Vertical Spike End-to-End) (~10h)
- **Mục tiêu:** Phát hiện mọi "rủi ro chết người" ngay từ tuần đầu, chứng minh luồng hoạt động thông suốt từ ảnh đến nghĩa.
- **Công việc chính:**
  1. Thu thập nhanh 20 ảnh mẫu (flashcard / chụp màn hình / tài liệu cơ bản).
  2. Pipeline tối thiểu: BGR2GRAY + Otsu thresholding (10 dòng code).
  3. OCR thô: pytesseract với `--oem 1 --psm 7 -l lao`.
  4. Từ điển mini: 30 entry CSV (`lao, vi, en, romanization`).
  5. CLI: `python -m src.run --image test.jpg` → in ra Text Lào + Phiên âm + Nghĩa.
- **Cổng ra (Exit Gate):**
  - [ ] $\ge 5/20$ ảnh ra kết quả đúng nghĩa.
  - [ ] Ghi nhận CER thô ban đầu làm mốc số 0 (Baseline Zero).
  - [ ] Tạo `docs/RISKS.md` liệt kê các lỗi phát sinh (PSM nào ổn? Tesseract bị kẹt ở đâu? Vấn đề ánh sáng?).

---

### 📦 P2 — Dữ liệu (Gold Set + Từ điển + Corpus tổng hợp) (~34h)
- **P2a. Gold Test Set Thật (Ground Truth):**
  - 150 flashcard từ vựng theo 10–12 bài giáo trình tiếng Lào, in trên 4 font.
  - Chụp ảnh thực tế: 3 điện thoại × 4 điều kiện sáng (ánh sáng tự nhiên, đèn huỳnh quang, thiếu sáng, bóng đổ) × 2–3 góc nghiêng → 450–550 ảnh.
  - 50 ảnh flashcard viết tay (đo lường giới hạn hệ thống).
  - 30 ảnh trang sách nhiều dòng (đánh giá module phân đoạn dòng P3).
  - Gán nhãn metadata: `filename, lao_text, vi, en, romanization, font, lighting, device, angle, type`.
  - Chia tập: **Dev 30%** (cho P3, P4, P5 tuning) / **Test 70%** (đóng băng tuyệt đối, chỉ mở ở P5 & P7).
- **P2b. Từ điển Giáo trình (`lao_vi_en.csv`):**
  - Quy mô: $\ge 500$ entries gồm `từ | nghĩa VI | nghĩa EN | phiên âm | từ loại | bài học | ví dụ`.
  - Nguồn tham khảo: MOPT, lo_spellcheck_dict, song ngữ Thái-Lào PyThaiNLP, ALT, Awesome-Lao-NLP.
- **P2c. Corpus tổng hợp (Synthetic Data):**
  - 60,000 – 100,000 ảnh dòng văn bản: 10–12 font đã thẩm định ở P0 × cỡ chữ × độ đậm nhạt.
  - Phân bổ: 40% từ đơn, 40% cụm 2–4 từ, 20% câu ngắn.
  - Augmentation thực tế: Motion/Gaussian blur, JPEG compression, Perspective warp $\pm 12^\circ$, gradient sáng, bóng điện thoại, nhiễu muối tiêu, texture giấy kẻ ô.
  - Tạo 2 tập: `synth_clean` và `synth_aug` (để đo đạc cống hiến của data augmentation ở P7).
- **Cổng ra (Exit Gate):**
  - [ ] Toàn bộ nhãn được kiểm tra 100% chuẩn hóa NFC.
  - [ ] Tạo file `docs/DATA.md` ghi rõ giao thức thu thập, bảng thống kê và hình lưới 3×3 mẫu ảnh.

---

### 🛠️ P3 — Khối tiền xử lý ảnh (Image Preprocessing Pipeline) (~28h)
- **Kiến trúc:** Thiết kế theo dạng plug-and-play, bật/tắt và chỉnh tham số qua YAML file config `pipeline(img, cfg)`.
- **9 bước lọc hình ảnh (A1 → A9):**
  - **A1. Xám hóa:** BGR2GRAY vs kênh V (HSV) vs kênh L (LAB).
  - **A2. Cân bằng ánh sáng:** CLAHE (clipLimit $\in \{1, 2, 4\}$) vs Gamma correction vs Homomorphic filtering.
  - **A3. Khử nhiễu:** Median filter vs Bilateral filter vs Non-Local Means (NLM) vs Gaussian.
  - **A4. Hiệu chỉnh phối cảnh:** Phát hiện biên card qua contour + `approxPolyDP` → `warpPerspective`.
  - **A5. Khử nghiêng (Deskew):** Hough Transform vs Moment bậc 2 vs Projection Profile vs FFT.
  - **A6. Nhị phân hóa (Trọng tâm):** Otsu vs Adaptive Gaussian vs Adaptive Mean vs Sauvola vs Niblack vs Wolf.
  - **A7. Hình thái học:** Opening/Closing với kernel $1 \times 1, 2 \times 2, 3 \times 3, 5 \times 5$.
  - **A8. Chuẩn hóa chiều cao dòng:** Resize thân chữ về $24, 32, 48, 64$ px.
  - **A9. Làm mảnh/dày nét:** Morphological thinning vs Dilate 1px.
- **Module tách dòng/vùng văn bản (đánh giá trên 30 trang sách):**
  - So sánh 4 phương pháp: Horizontal Projection Profile, RLSA, Connected Components, Text Detector học sâu (CRAFT/DB).
  - Đánh giá Precision / Recall / F1-score theo IoU.
- **Cổng ra (Exit Gate):**
  - [ ] Pipeline chạy trơn tru với $\ge 20$ tổ hợp cấu hình.
  - [ ] Notebook trích xuất hình ảnh trung gian qua từng bước.
  - [ ] Bảng so sánh 4 giải thuật phân đoạn dòng.

---

### 🔍 P4 — Baseline đa engine & Phân tích lỗi (~22h)
- **Khảo sát & So sánh các Engine:**
  - Tesseract 5 `lao` (tessdata_best) chạy quét các PSM 6, 7, 8, 11, 13.
  - Tesseract 5 + Tiền xử lý tối ưu.
  - PaddleOCR (kiểm tra hỗ trợ ký tự Lào).
  - Cloud OCR API (Google Cloud Vision / Azure Computer Vision) làm mốc trần thương mại.
  - Multimodal VLM (GPT-4o / Claude / Gemini Vision) làm mốc trần hiện đại.
  - Ghi nhận: EasyOCR không hỗ trợ tiếng Lào (đưa vào báo cáo).
- **Phân tích lỗi chuyên sâu (Error Taxonomy):**
  - Xây dựng Confusion Matrix cấp ký tự trên Dev Set → xuất `experiments/results/confusion_pairs.csv`.
  - Phân loại 5 nhóm lỗi:
    1. Nhầm lẫn ký tự tương đồng hình học (vd: `ດ` vs `ຄ`).
    2. Mất dấu thanh (Tone mark dropped).
    3. Sai trật tự Unicode do nguyên âm đứng trước.
    4. Thêm / sót ký tự.
    5. Hỏng hoàn toàn cấu trúc từ.
- **Cổng ra (Exit Gate):**
  - [ ] Bảng 1 & 2: So sánh hiệu năng các engine.
  - [ ] `confusion_pairs.csv` chứa tần suất nhầm lẫn thực tế (đầu vào trực tiếp cho P6).

---

### 🔬 P5 — Nghiên cứu Ablation (Đóng góp #1) (~24h)
- **Mục tiêu:** Chứng minh một cách khoa học lý do từng bước tiền xử lý được chọn bằng thực nghiệm leave-one-out và forward selection.
- **Bộ 8 bảng thực nghiệm:**
  - **Bảng 3:** So sánh 6 phương pháp nhị phân hóa (chứng minh Sauvola/Wolf áp đảo Otsu dưới ánh sáng phức tạp).
  - **Bảng 4:** Leave-one-out từng bước A1–A9 ($\Delta\text{CER}$ kèm 95% CI).
  - **Bảng 5:** Greedy forward selection xây dựng cấu hình tối ưu.
  - **Bảng 6:** Ảnh hưởng kích thước kernel hình thái học (chứng minh kernel $\ge 3 \times 3$ làm tụt CER do xóa dấu thanh).
  - **Bảng 7:** Ảnh hưởng của chiều cao dòng chuẩn hóa ($24, 32, 48, 64$ px).
  - **Bảng 8:** Phân tích CER phân tầng theo: Sáng × Thiết bị × Font × Góc chụp.
  - **Bảng 9:** Độ bền pipeline (CER curve) trước các mức độ nhiễu và mờ tăng dần.
  - **Bảng 10:** Đối chiếu hiệu năng: Chữ in vs Chữ viết tay.
- **Cổng ra (Exit Gate):**
  - [ ] Script `run_ablation.py` tự động hóa 100%.
  - [ ] Toàn bộ 8 bảng số liệu và 5 biểu đồ lưu trong `experiments/results/`.
  - [ ] Khóa cấu hình tiền xử lý tốt nhất cho toàn hệ thống.

---

### 🎯 P6 — Hậu xử lý từ điển có trọng số (Đóng góp #2) (~20h)
- **Mục tiêu:** Tận dụng không gian từ vựng đóng của flashcard giáo trình bằng thuật toán Weighted Levenshtein.
- **Thuật toán Dynamic Programming tự cài đặt:**
  - Chi phí thay thế $Cost(c_1, c_2)$ được suy ra trực tiếp từ xác suất nghịch đảo trong `confusion_pairs.csv` (ví dụ: `sub('ດ', 'ຄ') = 0.3`, trong khi `sub('ດ', 'ກ') = 1.0`).
  - Phạt mất dấu thanh có trọng số riêng ($0.2$).
  - Chuẩn hóa NFC và hoán vị trật tự nguyên âm trước khi tính khoảng cách.
  - Cơ chế ngưỡng tin cậy (Confidence Threshold): nếu khoảng cách vượt ngưỡng $\rightarrow$ cảnh báo "Không chắc chắn" + gợi ý Top-3 ứng viên.
- **Các bảng thực nghiệm:**
  - **Bảng 11:** Accuracy cấp từ + Top-1 / Top-3 / Top-5.
  - **Bảng 12:** So sánh Levenshtein tiêu chuẩn vs Levenshtein có trọng số.
  - **Bảng 13:** Ảnh hưởng của dung lượng từ điển ($100, 250, 500$ từ).
  - **Bảng 14:** So sánh với n-gram Language Model.
  - Biểu đồ Precision – Coverage theo ngưỡng tin cậy.
- **Cổng ra (Exit Gate):**
  - [ ] Bảng tổng hợp mức tăng độ chính xác từ: OCR thô $\rightarrow$ + Tiền xử lý $\rightarrow$ + Lexicon Snap có trọng số.

---

### 🧠 P7 — Huấn luyện mô hình nhận dạng (Đóng góp #3) (~34h)
- **P7a. Fine-tune Tesseract 5 LSTM:**
  - Chuẩn bị dữ liệu theo chuẩn `tesstrain`: cặp ảnh `.tif`/`.png` và nhãn `.gt.txt`.
  - Fine-tune từ `lao.traineddata` (tessdata_best) với `START_MODEL=lao`, LR = $0.0001$.
  - Đánh giá qua `lstmeval` và vẽ learning curve.
  - So sánh huấn luyện trên `synth_clean` vs `synth_aug` với các mốc dữ liệu $20k, 60k, 100k$ dòng.
- **P7b. Huấn luyện CRNN / SVTR:**
  - Kiến trúc: CNN (ResNet) + BiLSTM + CTC Loss (hoặc SVTR).
  - Tự định nghĩa bảng từ điển ký tự Lào (Lao Character Set bao gồm đầy đủ phụ âm, nguyên âm, dấu thanh, số và dấu câu).
  - Train trên GPU với data augmentation tương thích P2c.
- **P7c. Đối chiếu toàn diện:**
  - **Bảng 15:** Ma trận so sánh: Tesseract gốc vs Tesseract Fine-tuned vs CRNN vs SVTR (CER, WER, Word Acc, Inference time, Dung lượng model).
  - **Bảng 16:** Đường cong học tập theo quy mô tập huấn luyện.
  - **Bảng 17:** Định lượng tác động của Augmentation.
  - **Bảng 18:** Kết hợp từng mô hình với Lexicon Snap.
- **Cổng ra (Exit Gate):**
  - [ ] Hoàn thành Bảng tổng so sánh đầy đủ 6 dòng, đối chiếu với Cloud/VLM.

---

### 🌐 P8 — Tầng ngôn ngữ & Hỗ trợ học tập (~20h)
- **Tách từ (Word Tokenization):**
  - Tích hợp LaoNLP tokenizer.
  - So sánh hiệu năng tách từ: LaoNLP vs Seema/Chamkho vs ICU (Đo F1 biên giới từ).
  - Trích dẫn bối cảnh SOTA: Corpus 10k câu chuẩn vàng, XLM-RoBERTa (F1 0.75) vs LaoNLP (0.71).
- **Dịch offline & tra cứu:**
  - Từ đơn: Tra cứu bảng từ điển $\rightarrow$ Nghĩa Việt, Anh, từ loại, phiên âm, ví dụ.
  - Cụm từ / Câu: NLLB-200 distilled 600M (`lao_Laoo`).
  - Đánh giá dịch: So sánh Tra từ điển vs NLLB-600M vs NLLB-1.3B vs Google Translate (đo BLEU/chrF++ và đánh giá thủ công 150 mẫu).
- **Phiên âm Latin (Romanization):** Module chuyển đổi chữ Lào sang bảng chữ cái Latinh hỗ trợ người mới học.
- **Cổng ra (Exit Gate):**
  - [ ] CLI hoàn chỉnh nhận ảnh $\rightarrow$ trả về: Text Lào + Phiên âm Latin + Nghĩa Việt/Anh + Điểm tin cậy.
  - [ ] Bảng 19 (Tách từ), Bảng 20 (Dịch), Bảng 21 (Độ trễ thời gian từng module).

---

### 💻 P9 — Ứng dụng học tập hoàn chỉnh (~20h)
- **Giao diện Web Streamlit phục vụ học tập thực thụ:**
  - **Khu vực Tải ảnh:** Hỗ trợ Upload ảnh hoặc chụp trực tiếp từ Webcam/Camera điện thoại.
  - **Lưới trực quan hóa tiền xử lý (Preprocessing Inspector):** Hiển thị trực quan từng bước ảnh (Ảnh xám $\rightarrow$ Cân bằng sáng $\rightarrow$ Khử nhiễu $\rightarrow$ Nhị phân hóa $\rightarrow$ Khử nghiêng) để chấm điểm phần Xử lý ảnh.
  - **Bảng kết quả thông minh:** Chữ Lào nhận dạng + Top-3 ứng viên gợi ý từ Lexicon Snap + Điểm tin cậy.
  - **Thẻ thông tin ngữ nghĩa (Vocab Card):** Phiên âm Latin, từ loại, nghĩa tiếng Việt, nghĩa tiếng Anh, câu ví dụ minh họa.
  - **Sổ tay từ vựng & Thuật toán lặp lại ngắt quãng (Spaced Repetition SM-2):** Cho phép lưu từ đã tra vào bộ ôn tập cá nhân.
  - **Tùy chọn OCR Engine:** Dropdown cho phép chuyển đổi tức thời giữa Tesseract gốc, Tesseract Fine-tune, CRNN để demo trực quan.
  - **Bảng số liệu tương tác (Dashboard):** Xem lại các bảng Ablation Study và Confusion Matrix.
  - **Vòng phản hồi (User Feedback Loop):** Lưu các trường hợp người dùng sửa kết quả vào log để làm giàu từ điển.
- **Cổng ra (Exit Gate):**
  - [ ] Ứng dụng chạy mượt mà, không giật lag, kèm 5 ảnh mẫu test sẵn.

---

### 🎓 P10 — Báo cáo & Bảo vệ đồ án (~24h)
- **Tài liệu báo cáo hoàn chỉnh (LaTeX / Word):**
  - Chương 1: Giới thiệu, bối cảnh giảng dạy tiếng Lào, phát biểu bài toán.
  - Chương 2: Đặc thù chữ Lào & Thách thức thị giác máy tính (cấu trúc 4 tầng, tổ hợp Unicode, nguyên âm đi trước).
  - Chương 3: Khảo sát các công trình liên quan & Công cụ hiện có.
  - Chương 4: Xây dựng tập dữ liệu (Gold test set & Synth corpus).
  - Chương 5: Phương pháp đề xuất (Pipeline tiền xử lý thích nghi, Levenshtein có trọng số, Kiến trúc mô hình).
  - Chương 6: Kết quả thực nghiệm (21 bảng số liệu + 12 biểu đồ).
  - Chương 7: Ứng dụng thực tế & Đánh giá giao diện người dùng.
  - Chương 8: Kết luận, hạn chế và hướng phát triển.
- **Bộ 8 câu hỏi cốt lõi bảo vệ:**
  1. *Vì sao Sauvola/Wolf lại vượt trội Otsu trong bài toán này?*
  2. *Tại sao không cắt tách từng ký tự (Character Segmentation)?*
  3. *Trọng số trong ma trận khoảng cách Levenshtein được sinh ra từ đâu?*
  4. *Fine-tune Tesseract vs CRNN/SVTR: phương án nào thắng và lý giải nguyên nhân?*
  5. *Hệ thống sẽ thất bại trong những trường hợp biên (edge cases) nào?*
  6. *Khoảng tin cậy Bootstrap 95% có khẳng định sự vượt trội có ý nghĩa thống kê?*
  7. *Việc dùng từ điển đóng có làm mất tính tổng quát của OCR không?*
  8. *Để mở rộng sang chữ viết tay hoàn toàn, hệ thống cần bổ sung những gì?*
- **Cổng ra (Exit Gate):**
  - [ ] Slide thuyết trình chuyên nghiệp.
  - [ ] Video demo chức năng.
  - [ ] Báo cáo toàn văn đúng chuẩn học thuật.
