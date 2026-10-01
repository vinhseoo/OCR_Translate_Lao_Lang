"""
Module Phân đoạn dòng và vùng văn bản (Line & Text Region Segmentation).
Bao gồm 4 giải thuật so sánh trên tập 30 trang sách (Phase P3):
  1. Horizontal Projection Profile (HPP) - Phân tích đặc thù 4 tầng chữ Lào
  2. RLSA (Run-Length Smoothing Algorithm)
  3. Connected Components + X-overlap bounding box merging
  4. Density / Morphological Text Line Detector
"""
import math
from typing import List, Tuple, Dict, Any
import numpy as np
import cv2


def segment_lines_horizontal_projection(binary_img: np.ndarray, min_line_height: int = 15, valley_thresh: int = 2) -> List[Tuple[int, int, int, int]]:
    """
    Phương pháp 1: Horizontal Projection Profile (HPP).
    Chiếu tổng số điểm ảnh đen theo từng hàng (Horizontal histogram).
    Các thung lũng (Valleys) giữa các đỉnh thể hiện khoảng cách giữa các dòng.
    Đặc thù chữ Lào: Dấu thanh tầng 1 của dòng dưới đôi khi chạm nguyên âm dưới tầng 4 của dòng trên.
    """
    h, w = binary_img.shape
    # Điểm ảnh chữ màu đen (0) -> đếm số lượng pixel chữ trên từng hàng y
    text_pixels = np.sum(binary_img == 0, axis=1)
    
    lines = []
    in_line = False
    start_y = 0
    
    for y in range(h):
        val = text_pixels[y]
        if val > valley_thresh and not in_line:
            in_line = True
            start_y = y
        elif val <= valley_thresh and in_line:
            in_line = False
            end_y = y
            if (end_y - start_y) >= min_line_height:
                lines.append((0, start_y, w, end_y))
                
    if in_line and (h - start_y) >= min_line_height:
        lines.append((0, start_y, w, h))
        
    return lines


def run_length_smoothing(binary_img: np.ndarray, threshold_h: int = 30) -> np.ndarray:
    """
    Giải thuật RLSA (Run-Length Smoothing Algorithm) theo chiều ngang:
    Nối các khoảng trắng nhỏ hơn threshold_h giữa các nét chữ để tạo thành dải băng dòng.
    """
    h, w = binary_img.shape
    smoothed = binary_img.copy()
    
    for row in range(h):
        line = smoothed[row]
        # Tìm các chuỗi điểm trắng (255) nằm giữa các điểm đen (0)
        black_indices = np.where(line == 0)[0]
        if len(black_indices) < 2:
            continue
        gaps = np.diff(black_indices)
        for i, gap in enumerate(gaps):
            if 1 < gap <= threshold_h:
                start_x = black_indices[i]
                end_x = black_indices[i + 1]
                line[start_x:end_x] = 0
                
    return smoothed


def segment_lines_rlsa(binary_img: np.ndarray, thresh_h: int = 35) -> List[Tuple[int, int, int, int]]:
    """Phương pháp 2: Tách dòng qua RLSA."""
    smoothed = run_length_smoothing(binary_img, threshold_h=thresh_h)
    inv = (255 - smoothed).astype(np.uint8)
    contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    lines = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 50 and h > 15:
            lines.append((x, y, x + w, y + h))
            
    # Sắp xếp các dòng theo tọa độ y từ trên xuống
    lines.sort(key=lambda b: b[1])
    return lines


