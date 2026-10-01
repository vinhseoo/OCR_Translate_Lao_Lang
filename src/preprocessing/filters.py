"""
Bộ lọc tiền xử lý ảnh A1 - A9 (Image Preprocessing Filters A1 - A9).
Tất cả các hàm nhận ảnh np.ndarray và trả về ảnh mới, không side-effect.
Hỗ trợ chuyển đổi linh hoạt qua file cấu hình YAML phục vụ Ablation Study (Phase P5).
"""
import math
from typing import Tuple, Optional
import numpy as np
from PIL import Image

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from scipy.ndimage import median_filter, gaussian_filter
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ==============================================================================
# A1: XÁM HÓA (GRAYSCALE)
# ==============================================================================
def convert_to_grayscale(img_rgb: np.ndarray, method: str = "bgr2gray") -> np.ndarray:
    """
    Chuyển đổi ảnh màu sang ảnh xám:
      - 'bgr2gray' / 'rgb2gray': Trọng số chuẩn CIE 0.299 R + 0.587 G + 0.114 B
      - 'hsv_v': Kênh độ sáng Value trong không gian HSV
      - 'lab_l': Kênh độ chói Lightness trong không gian LAB
    """
    method = method.lower()
    if img_rgb.ndim == 2:
        return img_rgb.copy()
        
    if HAS_CV2:
        if method == "hsv_v":
            hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            return hsv[:, :, 2]
        elif method == "lab_l":
            lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
            return lab[:, :, 0]
        else:
            return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    else:
        # Fallback NumPy
        r, g, b = img_rgb[:, :, 0], img_rgb[:, :, 1], img_rgb[:, :, 2]
        if method == "hsv_v":
            return np.maximum(np.maximum(r, g), b).astype(np.uint8)
        else:
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            return np.clip(gray, 0, 255).astype(np.uint8)


# ==============================================================================
# A2: CÂN BẰNG ÁNH SÁNG (ILLUMINATION NORMALIZATION)
# ==============================================================================
def apply_clahe(gray_img: np.ndarray, clip_limit: float = 2.0, tile_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
    """CLAHE: Cân bằng biểu đồ độ sáng thích ứng cục bộ giới hạn tương phản."""
    if HAS_CV2:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        return clahe.apply(gray_img)
    else:
        return gray_img.copy()


def apply_gamma_correction(gray_img: np.ndarray, gamma: float = 1.2) -> np.ndarray:
    """Hiệu chỉnh Gamma: I' = 255 * (I / 255) ^ (1 / gamma)."""
    inv_gamma = 1.0 / max(gamma, 0.001)
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
    if HAS_CV2:
        return cv2.LUT(gray_img, table)
    else:
        return table[gray_img]


def apply_homomorphic_filter(gray_img: np.ndarray, cutoff: float = 30.0) -> np.ndarray:
    """
    Homomorphic Filtering xấp xỉ không gian:
    Tách thành phần phản xạ (chi tiết chữ - tần số cao) và thành phần chiếu sáng (bóng đổ - tần số thấp).
    """
    img_log = np.log1p(gray_img.astype(np.float32))
    if HAS_CV2:
        low_pass = cv2.GaussianBlur(img_log, (0, 0), sigmaX=cutoff)
    else:
        low_pass = img_log
    high_pass = img_log - low_pass
    # Tăng cường high-pass và nén low-pass
    enhanced = np.exp(low_pass * 0.5 + high_pass * 1.5) - 1.0
    res = np.clip((enhanced - np.min(enhanced)) / (np.max(enhanced) - np.min(enhanced) + 1e-5) * 255, 0, 255)
    return res.astype(np.uint8)


# ==============================================================================
# A3: KHỬ NHIỄU (DENOISING)
# ==============================================================================
def apply_denoise(gray_img: np.ndarray, method: str = "gaussian", kernel_size: int = 3, sigma: float = 1.0) -> np.ndarray:
    """Khử nhiễu ảnh: median, bilateral, nlm, gaussian."""
    method = method.lower()
    if kernel_size % 2 == 0:
        kernel_size += 1
        
    if method == "median":
        if HAS_CV2:
            return cv2.medianBlur(gray_img, kernel_size)
        elif HAS_SCIPY:
            return median_filter(gray_img, size=kernel_size)
    elif method == "bilateral" and HAS_CV2:
        return cv2.bilateralFilter(gray_img, d=kernel_size, sigmaColor=75, sigmaSpace=75)
    elif method == "nlm" and HAS_CV2:
        return cv2.fastNlMeansDenoising(gray_img, h=10)
    elif method == "gaussian":
        if HAS_CV2:
            return cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), sigmaX=sigma)
        elif HAS_SCIPY:
            return np.clip(gaussian_filter(gray_img.astype(float), sigma=sigma), 0, 255).astype(np.uint8)
            
    return gray_img.copy()


