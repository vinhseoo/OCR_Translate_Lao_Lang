"""
ỨNG DỤNG WEB GIÁO DỤC TRỰC TUYẾN: OCR & HỖ TRỢ DỊCH TIẾNG LÀO
Dự án: Hệ thống OCR và Hỗ trợ Dịch Tiếng Lào cho Giáo dục Trực tuyến
Môn học: Xử lý ảnh (Digital Image Processing)
Framework: Streamlit
Hỗ trợ:
- Nhận dạng chữ in tiếng Lào đa động cơ (LaoCRNN SOTA, Tesseract P5, Tesseract Raw)
- Hậu xử lý từ điển Weighted Levenshtein & Lexicon Snap
- Tách từ, Phiên âm Latinh & Dịch nghĩa song ngữ Lào - Việt - Anh
- Kính lúp tiền xử lý ảnh (Preprocessing Inspector)
- Bộ thẻ Flashcard cá nhân hóa tích hợp thuật toán Spaced Repetition (SuperMemo SM-2)
- Tra cứu kho từ điển giáo trình 1,200 mục từ
- Dashboard kết quả nghiên cứu khoa học (Bảng 1–21 & Biểu đồ)
"""
import os
import sys
import json
import time
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
import streamlit as st
import pandas as pd
from dataclasses import asdict

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Tự động nhận diện đường dẫn Tesseract OCR trên Windows
tess_candidates = [
    os.path.expandvars(r'%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe'),
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
]
for tc in tess_candidates:
    if os.path.exists(tc):
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = tc
        except Exception:
            pass
        break

tessdata_best_dir = os.path.join(PROJECT_ROOT, "models", "tessdata_best")
if os.path.exists(tessdata_best_dir):
    os.environ["TESSDATA_PREFIX"] = tessdata_best_dir

from src.preprocessing.normalize import normalize_lao
from src.preprocessing.pipeline import PreprocessingPipeline
from src.postprocessing.lexicon_matcher import LexiconMatcher
from src.translation.tokenizer import LaoTokenizer
from src.translation.romanizer import LaoRomanizer
from src.translation.dictionary_lookup import LaoDictionary
from src.translation.translator import LaoTranslator
from src.education.sm2 import FlashcardReviewState, review_card
from src.education.feedback import save_user_correction

# Thiết lập cấu hình trang Streamlit
st.set_page_config(
    page_title="Lao OCR & Educational Translation",
    page_icon="🇱🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện hiện đại, trực quan
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3799;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a69bd;
        margin-bottom: 20px;
    }
    .flashcard-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 24px;
        border: 2px solid #ced4da;
        box-shadow: 0 8px 16px rgba(0,0,0,0.06);
        text-align: center;
        margin: 15px 0;
    }
    .lao-text-huge {
        font-size: 2.8rem;
        font-weight: 700;
        color: #0c2461;
        margin-bottom: 8px;
    }
    .rom-text {
        font-size: 1.3rem;
        color: #e55039;
        font-style: italic;
        margin-bottom: 12px;
    }
    .vi-trans {
        font-size: 1.5rem;
        color: #079992;
        font-weight: 600;
    }
    .en-trans {
        font-size: 1.2rem;
        color: #78e08f;
        font-weight: 500;
    }
    .metric-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        background-color: #38ada9;
        color: white;
        font-weight: bold;
        font-size: 0.85rem;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system_engines():
    """Tải và lưu trữ vào bộ nhớ các mô hình và động cơ toàn luồng."""
    pipeline = PreprocessingPipeline(config={
        "grayscale": {"enabled": True, "method": "bgr2gray"},
        "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
        "denoise": {"enabled": True, "method": "bilateral"},
        "deskew": {"enabled": False},
        "binarization": {"enabled": True, "method": "otsu"},
        "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]},
        "height_normalization": {"enabled": True, "target_height": 48},
        "border_padding": {"enabled": True, "padding_px": 15, "crop_outer_px": 0}
    })
    
    matcher = LexiconMatcher()
    translator = LaoTranslator()
    
    # Nạp mô hình CRNN nếu có trọng số
    crnn_model = None
    checkpoint_path = os.path.join(PROJECT_ROOT, "models", "crnn_lao.pt")
    if os.path.exists(checkpoint_path):
        import torch
        from src.models.crnn import LaoCRNN
        from src.models.lao_vocab import DEFAULT_LAO_VOCAB
        try:
            checkpoint = torch.load(checkpoint_path, map_location="cpu")
            crnn_model = LaoCRNN(vocab=DEFAULT_LAO_VOCAB, hidden_size=256)
            if "model_state_dict" in checkpoint:
                crnn_model.load_state_dict(checkpoint["model_state_dict"])
            else:
                crnn_model.load_state_dict(checkpoint)
            crnn_model.eval()
        except Exception as e:
            print("Lỗi nạp CRNN:", e)
            crnn_model = None
            
    return pipeline, matcher, translator, crnn_model


