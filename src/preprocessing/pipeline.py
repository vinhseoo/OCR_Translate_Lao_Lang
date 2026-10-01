"""
Khối tiền xử lý ảnh (Image Preprocessing Pipeline).
Cung cấp hàm tiền xử lý tối thiểu cho Phase P1 (Grayscale + Otsu)
và cấu trúc linh hoạt để tích hợp A1 - A9 ở Phase P3.
"""
from typing import Tuple, Dict, Any, Optional
import numpy as np
from PIL import Image, ImageOps


def otsu_threshold(gray_img: np.ndarray) -> np.ndarray:
    """
    Thuật toán nhị phân hóa Otsu thuần túy (Otsu's Global Thresholding).
    Tìm ngưỡng t tối đa hóa phương sai giữa hai lớp (Between-class variance).
    """
    hist, bin_edges = np.histogram(gray_img.ravel(), bins=256, range=(0, 256))
    total_pixels = gray_img.size
    current_max = 0.0
    threshold = 0
    
    sum_total = np.dot(np.arange(256), hist)
    sum_b = 0.0
    w_b = 0.0
    
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total_pixels - w_b
        if w_f == 0:
            break
            
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        
        # Phương sai giữa 2 lớp
        var_between = w_b * w_f * ((m_b - m_f) ** 2)
        
        if var_between > current_max:
            current_max = var_between
            threshold = t
            
    # Áp dụng ngưỡng: điểm ảnh < threshold -> 0 (chữ đen), ngược lại 255 (nền trắng)
    binary_img = np.where(gray_img < threshold, 0, 255).astype(np.uint8)
    return binary_img


def preprocess_image_p1(image_input: Any) -> Image.Image:
    """
    Pipeline tiền xử lý tối thiểu cho Phase P1 (Lát cắt dọc Spike):
    1. Chuyển sang ảnh xám (Grayscale).
    2. Nhị phân hóa Otsu.
    Trả về PIL Image (1-channel L hoặc binary) chuẩn bị cho Tesseract OCR.
    """
    if isinstance(image_input, str):
        pil_img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        pil_img = image_input.convert("RGB")
    elif isinstance(image_input, np.ndarray):
        pil_img = Image.fromarray(image_input).convert("RGB")
    else:
        raise ValueError(f"Không hỗ trợ kiểu dữ liệu: {type(image_input)}")

    # 1. Chuyển sang ảnh xám
    gray_pil = ImageOps.grayscale(pil_img)
    w, h = gray_pil.size
    
    # Cắt bỏ 16px viền ngoài để loại bỏ nét viền khung thẻ gây nhiễu OCR
    if w > 40 and h > 40:
        gray_pil = gray_pil.crop((16, 16, w - 16, h - 16))
    
    gray_arr = np.array(gray_pil)
    
    # 2. Nhị phân hóa Otsu
    binary_arr = otsu_threshold(gray_arr)
    
    # 3. Thêm viền trắng 10px an toàn (Tesseract nhận diện tốt hơn khi có margin trắng)
    binary_pil = Image.fromarray(binary_arr)
    padded_pil = ImageOps.expand(binary_pil, border=15, fill=255)
    
    return padded_pil