def segment_lines_connected_components(binary_img: np.ndarray, x_overlap_thresh: float = 0.3) -> List[Tuple[int, int, int, int]]:
    """
    Phương pháp 3: Connected Components + Gộp theo trục Y và độ chồng lấn.
    """
    inv = (255 - binary_img).astype(np.uint8)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inv, connectivity=8)
    
    boxes = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area > 10 and h > 5:
            boxes.append([x, y, x + w, y + h])
            
    if not boxes:
        return []
        
    boxes.sort(key=lambda b: (b[1], b[0]))
    
    # Gộp các component có cùng khoảng dòng (Y overlap)
    merged_lines = []
    for box in boxes:
        x1, y1, x2, y2 = box
        matched = False
        for line in merged_lines:
            # Kiểm tra độ chồng lấn theo trục Y
            ly1, ly2 = line[1], line[3]
            overlap = max(0, min(y2, ly2) - max(y1, ly1))
            min_h = min(y2 - y1, ly2 - ly1)
            if min_h > 0 and (overlap / min_h) > 0.4:
                # Gộp vào dòng hiện tại
                line[0] = min(line[0], x1)
                line[1] = min(line[1], y1)
                line[2] = max(line[2], x2)
                line[3] = max(line[3], y2)
                matched = True
                break
        if not matched:
            merged_lines.append([x1, y1, x2, y2])
            
    # Lọc các dòng quá nhỏ
    valid_lines = [(l[0], l[1], l[2], l[3]) for l in merged_lines if (l[2] - l[0]) > 50 and (l[3] - l[1]) > 15]
    valid_lines.sort(key=lambda b: b[1])
    return valid_lines


def segment_lines_morphological(binary_img: np.ndarray, kernel_w: int = 40, kernel_h: int = 3) -> List[Tuple[int, int, int, int]]:
    """
    Phương pháp 4: Morphological Dilation Text Detector.
    Dùng kernel chữ nhật nằm ngang kéo dài để dính các chữ trong cùng dòng thành 1 contour.
    """
    inv = (255 - binary_img).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_w, kernel_h))
    dilated = cv2.dilate(inv, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lines = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 60 and h > 15:
            lines.append((x, y, x + w, y + h))
            
    lines.sort(key=lambda b: b[1])
    return lines


# ==============================================================================
# HÀM ĐÁNH GIÁ ĐO LƯỜNG IOU, PRECISION, RECALL, F1
# ==============================================================================
def compute_box_iou(box1: Tuple[int, int, int, int], box2: Tuple[int, int, int, int]) -> float:
    """
    Tính Intersection over Union (IoU) giữa 2 bounding box dòng chữ (x1, y1, x2, y2).
    Đối với phân đoạn dòng (Line Segmentation), chuẩn hóa phạm vi chiều ngang để đo chính xác
    độ phủ phân cách giữa các dòng theo trục Y (tránh phạt oan do chênh lệch lề ngang).
    """
    # Chuẩn hóa về cùng phạm vi ngang chung để đánh giá biên dòng theo trục Y
    y1_inter = max(box1[1], box2[1])
    y2_inter = min(box1[3], box2[3])
    inter_h = max(0, y2_inter - y1_inter)
    
    h1 = box1[3] - box1[1]
    h2 = box2[3] - box2[1]
    union_h = h1 + h2 - inter_h
    
    if union_h <= 0:
        return 0.0
    return float(inter_h) / union_h


def evaluate_line_segmentation(gt_boxes: List[Tuple[int, int, int, int]], pred_boxes: List[Tuple[int, int, int, int]], iou_thresh: float = 0.5) -> Dict[str, float]:
    """
    Đo Precision, Recall, F1 theo ngưỡng IoU (thường là 0.5).
    """
    if not gt_boxes and not pred_boxes:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if not gt_boxes or not pred_boxes:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        
    matched_gt = set()
    tp = 0
    
    for pb in pred_boxes:
        best_iou = 0.0
        best_gt_idx = -1
        for g_idx, gb in enumerate(gt_boxes):
            if g_idx in matched_gt:
                continue
            iou = compute_box_iou(pb, gb)
            if iou > best_iou:
                best_iou = iou
                best_gt_idx = g_idx
                
        if best_iou >= iou_thresh and best_gt_idx >= 0:
            tp += 1
            matched_gt.add(best_gt_idx)
            
    fp = len(pred_boxes) - tp
    fn = len(gt_boxes) - tp
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}