pipeline, matcher, translator, crnn_model = load_system_engines()

# Khởi tạo Deck Flashcard trong session_state
FLASHCARD_DB = os.path.join(PROJECT_ROOT, "data", "flashcards_deck.json")

def load_user_flashcards():
    if not os.path.exists(FLASHCARD_DB):
        # Mẫu mặc định ban đầu
        default_cards = [
            FlashcardReviewState("c1", "ສະບາຍດີ", "Xin chào", "sa-baai-dee", 0, 1, 2.5),
            FlashcardReviewState("c2", "ຂອບໃຈ", "Cảm ơn", "khop-chai", 0, 1, 2.5),
            FlashcardReviewState("c3", "ເຂົ້າໜຽວ", "Xôi nếp Lào", "khao-niaao", 0, 1, 2.5),
            FlashcardReviewState("c4", "ຮຽນພາສາລາວ", "Học tiếng Lào", "hian-phaa-saa-laao", 0, 1, 2.5)
        ]
        return [asdict(c) for c in default_cards]
    try:
        with open(FLASHCARD_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_user_flashcards(cards):
    os.makedirs(os.path.dirname(FLASHCARD_DB), exist_ok=True)
    with open(FLASHCARD_DB, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

if "flashcards" not in st.session_state:
    st.session_state.flashcards = load_user_flashcards()


# =============================================================================
# GIAO DIỆN CHÍNH & SIDEBAR
# =============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Flag_of_Laos.svg/320px-Flag_of_Laos.svg.png", width=120)
st.sidebar.title("🇱🇦 Lao OCR & EdTech")
st.sidebar.markdown("**Hệ thống OCR & Dịch Tiếng Lào cho Giáo dục Trực tuyến**")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "CHỌN PHÂN HỆ CHỨC NĂNG:",
    [
        "📸 1. Nhận Dạng & Thẻ Flashcard (Live OCR)",
        "🔬 2. Kính Lúp Tiền Xử Lý (Image Inspector)",
        "🧠 3. Ôn Tập Ghi Nhớ (Spaced Repetition SM-2)",
        "📖 4. Tra Cứu Từ Điển Giáo Trình (1,200 từ)",
        "📊 5. Bảng Điều Khiển Nghiên Cứu (Dashboard)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Thông tin Hệ thống:**
- **Mô hình OCR:** LaoCRNN + CTC
- **Từ điển:** 1,200 từ chuẩn NFC
- **Độ chính xác Word Acc:** **85.35%** (Top-3: **91.72%**)
- **Độ trễ toàn luồng:** **51.5 ms** (CPU Offline)
- **Môn học:** Xử lý ảnh số (DIP)
""")

# =============================================================================
# TAB 1: NHẬN DẠNG & THẺ FLASHCARD TƯƠNG TÁC (LIVE OCR)
# =============================================================================
if app_mode == "📸 1. Nhận Dạng & Thẻ Flashcard (Live OCR)":
    st.markdown('<p class="main-header">📸 NHẬN DẠNG CHỮ & TẠO THẺ FLASHCARD GIÁO DỤC</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Nhận dạng ảnh chụp flashcard / từ vựng tiếng Lào, tự động sửa lỗi bằng từ điển, phiên âm và tạo thẻ học tập song ngữ tức thì.</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1. Chọn nguồn ảnh đầu vào")
        input_source = st.radio("Nguồn ảnh:", ["Tải ảnh lên từ máy tính", "Chọn từ thư viện Gold Set"], horizontal=True)
        
        image_to_process = None
        image_name = "sample.jpg"

        if input_source == "Tải ảnh lên từ máy tính":
            uploaded_file = st.file_uploader("Tải lên ảnh thẻ flashcard hoặc văn bản chữ Lào (PNG/JPG):", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                image_to_process = Image.open(uploaded_file).convert("RGB")
                image_name = uploaded_file.name
                st.image(image_to_process, caption="Ảnh bạn vừa tải lên", use_container_width=True)
        else:
            gold_dir = os.path.join(PROJECT_ROOT, "data", "gold", "images")
            if os.path.exists(gold_dir):
                sample_files = [f for f in os.listdir(gold_dir) if f.endswith((".jpg", ".png"))][:15]
                selected_sample = st.selectbox("Chọn ảnh mẫu trong tập Gold Set:", sample_files)
                if selected_sample:
                    image_path = os.path.join(gold_dir, selected_sample)
                    image_to_process = Image.open(image_path).convert("RGB")
                    image_name = selected_sample
                    st.image(image_to_process, caption=f"Mẫu: {selected_sample}", use_container_width=True)

        st.subheader("2. Cấu hình Nhận dạng")
        engine_choice = st.selectbox(
            "Chọn Mô hình Nhận dạng OCR:",
            [
                "🚀 LaoCRNN + Weighted Lexicon Snap (Khuyến nghị - SOTA 85.35% Acc)",
                "⚡ LaoCRNN Standalone (Học sâu thuần túy - 35.67% Acc)",
                "🔧 Tesseract 5 + Tiền xử lý tối ưu P5 (7.01% Acc)",
                "📜 Tesseract 5 Raw (Baseline Gốc - 6.37% Acc)"
            ]
        )
        use_deskew = st.checkbox("Khử nghiêng ảnh (Moment Deskew)", value=False, help="Lưu ý: Nghiên cứu P5 cho thấy Deskew có thể làm lệch trục flashcard ngắn.")

    with col_right:
        st.subheader("3. Kết quả Nhận dạng & Dịch thuật")
        
        if "ocr_result" not in st.session_state:
            st.session_state.ocr_result = None

        if image_to_process is not None:
            if st.button("🚀 THỰC HIỆN NHẬN DẠNG & TỔNG HỢP FLASHCARD", type="primary", use_container_width=True):
                with st.spinner("Đang xử lý toàn luồng qua Pipeline Xử lý ảnh -> OCR -> Từ điển -> NLP..."):
                    t_start = time.perf_counter()
                    img_np = np.array(image_to_process)

                    # 1. Tiền xử lý ảnh
                    if hasattr(pipeline, "config") and isinstance(pipeline.config.get("deskew"), dict):
                        pipeline.config["deskew"]["enabled"] = use_deskew
                    proc_res = pipeline.process(img_np)
                    processed_img = proc_res[0] if isinstance(proc_res, tuple) else proc_res

                    # 2. Nhận dạng OCR đa động cơ
                    raw_pred = ""
                    if "LaoCRNN" in engine_choice and crnn_model is not None:
                        raw_pred = crnn_model.predict_image(processed_img)
                        # Nếu CRNN chưa đọc được, hỗ trợ thêm qua Tesseract
                        if not raw_pred.strip():
                            try:
                                import pytesseract
                                raw_pred = pytesseract.image_to_string(processed_img, lang='lao', config='--psm 7')
                            except Exception:
                                pass
                    else:
                        # Tesseract Engine
                        try:
                            import pytesseract
                            raw_pred = pytesseract.image_to_string(processed_img, lang='lao', config='--psm 7')
                        except Exception:
                            raw_pred = ""

                    raw_pred = normalize_lao(raw_pred).strip()

                    # 3. Hậu xử lý từ điển Levenshtein
                    final_lao = raw_pred
                    confidence = 1.0
                    if raw_pred and "Lexicon Snap" in engine_choice:
                        snap_res = matcher.match(raw_pred, method="weighted_levenshtein")
                        if snap_res.best_lao and snap_res.confidence >= 0.35:
                            final_lao = snap_res.best_lao
                            confidence = snap_res.confidence

                    elapsed_ms = (time.perf_counter() - t_start) * 1000

                    st.session_state.ocr_result = {
                        "raw_pred": raw_pred,
                        "final_lao": final_lao,
                        "elapsed_ms": elapsed_ms,
                        "engine_choice": engine_choice,
                        "confidence": confidence,
                        "image_name": image_name
                    }

            # Hiển thị kết quả nhận dạng và thẻ Flashcard
            if st.session_state.ocr_result is not None:
                res = st.session_state.ocr_result
                current_text = res["final_lao"]

                # Nếu OCR chưa nhận dạng được ký tự rõ ràng
                if not current_text:
                    st.warning("⚠️ OCR chưa nhận diện rõ ký tự từ ảnh (do chữ mờ, ảnh chụp màn hình bị nén hoặc góc chụp). Bạn có thể kiểm tra hoặc nhập trực tiếp chữ Lào vào ô bên dưới:")
                    default_input = "ທຸກໆຄົນ"
                else:
                    default_input = current_text

                # Hộp kiểm tra / điều chỉnh từ vựng trực quan
                active_lao = st.text_input(
                    "✏️ Văn bản tiếng Lào đã nhận dạng (có thể tinh chỉnh nếu cần):",
                    value=default_input,
                    key="active_lao_input"
                )
                active_lao = normalize_lao(active_lao).strip()

                if active_lao:
                    trans_output = translator.translate(active_lao)

                    # Hiển thị thẻ Flashcard cao cấp
                    st.markdown(f"""
                    <div class="flashcard-box">
                        <div class="lao-text-huge">{trans_output.original_lao}</div>
                        <div class="rom-text">🔊 /{trans_output.romanization}/</div>
                        <div class="vi-trans">🇻🇳 {trans_output.translation_vi}</div>
                        <div class="en-trans">🇬🇧 {trans_output.translation_en}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <span class="metric-badge">Độ trễ: {res['elapsed_ms']:.1f} ms</span>
                    <span class="metric-badge">Động cơ: {res['engine_choice'].split('(')[0]}</span>
                    <span class="metric-badge">Số từ: {len(trans_output.tokens)}</span>
                    """, unsafe_allow_html=True)

                    # Hiển thị chú giải chi tiết từng từ
                    st.markdown("#### 📖 Chú Giải Từng Từ Vựng (Word Glosses)")
                    gloss_data = []
                    for g in trans_output.glosses:
                        gloss_data.append({
                            "Từ tiếng Lào": g.lao,
                            "Phiên âm": g.romanization,
                            "Từ loại": g.pos,
                            "Nghĩa Tiếng Việt": g.vi,
                            "Nghĩa Tiếng Anh": g.en,
                            "Ví dụ": f"{g.example_lao} ({g.example_vi})" if g.example_lao else "-"
                        })
                    st.dataframe(pd.DataFrame(gloss_data), use_container_width=True)

                    # Nút thêm vào Flashcard ôn tập cá nhân
                    if st.button("➕ Thêm Thẻ Này Vào Bộ Nhớ Ôn Tập (SM-2)", use_container_width=True):
                        card_id = f"c_{int(time.time())}"
                        new_card = FlashcardReviewState(
                            card_id=card_id,
                            lao_text=trans_output.original_lao,
                            vi_meaning=trans_output.translation_vi,
                            romanization=trans_output.romanization
                        )
                        st.session_state.flashcards.append(asdict(new_card))
                        save_user_flashcards(st.session_state.flashcards)
                        st.success("✅ Đã thêm thẻ vào bộ Spaced Repetition cá nhân!")

                    # Hộp đóng góp phản hồi sửa lỗi
                    with st.expander("🛠️ Phát hiện kết quả chưa chuẩn? Gửi phản hồi sửa lỗi cho chúng tôi"):
                        user_correct = st.text_input("Nội dung tiếng Lào đúng:", value=trans_output.original_lao, key="feedback_input")
                        user_note = st.text_input("Ghi chú bổ sung (tuỳ chọn):", key="feedback_note")
                        if st.button("Gửi đóng góp sửa lỗi"):
                            save_user_correction(res["image_name"], res["raw_pred"], user_correct, res["engine_choice"], user_note)
                            st.info("Cảm ơn bạn! Đóng góp đã được lưu vào hệ thống Continuous Learning.")
        else:
            st.info("👈 Vui lòng tải ảnh lên hoặc chọn ảnh mẫu bên trái để thực hiện nhận dạng.")


# =============================================================================
# TAB 2: KÍNH LÚP TIỀN XỬ LÝ ẢNH (PREPROCESSING INSPECTOR)
# =============================================================================
elif app_mode == "🔬 2. Kính Lúp Tiền Xử Lý (Image Inspector)":
    st.markdown('<p class="main-header">🔬 KÍNH LÚP TIỀN XỬ LÝ ẢNH (PREPROCESSING INSPECTOR)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Trực quan hóa từng bước trong chuỗi 12 phép biến đổi xử lý ảnh số (Digital Image Processing) phục vụ chẩn đoán và nghiên cứu khoa học.</p>', unsafe_allow_html=True)

    gold_dir = os.path.join(PROJECT_ROOT, "data", "gold", "images")
    sample_files = [f for f in os.listdir(gold_dir) if f.endswith((".jpg", ".png"))][:10] if os.path.exists(gold_dir) else []
    sel_img = st.selectbox("Chọn ảnh mẫu để phân tích các bước trung gian:", sample_files)
    
    if sel_img:
        img_p = os.path.join(gold_dir, sel_img)
        orig_bgr = cv2.imread(img_p)
        orig_rgb = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB)
        
        # Tạo các bước trung gian
        gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY)
        clahe_obj = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe_obj.apply(gray)
        denoised = cv2.bilateralFilter(clahe_img, d=9, sigmaColor=75, sigmaSpace=75)
        _, otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Resize 48px
        h, w = otsu.shape
        target_h = 48
        scale = target_h / float(h)
        new_w = max(int(round(w * scale)), 32)
        scaled = cv2.resize(otsu, (new_w, target_h), interpolation=cv2.INTER_CUBIC)
        padded = cv2.copyMakeBorder(scaled, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=255)

        st.markdown("### Lưới ảnh các bước biến đổi liên tục")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(orig_rgb, caption="1. Ảnh gốc (RGB)", use_container_width=True)
            st.image(denoised, caption="4. Khử nhiễu Bilateral (A3)", use_container_width=True)
        with c2:
            st.image(gray, caption="2. Ảnh xám Grayscale (A1)", use_container_width=True)
            st.image(otsu, caption="5. Nhị phân hóa Otsu (A6)", use_container_width=True)
        with c3:
            st.image(clahe_img, caption="3. Cân bằng sáng CLAHE (A2)", use_container_width=True)
            st.image(padded, caption="6. Chuẩn hóa 48px + Đệm trắng (A8+A9)", use_container_width=True)

        st.markdown("---")
        st.markdown("### Phân tích biểu đồ mức xám (Grayscale Histogram)")
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        st.bar_chart(pd.DataFrame(hist, columns=["Tần suất mức xám"]))


# =============================================================================
# TAB 3: ÔN TẬP GHI NHỚ (SPACED REPETITION SM-2)
# =============================================================================
elif app_mode == "🧠 3. Ôn Tập Ghi Nhớ (Spaced Repetition SM-2)":
    st.markdown('<p class="main-header">🧠 ÔN TẬP THẺ NHỚ (SPACED REPETITION SM-2)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ứng dụng thuật toán khoa học SuperMemo SM-2 tự động tính toán chu kỳ lặp lại giúp người học tiếng Lào ghi nhớ vĩnh viễn.</p>', unsafe_allow_html=True)

    deck = st.session_state.flashcards
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    st.markdown(f"**Tổng số thẻ cá nhân:** {len(deck)} thẻ | **Ngày hôm nay:** `{today_str}`")

    if not deck:
        st.info("Hiện tại bạn chưa có thẻ flashcard nào. Hãy sang Tab 1 để tạo thẻ từ ảnh!")
    else:
        # Lựa chọn thẻ để ôn tập
        card_idx = st.selectbox("Chọn thẻ ôn tập:", range(len(deck)), format_func=lambda i: f"Thẻ {i+1}: {deck[i]['lao_text']} ({deck[i]['vi_meaning']})")
        curr_card = deck[card_idx]

        st.markdown(f"""
        <div class="flashcard-box">
            <div style="font-size: 0.9rem; color: #6c757d;">MẶT TRƯỚC (CHỮ LÀO)</div>
            <div class="lao-text-huge">{curr_card['lao_text']}</div>
        </div>
        """, unsafe_allow_html=True)

        show_ans = st.checkbox("👁️ Lật thẻ xem đáp án & phiên âm", value=False)
        if show_ans:
            st.markdown(f"""
            <div class="flashcard-box" style="border-color: #2ecc71;">
                <div style="font-size: 0.9rem; color: #27ae60;">MẶT SAU (ĐÁP ÁN)</div>
                <div class="rom-text">🔊 /{curr_card['romanization']}/</div>
                <div class="vi-trans">🇻🇳 {curr_card['vi_meaning']}</div>
                <hr style="margin: 10px 0;">
                <div style="font-size: 0.85rem; color: #555;">
                    Chu kỳ hiện tại: <b>{curr_card.get('interval_days', 1)} ngày</b> | 
                    Hệ số dễ nhớ EF: <b>{curr_card.get('easiness_factor', 2.5):.2f}</b> | 
                    Số lần nhớ đúng: <b>{curr_card.get('repetitions', 0)} lần</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Đánh giá mức độ ghi nhớ của bạn (Thuật toán SM-2):")
            b_cols = st.columns(6)
            ratings = [
                (0, "0: Quên sạch"),
                (1, "1: Nhớ sai"),
                (2, "2: Nhớ mang máng"),
                (3, "3: Nhớ khó khăn"),
                (4, "4: Nhớ tốt"),
                (5, "5: Nhớ hoàn hảo")
            ]
            for col, (score, label) in zip(b_cols, ratings):
                if col.button(label, key=f"rate_{score}"):
                    card_obj = FlashcardReviewState(**curr_card)
                    updated_card = review_card(card_obj, quality=score)
                    deck[card_idx] = asdict(updated_card)
                    st.session_state.flashcards = deck
                    save_user_flashcards(deck)
                    st.success(f"Đã lưu đánh giá {score}! Lần ôn tập tiếp theo: {updated_card.next_review} (sau {updated_card.interval_days} ngày)")
                    st.rerun()


# =============================================================================
# TAB 4: TRA CỨU TỪ ĐIỂN GIÁO TRÌNH (1,200 TỪ)
# =============================================================================
elif app_mode == "📖 4. Tra Cứu Từ Điển Giáo Trình (1,200 từ)":
    st.markdown('<p class="main-header">📖 KHO TỪ ĐIỂN GIÁO TRÌNH TIẾNG LÀO (1,200 MỤC TỪ)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tra cứu song ngữ Lào - Việt - Anh, từ loại, phiên âm và câu ví dụ minh họa chuẩn xác.</p>', unsafe_allow_html=True)

    dict_obj = translator.dictionary
    all_words = dict_obj.get_all_words()
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_kw = st.text_input("🔍 Tìm kiếm từ vựng (Nhập tiếng Lào hoặc tiếng Việt):", placeholder="Ví dụ: ສະບາຍດີ, Cảm ơn, Ăn, Du lịch...")
    with col_filter:
        lessons = sorted(list(set([dict_obj.lookup(w).get("lesson", "") for w in all_words])))
        selected_lesson = st.selectbox("Lọc theo chủ đề bài học:", ["Tất cả chủ đề"] + lessons)

    results = []
    for w in all_words:
        entry = dict_obj.lookup(w)
        if selected_lesson != "Tất cả chủ đề" and entry.get("lesson") != selected_lesson:
            continue
        if search_kw:
            sk = search_kw.lower()
            if sk not in entry["lao"] and sk not in entry["vi"].lower() and sk not in entry["en"].lower():
                continue
        results.append({
            "Từ tiếng Lào": entry["lao"],
            "Phiên âm": entry["romanization"],
            "Từ loại": entry["pos"],
            "Nghĩa Tiếng Việt": entry["vi"],
            "Nghĩa Tiếng Anh": entry["en"],
            "Chủ đề": entry["lesson"],
            "Ví dụ tiếng Lào": entry["example_lao"],
            "Dịch nghĩa ví dụ": entry["example_vi"]
        })

    st.markdown(f"**Tìm thấy:** `{len(results)}` mục từ phù hợp.")
    st.dataframe(pd.DataFrame(results), use_container_width=True, height=500)


# =============================================================================
# TAB 5: BẢNG ĐIỀU KHIỂN NGHIÊN CỨU (DASHBOARD)
# =============================================================================
elif app_mode == "📊 5. Bảng Điều Khiển Nghiên Cứu (Dashboard)":
    st.markdown('<p class="main-header">📊 BẢNG ĐIỀU KHIỂN KẾT QUẢ NGHIÊN CỨU KHOA HỌC</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tổng hợp đầy đủ 21 bảng số liệu và 12 biểu đồ chẩn đoán khoa học của toàn bộ đề tài (P0 đến P8).</p>', unsafe_allow_html=True)

    res_dir = os.path.join(PROJECT_ROOT, "experiments", "results")
    
    st.markdown("### 🏆 3 ĐÓNG GÓP KHOA HỌC CỐT LÕI CỦA ĐỀ TÀI")
    c1, c2, c3 = st.columns(3)
    c1.metric("Đóng góp #1 (P5)", "Ablation Study", "Khóa YAML & Golden Rule #3")
    c2.metric("Đóng góp #2 (P6)", "Weighted Levenshtein", "Word Acc 3.82% -> 29.30% (p<0.05)")
    c3.metric("Đóng góp #3 (P7+P8)", "LaoCRNN + Snap", "Word Acc 85.35% (28.5ms CPU)")

    st.markdown("---")
    dash_tab = st.selectbox("Chọn bảng số liệu muốn xem chi tiết:", [
        "Bảng 15: Điểm chuẩn Đa Kiến Trúc (Multi-Model Benchmark)",
        "Bảng 16: Đường cong học tập theo quy mô dữ liệu (Learning Curves)",
        "Bảng 18: Hiệp đồng Mô hình Học Sâu & Lexicon Snap",
        "Bảng 19: Phân đoạn từ tiếng Lào (Word Tokenization)",
        "Bảng 20: Đánh giá chất lượng dịch thuật (BLEU / chrF++)",
        "Bảng 21: Phân rã độ trễ toàn luồng End-to-End Pipeline",
        "Xem toàn bộ các Biểu đồ Khoa học PNG"
    ])

    if "Bảng 15" in dash_tab:
        f = os.path.join(res_dir, "p7_table15_multi_model_benchmark.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
            p = os.path.join(res_dir, "p7_model_comparison_radar_or_bars.png")
            if os.path.exists(p):
                st.image(p, caption="Biểu đồ so sánh Đa Kiến trúc OCR", use_container_width=True)
    elif "Bảng 16" in dash_tab:
        f = os.path.join(res_dir, "p7_table16_learning_curves_data_scale.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
            p = os.path.join(res_dir, "p7_learning_curves_and_scale.png")
            if os.path.exists(p):
                st.image(p, caption="Đường cong học tập theo quy mô dữ liệu", use_container_width=True)
    elif "Bảng 18" in dash_tab:
        f = os.path.join(res_dir, "p7_table18_lexicon_snap_integration.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
    elif "Bảng 19" in dash_tab:
        f = os.path.join(res_dir, "p8_table19_word_segmentation_comparison.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
    elif "Bảng 20" in dash_tab:
        f = os.path.join(res_dir, "p8_table20_translation_quality.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
    elif "Bảng 21" in dash_tab:
        f = os.path.join(res_dir, "p8_table21_latency_breakdown.csv")
        if os.path.exists(f):
            st.dataframe(pd.read_csv(f), use_container_width=True)
    elif "Biểu đồ" in dash_tab:
        png_files = [f for f in os.listdir(res_dir) if f.endswith(".png")]
        for pf in png_files:
            st.image(os.path.join(res_dir, pf), caption=pf, use_container_width=True)
