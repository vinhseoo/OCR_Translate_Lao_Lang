"""
Module Nhận Dạng Đoạn Văn Bản & Tài Liệu Tiếng Lào (Paragraph & Document OCR Engine).
Kết hợp Xử lý ảnh số (DIP Line Segmentation: HPP / RLSA) với Động cơ OCR
(LaoCRNN Line-by-line hoặc Tesseract Multi-line Block).
"""
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import cv2
from PIL import Image

from src.preprocessing.normalize import normalize_lao
from src.preprocessing.segmentation import (
    segment_lines_horizontal_projection,
    segment_lines_rlsa,
)


@dataclass
class LineResult:
    line_index: int
    box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    text: str
    confidence: float = 1.0


@dataclass
class DocumentOCRResult:
    full_text: str
    lines: List[LineResult]
    annotated_image: np.ndarray
    num_lines: int
    elapsed_ms: float
    engine_name: str


def detect_and_crop_lines(
    image_np: np.ndarray,
    method: str = "hpp",
    min_line_height: int = 15,
    padding_y: int = 4
) -> Tuple[List[np.ndarray], List[Tuple[int, int, int, int]], np.ndarray]:
    """
    Phát hiện và cắt các dòng văn bản từ ảnh tài liệu nhiều dòng.
    Đặc thù tiếng Lào: Thêm padding_y để bảo toàn dấu thanh tầng 1 và nguyên âm tầng 4.
    
    Args:
        image_np: Ảnh đầu vào (H, W) hoặc (H, W, C)
        method: 'hpp' (Horizontal Projection) hoặc 'rlsa' (Run-Length Smoothing)
        min_line_height: Chiều cao tối thiểu của một dòng hợp lệ (pixel)
        padding_y: Khoảng đệm an toàn theo trục dọc để tránh cắt cụt dấu

    Returns:
        cropped_lines: Danh sách ảnh con từng dòng
        line_boxes: Danh sách tọa độ (x1, y1, x2, y2)
        annotated_img: Ảnh gốc có vẽ bounding box minh họa
    """
    h, w = image_np.shape[:2]
    
    # 1. Chuyển sang ảnh xám và nhị phân hóa Otsu phục vụ phát hiện dòng
    if image_np.ndim == 3:
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        annotated_img = image_np.copy()
    else:
        gray = image_np.copy()
        annotated_img = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)

    # Khử nhiễu nhẹ trước khi nhị phân
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Đảm bảo chữ màu đen (0), nền trắng (255)
    white_pixels = np.sum(binary == 255)
    black_pixels = np.sum(binary == 0)
    if black_pixels > white_pixels:
        binary = cv2.bitwise_not(binary)

    # 2. Phân đoạn dòng
    if method.lower() == "rlsa":
        raw_boxes = segment_lines_rlsa(binary, thresh_h=35)
    else:
        raw_boxes = segment_lines_horizontal_projection(binary, min_line_height=min_line_height, valley_thresh=3)

    # Nếu không phát hiện được dòng nào, coi toàn bộ ảnh là 1 dòng
    if not raw_boxes:
        raw_boxes = [(0, 0, w, h)]

    # Sắp xếp các dòng theo tọa độ y từ trên xuống dưới
    raw_boxes.sort(key=lambda b: b[1])

    cropped_lines = []
    line_boxes = []

    for idx, (x1, y1, x2, y2) in enumerate(raw_boxes):
        # Mở rộng đệm padding an toàn cho 4 tầng độ cao chữ Lào
        adj_y1 = max(0, y1 - padding_y)
        adj_y2 = min(h, y2 + padding_y)
        adj_x1 = max(0, x1)
        adj_x2 = min(w, x2)

        line_h = adj_y2 - adj_y1
        if line_h < min_line_height:
            continue

        box = (adj_x1, adj_y1, adj_x2, adj_y2)
        line_boxes.append(box)

        # Cắt dòng từ ảnh gốc
        line_crop = image_np[adj_y1:adj_y2, adj_x1:adj_x2]
        cropped_lines.append(line_crop)

        # Vẽ bounding box lên annotated_img
        cv2.rectangle(annotated_img, (adj_x1, adj_y1), (adj_x2, adj_y2), (46, 204, 113), 2)
        badge_text = f"L{idx + 1}"
        cv2.putText(
            annotated_img,
            badge_text,
            (adj_x1 + 4, max(adj_y1 + 16, 16)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (231, 76, 60),
            2,
            cv2.LINE_AA
        )

    return cropped_lines, line_boxes, annotated_img


def run_document_ocr(
    image_np: np.ndarray,
    crnn_model=None,
    engine_choice: str = "crnn_lines",
    segmentation_method: str = "hpp"
) -> DocumentOCRResult:
    """
    Thực thi toàn luồng Nhận dạng đoạn văn bản tiếng Lào.
    
    Args:
        image_np: Ảnh đầu vào
        crnn_model: Mô hình LaoCRNN (nếu có)
        engine_choice: 'crnn_lines' hoặc 'tesseract_block'
        segmentation_method: 'hpp' hoặc 'rlsa'
    """
    t_start = time.perf_counter()

    # 1. Phân đoạn dòng
    cropped_lines, line_boxes, annotated_img = detect_and_crop_lines(
        image_np,
        method=segmentation_method,
        min_line_height=14,
        padding_y=3
    )

    line_results: List[LineResult] = []
    text_lines: List[str] = []

    # 2. Động cơ nhận dạng theo dòng (Line-by-line LaoCRNN)
    if "crnn" in engine_choice.lower() and crnn_model is not None:
        for idx, (crop, box) in enumerate(zip(cropped_lines, line_boxes)):
            try:
                line_text = crnn_model.predict_image(crop)
            except Exception:
                line_text = ""

            # Dự phòng Tesseract nếu CRNN chưa nhận diện được dòng đó
            if not line_text.strip():
                try:
                    import pytesseract
                    line_text = pytesseract.image_to_string(crop, lang="lao", config="--psm 7")
                except Exception:
                    pass

            norm_line = normalize_lao(line_text).strip()
            if norm_line:
                text_lines.append(norm_line)
                line_results.append(LineResult(line_index=idx + 1, box=box, text=norm_line))
    else:
        # Chế độ Tesseract Multi-line Block
        try:
            import pytesseract
            raw_doc_text = pytesseract.image_to_string(image_np, lang="lao", config="--psm 6")
        except Exception:
            raw_doc_text = ""

        raw_lines = [normalize_lao(l).strip() for l in raw_doc_text.splitlines() if l.strip()]
        for idx, l_text in enumerate(raw_lines):
            box = line_boxes[idx] if idx < len(line_boxes) else (0, 0, image_np.shape[1], image_np.shape[0])
            line_results.append(LineResult(line_index=idx + 1, box=box, text=l_text))
            text_lines.append(l_text)

    full_text = "\n".join(text_lines)
    full_text = normalize_lao(full_text)
    elapsed_ms = (time.perf_counter() - t_start) * 1000

    return DocumentOCRResult(
        full_text=full_text,
        lines=line_results,
        annotated_image=annotated_img,
        num_lines=len(line_results),
        elapsed_ms=elapsed_ms,
        engine_name="LaoCRNN + HPP Line Segmentation" if "crnn" in engine_choice.lower() else "Tesseract PSM 6 Block"
    )
