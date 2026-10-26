"""
ỨNG DỤNG WEB GIÁO DỤC TRỰC TUYẾN: OCR & HỖ TRỢ DỊCH TIẾNG LÀO
Dự án: Hệ thống OCR và Hỗ trợ Dịch Tiếng Lào cho Giáo dục Trực tuyến
Môn học: Xử lý ảnh (Digital Image Processing)
Framework: Streamlit
Hỗ trợ:
- Nhận dạng chữ in tiếng Lào đa động cơ (LaoCRNN SOTA, Tesseract P5, Tesseract Raw)
- Hậu xử lý từ điển Weighted Levenshtein & Lexicon Snap
- Tách từ, Phiên âm Latinh & Dịch nghĩa song ngữ Lào - Việt - Anh
- Kính lúp tiền xử lý ảnh số tương tác (Interactive Preprocessing Inspector)
- Bộ thẻ Flashcard cá nhân hóa tích hợp thuật toán Spaced Repetition (SuperMemo SM-2)
- Tra cứu kho từ điển giáo trình 1,200 mục từ (Hỗ trợ tìm kiếm ngữ âm / Romanization)
- Dashboard khoa học toàn diện tổng hợp 21 bảng số liệu và 12 biểu đồ nghiên cứu (P0 - P8)
"""
import os
import sys
import json
import time
from datetime import datetime
from dataclasses import asdict
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import cv2
from PIL import Image
import streamlit as st
import pandas as pd

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
from src.translation.translator import LaoTranslator, translate_full_paragraph
from src.education.sm2 import FlashcardReviewState, review_card
from src.education.feedback import save_user_correction
from src.ocr.document_ocr import run_document_ocr, detect_and_crop_lines
from src.postprocessing.sentence_corrector import LaoSentenceCorrector

# Thiết lập cấu hình trang Streamlit
local_flag_path = os.path.join(PROJECT_ROOT, "data", "assets", "lao_flag.png")
st.set_page_config(
    page_title="Lao OCR & Educational Translation",
    page_icon=local_flag_path if os.path.exists(local_flag_path) else "🇱🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện hiện đại, sang trọng, tương thích dark/light
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+Lao:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-header {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1e3a8a, #0284c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 22px;
        line-height: 1.5;
    }

    /* Thẻ Flashcard cao cấp */
    .flashcard-premium {
        background: radial-gradient(circle at 10% 20%, rgba(248, 250, 252, 0.95) 0%, rgba(241, 245, 249, 0.95) 90%);
        border-radius: 20px;
        padding: 28px 24px;
        border: 1px solid rgba(203, 213, 225, 0.8);
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
    }
    .flashcard-premium::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 5px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981);
    }
    .lao-text-huge {
        font-family: 'Noto Sans Lao', 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #0f172a;
        margin: 10px 0;
        line-height: 1.3;
        letter-spacing: 0.5px;
    }
    .rom-badge {
        display: inline-block;
        background: #fee2e2;
        color: #b91c1c;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 1.15rem;
        font-weight: 500;
        font-style: italic;
        margin-bottom: 14px;
        border: 1px solid #fecaca;
    }
    .vi-trans-text {
        font-size: 1.6rem;
        color: #047857;
        font-weight: 700;
        margin: 8px 0;
    }
    .en-trans-text {
        font-size: 1.25rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 6px;
    }

    /* Badges & Pills */
    .metric-badge {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 9999px;
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    .metric-badge-primary {
        background-color: #eff6ff;
        color: #1d4ed8;
        border-color: #bfdbfe;
    }
    .metric-badge-success {
        background-color: #ecfdf5;
        color: #047857;
        border-color: #a7f3d0;
    }

    /* Khung hiển thị tài liệu đoạn văn */
    .doc-display-card {
        background: #0f172a;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #1e293b;
        margin: 16px 0;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.4);
    }
    .doc-trans-section {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 8px;
        font-size: 1.12rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }

    /* Stat card tổng quan SM-2 */
    .sm2-stat-box {
        background: #f8fafc;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .sm2-stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e3a8a;
    }
    .sm2-stat-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
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
    
    # Nạp mô hình CRNN nếu có checkpoint
    crnn_model = None
    checkpoint_path = os.path.join(PROJECT_ROOT, "models", "crnn_lao.pt")
    if os.path.exists(checkpoint_path):
        import torch
        from src.models.crnn import LaoCRNN
        from src.models.lao_vocab import DEFAULT_LAO_VOCAB
        try:
            checkpoint = torch.load(checkpoint_path, map_location="cpu")
            crnn_model = LaoCRNN(vocab=DEFAULT_LAO_VOCAB, hidden_size=256)
            if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                crnn_model.load_state_dict(checkpoint["model_state_dict"])
            else:
                crnn_model.load_state_dict(checkpoint)
            crnn_model.eval()
        except Exception as e:
            print("[Warning] Không thể nạp CRNN checkpoint:", e)
            crnn_model = None
            
    return pipeline, matcher, translator, crnn_model


pipeline, matcher, translator, crnn_model = load_system_engines()
if not hasattr(translator, "translate_full_paragraph"):
    import types
    translator.translate_full_paragraph = types.MethodType(
        lambda self, text: translate_full_paragraph(text, translator=self), translator
    )

# Khởi tạo Deck Flashcard trong session_state
FLASHCARD_DB = os.path.join(PROJECT_ROOT, "data", "flashcards_deck.json")

def load_user_flashcards() -> List[Dict[str, Any]]:
    if not os.path.exists(FLASHCARD_DB):
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

