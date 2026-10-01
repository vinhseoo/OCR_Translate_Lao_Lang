"""
Tesseract OCR Engine Wrapper cho tiếng Lào.
Tuân thủ cấu hình: tessdata_best, --oem 1 (LSTM only), --psm 7 (Single line).
"""
import os
import shutil
from typing import Optional, Dict, Any
from PIL import Image
import pytesseract

from src.preprocessing.normalize import normalize_lao

# Danh sách đường dẫn khả dĩ của tesseract.exe trên Windows
POSSIBLE_TESSERACT_PATHS = [
    r"C:\Users\maiduc.vinh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]


def find_tesseract_binary() -> Optional[str]:
    """Tìm đường dẫn tesseract executable."""
    which_path = shutil.which("tesseract")
    if which_path and os.path.exists(which_path):
        return which_path
        
    for p in POSSIBLE_TESSERACT_PATHS:
        if os.path.exists(p):
            return p
    return None


class TesseractLaoEngine:
    def __init__(
        self,
        tesseract_cmd: Optional[str] = None,
        lang: str = "lao",
        oem: int = 1,
        psm: int = 7,
        tessdata_dir: Optional[str] = None
    ):
        cmd = tesseract_cmd or find_tesseract_binary()
        if not cmd:
            raise FileNotFoundError("Không tìm thấy tesseract binary trên hệ thống!")
        
        pytesseract.pytesseract.tesseract_cmd = cmd
        self.cmd = cmd
        self.lang = lang
        self.oem = oem
        self.psm = psm
        self.tessdata_dir = tessdata_dir

    def recognize(self, image: Image.Image, auto_normalize: bool = True) -> str:
        """
        Nhận dạng chữ tiếng Lào từ ảnh.
        Config: --oem <oem> --psm <psm>
        """
        config = f"--oem {self.oem} --psm {self.psm}"
        if self.tessdata_dir and os.path.exists(self.tessdata_dir):
            config += f' --tessdata-dir "{self.tessdata_dir}"'
            
        raw_text = pytesseract.image_to_string(
            image,
            lang=self.lang,
            config=config
        )
        
        # Bắt buộc chuẩn hóa qua normalize_lao theo Quy tắc vàng
        if auto_normalize:
            return normalize_lao(raw_text)
        return raw_text.strip()
