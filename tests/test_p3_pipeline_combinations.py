"""
Kiểm thử Cổng ra P3: Đảm bảo pipeline(img, cfg) chạy sạch với >= 20 cấu hình khác nhau.
Kiểm tra từng bước A1 - A9 độc lập và kết hợp.
"""
import os
import sys
import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.pipeline import PreprocessingPipeline

SAMPLE_IMAGE = os.path.join(PROJECT_ROOT, "data", "gold", "images", "gold_card_0001.jpg")


def test_24_pipeline_configurations():
    assert os.path.exists(SAMPLE_IMAGE), f"Không tìm thấy ảnh mẫu: {SAMPLE_IMAGE}"
    
    # Danh sách 24 cấu hình thử nghiệm đa dạng cho A1 - A9
    test_configs = [
        # Nhóm 1: Các phương pháp xám hóa (A1)
        {"name": "A1_bgr2gray", "grayscale": {"enabled": True, "method": "bgr2gray"}},
        {"name": "A1_hsv_v", "grayscale": {"enabled": True, "method": "hsv_v"}},
        {"name": "A1_lab_l", "grayscale": {"enabled": True, "method": "lab_l"}},
        
        # Nhóm 2: Cân bằng sáng (A2)
        {"name": "A2_clahe_clip1", "illumination": {"enabled": True, "method": "clahe", "clip_limit": 1.0}},
        {"name": "A2_clahe_clip2", "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0}},
        {"name": "A2_clahe_clip4", "illumination": {"enabled": True, "method": "clahe", "clip_limit": 4.0}},
        {"name": "A2_gamma_08", "illumination": {"enabled": True, "method": "gamma", "gamma": 0.8}},
        {"name": "A2_gamma_15", "illumination": {"enabled": True, "method": "gamma", "gamma": 1.5}},
        {"name": "A2_homomorphic", "illumination": {"enabled": True, "method": "homomorphic", "cutoff": 25.0}},
        
        # Nhóm 3: Khử nhiễu (A3)
        {"name": "A3_gaussian", "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3}},
        {"name": "A3_median", "denoise": {"enabled": True, "method": "median", "kernel_size": 3}},
        {"name": "A3_bilateral", "denoise": {"enabled": True, "method": "bilateral", "kernel_size": 5}},
        {"name": "A3_nlm", "denoise": {"enabled": True, "method": "nlm"}},
        
        # Nhóm 4: Nhị phân hóa 6 phương pháp (A6 - Bảng quan trọng nhất)
        {"name": "A6_otsu", "binarization": {"enabled": True, "method": "otsu"}},
        {"name": "A6_adaptive_mean", "binarization": {"enabled": True, "method": "adaptive_mean", "window_size": 25}},
        {"name": "A6_adaptive_gaussian", "binarization": {"enabled": True, "method": "adaptive_gaussian", "window_size": 25}},
        {"name": "A6_sauvola_k02", "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2}},
        {"name": "A6_sauvola_k05", "binarization": {"enabled": True, "method": "sauvola", "window_size": 31, "k": 0.5}},
        {"name": "A6_niblack", "binarization": {"enabled": True, "method": "niblack", "window_size": 25, "k": -0.2}},
        {"name": "A6_wolf", "binarization": {"enabled": True, "method": "wolf", "window_size": 25, "k": 0.5}},
        
        # Nhóm 5: Hình thái học (A7)
        {"name": "A7_opening_1x1", "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]}},
        {"name": "A7_opening_2x2", "morphology": {"enabled": True, "operation": "opening", "kernel_size": [2, 2]}},
        {"name": "A7_closing_2x2", "morphology": {"enabled": True, "operation": "closing", "kernel_size": [2, 2]}},
        
        # Nhóm 6: Chuẩn hóa chiều cao dòng (A8)
        {"name": "A8_height_24", "height_normalization": {"enabled": True, "target_height": 24}},
        {"name": "A8_height_32", "height_normalization": {"enabled": True, "target_height": 32}},
        {"name": "A8_height_48", "height_normalization": {"enabled": True, "target_height": 48}},
        {"name": "A8_height_64", "height_normalization": {"enabled": True, "target_height": 64}},
        
        # Nhóm 7: Làm mảnh / Làm dày nét (A9)
        {"name": "A9_dilate_1px", "stroke_adjust": {"enabled": True, "operation": "dilate_1px"}},
        {"name": "A9_thinning", "stroke_adjust": {"enabled": True, "operation": "thinning"}},
        
        # Nhóm 8: Chuỗi tiền xử lý tổ hợp tối ưu hoàn chỉnh
        {
            "name": "Full_Optimal_Pipeline",
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3},
            "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2},
            "height_normalization": {"enabled": True, "target_height": 32}
        }
    ]
    
    print(f"Tổng số cấu hình kiểm thử: {len(test_configs)}")
    passed_count = 0
    
    for idx, cfg in enumerate(test_configs, start=1):
        name = cfg.pop("name")
        pipeline = PreprocessingPipeline(config=cfg)
        out_img, stages = pipeline.process(SAMPLE_IMAGE, return_stages=True)
        
        # Kiểm tra tính toàn vẹn của kết quả
        assert isinstance(out_img, np.ndarray), f"Cấu hình {name} không trả về np.ndarray"
        assert out_img.ndim == 2, f"Cấu hình {name} ảnh không phải 2D (shape={out_img.shape})"
        assert out_img.dtype == np.uint8, f"Cấu hình {name} dtype không phải uint8 ({out_img.dtype})"
        assert len(stages) > 0, f"Cấu hình {name} không có debug stages"
        
        passed_count += 1
        print(f"  [{idx:02d}/{len(test_configs)}] ✅ Cấu hình '{name}': Shape {out_img.shape} -> Thành công sạch sẽ.")
        
    print(f"\n🎉 CỔNG RA P3 (TIÊU CHÍ 1): {passed_count}/{len(test_configs)} cấu hình tiền xử lý chạy hoàn toàn sạch!")


if __name__ == "__main__":
    test_24_pipeline_configurations()
