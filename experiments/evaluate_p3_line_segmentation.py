"""
Thực nghiệm so sánh 4 giải thuật phân đoạn dòng chữ trên tập 30 trang sách (Phase P3).
Đo Precision, Recall, F1 theo IoU >= 0.5 và xuất biểu đồ bằng chứng trực quan cấu trúc 4 tầng chữ Lào.
"""
import os
import sys
import csv
from typing import List, Tuple, Dict, Any
import numpy as np
import cv2
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.segmentation import (
    segment_lines_horizontal_projection,
    segment_lines_rlsa,
    segment_lines_connected_components,
    segment_lines_morphological,
    evaluate_line_segmentation,
)
from src.preprocessing.binarization import binarize_otsu

IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "gold", "images")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments", "results")
CSV_OUTPUT = os.path.join(RESULTS_DIR, "line_segmentation_comparison.csv")
PLOT_OUTPUT = os.path.join(RESULTS_DIR, "lao_4tiers_projection_profile.png")


def get_ground_truth_boxes_for_page(page_idx: int, pw: int = 700, ph: int = 950) -> List[Tuple[int, int, int, int]]:
    """
    Sinh tọa độ ground truth dòng chữ tương ứng với cấu trúc trang sách sinh ở P2a:
    Tiêu đề bài học tại y = [50, 105] và 8 dòng câu tại cur_y = 135 + line_no * 75.
    """
    gt_boxes = []
    # 1. Hộp tiêu đề
    gt_boxes.append((50, 45, pw - 50, 110))
    # 2. 8 dòng câu
    for line_no in range(8):
        y1 = 125 + line_no * 75
        y2 = y1 + 55
        gt_boxes.append((50, y1, pw - 50, y2))
    return gt_boxes


def run_line_segmentation_benchmark():
    print("=" * 70)
    print("🔬 ĐÁNH GIÁ 4 PHƯƠNG PHÁP TÁCH DÒNG VĂN BẢN TIẾNG LÀO (PHASE P3)")
    print("=" * 70)
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    page_files = [f"textbook_page_{i:02d}.jpg" for i in range(1, 31)]
    print(f"Tổng số trang sách đánh giá: {len(page_files)} trang")
    
    methods = {
        "Horizontal_Projection_Profile": segment_lines_horizontal_projection,
        "RLSA_Algorithm": segment_lines_rlsa,
        "Connected_Components_Merging": segment_lines_connected_components,
        "Morphological_Line_Detector": segment_lines_morphological,
    }
    
    method_scores = {m: {"precisions": [], "recalls": [], "f1s": []} for m in methods}
    
    for p_idx, fname in enumerate(page_files, start=1):
        fpath = os.path.join(IMAGES_DIR, fname)
        if not os.path.exists(fpath):
            continue
            
        img_bgr = cv2.imread(fpath)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        binary = binarize_otsu(gray)
        h, w = binary.shape
        
        gt_boxes = get_ground_truth_boxes_for_page(p_idx, pw=w, ph=h)
        
        for m_name, func in methods.items():
            pred_boxes = func(binary)
            metrics = evaluate_line_segmentation(gt_boxes, pred_boxes, iou_thresh=0.5)
            method_scores[m_name]["precisions"].append(metrics["precision"])
            method_scores[m_name]["recalls"].append(metrics["recall"])
            method_scores[m_name]["f1s"].append(metrics["f1"])
            
    # Tổng kết bảng kết quả
    summary_rows = []
    print("\n" + "-" * 70)
    print(f"{'Phương pháp phân đoạn':<32} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 70)
    
    for m_name, vals in method_scores.items():
        avg_p = float(np.mean(vals["precisions"]))
        avg_r = float(np.mean(vals["recalls"]))
        avg_f1 = float(np.mean(vals["f1s"]))
        
        summary_rows.append({
            "method": m_name,
            "precision": round(avg_p, 4),
            "recall": round(avg_r, 4),
            "f1_score": round(avg_f1, 4)
        })
        print(f"{m_name:<32} | {avg_p * 100:>8.2f}% | {avg_r * 100:>8.2f}% | {avg_f1 * 100:>8.2f}%")
        
    print("-" * 70)
    
    # Ghi ra CSV
    with open(CSV_OUTPUT, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["method", "precision", "recall", "f1_score"])
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"✅ Đã xuất bảng so sánh chi tiết ra: {CSV_OUTPUT}")
    
    # 2. Sinh biểu đồ phân tích 4 tầng độ cao tiếng Lào trên Horizontal Projection Profile
    generate_tier_diagnostic_plot(os.path.join(IMAGES_DIR, "textbook_page_01.jpg"))
    return summary_rows


def generate_tier_diagnostic_plot(sample_page_path: str):
    """
    Vẽ đồ thị Horizontal Projection Profile minh họa cấu trúc 4 tầng chữ Lào:
    - Tầng 1: Dấu thanh (Tone marks) trên cùng
    - Tầng 2: Nguyên âm trên (Upper vowels)
    - Tầng 3: Thân phụ âm chính (Base consonants)
    - Tầng 4: Nguyên âm dưới (Lower vowels)
    Chứng minh bằng trực quan lý do phân đoạn dòng tiếng Lào phức tạp hơn tiếng Anh/Việt.
    """
    img_bgr = cv2.imread(sample_page_path)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    binary = binarize_otsu(gray)
    h, w = binary.shape
    
    # Cắt 1 vùng dòng chữ tiêu biểu (từ y=120 đến y=290, gồm 2 dòng kề nhau)
    roi_y1, roi_y2 = 120, 290
    crop_bin = binary[roi_y1:roi_y2, 50:w-50]
    proj = np.sum(crop_bin == 0, axis=1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.5, 1]})
    
    # Ảnh dòng văn bản cắt mẫu
    ax1.imshow(crop_bin, cmap="gray")
    ax1.set_title("Văn bản Tiếng Lào 2 dòng liên tiếp (Cắt từ textbook_page_01)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Chiều ngang (px)")
    ax1.set_ylabel("Tọa độ Y (px)")
    
    # Đồ thị Horizontal Projection Profile
    y_coords = np.arange(len(proj))
    ax2.plot(proj, y_coords, color="crimson", linewidth=1.5)
    ax2.invert_yaxis()
    ax2.set_title("Horizontal Projection Profile (Số lượng pixel chữ)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Mật độ điểm ảnh đen")
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    # Chú thích các tầng chữ Lào trên đồ thị
    ax2.axhline(y=20, color="blue", linestyle=":", label="Tầng 1: Dấu thanh (Tone Marks)")
    ax2.axhline(y=38, color="green", linestyle=":", label="Tầng 2: Nguyên âm trên (Vowels above)")
    ax2.axhline(y=55, color="orange", linestyle=":", label="Tầng 3: Phụ âm chính (Base Consonants)")
    ax2.axhline(y=75, color="purple", linestyle=":", label="Tầng 4: Nguyên âm dưới (Vowels below)")
    ax2.axhline(y=95, color="black", linestyle="--", label="Thung lũng phân cách dòng (Line Valley)")
    ax2.legend(loc="lower right", fontsize=9)
    
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT, dpi=200)
    plt.close()
    print(f"✅ Đã xuất biểu đồ chẩn đoán cấu trúc 4 tầng chữ Lào: {PLOT_OUTPUT}")


if __name__ == "__main__":
    run_line_segmentation_benchmark()
