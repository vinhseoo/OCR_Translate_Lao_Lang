"""
Module Hiệu chỉnh phối cảnh (Perspective Correction - Bước A4).
Tự động phát hiện 4 góc thẻ flashcard qua contour + approxPolyDP và nắn thẳng (Warp Perspective).
"""
from typing import Tuple
import numpy as np
import cv2


def order_points(pts: np.ndarray) -> np.ndarray:
    """Sắp xếp 4 điểm theo thứ tự: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left (tổng x+y nhỏ nhất)
    rect[2] = pts[np.argmax(s)]  # Bottom-right (tổng x+y lớn nhất)
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-right (hiệu y-x nhỏ nhất)
    rect[3] = pts[np.argmax(diff)]  # Bottom-left (hiệu y-x lớn nhất)
    return rect


def four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Biến đổi phối cảnh phối hợp ma trận đồng biến (Homography Matrix)."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Tính chiều rộng mới
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_w = max(int(width_a), int(width_b))
    
    # Tính chiều cao mới
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_h = max(int(height_a), int(height_b))
    
    dst = np.array([
        [0, 0],
        [max_w - 1, 0],
        [max_w - 1, max_h - 1],
        [0, max_h - 1]
    ], dtype="float32")
    
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (max_w, max_h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return warped


def apply_perspective_correction(image_rgb: np.ndarray, min_area: float = 5000.0) -> Tuple[np.ndarray, bool]:
    """
    Phát hiện đường bao thẻ flashcard và nắn thẳng phối cảnh.
    Trả về: (Ảnh đã nắn hoặc ảnh gốc, boolean báo hiệu có nắn hay không).
    """
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            warped = four_point_transform(image_rgb, approx.reshape(4, 2))
            return warped, True
            
    return image_rgb.copy(), False
