"""
Module Ghi Nhận Phản Hồi & Đóng Góp Sửa Lỗi (User Feedback & Continuous Learning).
Lưu trữ các trường hợp người học / giảng viên hiệu đính kết quả nhận dạng
phục vụ tái huấn luyện mô hình (Active Learning Loop).
"""
import os
import csv
from datetime import datetime
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FEEDBACK_DIR = os.path.join(PROJECT_ROOT, "data", "feedback")
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "user_corrections.csv")


def save_user_correction(
    image_name: str,
    raw_ocr: str,
    corrected_text: str,
    engine_used: str,
    user_note: str = ""
) -> bool:
    """Lưu trữ phản hồi sửa lỗi của người dùng vào tệp CSV."""
    os.makedirs(FEEDBACK_DIR, exist_ok=True)
    file_exists = os.path.exists(FEEDBACK_FILE)
    
    with open(FEEDBACK_FILE, mode="a", encoding="utf-8", newline="") as f:
        fieldnames = ["timestamp", "image_name", "raw_ocr", "corrected_text", "engine_used", "user_note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_name": image_name,
            "raw_ocr": raw_ocr,
            "corrected_text": corrected_text,
            "engine_used": engine_used,
            "user_note": user_note,
        })
    return True


def load_user_corrections() -> List[Dict[str, str]]:
    """Tải danh sách các phản hồi đã lưu."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    corrections = []
    with open(FEEDBACK_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            corrections.append(dict(r))
    return corrections