# ==============================================================================
# A5: KHỬ NGHIÊNG (DESKEW)
# ==============================================================================
def compute_skew_angle_moment(binary_img: np.ndarray) -> float:
    """Tính góc nghiêng văn bản qua Moment bậc 2 trung tâm."""
    # Lấy tọa độ các điểm ảnh chữ (màu đen = 0, chuyển thành mask chữ)
    pts = np.column_stack(np.where(binary_img < 128))
    if len(pts) < 50:
        return 0.0
    if HAS_CV2:
        moments = cv2.moments((binary_img < 128).astype(np.uint8))
        if abs(moments["mu20"] - moments["mu02"]) < 1e-5:
            return 0.0
        theta = 0.5 * math.atan2(2 * moments["mu11"], moments["mu20"] - moments["mu02"])
        return math.degrees(theta)
    return 0.0


def compute_skew_angle_hough(binary_img: np.ndarray) -> float:
    """Tính góc nghiêng văn bản bằng phép biến đổi Hough Lines."""
    if not HAS_CV2:
        return 0.0
    edges = cv2.Canny(binary_img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    if lines is None:
        return 0.0
        
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        if abs(angle) < 45:
            angles.append(angle)
            
    if not angles:
        return 0.0
    return float(np.median(angles))


def rotate_image(img: np.ndarray, angle: float, bg_color: int = 255) -> np.ndarray:
    """Xoay ảnh theo góc góc chỉ định với nền trắng."""
    if abs(angle) < 0.1:
        return img.copy()
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    if HAS_CV2:
        m = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=bg_color)
    else:
        pil_img = Image.fromarray(img)
        return np.array(pil_img.rotate(angle, resample=Image.BICUBIC, fillcolor=bg_color))


def apply_deskew(img: np.ndarray, method: str = "moment", max_angle: float = 45.0) -> Tuple[np.ndarray, float]:
    """Khử nghiêng ảnh theo phương pháp hough / moment."""
    method = method.lower()
    if img.ndim == 3:
        gray = convert_to_grayscale(img)
    else:
        gray = img
        
    if method == "hough":
        angle = compute_skew_angle_hough(gray)
    else:
        angle = compute_skew_angle_moment(gray)
        
    if abs(angle) > max_angle:
        angle = 0.0
        
    rotated = rotate_image(img, -angle, bg_color=255)
    return rotated, angle


# ==============================================================================
# A7: HÌNH THÁI HỌC (MORPHOLOGY) — CẢNH BÁO KERNEL >= 3x3 LÀM RỤNG DẤU
# ==============================================================================
def apply_morphology(binary_img: np.ndarray, operation: str = "opening", kernel_size: Tuple[int, int] = (1, 1)) -> np.ndarray:
    """
    Phép toán hình thái học Opening/Closing.
    Tuân thủ tuyệt đối Quy tắc vàng #3: kernel >= 3x3 xóa sạch dấu thanh tiếng Lào.
    """
    operation = operation.lower()
    kw, kh = kernel_size
    if kw <= 1 and kh <= 1:
        return binary_img.copy()
        
    # Trên ảnh nhị phân: chữ màu đen (0), nền trắng (255)
    # Cần đảo bit để chữ thành 1, thực hiện morphology, sau đó đảo lại
    inverted = (255 - binary_img).astype(np.uint8)
    
    if HAS_CV2:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kw, kh))
        if operation == "opening":
            res = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel)
        elif operation == "closing":
            res = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel)
        else:
            res = inverted
        return 255 - res
    return binary_img.copy()


# ==============================================================================
# A8: CHUẨN HÓA CHIỀU CAO DÒNG (HEIGHT NORMALIZATION)
# ==============================================================================
def apply_height_normalization(img: np.ndarray, target_height: int = 32) -> np.ndarray:
    """
    Chuẩn hóa chiều cao dòng chữ về 24, 32, 48, 64 px giữ nguyên tỷ lệ khung hình.
    Tesseract LSTM rất nhạy cảm với kích thước chiều cao ký tự.
    """
    h, w = img.shape[:2]
    if h == 0 or w == 0:
        return img
    scale = target_height / float(h)
    new_w = max(int(round(w * scale)), 1)
    
    if HAS_CV2:
        interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
        return cv2.resize(img, (new_w, target_height), interpolation=interp)
    else:
        pil_img = Image.fromarray(img)
        res = pil_img.resize((new_w, target_height), Image.Resampling.LANCZOS)
        return np.array(res)


# ==============================================================================
# A9: LÀM MẢNH / LÀM DÀY NÉT (STROKE ADJUSTMENT)
# ==============================================================================
def apply_stroke_adjustment(binary_img: np.ndarray, operation: str = "none") -> np.ndarray:
    """Làm mảnh nét (Thinning) hoặc làm dày nét (Dilate 1px)."""
    operation = operation.lower()
    if operation == "none" or not HAS_CV2:
        return binary_img.copy()
        
    inverted = (255 - binary_img).astype(np.uint8)
    kernel = np.ones((2, 2), np.uint8)
    
    if operation == "dilate_1px":
        # Làm dày nét chữ (dilate chữ)
        thickened = cv2.dilate(inverted, kernel, iterations=1)
        return 255 - thickened
    elif operation == "thinning":
        # Làm mảnh nét chữ (erode chữ 1px)
        thinned = cv2.erode(inverted, kernel, iterations=1)
        return 255 - thinned
        
    return binary_img.copy()
