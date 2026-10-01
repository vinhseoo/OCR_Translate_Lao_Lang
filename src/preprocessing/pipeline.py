"""
Pipeline tiền xử lý ảnh hoàn chỉnh và hướng cấu hình (Config-Driven Pipeline A1 - A9).
Hỗ trợ:
  1. Bật/tắt và tùy chỉnh siêu tham số từng bước A1 - A9 phục vụ Ablation Study (Phase P5).
  2. Trả về cả ảnh kết quả và từ điển các bước trung gian (debug_stages) cho Streamlit & Báo cáo.
  3. Đọc trực tiếp cấu hình từ YAML hoặc dict.
"""
from typing import Dict, Any, Tuple, Optional
import numpy as np
from PIL import Image

from src.preprocessing.filters import (
    convert_to_grayscale,
    apply_clahe,
    apply_gamma_correction,
    apply_homomorphic_filter,
    apply_denoise,
    apply_deskew,
    apply_morphology,
    apply_height_normalization,
    apply_stroke_adjustment,
)
from src.preprocessing.perspective import apply_perspective_correction
from src.preprocessing.binarization import apply_binarization


class PreprocessingPipeline:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Khởi tạo pipeline với cấu hình mặc định hoặc tùy biến."""
        self.config = config or self.get_default_config()

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Cấu hình mặc định tiêu chuẩn."""
        return {
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": False, "method": "clahe", "clip_limit": 2.0, "gamma": 1.2},
            "denoise": {"enabled": False, "method": "gaussian", "kernel_size": 3, "sigma": 1.0},
            "perspective_correction": {"enabled": False, "contour_min_area": 5000.0},
            "deskew": {"enabled": False, "method": "moment", "max_angle": 45.0},
            "binarization": {"enabled": True, "method": "otsu", "window_size": 25, "k": 0.2},
            "morphology": {"enabled": False, "operation": "opening", "kernel_size": [1, 1]},
            "height_normalization": {"enabled": False, "target_height": 32},
            "stroke_adjust": {"enabled": False, "operation": "none"},
            "border_padding": {"enabled": True, "padding_px": 15, "crop_outer_px": 16}
        }

    def process(self, image_input: Any, return_stages: bool = False) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Thực thi tuần tự quy trình tiền xử lý A1 - A9 theo cấu hình.
        Input: Đường dẫn file, PIL Image, hoặc NumPy ndarray (RGB).
        Output: (Ảnh nhị phân đầu ra, dict chứa ảnh các bước trung gian nếu return_stages=True).
        """
        stages = {}
        
        # 0. Chuẩn hóa ảnh đầu vào sang NumPy RGB
        if isinstance(image_input, str):
            pil_img = Image.open(image_input).convert("RGB")
            cur_img = np.array(pil_img)
        elif isinstance(image_input, Image.Image):
            cur_img = np.array(image_input.convert("RGB"))
        elif isinstance(image_input, np.ndarray):
            cur_img = image_input.copy()
            if cur_img.ndim == 2:
                cur_img = np.stack([cur_img] * 3, axis=-1)
        else:
            raise ValueError(f"Không hỗ trợ kiểu dữ liệu: {type(image_input)}")
            
        stages["0_original"] = cur_img.copy()
        
        cfg = self.config
        
        # A4: SỬA PHỐI CẢNH (Trước khi xám hóa để tận dụng kênh màu và cạnh sắc)
        persp_cfg = cfg.get("perspective_correction", {})
        if persp_cfg.get("enabled", False):
            min_area = persp_cfg.get("contour_min_area", 5000.0)
            cur_img, warped = apply_perspective_correction(cur_img, min_area=min_area)
            stages["A4_perspective"] = cur_img.copy()

        # Bỏ viền ngoài nếu là ảnh flashcard
        pad_cfg = cfg.get("border_padding", {})
        crop_outer = pad_cfg.get("crop_outer_px", 0)
        if crop_outer > 0 and cur_img.shape[0] > 2 * crop_outer and cur_img.shape[1] > 2 * crop_outer:
            cur_img = cur_img[crop_outer:-crop_outer, crop_outer:-crop_outer]
            stages["border_crop"] = cur_img.copy()
            
        # A1: XÁM HÓA (GRAYSCALE)
        gray_cfg = cfg.get("grayscale", {})
        if gray_cfg.get("enabled", True):
            method = gray_cfg.get("method", "bgr2gray")
            cur_gray = convert_to_grayscale(cur_img, method=method)
        else:
            cur_gray = convert_to_grayscale(cur_img, method="bgr2gray")
        stages["A1_grayscale"] = cur_gray.copy()
        
        # A2: CÂN BẰNG ÁNH SÁNG (ILLUMINATION)
        illum_cfg = cfg.get("illumination", {})
        if illum_cfg.get("enabled", False):
            method = illum_cfg.get("method", "clahe").lower()
            if method == "clahe":
                clip = illum_cfg.get("clip_limit", 2.0)
                cur_gray = apply_clahe(cur_gray, clip_limit=clip)
            elif method == "gamma":
                gamma = illum_cfg.get("gamma", 1.2)
                cur_gray = apply_gamma_correction(cur_gray, gamma=gamma)
            elif method == "homomorphic":
                cutoff = illum_cfg.get("cutoff", 30.0)
                cur_gray = apply_homomorphic_filter(cur_gray, cutoff=cutoff)
            stages["A2_illumination"] = cur_gray.copy()
            
        # A3: KHỬ NHIỄU (DENOISE)
        denoise_cfg = cfg.get("denoise", {})
        if denoise_cfg.get("enabled", False):
            method = denoise_cfg.get("method", "gaussian")
            ksize = denoise_cfg.get("kernel_size", 3)
            sigma = denoise_cfg.get("sigma", 1.0)
            cur_gray = apply_denoise(cur_gray, method=method, kernel_size=ksize, sigma=sigma)
            stages["A3_denoise"] = cur_gray.copy()
            
        # A5: KHỬ NGHIÊNG (DESKEW)
        deskew_cfg = cfg.get("deskew", {})
        if deskew_cfg.get("enabled", False):
            method = deskew_cfg.get("method", "moment")
            max_angle = deskew_cfg.get("max_angle", 45.0)
            cur_gray, angle = apply_deskew(cur_gray, method=method, max_angle=max_angle)
            stages["A5_deskew"] = cur_gray.copy()
            
        # A6: NHỊ PHÂN HÓA (BINARIZATION)
        bin_cfg = cfg.get("binarization", {})
        if bin_cfg.get("enabled", True):
            method = bin_cfg.get("method", "otsu")
            bin_params = {k: v for k, v in bin_cfg.items() if k not in ("enabled", "method")}
            cur_bin = apply_binarization(cur_gray, method=method, **bin_params)
        else:
            cur_bin = apply_binarization(cur_gray, method="otsu")
        stages["A6_binarization"] = cur_bin.copy()
        
        # A7: HÌNH THÁI HỌC (MORPHOLOGY)
        morph_cfg = cfg.get("morphology", {})
        if morph_cfg.get("enabled", False):
            op = morph_cfg.get("operation", "opening")
            ksize = tuple(morph_cfg.get("kernel_size", [1, 1]))
            cur_bin = apply_morphology(cur_bin, operation=op, kernel_size=ksize)
            stages["A7_morphology"] = cur_bin.copy()
            
        # A8: CHUẨN HÓA CHIỀU CAO (HEIGHT NORMALIZATION)
        h_norm_cfg = cfg.get("height_normalization", {})
        if h_norm_cfg.get("enabled", False):
            target_h = h_norm_cfg.get("target_height", 32)
            cur_bin = apply_height_normalization(cur_bin, target_height=target_h)
            stages["A8_height_norm"] = cur_bin.copy()
            
        # A9: LÀM MẢNH / DÀY NÉT (STROKE ADJUST)
        stroke_cfg = cfg.get("stroke_adjust", {})
        if stroke_cfg.get("enabled", False):
            op = stroke_cfg.get("operation", "none")
            cur_bin = apply_stroke_adjustment(cur_bin, operation=op)
            stages["A9_stroke_adjust"] = cur_bin.copy()
            
        # Thêm padding trắng an toàn
        padding_px = pad_cfg.get("padding_px", 15)
        if padding_px > 0:
            cur_bin = np.pad(cur_bin, padding_px, mode="constant", constant_values=255)
            stages["final_padded"] = cur_bin.copy()
            
        if return_stages:
            return cur_bin, stages
        return cur_bin, {}


def process_image(image_input: Any, config: Optional[Dict[str, Any]] = None, return_stages: bool = False):
    """Hàm tiện ích cấp module nhận ảnh và trả về kết quả."""
    pipeline = PreprocessingPipeline(config=config)
    return pipeline.process(image_input, return_stages=return_stages)