def save_user_flashcards(cards: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(FLASHCARD_DB), exist_ok=True)
    with open(FLASHCARD_DB, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

if "flashcards" not in st.session_state:
    st.session_state.flashcards = load_user_flashcards()


# =============================================================================
# GIAO DIỆN CHÍNH & SIDEBAR
# =============================================================================
if os.path.exists(local_flag_path):
    st.sidebar.image(local_flag_path, width=130)

st.sidebar.markdown("""
<div style="margin-top: 4px; margin-bottom: 14px;">
    <h2 style="margin: 0; font-size: 1.55rem; font-weight: 800; color: #38bdf8; letter-spacing: -0.4px;">Lao OCR & EdTech</h2>
    <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8; font-weight: 500;">Hệ thống OCR & Dịch Tiếng Lào cho Giáo dục Trực tuyến</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")


app_mode = st.sidebar.radio(
    "CHỌN PHÂN HỆ CHỨC NĂNG:",
    [
        "🎴 1. Nhận Dạng Thẻ Flashcard (Live OCR)",
        "📄 2. Nhận Dạng Đoạn Văn Bản (Document OCR)",
        "🔬 3. Kính Lúp Tiền Xử Lý (Image Inspector)",
        "🧠 4. Ôn Tập Ghi Nhớ (Spaced Repetition SM-2)",
        "📖 5. Tra Cứu Từ Điển Giáo Trình (1,200 từ)",
        "📊 6. Bảng Điều Khiển Nghiên Cứu (Dashboard)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Thông tin Hệ thống:**
- **Mô hình OCR:** LaoCRNN + CTC (SOTA 85.35% Acc)
- **Hậu xử lý:** Weighted Levenshtein (p < 0.05)
- **Từ điển:** 1,200 từ chuẩn NFC
- **Độ trễ toàn luồng:** **51.5 ms** (CPU Offline)
- **Môn học:** Xử lý ảnh số (Digital Image Processing)
""")


# =============================================================================
# PHÂN HỆ 1: NHẬN DẠNG & THẺ FLASHCARD TƯƠNG TÁC (LIVE OCR)
# =============================================================================
if app_mode == "🎴 1. Nhận Dạng Thẻ Flashcard (Live OCR)":
    st.markdown('<p class="main-header">🎴 NHẬN DẠNG TỪ VỰNG & TẠO THẺ FLASHCARD</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Nhận dạng chữ in tiếng Lào từ flashcard / thẻ từ vựng đơn dòng, tự động sửa lỗi qua từ điển có trọng số và tạo thẻ ôn tập Spaced Repetition (SM-2).</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("1. Chọn nguồn ảnh đầu vào")
        input_source = st.radio(
            "Nguồn ảnh:",
            ["Tải ảnh lên từ máy tính", "Chọn từ thư viện Gold Set"],
            horizontal=True,
            key="tab1_source_radio"
        )
        
        image_to_process = None
        image_name = "sample.jpg"
        current_image_id = None

        if input_source == "Tải ảnh lên từ máy tính":
            uploaded_file = st.file_uploader(
                "Tải lên ảnh thẻ flashcard hoặc từ vựng tiếng Lào (PNG/JPG):",
                type=["png", "jpg", "jpeg"],
                key="tab1_uploader"
            )
            if uploaded_file is not None:
                image_to_process = Image.open(uploaded_file).convert("RGB")
                image_name = uploaded_file.name
                current_image_id = f"upload_{uploaded_file.name}_{uploaded_file.size}"
                st.image(image_to_process, caption=f"Ảnh tải lên: {uploaded_file.name}", use_container_width=True)
                
                # Cảnh báo thông minh nếu ảnh có nhiều dòng
                img_w, img_h = image_to_process.size
                if img_h > 100 and (img_w / img_h) < 4.0:
                    st.warning("💡 **Lưu ý:** Ảnh này có vẻ là một **đoạn văn bản nhiều dòng**! Phân hệ này tối ưu cho từ vựng / cụm từ 1 dòng. Nếu muốn nhận dạng và dịch trọn vẹn cả đoạn văn, bạn hãy chọn phân hệ **'📄 2. Nhận Dạng Đoạn Văn Bản (Document OCR)'** ở thanh bên.")
            else:
                st.info("👆 Vui lòng chọn file ảnh định dạng PNG hoặc JPG từ máy tính của bạn.")
        else:
            gold_dir = os.path.join(PROJECT_ROOT, "data", "gold", "images")
            if os.path.exists(gold_dir):
                sample_files = [f for f in os.listdir(gold_dir) if f.endswith((".jpg", ".png"))][:30]
                selected_sample = st.selectbox("Chọn ảnh mẫu trong tập Gold Set:", sample_files, key="tab1_gold_select")
                if selected_sample:
                    image_path = os.path.join(gold_dir, selected_sample)
                    image_to_process = Image.open(image_path).convert("RGB")
                    image_name = selected_sample
                    current_image_id = f"gold_{selected_sample}"
                    st.image(image_to_process, caption=f"Mẫu Gold Set: {selected_sample}", use_container_width=True)
            else:
                st.warning("Chưa tìm thấy thư mục Gold Set tại `data/gold/images`.")

        st.subheader("2. Cấu hình Nhận dạng")
        engine_choice = st.selectbox(
            "Chọn Mô hình Nhận dạng OCR:",
            [
                "🚀 LaoCRNN + Weighted Lexicon Snap (Khuyến nghị - SOTA 85.35% Acc)",
                "⚡ LaoCRNN Standalone (Học sâu thuần túy - 35.67% Acc)",
                "🔧 Tesseract 5 + Tiền xử lý tối ưu P5 (7.01% Acc)",
                "📜 Tesseract 5 Raw (Baseline Gốc - 6.37% Acc)"
            ],
            key="tab1_engine_select"
        )
        use_deskew = st.checkbox(
            "Khử nghiêng ảnh (Moment Deskew)",
            value=False,
            help="Lưu ý: Nghiên cứu P5 cho thấy Deskew có thể làm lệch trục flashcard dòng ngắn.",
            key="tab1_deskew_chk"
        )

    with col_right:
        st.subheader("3. Kết quả Nhận dạng & Dịch thuật")
        
        if "ocr_result" not in st.session_state:
            st.session_state.ocr_result = None
        if "last_processed_img_id" not in st.session_state:
            st.session_state.last_processed_img_id = None

        # Tự động xóa kết quả OCR của ảnh cũ khi người dùng đổi ảnh mới
        if current_image_id is not None and st.session_state.last_processed_img_id != current_image_id:
            st.session_state.ocr_result = None

        if image_to_process is not None:
            if st.button("🚀 THỰC HIỆN NHẬN DẠNG & TỔNG HỢP FLASHCARD", type="primary", use_container_width=True, key="tab1_run_btn"):
                with st.spinner("Đang chạy toàn luồng: Tiền xử lý DIP ➔ OCR ➔ Weighted Lexicon Snap ➔ NLP Dịch thuật..."):
                    t_start = time.perf_counter()
                    img_np = np.array(image_to_process)

                    # TỰ ĐỘNG PHÁT HIỆN: Ảnh có phải là đoạn văn bản nhiều dòng không?
                    detected_crops, detected_boxes, annotated_line_img = detect_and_crop_lines(img_np, method="hpp")
                    is_multi_line = len(detected_crops) >= 2

                    if is_multi_line:
                        # TỔNG HỢP VĂN BẢN ĐA DÒNG CHO THẺ FLASHCARD
                        doc_res = run_document_ocr(
                            image_np=img_np,
                            crnn_model=crnn_model,
                            engine_choice="crnn",
                            segmentation_method="hpp"
                        )
                        elapsed_ms = (time.perf_counter() - t_start) * 1000

                        st.session_state.last_processed_img_id = current_image_id
                        st.session_state.ocr_result = {
                            "is_multi_line": True,
                            "raw_pred": doc_res.full_text,
                            "final_lao": doc_res.full_text,
                            "annotated_image": doc_res.annotated_image,
                            "num_lines": doc_res.num_lines,
                            "elapsed_ms": elapsed_ms,
                            "engine_choice": "LaoCRNN + HPP Line Segmentation",
                            "confidence": 1.0,
                            "image_name": image_name
                        }
                        st.session_state["active_lao_input"] = doc_res.full_text
                        st.session_state["feedback_input"] = doc_res.full_text
                    else:
                        # Tiền xử lý ảnh đơn dòng
                        cfg_copy = dict(pipeline.config)
                        if isinstance(cfg_copy.get("deskew"), dict):
                            cfg_copy["deskew"] = dict(cfg_copy["deskew"])
                            cfg_copy["deskew"]["enabled"] = use_deskew
                        
                        sub_pipe = PreprocessingPipeline(config=cfg_copy)
                        proc_res = sub_pipe.process(img_np)
                        processed_img = proc_res[0] if isinstance(proc_res, tuple) else proc_res

                        # OCR đa động cơ
                        raw_pred = ""
                        if "LaoCRNN" in engine_choice and crnn_model is not None:
                            try:
                                raw_pred = crnn_model.predict_image(processed_img)
                            except Exception:
                                raw_pred = ""
                            if not raw_pred.strip():
                                try:
                                    import pytesseract
                                    raw_pred = pytesseract.image_to_string(processed_img, lang='lao', config='--psm 7')
                                except Exception:
                                    pass
                        else:
                            try:
                                import pytesseract
                                raw_pred = pytesseract.image_to_string(processed_img, lang='lao', config='--psm 7')
                            except Exception:
                                raw_pred = ""

                        raw_pred = normalize_lao(raw_pred).strip()

                        # Hậu xử lý từ điển Weighted Levenshtein
                        final_lao = raw_pred
                        confidence = 1.0
                        if raw_pred and "Lexicon Snap" in engine_choice:
                            snap_res = matcher.match(raw_pred, method="weighted_levenshtein")
                            if snap_res.best_lao and snap_res.confidence >= 0.35:
                                final_lao = snap_res.best_lao
                                confidence = snap_res.confidence

                        elapsed_ms = (time.perf_counter() - t_start) * 1000

                        st.session_state.last_processed_img_id = current_image_id
                        st.session_state.ocr_result = {
                            "is_multi_line": False,
                            "raw_pred": raw_pred,
                            "final_lao": final_lao,
                            "elapsed_ms": elapsed_ms,
                            "engine_choice": engine_choice,
                            "confidence": confidence,
                            "image_name": image_name
                        }
                        st.session_state["active_lao_input"] = final_lao if final_lao else "ທຸກໆຄົນ"
                        st.session_state["feedback_input"] = final_lao if final_lao else ""

            # Hiển thị kết quả nhận dạng & Thẻ Flashcard học tập
            if st.session_state.ocr_result is not None:
                res = st.session_state.ocr_result

                if res.get("is_multi_line", False):
                    st.info(
                        f"💡 **Phát hiện {res.get('num_lines', 2)} dòng chữ:** Toàn bộ nội dung đã được nhận dạng thành Thẻ bên dưới. "
                        "Bạn cũng có thể sang phân hệ **'📄 2. Nhận Dạng Đoạn Văn Bản'** để xem từng dòng phân đoạn."
                    )

                current_text = res["final_lao"]
                if not current_text:
                    st.warning("⚠️ OCR chưa nhận diện rõ ký tự từ ảnh. Bạn có thể tự gõ chữ tiếng Lào vào ô bên dưới:")

                if "active_lao_input" not in st.session_state:
                    st.session_state["active_lao_input"] = current_text if current_text else "ສະບາຍດີ"

                if res.get("is_multi_line", False):
                    active_lao = st.text_area(
                        "✏️ Văn bản tiếng Lào nhận dạng (có thể sửa nhanh):",
                        key="active_lao_input",
                        height=100
                    )
                else:
                    active_lao = st.text_input(
                        "✏️ Văn bản tiếng Lào nhận dạng (có thể sửa nhanh):",
                        key="active_lao_input"
                    )
                active_lao = normalize_lao(active_lao).strip()

                if active_lao:
                    # Dịch thuật
                    if "\n" in active_lao or len(active_lao.split()) > 2:
                        vi_trans, en_trans, doc_glosses = translate_full_paragraph(active_lao, translator=translator)
                        trans_output = translator.translate(active_lao)
                        if vi_trans:
                            trans_output.translation_vi = vi_trans
                        if en_trans:
                            trans_output.translation_en = en_trans
                        if doc_glosses:
                            trans_output.glosses = doc_glosses
                    else:
                        trans_output = translator.translate(active_lao)

                    # HIỂN THỊ THẺ FLASHCARD CAO CẤP
                    st.markdown(f"""
                    <div class="flashcard-premium">
                        <div class="lao-text-huge">{trans_output.original_lao}</div>
                        <div class="rom-badge">🔊 /{trans_output.romanization}/</div>
                        <div class="vi-trans-text">🇻🇳 {trans_output.translation_vi}</div>
                        <div class="en-trans-text">🇬🇧 {trans_output.translation_en}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div>
                        <span class="metric-badge metric-badge-primary">⏱️ Độ trễ: {res['elapsed_ms']:.1f} ms</span>
                        <span class="metric-badge metric-badge-success">🎯 Động cơ: {res['engine_choice'].split('(')[0].strip()}</span>
                        <span class="metric-badge">📚 Số từ: {len(trans_output.tokens)}</span>
                        <span class="metric-badge">Độ tin cậy: {res['confidence'] * 100:.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Chú giải chi tiết từng từ
                    if trans_output.glosses:
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

                    # Thao tác hành động
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        if st.button("➕ Thêm Vào Bộ Ôn Tập SM-2", type="primary", use_container_width=True, key="tab1_add_sm2_btn"):
                            card_id = f"c_{int(time.time())}"
                            new_card = FlashcardReviewState(
                                card_id=card_id,
                                lao_text=trans_output.original_lao,
                                vi_meaning=trans_output.translation_vi,
                                romanization=trans_output.romanization
                            )
                            st.session_state.flashcards.append(asdict(new_card))
                            save_user_flashcards(st.session_state.flashcards)
                            st.success("✅ Đã lưu thẻ vào bộ nhớ Spaced Repetition cá nhân!")
                    with btn_col2:
                        st.caption("Mẹo: Bạn có thể chỉnh sửa chữ trực tiếp trong ô phía trên trước khi thêm vào bộ nhớ.")

                    # Hộp phản hồi sửa lỗi
                    with st.expander("🛠️ Phát hiện kết quả chưa chuẩn? Gửi phản hồi sửa lỗi"):
                        user_correct = st.text_input("Nội dung tiếng Lào đúng:", key="feedback_input")
                        user_note = st.text_input("Ghi chú bổ sung (tuỳ chọn):", key="feedback_note")
                        if st.button("Gửi đóng góp", key="tab1_send_feedback_btn"):
                            save_user_correction(res["image_name"], res["raw_pred"], user_correct, res["engine_choice"], user_note)
                            st.info("Cảm ơn bạn! Đóng góp đã được lưu vào hệ thống Continuous Learning.")
            else:
                st.info("👆 Hãy bấm nút **'🚀 THỰC HIỆN NHẬN DẠNG & TỔNG HỢP FLASHCARD'** để bắt đầu phân tích ảnh.")
        else:
            st.info("👈 Hãy tải ảnh lên hoặc chọn một mẫu từ thư viện Gold Set bên trái.")


# =============================================================================
# PHÂN HỆ 2: NHẬN DẠNG ĐOẠN VĂN BẢN & TÀI LIỆU (DOCUMENT OCR)
# =============================================================================
elif app_mode == "📄 2. Nhận Dạng Đoạn Văn Bản (Document OCR)":
    st.markdown('<p class="main-header">📄 NHẬN DẠNG ĐOẠN VĂN BẢN & TÀI LIỆU TIẾNG LÀO</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Phân đoạn dòng tự động bằng thuật toán DIP (HPP / RLSA), nhận dạng đa dòng, dịch thuật ngữ cảnh và tự động nắn chỉnh chính tả.</p>', unsafe_allow_html=True)

    doc_col_left, doc_col_right = st.columns([1, 1], gap="large")

    with doc_col_left:
        st.subheader("1. Chọn nguồn ảnh tài liệu / đoạn văn")
        doc_input_source = st.radio(
            "Nguồn ảnh tài liệu:",
            ["Tải ảnh lên từ máy tính", "Chọn từ thư viện Gold Set"],
            horizontal=True,
            key="doc_input_source"
        )
        
        doc_image_to_process = None
        doc_image_name = "document.jpg"
        current_doc_image_id = None

        if doc_input_source == "Tải ảnh lên từ máy tính":
            uploaded_doc = st.file_uploader(
                "Tải lên ảnh chụp đoạn văn bản / tài liệu tiếng Lào (PNG/JPG):",
                type=["png", "jpg", "jpeg"],
                key="doc_file_uploader"
            )
            if uploaded_doc is not None:
                doc_image_to_process = Image.open(uploaded_doc).convert("RGB")
                doc_image_name = uploaded_doc.name
                current_doc_image_id = f"doc_upload_{uploaded_doc.name}_{uploaded_doc.size}"
                st.image(doc_image_to_process, caption="Ảnh tài liệu tải lên", use_container_width=True)
            else:
                st.info("👆 Vui lòng tải lên ảnh chụp tài liệu tiếng Lào từ máy tính.")
        else:
            gold_dir = os.path.join(PROJECT_ROOT, "data", "gold", "images")
            if os.path.exists(gold_dir):
                # Ưu tiên các ảnh textbook
                all_gold = os.listdir(gold_dir)
                textbook_samples = [f for f in all_gold if "textbook" in f and f.endswith((".jpg", ".png"))]
                other_samples = [f for f in all_gold if f.endswith((".jpg", ".png")) and f not in textbook_samples][:20]
                sample_files = textbook_samples + other_samples
                
                selected_doc = st.selectbox("Chọn ảnh mẫu tài liệu trong Gold Set:", sample_files, key="doc_sample_select")
                if selected_doc:
                    doc_path = os.path.join(gold_dir, selected_doc)
                    doc_image_to_process = Image.open(doc_path).convert("RGB")
                    doc_image_name = selected_doc
                    current_doc_image_id = f"doc_gold_{selected_doc}"
                    st.image(doc_image_to_process, caption=f"Mẫu tài liệu: {selected_doc}", use_container_width=True)

        st.subheader("2. Cấu hình Nhận dạng Đoạn văn")
        doc_engine_choice = st.selectbox(
            "Chọn Động cơ OCR Đoạn văn:",
            [
                "🌟 Động cơ Lai Thông minh (Hybrid CRNN + Tesseract + Lexicon Snap - Khuyên dùng)",
                "🚀 LaoCRNN + Line Segmentation (SOTA Tách dòng DIP)",
                "📜 Tesseract 5 PSM 7 (Line-by-line Tách dòng)",
                "📦 Tesseract 5 PSM 6 (Khối toàn trang - Baseline)"
            ],
            key="doc_engine_choice"
        )
        seg_method = st.selectbox(
            "Thuật toán phân đoạn dòng (Line Segmentation):",
            ["Horizontal Projection Profile (HPP)", "Run-Length Smoothing Algorithm (RLSA)"],
            help="HPP phân tích biểu đồ mật độ pixel theo trục Y; RLSA nối dài khoảng trống nét chữ.",
            key="doc_seg_method"
        )

    with doc_col_right:
        st.subheader("3. Kết quả Nhận dạng & Dịch thuật Đoạn văn")

        if "doc_ocr_result" not in st.session_state:
            st.session_state.doc_ocr_result = None
        if "doc_last_processed_img_id" not in st.session_state:
            st.session_state.doc_last_processed_img_id = None

        if current_doc_image_id is not None and st.session_state.doc_last_processed_img_id != current_doc_image_id:
            st.session_state.doc_ocr_result = None

        if doc_image_to_process is not None:
            if st.button("🚀 THỰC HIỆN NHẬN DẠNG ĐOẠN VĂN & DỊCH THUẬT", type="primary", use_container_width=True, key="btn_run_doc_ocr"):
                with st.spinner("Đang xử lý phân đoạn dòng DIP -> OCR đa dòng -> NLP -> Dịch thuật..."):
                    doc_img_np = np.array(doc_image_to_process)
                    method_code = "rlsa" if "RLSA" in seg_method else "hpp"
                    if "Lai" in doc_engine_choice:
                        engine_code = "hybrid"
                    elif "LaoCRNN" in doc_engine_choice:
                        engine_code = "crnn"
                    elif "PSM 6" in doc_engine_choice:
                        engine_code = "block"
                    else:
                        engine_code = "tess_lines"

                    doc_res = run_document_ocr(
                        image_np=doc_img_np,
                        crnn_model=crnn_model,
                        engine_choice=engine_code,
                        segmentation_method=method_code
                    )

                    st.session_state.doc_last_processed_img_id = current_doc_image_id
                    st.session_state.doc_ocr_result = doc_res
                    st.session_state["active_doc_lao_input"] = doc_res.full_text

            if st.session_state.doc_ocr_result is not None:
                d_res = st.session_state.doc_ocr_result

                st.markdown(f"""
                <div style="margin-bottom: 12px;">
                    <span class="metric-badge metric-badge-primary">📏 Phát hiện: {d_res.num_lines} dòng</span>
                    <span class="metric-badge metric-badge-success">⚡ Độ trễ: {d_res.elapsed_ms:.1f} ms</span>
                    <span class="metric-badge">⚙️ Động cơ: {d_res.engine_name}</span>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔬 Xem Bounding Boxes phân đoạn dòng (Line Segmentation DIP)", expanded=False):
                    st.image(d_res.annotated_image, caption=f"Phát hiện {d_res.num_lines} dòng văn bản (Khung xanh)", use_container_width=True)

                if "active_doc_lao_input" not in st.session_state:
                    st.session_state["active_doc_lao_input"] = d_res.full_text

                active_doc_text = st.text_area(
                    "✏️ Văn bản tiếng Lào đã nhận dạng (có thể chỉnh sửa nếu cần):",
                    key="active_doc_lao_input",
                    height=130
                )

                if st.button("🪄 Tự Động Nắn Chỉnh Lỗi Chính Tả & Khớp Từ Điển (Spell-Fix)", use_container_width=True, key="btn_doc_spellfix"):
                    corrector = LaoSentenceCorrector()
                    fixed_text = corrector.correct_sentence(st.session_state.get("active_doc_lao_input", ""))
                    st.session_state["active_doc_lao_input"] = fixed_text
                    st.rerun()

                active_doc_text = normalize_lao(active_doc_text).strip()

                if active_doc_text:
                    full_vi_text, full_en_text, all_glosses = translate_full_paragraph(active_doc_text, translator=translator)

                    st.markdown(f"""
                    <div class="doc-display-card">
                        <div style="margin-bottom: 16px;">
                            <div style="font-weight: 700; font-size: 1.15rem; color: #fbbf24; margin-bottom: 6px;">
                                🇻🇳 BẢN DỊCH TIẾNG VIỆT
                            </div>
                            <div class="doc-trans-section" style="color: #f8fafc; border-left: 4px solid #f59e0b;">
{full_vi_text}
                            </div>
                        </div>
                        <div style="margin-top: 14px;">
                            <div style="font-weight: 700; font-size: 1.1rem; color: #34d399; margin-bottom: 6px;">
                                🇬🇧 BẢN DỊCH TIẾNG ANH (ENGLISH)
                            </div>
                            <div class="doc-trans-section" style="color: #f1f5f9; border-left: 4px solid #10b981;">
{full_en_text}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if all_glosses:
                        st.markdown("#### 📚 Bóc Tách Từ Vựng Cốt Lõi Trong Bài (Key Vocabulary)")
                        doc_vocab_data = []
                        for g in all_glosses:
                            doc_vocab_data.append({
                                "Từ tiếng Lào": g.lao,
                                "Phiên âm": g.romanization,
                                "Từ loại": g.pos,
                                "Nghĩa Tiếng Việt": g.vi,
                                "Nghĩa Tiếng Anh": g.en,
                                "Ví dụ": f"{g.example_lao} ({g.example_vi})" if g.example_lao else "-"
                            })
                        st.dataframe(pd.DataFrame(doc_vocab_data), use_container_width=True)

                        if st.button("➕ Thêm Tất Cả Từ Vựng Bài Này Vào Bộ Nhớ Ôn Tập (SM-2)", use_container_width=True, key="btn_add_all_doc_vocab"):
                            added_count = 0
                            for g in all_glosses:
                                c_id = f"doc_{int(time.time())}_{added_count}"
                                new_card = FlashcardReviewState(
                                    card_id=c_id,
                                    lao_text=g.lao,
                                    vi_meaning=g.vi,
                                    romanization=g.romanization
                                )
                                st.session_state.flashcards.append(asdict(new_card))
                                added_count += 1
                            save_user_flashcards(st.session_state.flashcards)
                            st.success(f"✅ Đã thêm thành công {added_count} từ vựng từ bài đọc vào bộ Spaced Repetition!")
            else:
                st.info("👆 Vui lòng bấm nút **'🚀 THỰC HIỆN NHẬN DẠNG ĐOẠN VĂN & DỊCH THUẬT'** ở trên để phân tích ảnh.")
        else:
            st.info("👈 Vui lòng tải ảnh tài liệu lên hoặc chọn mẫu bên trái.")


# =============================================================================
# PHÂN HỆ 3: KÍNH LÚP TIỀN XỬ LÝ ẢNH (PREPROCESSING INSPECTOR)
# =============================================================================
elif app_mode == "🔬 3. Kính Lúp Tiền Xử Lý (Image Inspector)":
    st.markdown('<p class="main-header">🔬 KÍNH LÚP TIỀN XỬ LÝ ẢNH (PREPROCESSING INSPECTOR)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Trực quan hóa từng bước trong chuỗi 12 phép biến đổi xử lý ảnh số (Digital Image Processing) phục vụ nghiên cứu khoa học và chẩn đoán mô hình.</p>', unsafe_allow_html=True)

    insp_c1, insp_c2 = st.columns([1, 2], gap="large")

    with insp_c1:
        st.subheader("1. Nguồn ảnh kiểm tra")
        insp_source = st.radio("Chọn nguồn ảnh:", ["Ảnh mẫu Gold Set", "Tải ảnh từ máy tính"], horizontal=True, key="insp_source_radio")
        
        target_img = None
        if insp_source == "Ảnh mẫu Gold Set":
            gold_dir = os.path.join(PROJECT_ROOT, "data", "gold", "images")
            sample_files = [f for f in os.listdir(gold_dir) if f.endswith((".jpg", ".png"))][:25] if os.path.exists(gold_dir) else []
            sel_img = st.selectbox("Chọn ảnh mẫu:", sample_files, key="insp_sample_select")
            if sel_img:
                img_p = os.path.join(gold_dir, sel_img)
                target_img = cv2.imread(img_p)
                target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
        else:
            up_insp = st.file_uploader("Tải lên ảnh cần soi kính lúp DIP:", type=["png", "jpg", "jpeg"], key="insp_uploader")
            if up_insp:
                target_img = np.array(Image.open(up_insp).convert("RGB"))

        st.subheader("2. Siêu tham số điều chỉnh tương tác")
        clahe_clip = st.slider("CLAHE Clip Limit (A2 Cân bằng sáng):", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
        denoise_choice = st.selectbox("Bộ lọc khử nhiễu (A3 Denoise):", ["Bilateral Filter (Bảo toàn cạnh)", "Gaussian Filter", "Median Filter"])
        bin_choice = st.selectbox("Thuật toán Nhị phân hóa (A6 Binarization):", ["Otsu (Toàn cục)", "Sauvola (Thích nghi cửa sổ)", "Adaptive Mean", "Adaptive Gaussian"])
        target_h_norm = st.select_slider("Chuẩn hóa chiều cao dòng chữ (A8 Height Norm):", options=[24, 32, 48, 64], value=48)

    with insp_c2:
        if target_img is not None:
            st.subheader("3. Lưới các bước biến đổi trung gian của Pipeline")
            
            # Khởi tạo pipeline với siêu tham số tương tác
            bin_map = {"Otsu (Toàn cục)": "otsu", "Sauvola (Thích nghi cửa sổ)": "sauvola", "Adaptive Mean": "adaptive_mean", "Adaptive Gaussian": "adaptive_gaussian"}
            denoise_map = {"Bilateral Filter (Bảo toàn cạnh)": "bilateral", "Gaussian Filter": "gaussian", "Median Filter": "median"}

            interactive_cfg = {
                "grayscale": {"enabled": True, "method": "bgr2gray"},
                "illumination": {"enabled": True, "method": "clahe", "clip_limit": clahe_clip},
                "denoise": {"enabled": True, "method": denoise_map[denoise_choice]},
                "deskew": {"enabled": False},
                "binarization": {"enabled": True, "method": bin_map[bin_choice], "window_size": 25, "k": 0.2},
                "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]},
                "height_normalization": {"enabled": True, "target_height": target_h_norm},
                "border_padding": {"enabled": True, "padding_px": 15, "crop_outer_px": 0}
            }
            
            pipe_insp = PreprocessingPipeline(config=interactive_cfg)
            final_bin, stages = pipe_insp.process(target_img, return_stages=True)

            g1, g2, g3 = st.columns(3)
            with g1:
                st.image(stages.get("0_original", target_img), caption="1. Ảnh gốc (RGB)", use_container_width=True)
                st.image(stages.get("A3_denoise", target_img), caption="4. Khử nhiễu (A3)", use_container_width=True)
            with g2:
                st.image(stages.get("A1_grayscale", target_img), caption="2. Ảnh xám Grayscale (A1)", use_container_width=True)
                st.image(stages.get("A6_binarization", target_img), caption="5. Nhị phân hóa (A6)", use_container_width=True)
            with g3:
                st.image(stages.get("A2_illumination", target_img), caption=f"3. CLAHE Clip={clahe_clip} (A2)", use_container_width=True)
                st.image(final_bin, caption=f"6. Chuẩn hóa {target_h_norm}px + Đệm (A8+A9)", use_container_width=True)

            st.markdown("---")
            st.subheader("4. Phân tích Biểu đồ Mức Xám (Grayscale Histogram)")
            gray_stage = stages.get("A1_grayscale", cv2.cvtColor(target_img, cv2.COLOR_RGB2GRAY))
            hist = cv2.calcHist([gray_stage], [0], None, [256], [0, 256]).ravel()
            hist_df = pd.DataFrame({"Mức xám (0 - 255)": range(256), "Tần suất pixel": hist})
            st.bar_chart(hist_df, x="Mức xám (0 - 255)", y="Tần suất pixel", height=240)
        else:
            st.info("👈 Hãy chọn một ảnh mẫu hoặc tải ảnh lên để bắt đầu soi các bước xử lý ảnh số.")


# =============================================================================
# PHÂN HỆ 4: ÔN TẬP GHI NHỚ (SPACED REPETITION SM-2)
# =============================================================================
elif app_mode == "🧠 4. Ôn Tập Ghi Nhớ (Spaced Repetition SM-2)":
    st.markdown('<p class="main-header">🧠 ÔN TẬP THẺ NHỚ (SPACED REPETITION SM-2)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Thuật toán khoa học SuperMemo SM-2 tự động tính toán hệ số dễ nhớ (Easiness Factor EF) và khoảng cách ngày ôn tập tối ưu để chống quên lãng.</p>', unsafe_allow_html=True)

    deck = st.session_state.flashcards
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Thống kê nhanh
    due_today_count = sum(1 for c in deck if c.get("next_review", today_str) <= today_str)
    mastered_count = sum(1 for c in deck if c.get("repetitions", 0) >= 3 and c.get("easiness_factor", 2.5) >= 2.5)
    learning_count = len(deck) - mastered_count

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="sm2-stat-box"><div class="sm2-stat-num">{len(deck)}</div><div class="sm2-stat-label">Tổng số thẻ</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="sm2-stat-box"><div class="sm2-stat-num" style="color: #dc2626;">{due_today_count}</div><div class="sm2-stat-label">Cần ôn hôm nay</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="sm2-stat-box"><div class="sm2-stat-num" style="color: #16a34a;">{mastered_count}</div><div class="sm2-stat-label">Đã thuộc làu</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="sm2-stat-box"><div class="sm2-stat-num" style="color: #d97706;">{learning_count}</div><div class="sm2-stat-label">Đang học</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    if not deck:
        st.info("Hiện tại bạn chưa có thẻ flashcard nào trong bộ nhớ. Hãy sang Phân hệ 1 hoặc Phân hệ 2 để thêm thẻ từ ảnh!")
    else:
        filter_mode = st.radio("Chế độ ôn tập:", ["Chỉ ôn thẻ đến hạn hôm nay (Due Today)", "Duyệt tất cả thẻ trong kho"], horizontal=True, key="sm2_filter_radio")
        
        filtered_indices = []
        for idx, c in enumerate(deck):
            if filter_mode == "Chỉ ôn thẻ đến hạn hôm nay (Due Today)":
                if c.get("next_review", today_str) <= today_str:
                    filtered_indices.append(idx)
            else:
                filtered_indices.append(idx)

        if not filtered_indices:
            st.success("🎉 Xuất sắc! Bạn đã hoàn thành toàn bộ các thẻ cần ôn tập cho ngày hôm nay! Bạn có thể chuyển sang chế độ 'Duyệt tất cả thẻ' nếu muốn ôn lại.")
        else:
            selected_filtered_idx = st.selectbox(
                "Chọn thẻ cần ôn tập:",
                range(len(filtered_indices)),
                format_func=lambda i: f"Thẻ #{filtered_indices[i]+1}: {deck[filtered_indices[i]]['lao_text']} ({deck[filtered_indices[i]]['vi_meaning']})",
                key="sm2_card_select"
            )
            real_card_idx = filtered_indices[selected_filtered_idx]
            curr_card = deck[real_card_idx]

            # MẶT TRƯỚC
            st.markdown(f"""
            <div class="flashcard-premium">
                <div style="font-size: 0.95rem; font-weight: 700; color: #64748b; letter-spacing: 1px;">MẶT TRƯỚC (CHỮ LÀO)</div>
                <div class="lao-text-huge">{curr_card['lao_text']}</div>
            </div>
            """, unsafe_allow_html=True)

            show_ans = st.checkbox("👁️ Lật thẻ xem đáp án & phiên âm", value=False, key=f"show_ans_{real_card_idx}")
            if show_ans:
                st.markdown(f"""
                <div class="flashcard-premium" style="border-color: #86efac; background: #f0fdf4;">
                    <div style="font-size: 0.95rem; font-weight: 700; color: #15803d; letter-spacing: 1px;">MẶT SAU (ĐÁP ÁN)</div>
                    <div class="rom-badge">🔊 /{curr_card['romanization']}/</div>
                    <div class="vi-trans-text">🇻🇳 {curr_card['vi_meaning']}</div>
                    <div style="margin-top: 10px; font-size: 0.88rem; color: #475569;">
                        Chu kỳ hiện tại: <b>{curr_card.get('interval_days', 1)} ngày</b> | 
                        Hệ số dễ nhớ EF: <b>{curr_card.get('easiness_factor', 2.5):.2f}</b> | 
                        Số lần lặp đúng: <b>{curr_card.get('repetitions', 0)} lần</b> |
                        Lần ôn tới: <b>{curr_card.get('next_review', today_str)}</b>
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
                    if col.button(label, key=f"rate_{score}_{real_card_idx}", use_container_width=True):
                        card_obj = FlashcardReviewState(**curr_card)
                        updated_card = review_card(card_obj, quality=score)
                        deck[real_card_idx] = asdict(updated_card)
                        st.session_state.flashcards = deck
                        save_user_flashcards(deck)
                        st.success(f"Đã lưu đánh giá {score}! Thẻ này sẽ được lặp lại vào ngày {updated_card.next_review} (sau {updated_card.interval_days} ngày).")
                        st.rerun()

            st.markdown("---")
            with st.expander("⚙️ Quản lý thẻ này (Xóa thẻ)"):
                if st.button("🗑️ Xóa thẻ này khỏi kho cá nhân", type="secondary"):
                    deck.pop(real_card_idx)
                    st.session_state.flashcards = deck
                    save_user_flashcards(deck)
                    st.success("Đã xóa thẻ thành công!")
                    st.rerun()


# =============================================================================
# PHÂN HỆ 5: TRA CỨU TỪ ĐIỂN GIÁO TRÌNH (1,200 TỪ)
# =============================================================================
elif app_mode == "📖 5. Tra Cứu Từ Điển Giáo Trình (1,200 từ)":
    st.markdown('<p class="main-header">📖 KHO TỪ ĐIỂN GIÁO TRÌNH TIẾNG LÀO (1,200 MỤC TỪ)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Hỗ trợ tra cứu song ngữ Lào - Việt - Anh, từ loại, phiên âm chuẩn ngữ âm và câu ví dụ minh họa ngữ cảnh bài học.</p>', unsafe_allow_html=True)

    dict_obj = translator.dictionary
    all_words = dict_obj.get_all_words()
    
    col_search, col_filter = st.columns([2, 1], gap="medium")
    with col_search:
        search_kw = st.text_input(
            "🔍 Tìm kiếm từ vựng (Nhập Tiếng Lào, Tiếng Việt, Tiếng Anh hoặc Phiên âm Latinh):",
            placeholder="Ví dụ: ສະບາຍດີ, sabaaidee, Cảm ơn, Ăn, Du lịch..."
        )
    with col_filter:
        lessons = sorted(list(set([dict_obj.entries[w].get("lesson", "") for w in all_words if w in dict_obj.entries])))
        selected_lesson = st.selectbox("Lọc theo chủ đề bài học:", ["Tất cả chủ đề"] + lessons)

    results = []
    sk = search_kw.strip().lower() if search_kw else ""

    for w in all_words:
        entry = dict_obj.entries.get(w, {})
        if not entry:
            continue
        if selected_lesson != "Tất cả chủ đề" and entry.get("lesson") != selected_lesson:
            continue
        if sk:
            lao_val = entry.get("lao", "").lower()
            vi_val = entry.get("vi", "").lower()
            en_val = entry.get("en", "").lower()
            rom_val = entry.get("romanization", "").lower()
            if sk not in lao_val and sk not in vi_val and sk not in en_val and sk not in rom_val:
                continue
        results.append({
            "Từ tiếng Lào": entry.get("lao", ""),
            "Phiên âm": entry.get("romanization", ""),
            "Từ loại": entry.get("pos", ""),
            "Nghĩa Tiếng Việt": entry.get("vi", ""),
            "Nghĩa Tiếng Anh": entry.get("en", ""),
            "Chủ đề": entry.get("lesson", ""),
            "Ví dụ tiếng Lào": entry.get("example_lao", "-"),
            "Dịch nghĩa ví dụ": entry.get("example_vi", "-")
        })

    st.markdown(f"**Kết quả tra cứu:** Tìm thấy **{len(results)}** / {len(all_words)} mục từ phù hợp.")
    st.dataframe(pd.DataFrame(results), use_container_width=True, height=520)


# =============================================================================
# PHÂN HỆ 6: BẢNG ĐIỀU KHIỂN NGHIÊN CỨU (DASHBOARD)
# =============================================================================
elif app_mode == "📊 6. Bảng Điều Khiển Nghiên Cứu (Dashboard)":
    st.markdown('<p class="main-header">📊 BẢNG ĐIỀU KHIỂN KẾT QUẢ NGHIÊN CỨU KHOA HỌC</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tổng hợp đầy đủ toàn bộ 21 bảng số liệu và 12 biểu đồ chẩn đoán khoa học của đề tài qua các giai đoạn (P0 đến P8).</p>', unsafe_allow_html=True)

    res_dir = os.path.join(PROJECT_ROOT, "experiments", "results")
    
    st.markdown("### 🏆 3 ĐÓNG GÓP KHOA HỌC & KỸ THUẬT CỐT LÕI CỦA ĐỀ TÀI")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**Đóng góp #1 (P5 Ablation)**\nKhóa cấu hình tiền xử lý ảnh tối ưu YAML & Kiểm chứng Lao Golden Rule #3.")
    with c2:
        st.success("**Đóng góp #2 (P6 Hậu xử lý)**\nWeighted Levenshtein tích hợp ma trận nhầm lẫn thực nghiệm: Tăng Word Acc từ 3.82% lên 29.30% ($p < 0.05$).")
    with c3:
        st.warning("**Đóng góp #3 (P7+P8 SOTA)**\nHiệp đồng LaoCRNN + Lexicon Snap: Đưa Word Acc nhảy vọt lên **85.35%** (Top-3 **91.72%**) với độ trễ siêu tốc **51.5 ms** CPU.")

    st.markdown("---")

    dash_tabs = st.tabs([
        "Phase P4: Baseline & Lỗi",
        "Phase P5: Nghiên Cứu Ablation (8 Bảng)",
        "Phase P6: Hậu Xử Lý Từ Điển (#2)",
        "Phase P7: Huấn Luyện Mô Hình (#3)",
        "Phase P8: Tầng Ngôn Ngữ & Dịch",
        "🖼️ Thư Viện Biểu Đồ Khoa Học (12 PNG)"
    ])

    # Tab 1: P4
    with dash_tabs[0]:
        st.subheader("Bảng 1: Quét chế độ phân đoạn trang PSM (Page Segmentation Modes)")
        f1 = os.path.join(res_dir, "p4_psm_scan_results.csv")
        if os.path.exists(f1):
            st.dataframe(pd.read_csv(f1), use_container_width=True)

        st.subheader("Bảng 2: So sánh đa động cơ Baseline (Tesseract vs EasyOCR vs PaddleOCR vs Cloud)")
        f2 = os.path.join(res_dir, "p4_engine_comparison.csv")
        if os.path.exists(f2):
            st.dataframe(pd.read_csv(f2), use_container_width=True)

        col_p4_a, col_p4_b = st.columns(2)
        with col_p4_a:
            st.subheader("Phân loại 5 nhóm lỗi (Error Taxonomy)")
            f_tax = os.path.join(res_dir, "p4_error_taxonomy.csv")
            if os.path.exists(f_tax):
                st.dataframe(pd.read_csv(f_tax), use_container_width=True)
        with col_p4_b:
            st.subheader("Cặp ký tự nhầm lẫn thực nghiệm (Confusion Pairs)")
            f_conf = os.path.join(res_dir, "confusion_pairs.csv")
            if os.path.exists(f_conf):
                st.dataframe(pd.read_csv(f_conf).head(20), use_container_width=True)

    # Tab 2: P5
    with dash_tabs[1]:
        p5_sel = st.selectbox("Chọn bảng số liệu Ablation Study muốn xem:", [
            "Bảng 3: So sánh 6 phương pháp nhị phân hóa",
            "Bảng 4: Phân tích đóng góp Leave-one-out từng bước A1–A9",
            "Bảng 5: Lựa chọn tham lam tiến dần (Forward Selection)",
            "Bảng 6: Kiểm chứng quy tắc kernel hình thái học (Golden Rule #3)",
            "Bảng 7: Ảnh hưởng của chiều cao dòng ký tự (Line Height)",
            "Bảng 8: Phân tích CER phân tầng (Ánh sáng x Thiết bị x Font x Góc)",
            "Bảng 9: Độ bền pipeline với mức nhiễu & mờ tăng dần",
            "Bảng 10: Đối chiếu chữ in vs Chữ viết tay"
        ])
        p5_map = {
            "Bảng 3": "p5_table3_binarization.csv",
            "Bảng 4": "p5_table4_leave_one_out.csv",
            "Bảng 5": "p5_table5_forward_selection.csv",
            "Bảng 6": "p5_table6_morphology_kernel.csv",
            "Bảng 7": "p5_table7_line_height.csv",
            "Bảng 8": "p5_table8_stratified.csv",
            "Bảng 9": "p5_table9_noise_robustness.csv",
            "Bảng 10": "p5_table10_printed_vs_handwritten.csv"
        }
        key_code = p5_sel.split(":")[0].strip()
        f_p5 = os.path.join(res_dir, p5_map[key_code])
        if os.path.exists(f_p5):
            st.dataframe(pd.read_csv(f_p5), use_container_width=True)

    # Tab 3: P6
    with dash_tabs[2]:
        st.subheader("Bảng Tổng hợp Luồng Tích lũy (Cumulative Pipeline Progression)")
        f_cum = os.path.join(res_dir, "p6_cumulative_pipeline_summary.csv")
        if os.path.exists(f_cum):
            st.dataframe(pd.read_csv(f_cum), use_container_width=True)

        st.subheader("Bảng 12: So sánh Levenshtein thường vs Levenshtein có trọng số (Weighted)")
        f12 = os.path.join(res_dir, "p6_table12_standard_vs_weighted_levenshtein.csv")
        if os.path.exists(f12):
            st.dataframe(pd.read_csv(f12), use_container_width=True)

        col_p6_1, col_p6_2 = st.columns(2)
        with col_p6_1:
            st.subheader("Bảng 11: Top-k Accuracy")
            f11 = os.path.join(res_dir, "p6_table11_accuracy_and_topk.csv")
            if os.path.exists(f11):
                st.dataframe(pd.read_csv(f11), use_container_width=True)
        with col_p6_2:
            st.subheader("Bảng 14: n-gram Jaccard vs Weighted Levenshtein")
            f14 = os.path.join(res_dir, "p6_table14_ngram_vs_levenshtein.csv")
            if os.path.exists(f14):
                st.dataframe(pd.read_csv(f14), use_container_width=True)

    # Tab 4: P7
    with dash_tabs[3]:
        st.subheader("Bảng 15: Điểm chuẩn Đa Kiến Trúc Toàn Diện (Multi-Model Benchmark)")
        f15 = os.path.join(res_dir, "p7_table15_multi_model_benchmark.csv")
        if os.path.exists(f15):
            st.dataframe(pd.read_csv(f15), use_container_width=True)

        st.subheader("Bảng 18: Hiệp đồng Mô hình Học Sâu LaoCRNN & Lexicon Snap (Đạt 85.35% Word Acc)")
        f18 = os.path.join(res_dir, "p7_table18_lexicon_snap_integration.csv")
        if os.path.exists(f18):
            st.dataframe(pd.read_csv(f18), use_container_width=True)

        col_p7_1, col_p7_2 = st.columns(2)
        with col_p7_1:
            st.subheader("Bảng 16: Đường cong học tập theo quy mô dữ liệu")
            f16 = os.path.join(res_dir, "p7_table16_learning_curves_data_scale.csv")
            if os.path.exists(f16):
                st.dataframe(pd.read_csv(f16), use_container_width=True)
        with col_p7_2:
            st.subheader("Bảng 17: Cống hiến của Data Augmentation quang học")
            f17 = os.path.join(res_dir, "p7_table17_augmentation_impact.csv")
            if os.path.exists(f17):
                st.dataframe(pd.read_csv(f17), use_container_width=True)

    # Tab 5: P8
    with dash_tabs[4]:
        st.subheader("Bảng 19: Phân đoạn từ tiếng Lào (Word Tokenization F1)")
        f19 = os.path.join(res_dir, "p8_table19_word_segmentation_comparison.csv")
        if os.path.exists(f19):
            st.dataframe(pd.read_csv(f19), use_container_width=True)

        st.subheader("Bảng 20: Đánh giá chất lượng dịch thuật (BLEU & chrF++)")
        f20 = os.path.join(res_dir, "p8_table20_translation_quality.csv")
        if os.path.exists(f20):
            st.dataframe(pd.read_csv(f20), use_container_width=True)

        st.subheader("Bảng 21: Phân rã độ trễ toàn luồng End-to-End Pipeline (51.5 ms CPU)")
        f21 = os.path.join(res_dir, "p8_table21_latency_breakdown.csv")
        if os.path.exists(f21):
            st.dataframe(pd.read_csv(f21), use_container_width=True)

    # Tab 6: PNG Plots Gallery
    with dash_tabs[5]:
        st.subheader("🖼️ Thư viện 12 Biểu đồ & Ảnh Trực quan hóa Khoa học")
        png_files = [f for f in os.listdir(res_dir) if f.endswith(".png")]
        
        plot_descriptions = {
            "p7_model_comparison_radar_or_bars.png": "So sánh đa chiều hiệu năng các kiến trúc nhận dạng OCR.",
            "p7_learning_curves_and_scale.png": "Đường cong học tập và khả năng khái quát hóa theo số lượng dữ liệu tổng hợp.",
            "p6_topk_and_methods_comparison.png": "Độ chính xác Top-k giữa Levenshtein chuẩn, Levenshtein có trọng số và n-gram.",
            "p6_precision_coverage_curve.png": "Đường cong đánh đổi Precision - Coverage theo ngưỡng tin cậy hậu xử lý.",
            "p8_translation_and_segmentation.png": "Độ trễ toàn luồng và chất lượng phân đoạn từ, dịch thuật song ngữ.",
            "ablation_table3_binarization.png": "So sánh 6 phương pháp nhị phân hóa ảnh.",
            "ablation_table4_leave_one_out.png": "Đóng góp Leave-one-out của từng bộ lọc DIP A1–A9.",
            "ablation_table6_morphology_kernel.png": "Kiểm chứng tác hại phá hủy dấu thanh khi kernel hình thái học >= 3x3.",
            "ablation_table8_stratified.png": "Hiệu năng CER phân tầng theo điều kiện chiếu sáng, góc chụp và font chữ.",
            "ablation_table9_noise_robustness.png": "Độ bền pipeline tiền xử lý khi mức nhiễu và độ mờ tăng dần.",
            "lao_4tiers_projection_profile.png": "Biểu đồ mật độ 4 tầng độ cao ký tự tiếng Lào theo trục Y.",
            "preprocessing_stages_inspection.png": "Trực quan hóa 12 bước trung gian của quy trình xử lý ảnh số."
        }

        cols_grid = st.columns(2)
        for i, pf in enumerate(png_files):
            col_target = cols_grid[i % 2]
            with col_target:
                p_path = os.path.join(res_dir, pf)
                desc = plot_descriptions.get(pf, pf)
                st.image(p_path, caption=f"{pf} — {desc}", use_container_width=True)
