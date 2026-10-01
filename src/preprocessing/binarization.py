"""
Module Nhị phân hóa ảnh (Binarization - Bước A6).
Bao gồm 6 phương pháp đối chứng phục vụ nghiên cứu Ablation (Bảng 3 - P5):
  1. Otsu (Global)
  2. Adaptive Mean (Local)
  3. Adaptive Gaussian (Local)
  4. Sauvola (Thích nghi cửa sổ trượt - chịu bóng đổ)
  5. Niblack
  6. Wolf (Cải tiến của Sauvola)
"""
from typing import Tuple
import numpy as np


def binarize_otsu(gray_img: np.ndarray) -> np.ndarray:
    """Otsu Global Thresholding."""
    hist, _ = np.histogram(gray_img.ravel(), bins=256, range=(0, 256))
    total = gray_img.size
    current_max = 0.0
    thresh = 128
    
    sum_total = np.dot(np.arange(256), hist)
    sum_b = 0.0
    w_b = 0.0
    
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
            
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        
        var_between = w_b * w_f * ((m_b - m_f) ** 2)
        if var_between > current_max:
            current_max = var_between
            thresh = t
            
    binary = np.where(gray_img < thresh, 0, 255).astype(np.uint8)
    return binary


def binarize_adaptive_mean(gray_img: np.ndarray, window_size: int = 25, c: int = 10) -> np.ndarray:
    """Adaptive Mean Thresholding sử dụng integral image để tính nhanh."""
    if window_size % 2 == 0:
        window_size += 1
    r = window_size // 2
    
    h, w = gray_img.shape
    padded = np.pad(gray_img, r, mode="reflect").astype(np.float64)
    integral = np.pad(padded.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode="constant")
    
    y0 = np.arange(h)
    y1 = y0 + window_size
    x0 = np.arange(w)
    x1 = x0 + window_size
    
    Y0, X0 = np.meshgrid(y0, x0, indexing="ij")
    Y1, X1 = np.meshgrid(y1, x1, indexing="ij")
    
    area = window_size * window_size
    local_mean = (integral[Y1, X1] - integral[Y0, X1] - integral[Y1, X0] + integral[Y0, X0]) / area
    threshold = local_mean - c
    
    binary = np.where(gray_img < threshold, 0, 255).astype(np.uint8)
    return binary


def binarize_adaptive_gaussian(gray_img: np.ndarray, window_size: int = 25, c: int = 5) -> np.ndarray:
    """Adaptive Gaussian Thresholding xấp xỉ qua box filter 2 tầng."""
    try:
        import cv2
        if window_size % 2 == 0:
            window_size += 1
        return cv2.adaptiveThreshold(
            gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, window_size, c
        )
    except Exception:
        # Fallback tính qua local mean nếu chưa load được cv2
        return binarize_adaptive_mean(gray_img, window_size, c)


def compute_local_mean_and_std(gray_img: np.ndarray, window_size: int) -> Tuple[np.ndarray, np.ndarray]:
    """Tính mean và std cục bộ trong cửa sổ trượt bằng Integral Images (O(1) mỗi điểm)."""
    if window_size % 2 == 0:
        window_size += 1
    r = window_size // 2
    h, w = gray_img.shape
    
    img_f = gray_img.astype(np.float64)
    img_sq = img_f ** 2
    
    pad_f = np.pad(img_f, r, mode="reflect")
    pad_sq = np.pad(img_sq, r, mode="reflect")
    
    int_f = np.pad(pad_f.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode="constant")
    int_sq = np.pad(pad_sq.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode="constant")
    
    y0 = np.arange(h)
    y1 = y0 + window_size
    x0 = np.arange(w)
    x1 = x0 + window_size
    
    Y0, X0 = np.meshgrid(y0, x0, indexing="ij")
    Y1, X1 = np.meshgrid(y1, x1, indexing="ij")
    
    area = window_size * window_size
    mean = (int_f[Y1, X1] - int_f[Y0, X1] - int_f[Y1, X0] + int_f[Y0, X0]) / area
    sq_mean = (int_sq[Y1, X1] - int_sq[Y0, X1] - int_sq[Y1, X0] + int_sq[Y0, X0]) / area
    
    variance = np.maximum(sq_mean - mean ** 2, 0.0)
    std = np.sqrt(variance)
    return mean, std


def binarize_sauvola(gray_img: np.ndarray, window_size: int = 25, k: float = 0.2, r: float = 128.0) -> np.ndarray:
    """
    Thuật toán Sauvola:
      T(x,y) = m(x,y) * (1 + k * (s(x,y) / R - 1))
    Khắc phục vượt trội hiện tượng bóng đổ và ánh sáng không đồng đều.
    """
    mean, std = compute_local_mean_and_std(gray_img, window_size)
    threshold = mean * (1.0 + k * (std / r - 1.0))
    binary = np.where(gray_img < threshold, 0, 255).astype(np.uint8)
    return binary


def binarize_niblack(gray_img: np.ndarray, window_size: int = 25, k: float = -0.2) -> np.ndarray:
    """
    Thuật toán Niblack:
      T(x,y) = m(x,y) + k * s(x,y)
    """
    mean, std = compute_local_mean_and_std(gray_img, window_size)
    threshold = mean + k * std
    binary = np.where(gray_img < threshold, 0, 255).astype(np.uint8)
    return binary


def binarize_wolf(gray_img: np.ndarray, window_size: int = 25, k: float = 0.5) -> np.ndarray:
    """
    Thuật toán Wolf & Jolion:
      Cải tiến của Sauvola bằng cách chuẩn hóa theo độ lệch chuẩn cực đại R và giá trị xám cực tiểu M.
    """
    mean, std = compute_local_mean_and_std(gray_img, window_size)
    min_gray = float(np.min(gray_img))
    max_std = float(np.max(std))
    if max_std == 0:
        max_std = 1.0
        
    threshold = mean + k * (std / max_std) * (mean - min_gray)
    binary = np.where(gray_img < threshold, 0, 255).astype(np.uint8)
    return binary


def apply_binarization(gray_img: np.ndarray, method: str = "otsu", **kwargs) -> np.ndarray:
    """Hàm binarization tổng quát hướng cấu hình."""
    method = method.lower()
    window_size = kwargs.get("window_size", 25)
    
    if method == "otsu":
        return binarize_otsu(gray_img)
    elif method == "adaptive_mean":
        c = kwargs.get("c", 10)
        return binarize_adaptive_mean(gray_img, window_size, c)
    elif method == "adaptive_gaussian":
        c = kwargs.get("c", 5)
        return binarize_adaptive_gaussian(gray_img, window_size, c)
    elif method == "sauvola":
        k = kwargs.get("k", 0.2)
        r = kwargs.get("r", 128.0)
        return binarize_sauvola(gray_img, window_size, k, r)
    elif method == "niblack":
        k = kwargs.get("k", -0.2)
        return binarize_niblack(gray_img, window_size, k)
    elif method == "wolf":
        k = kwargs.get("k", 0.5)
        return binarize_wolf(gray_img, window_size, k)
    else:
        raise ValueError(f"Không hỗ trợ phương pháp nhị phân hóa: {method}")
