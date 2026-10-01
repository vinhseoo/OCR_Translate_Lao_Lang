"""
Chương trình thực thi chính (End-to-End CLI Pipeline).
Luồng hoạt động:
  Ảnh đầu vào -> Tiền xử lý (Grayscale + Otsu) -> Tesseract Lao OCR -> Tra từ điển -> Xuất kết quả
"""
import os
import sys
import time
import argparse
from PIL import Image

# Thêm thư mục gốc vào sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Cấu hình UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.pipeline import preprocess_image_p1
from src.ocr.tesseract_engine import TesseractLaoEngine
from src.postprocessing.mini_dict_matcher import MiniDictMatcher


def run_pipeline(image_path: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")
        
    start_time = time.time()
    
    # 1. Tải ảnh & Tiền xử lý
    orig_img = Image.open(image_path)
    processed_img = preprocess_image_p1(orig_img)
    
    # 2. Nhận dạng OCR
    engine = TesseractLaoEngine()
    recognized_text = engine.recognize(processed_img)
    
    # 3. Tra từ điển & Hậu xử lý
    matcher = MiniDictMatcher()
    result = matcher.lookup(recognized_text)
    
    elapsed = time.time() - start_time
    result["latency_seconds"] = round(elapsed, 3)
    result["image_path"] = image_path
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Hệ thống OCR & Dịch Tiếng Lào cho Giáo Dục Trực Tuyến")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn đến ảnh cần nhận dạng")
    args = parser.parse_args()
    
    print("=" * 60)
    print("🇱🇦 LAO OCR & EDUCATIONAL TRANSLATION PIPELINE (PHASE P1 SPIKE)")
    print("=" * 60)
    print(f"Ảnh đầu vào: {args.image}")
    
    try:
        res = run_pipeline(args.image)
        print("-" * 60)
        print(f"  • Chữ Lào nhận dạng : {res['lao']}")
        print(f"  • Phiên âm Latin    : {res['romanization']}")
        print(f"  • Nghĩa Tiếng Việt  : {res['vi']}")
        print(f"  • Nghĩa Tiếng Anh   : {res['en']}")
        print(f"  • Từ loại           : {res['type']}")
        print(f"  • Độ tin cậy        : {res['confidence'] * 100:.1f}% ({res['match_type']})")
        print(f"  • Thời gian xử lý   : {res['latency_seconds']} giây")
        print("=" * 60)
    except Exception as e:
        print(f"[LỖI XỬ LÝ]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
