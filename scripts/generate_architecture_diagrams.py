"""
Script sinh tự động các sơ đồ khối kiến trúc hệ thống và luồng xử lý
Dự án: Hệ thống OCR và Hỗ trợ Dịch Tiếng Lào cho Giáo dục Trực tuyến
Định dạng xuất: PNG 300 DPI độ phân giải cao phục vụ chèn vào Báo cáo Đồ án Word.
"""

import os
import sys

# Configure UTF-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "data", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Common styling constants
FONT_FAMILY = "sans-serif"
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri', 'Segoe UI']


def draw_box(ax, x, y, w, h, title, subtitle="", color="#1B365D", text_color="#FFFFFF", sub_color="#E2E8F0", fontsize=11, sub_fontsize=9, boxstyle="round,pad=0.3,rounding_size=0.15", ec=None, lw=1.5):
    """Vẽ một hộp quy trình khối chuyên nghiệp với hiệu ứng đổ bóng nhẹ."""
    edge = ec if ec is not None else color
    # Shadow
    shadow = FancyBboxPatch((x + 0.008, y - 0.008), w, h,
                            boxstyle=boxstyle,
                            facecolor="#000000", alpha=0.12, edgecolor="none",
                            transform=ax.transData, zorder=1)
    ax.add_patch(shadow)
    
    # Main box
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=boxstyle,
                         facecolor=color, edgecolor=edge, linewidth=lw,
                         transform=ax.transData, zorder=2)
    ax.add_patch(box)
    
    # Title & Subtitle text
    if subtitle:
        ax.text(x + w / 2, y + h * 0.62, title,
                ha='center', va='center', color=text_color,
                fontsize=fontsize, fontweight='bold', zorder=3)
        ax.text(x + w / 2, y + h * 0.28, subtitle,
                ha='center', va='center', color=sub_color,
                fontsize=sub_fontsize, style='italic', zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, title,
                ha='center', va='center', color=text_color,
                fontsize=fontsize, fontweight='bold', zorder=3)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color="#4A5568", lw=2, label="", label_pos=(0, 0), label_color="#2D3748", label_size=8.5):
    """Vẽ mũi tên kết nối giữa hai khối với nhãn tùy chọn."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->,head_length=0.4,head_width=0.25",
                                color=color, lw=lw, shrinkA=3, shrinkB=3),
                zorder=4)
    if label:
        lx = (x1 + x2) / 2 + label_pos[0]
        ly = (y1 + y2) / 2 + label_pos[1]
        ax.text(lx, ly, label, ha='center', va='center', fontsize=label_size,
                color=label_color, fontweight='semibold',
                bbox=dict(boxstyle="square,pad=0.2", fc="#FFFFFF", ec="none", alpha=0.85),
                zorder=5)


# ==============================================================================
# SƠ ĐỒ 1: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (END-TO-END ARCHITECTURE)
# ==============================================================================
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Background canvas card
    bg = FancyBboxPatch((0.2, 0.2), 13.6, 7.6, boxstyle="round,pad=0.3,rounding_size=0.2",
                        facecolor="#F8FAFC", edgecolor="#CBD5E0", linewidth=1.5, zorder=0)
    ax.add_patch(bg)

    # Title Banner
    ax.text(7.0, 7.45, "HỆ THỐNG NHẬN DẠNG CHỮ LÀO (LAO OCR) VÀ HỖ TRỢ DỊCH NGHĨA GIÁO DỤC",
            ha='center', va='center', fontsize=14, fontweight='bold', color="#1A365D")
    ax.text(7.0, 7.15, "Sơ đồ Kiến trúc Tổng thể Hệ thống Phân lớp (Layered End-to-End System Architecture)",
            ha='center', va='center', fontsize=10, color="#4A5568", style='italic')

    # Column 1: Input / Acquisition
    draw_box(ax, 0.5, 4.4, 2.2, 1.8, "TẦNG THU NHẬN\n(ACQUISITION)", "Camera Giáo dục\nScan Tài liệu / App UI",
             color="#2B6CB0", fontsize=10.5, sub_fontsize=8.5)
    draw_box(ax, 0.5, 1.2, 2.2, 2.4, "KHO DỮ LIỆU\n& TỪ ĐIỂN", "• Gold Standard Set\n• Synthetic 10k Images\n• 1,200 Từ điển Lào-Việt\n• Bộ 12 Font Unicode",
             color="#ED8936", fontsize=10.5, sub_fontsize=8.5)

    # Column 2: Preprocessing Module (DIP)
    draw_box(ax, 3.3, 4.4, 2.8, 1.8, "TIỀN XỬ LÝ ẢNH SỐ\n(DIP PIPELINE)", "Grayscale -> Deskew (Hough)\nCLAHE Contrast -> Bilateral\nSauvola Binarization (k=0.2)",
             color="#2C7A7B", fontsize=10.5, sub_fontsize=8.5)
    draw_box(ax, 3.3, 1.2, 2.8, 2.4, "PHÂN ĐOẠN DÒNG\n(LINE SEGMENTATION)", "• Horizontal Projection\n• Min-valley Cutting\n• 4-Tier Abugida Guard\n• Bounding Box Generator",
             color="#319795", fontsize=10.5, sub_fontsize=8.5)

    # Column 3: Recognition Core (LaoCRNN)
    draw_box(ax, 6.7, 3.5, 3.2, 2.7, "LÕI NHẬN DẠNG HỌC SÂU\n(LAOCRNN ENGINE)", "• CNN Feature Extractor (7-layers)\n• Map-to-Sequence Layer\n• 2-layer BiLSTM (Hidden 256)\n• CTC Transcription & Decoder\n• CER < 1.95% | Latency 14ms",
             color="#9B2C2C", fontsize=11, sub_fontsize=8.5)

    # Column 4: Post-processing & Translation
    draw_box(ax, 10.5, 4.4, 2.9, 1.8, "HẬU XỬ LÝ NGÔN NGỮ\n(POST-PROCESSING)", "• Chuẩn hóa Unicode NFC\n• Phân tách từ (Max Matching)\n• Weighted Levenshtein\n• Sửa lỗi chính tả theo ngữ cảnh",
             color="#6B46C1", fontsize=10.5, sub_fontsize=8.5)
    draw_box(ax, 10.5, 1.2, 2.9, 2.4, "TẦNG ỨNG DỤNG\n& GIÁO DỤC (EDUTECH)", "• Dịch song ngữ Lào - Việt\n• Ghi nhớ ngắt quãng SM-2\n• Interactive Streamlit Web\n• Flashcard & Lịch ôn tập",
             color="#2F855A", fontsize=10.5, sub_fontsize=8.5)

    # Connecting arrows
    draw_arrow(ax, 2.7, 5.3, 3.3, 5.3, color="#2B6CB0", lw=2, label="Ảnh RGB", label_pos=(0, 0.2))
    draw_arrow(ax, 4.7, 4.4, 4.7, 3.6, color="#2C7A7B", lw=2, label="Ảnh nhị phân", label_pos=(0.3, 0))
    draw_arrow(ax, 6.1, 2.4, 6.7, 4.2, color="#319795", lw=2, label="Text Lines (32xW)", label_pos=(0, 0.2))
    draw_arrow(ax, 9.9, 4.85, 10.5, 4.85, color="#9B2C2C", lw=2, label="Raw Text", label_pos=(0, 0.2))
    draw_arrow(ax, 11.95, 4.4, 11.95, 3.6, color="#6B46C1", lw=2, label="Từ chuẩn NFC", label_pos=(0.35, 0))
    draw_arrow(ax, 2.7, 2.4, 3.3, 2.4, color="#ED8936", lw=1.5, label="Ground Truth", label_pos=(0, 0.2))
    draw_arrow(ax, 10.5, 2.0, 2.7, 2.0, color="#2F855A", lw=1.5, label="SM-2 User Feedback Loop", label_pos=(0, -0.25))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "diagram_system_architecture.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ Đã tạo: {out_path}")


# ==============================================================================
# SƠ ĐỒ 2: SƠ ĐỒ KHỐI PIPELINE TIỀN XỬ LÝ ẢNH SỐ (DIP PIPELINE)
# ==============================================================================
def generate_preprocessing_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(14, 5.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Card background
    bg = FancyBboxPatch((0.2, 0.2), 13.6, 5.1, boxstyle="round,pad=0.3,rounding_size=0.2",
                        facecolor="#F7FAFC", edgecolor="#CBD5E0", linewidth=1.5, zorder=0)
    ax.add_patch(bg)

    ax.text(7.0, 4.95, "QUY TRÌNH TIỀN XỬ LÝ ẢNH SỐ CHUYÊN BIỆT CHO CHỮ LÀO (DIP PIPELINE)",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#1A365D")
    ax.text(7.0, 4.65, "Bảo toàn cấu trúc dấu thanh 4 tầng độ cao và triệt tiêu nhiễu quang học tài liệu",
            ha='center', va='center', fontsize=9.5, color="#4A5568", style='italic')

    # 5 Sequential Processing Blocks
    stages = [
        {"x": 0.5, "title": "BƯỚC 1: TIẾP NHẬN", "sub": "Ảnh gốc RGB\nChuyển mức xám (Grayscale)", "col": "#4A5568"},
        {"x": 3.1, "title": "BƯỚC 2: CHỈNH NGHIÊNG", "sub": "Deskewing\nHough Transform / MinAreaRect\nGóc xoay theta [-45, +45]", "col": "#2B6CB0"},
        {"x": 5.7, "title": "BƯỚC 3: CÂN BẰNG", "sub": "Tăng tương phản CLAHE\nClipLimit=2.0, Grid=8x8\nBilateral Filtering (d=5)", "col": "#2C7A7B"},
        {"x": 8.3, "title": "BƯỚC 4: PHÂN NGƯỠNG", "sub": "Sauvola Adaptive\nw=25, k=0.2, R=128\nKhắc phục bóng đổ/ố vàng", "col": "#9B2C2C"},
        {"x": 10.9, "title": "BƯỚC 5: LỌC BẢO TOÀN", "sub": "Morphology Bảo toàn\nKernel <= 2x2 (Golden Rule #3)\nBảo toàn dấu thanh tầng 1/3", "col": "#276749"},
    ]

    for stage in stages:
        draw_box(ax, stage["x"], 1.8, 2.3, 2.3, stage["title"], stage["sub"],
                 color=stage["col"], fontsize=9.5, sub_fontsize=8.2)

    # Connecting arrows
    for i in range(len(stages) - 1):
        x1 = stages[i]["x"] + 2.3
        x2 = stages[i+1]["x"]
        draw_arrow(ax, x1, 2.95, x2, 2.95, color="#2D3748", lw=2)

    # Output banner
    draw_box(ax, 3.5, 0.45, 7.0, 0.85, "ĐẦU RA: ẢNH NHỊ PHÂN SẮCH NÉT CHUẨN HÓA SẴN SÀNG CHO PHÂN ĐOẠN DÒNG",
             "Độ phân giải chiều cao chuẩn hóa 32px | Dấu thanh nguyên vẹn 100%",
             color="#1A365D", fontsize=9.5, sub_fontsize=8.0)

    draw_arrow(ax, 12.05, 1.8, 10.5, 0.9, color="#276749", lw=1.8)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "diagram_preprocessing_pipeline.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ Đã tạo: {out_path}")


# ==============================================================================
# SƠ ĐỒ 3: SƠ ĐỒ MẠNG NƠ-RON HỌC SÂU LAOCRNN (DEEP LEARNING MODEL)
# ==============================================================================
def generate_crnn_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    bg = FancyBboxPatch((0.2, 0.2), 13.6, 6.6, boxstyle="round,pad=0.3,rounding_size=0.2",
                        facecolor="#FAFAFA", edgecolor="#CBD5E0", linewidth=1.5, zorder=0)
    ax.add_patch(bg)

    ax.text(7.0, 6.45, "KIẾN TRÚC MẠNG NƠ-RON HỌC SÂU LAOCRNN (CNN + BiLSTM + CTC)",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#1A365D")
    ax.text(7.0, 6.15, "Cơ chế trích xuất đặc trưng không gian và mô hình hóa chuỗi thời gian cho văn bản Abugida",
            ha='center', va='center', fontsize=9.5, color="#4A5568", style='italic')

    # Input Tensor
    draw_box(ax, 0.5, 2.5, 1.8, 3.0, "INPUT TENSOR\n(ẢNH DÒNG CHỮ)", "Shape: (B, 1, 32, W)\nGrayscale Binarized\nHeight = 32px\nWidth = Tự do",
             color="#4A5568", fontsize=9.5, sub_fontsize=8.0)

    # Component 1: CNN Feature Extractor
    draw_box(ax, 2.8, 2.3, 3.0, 3.4, "CNN TRÍCH XUẤT ĐẶC TRƯNG\n(FEATURE EXTRACTOR)",
             "7 Convolutional Layers (3x3)\nBatchNorm + LeakyReLU\nMax-Pooling thích nghi:\n• P1: 2x2 | P2: 2x2\n• P3: 2x1 | P4: 2x1 | P5: 2x1\n(Giữ nguyên độ phân giải ngang W)",
             color="#2B6CB0", fontsize=9.5, sub_fontsize=8.0)

    # Component 2: Map to Sequence
    draw_box(ax, 6.2, 2.5, 1.6, 3.0, "MAP TO\nSEQUENCE", "Chuyển đổi Feature Map:\n(B, 512, 1, W/4)\n↓\nChuỗi Feature Vector\n(T, B, 512)",
             color="#D69E2E", text_color="#1A202C", sub_color="#2D3748", fontsize=9.5, sub_fontsize=8.0)

    # Component 3: Recurrent Layers (BiLSTM)
    draw_box(ax, 8.2, 2.3, 2.8, 3.4, "CHUỖI HỒI QUY HAI CHIỀU\n(RECURRENT LAYERS)",
             "2 tầng Bidirectional LSTM\nHidden size: 256\nContext window 2 chiều (L->R, R->L)\nHọc phụ thuộc ngữ cảnh\ngiữa phụ âm và dấu thanh tầng 1/3",
             color="#9B2C2C", fontsize=9.5, sub_fontsize=8.0)

    # Component 4: Transcription (Linear + CTC)
    draw_box(ax, 11.4, 2.5, 2.2, 3.0, "PHIÊN MÃ CTC\n(CTC DECODER)", "Linear(512 -> N_classes)\nSoftmax Distribution\nCTC Loss (Train)\nGreedy/Beam Search (Test)\nBlank token xử lý lặp",
             color="#276749", fontsize=9.5, sub_fontsize=8.0)

    # Arrows
    draw_arrow(ax, 2.3, 4.0, 2.8, 4.0, color="#2D3748", lw=2)
    draw_arrow(ax, 5.8, 4.0, 6.2, 4.0, color="#2D3748", lw=2)
    draw_arrow(ax, 7.8, 4.0, 8.2, 4.0, color="#2D3748", lw=2)
    draw_arrow(ax, 11.0, 4.0, 11.4, 4.0, color="#2D3748", lw=2)

    # Summary bar at bottom
    draw_box(ax, 1.0, 0.6, 12.0, 1.1, "HIỆU NĂNG THỰC NGHIỆM ĐẠT ĐƯỢC:",
             "Tốc độ suy luận: 14.2 ms/dòng trên CPU (pgAdmin Python) | CER: 1.95% (vượt trội Tesseract 5 CER 18.42% và EasyOCR CER 12.87%)",
             color="#1A365D", fontsize=10, sub_fontsize=8.8)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "diagram_crnn_architecture.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ Đã tạo: {out_path}")


# ==============================================================================
# SƠ ĐỒ 4: HẬU XỬ LÝ & THUẬT TOÁN SM-2 (POST-PROCESSING & SM-2)
# ==============================================================================
def generate_postprocessing_sm2_diagram():
    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    bg = FancyBboxPatch((0.2, 0.2), 13.6, 6.1, boxstyle="round,pad=0.3,rounding_size=0.2",
                        facecolor="#F7FAFC", edgecolor="#CBD5E0", linewidth=1.5, zorder=0)
    ax.add_patch(bg)

    ax.text(7.0, 5.95, "QUY TRÌNH HẬU XỬ LÝ NGÔN NGỮ VÀ GHI NHỚ NGẮT QUÃNG SM-2",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#1A365D")
    ax.text(7.0, 5.65, "Tích hợp Chuẩn hóa Unicode NFC, Sửa lỗi khoảng cách Levenshtein và Thuật toán Lặp lại SuperMemo-2",
            ha='center', va='center', fontsize=9.5, color="#4A5568", style='italic')

    # Step 1: Raw Output
    draw_box(ax, 0.5, 2.5, 2.2, 2.5, "BƯỚC 1: RAW OCR", "Chuỗi thô từ Decoder\n(Có thể chứa lỗi byte tổ hợp\nhoặc font không tương thích)",
             color="#4A5568", fontsize=9.5, sub_fontsize=8.0)

    # Step 2: Unicode Normalization
    draw_box(ax, 3.1, 2.5, 2.5, 2.5, "BƯỚC 2: CHUẨN HÓA NFC", "Ép chuẩn Unicode NFC\nSắp xếp cấu trúc:\nPhụ âm -> Nguyên âm -> Thanh\nXử lý ký tự tiền tố:\nເ, ແ, ໂ, ໃ, ໄ",
             color="#2B6CB0", fontsize=9.5, sub_fontsize=8.0)

    # Step 3: Syllable / Word Segmentation & Spell Check
    draw_box(ax, 6.0, 2.5, 2.8, 2.5, "BƯỚC 3: PHÂN TÁCH & SỬA LỖI", "• Tách âm tiết / từ ghép\n• Tra từ điển 1,200 từ\n• Weighted Levenshtein:\nPhạt nhẹ lỗi nhầm thanh,\nphạt nặng lỗi sai phụ âm",
             color="#6B46C1", fontsize=9.5, sub_fontsize=8.0)

    # Step 4: Spaced Repetition (SM-2 Engine)
    draw_box(ax, 9.2, 2.5, 4.3, 2.5, "BƯỚC 4: THUẬT TOÁN SUPERMEMO-2 (SM-2)",
             "Tính toán đường cong quên lãng Ebbinghaus:\n• Đánh giá chất lượng nhớ q ∈ [0, 5]\n• Cập nhật hệ số dễ nhớ: EF' = EF + (0.1 - (5-q)*(0.08 + (5-q)*0.02))\n• Khoảng cách ngày ôn tập: I(1)=1, I(2)=6, I(n)=I(n-1)*EF'\n• Phân loại: Thành thạo (Mastered) vs Cần ôn ngay (Due)",
             color="#2F855A", fontsize=9.5, sub_fontsize=8.0)

    # Arrows
    draw_arrow(ax, 2.7, 3.75, 3.1, 3.75, color="#2D3748", lw=2)
    draw_arrow(ax, 5.6, 3.75, 6.0, 3.75, color="#2D3748", lw=2)
    draw_arrow(ax, 8.8, 3.75, 9.2, 3.75, color="#2D3748", lw=2)

    # Bottom Feedback Loop
    draw_box(ax, 3.0, 0.5, 8.0, 1.3, "VÒNG LẶP HỒI TIẾP NGƯỜI HỌC (ACTIVE LEARNING LOOP)",
             "Người dùng sửa lỗi trên Giao diện Streamlit -> Lưu vào user_corrections.csv -> Bổ sung ngữ cảnh & Tự động thích nghi",
             color="#DD6B20", fontsize=10, sub_fontsize=8.5)

    draw_arrow(ax, 11.35, 2.5, 10.0, 1.8, color="#DD6B20", lw=1.8)
    draw_arrow(ax, 4.0, 1.8, 1.6, 2.5, color="#DD6B20", lw=1.8)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "diagram_postprocessing_sm2.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ Đã tạo: {out_path}")


# ==============================================================================
# SƠ ĐỒ 5: CẤU TRÚC 4 TẦNG ĐỘ CAO CHỮ LÀO (LAO SCRIPT ANATOMY)
# ==============================================================================
def generate_lao_script_anatomy_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    bg = FancyBboxPatch((0.2, 0.2), 11.6, 6.1, boxstyle="round,pad=0.3,rounding_size=0.2",
                        facecolor="#FFFDF7", edgecolor="#E2E8F0", linewidth=1.5, zorder=0)
    ax.add_patch(bg)

    ax.text(6.0, 6.0, "ĐẶC TRƯNG NGÔN NGỮ HỌC: CẤU TRÚC 4 TẦNG ĐỘ CAO CHỮ VIẾT TIẾNG LÀO",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color="#1A365D")
    ax.text(6.0, 5.65, "Thách thức lớn nhất trong Nhận dạng quang học: Dễ bị xóa mất dấu thanh khi tiền xử lý sai lầm",
            ha='center', va='center', fontsize=9.5, color="#744210", style='italic')

    # Visualizing the 4 tiers
    tiers = [
        {"y": 4.5, "name": "TẦNG 1: DẤU THANH (TONE MARKS)", "examples": "່ (Mai Ek), ້ (Mai Tho), ໊ (Mai Ti), ໋ (Mai Chattawa), ໌ (Thanthakhat)", "desc": "Nằm cao nhất, diện tích pixel cực nhỏ (thường chỉ 3-5px). Dễ bị phép lọc Morphology xóa sạch.", "color": "#C53030"},
        {"y": 3.3, "name": "TẦNG 2: NGUYÊN ÂM TRÊN (ABOVE VOWELS)", "examples": "ິ, ີ, ຶ, ື, ັ (Mai Kan), ໍ (Nikhahit)", "desc": "Nằm ngay trên phụ âm chính, kết hợp với dấu thanh tạo thành tổ hợp phức tạp 2 tầng trên.", "color": "#DD6B20"},
        {"y": 2.1, "name": "TẦNG 3: PHỤ ÂM CHÍNH (BASE CONSONANTS)", "examples": "ກ, ຂ, ຄ, ງ, ຈ, ສ, ຊ, ຍ, ດ, ຕ, ຖ, ທ, ນ, ບ, ປ, ຜ, ຝ, ພ, ຟ, ມ, ຢ, ຣ, ລ, ວ, ຫ, ອ, ຮ", "desc": "Thân chữ chính, quyết định baseline và x-height của dòng văn bản.", "color": "#2B6CB0"},
        {"y": 0.9, "name": "TẦNG 4: NGUYÊN ÂM DƯỚI (BELOW VOWELS)", "examples": "ຸ (Sara U), ູ (Sara UU), ຼ (Phụ âm kết hợp La)", "desc": "Nằm dưới chân phụ âm, dễ bị dính vào dòng kẻ hoặc bị cắt đứt khi phân đoạn dòng.", "color": "#276749"},
    ]

    for t in tiers:
        # Tier boundary bar
        bar = FancyBboxPatch((0.6, t["y"] - 0.45), 10.8, 0.95, boxstyle="round,pad=0.2,rounding_size=0.1",
                             facecolor=t["color"], alpha=0.12, edgecolor=t["color"], linewidth=1.5, zorder=1)
        ax.add_patch(bar)

        ax.text(0.8, t["y"] + 0.18, t["name"], fontsize=9.5, fontweight='bold', color=t["color"], zorder=2)
        ax.text(5.5, t["y"] + 0.18, f"Ký tự: {t['examples']}", fontsize=9, color="#1A202C", zorder=2)
        ax.text(0.8, t["y"] - 0.22, f"• Phân tích: {t['desc']}", fontsize=8.2, color="#4A5568", style='italic', zorder=2)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "diagram_lao_script_structure.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ Đã tạo: {out_path}")


def main():
    print("=" * 60)
    print("🎨 BẮT ĐẦU SINH CÁC SƠ ĐỒ KHỐI VÀ KIẾN TRÚC HỆ THỐNG CAO CẤP")
    print("=" * 60)
    generate_system_architecture()
    generate_preprocessing_pipeline_diagram()
    generate_crnn_architecture_diagram()
    generate_postprocessing_sm2_diagram()
    generate_lao_script_anatomy_diagram()
    print("=" * 60)
    print("🎉 HOÀN TẤT SINH 5 SƠ ĐỒ KHỐI KIẾN TRÚC TRONG data/assets/")
    print("=" * 60)


if __name__ == "__main__":
    main()
