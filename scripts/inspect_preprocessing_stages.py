"""
Script xuất ảnh trực quan hóa từng bước trung gian của Khối Tiền Xử Lý (Phase P3 Exit Gate).
Hiển thị lưới các bước biến đổi:
  Ảnh gốc -> Hiệu chỉnh phối cảnh -> Xám hóa -> Cân bằng sáng -> Khử nhiễu -> Khử nghiêng -> Nhị phân hóa -> Hình thái học -> Chuẩn hóa cao -> Làm nét.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.pipeline import PreprocessingPipeline

SAMPLE_IMAGE = os.path.join(PROJECT_ROOT, "data", "gold", "images", "gold_card_0004.jpg")
OUTPUT_INSPECTION_PLOT = os.path.join(PROJECT_ROOT, "experiments", "results", "preprocessing_stages_inspection.png")


def generate_preprocessing_inspection_panel():
    print(f"Ảnh đầu vào: {SAMPLE_IMAGE}")
    
    # Cấu hình bật toàn diện các bước A1 - A9 để trực quan hóa
    full_config = {
        "perspective_correction": {"enabled": True, "contour_min_area": 5000.0},
        "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
        "grayscale": {"enabled": True, "method": "bgr2gray"},
        "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.5},
        "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3, "sigma": 0.8},
        "deskew": {"enabled": True, "method": "moment", "max_angle": 45.0},
        "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.25},
        "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]},
        "height_normalization": {"enabled": True, "target_height": 64},
        "stroke_adjust": {"enabled": True, "operation": "dilate_1px"}
    }
    
    pipeline = PreprocessingPipeline(config=full_config)
    final_img, stages = pipeline.process(SAMPLE_IMAGE, return_stages=True)
    
    stage_items = list(stages.items())
    n_stages = len(stage_items)
    print(f"Số lượng bước trung gian trích xuất: {n_stages}")
    
    cols = 3
    rows = (n_stages + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 3.5))
    axes = axes.flatten()
    
    stage_labels = {
        "0_original": "0. Ảnh gốc (RGB)",
        "A4_perspective": "A4. Sửa phối cảnh (Perspective Warp)",
        "border_crop": "Cắt viền ngoài (Border Margin Crop)",
        "A1_grayscale": "A1. Xám hóa (Grayscale BGR2GRAY)",
        "A2_illumination": "A2. Cân bằng sáng (CLAHE clip=2.5)",
        "A3_denoise": "A3. Khử nhiễu (Gaussian sigma=0.8)",
        "A5_deskew": "A5. Khử nghiêng (Deskew Moment)",
        "A6_binarization": "A6. Nhị phân hóa (Sauvola k=0.25)",
        "A7_morphology": "A7. Hình thái học (Opening 1x1)",
        "A8_height_norm": "A8. Chuẩn hóa cao (Height 64px)",
        "A9_stroke_adjust": "A9. Làm dày nét nhẹ (Dilate 1px)",
        "final_padded": "Kết quả cuối (White Padded)"
    }
    
    for idx, (stage_key, img_arr) in enumerate(stage_items):
        ax = axes[idx]
        title = stage_labels.get(stage_key, stage_key)
        
        if img_arr.ndim == 3:
            ax.imshow(img_arr)
        else:
            ax.imshow(img_arr, cmap="gray")
            
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.axis("off")
        
    for j in range(n_stages, len(axes)):
        axes[j].axis("off")
        
    plt.suptitle("KIỂM TRA CÁC BƯỚC TIỀN XỬ LÝ ẢNH TRUNG GIAN A1 - A9 (PHASE P3 INSPECTOR)", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    os.makedirs(os.path.dirname(OUTPUT_INSPECTION_PLOT), exist_ok=True)
    plt.savefig(OUTPUT_INSPECTION_PLOT, dpi=200, bbox_inches="tight")
    plt.close()
    
    print(f"✅ Đã lưu ảnh trực quan hóa các bước trung gian ra: {OUTPUT_INSPECTION_PLOT}")


if __name__ == "__main__":
    generate_preprocessing_inspection_panel()
