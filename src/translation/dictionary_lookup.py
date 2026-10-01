"""
Module Tra Cứu Từ Điển Giáo Trình Đa Ngữ (Lao - Vietnamese - English Dictionary).
Hỗ trợ truy xuất $O(1)$ thông tin chi tiết của từng từ vựng:
- Nghĩa Tiếng Việt, Tiếng Anh
- Từ loại (Part of Speech: danh từ, động từ, tính từ, ...)
- Bài học / Chủ đề (Lesson / Category)
- Phiên âm Latinh chuẩn (Romanization)
- Câu ví dụ song ngữ minh họa (Bilingual Examples)
"""
import os
import sys
import csv
from typing import Dict, List, Optional, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao


class LaoDictionary:
    def __init__(self, csv_path: Optional[str] = None):
        """Khởi tạo kho từ điển từ file CSV chuẩn NFC."""
        self.entries: Dict[str, Dict[str, Any]] = {}
        default_csv = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
        self.csv_path = csv_path or default_csv
        self.load()

    def load(self):
        """Nạp dữ liệu từ điển vào bộ nhớ."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Không tìm thấy file từ điển tại: {self.csv_path}")

        self.entries.clear()
        with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lao_norm = normalize_lao(row.get("lao", "").strip())
                if lao_norm:
                    self.entries[lao_norm] = {
                        "lao": lao_norm,
                        "vi": row.get("vi", "").strip(),
                        "en": row.get("en", "").strip(),
                        "romanization": row.get("romanization", "").strip(),
                        "pos": row.get("pos", "").strip(),
                        "lesson": row.get("lesson", "").strip(),
                        "example_lao": normalize_lao(row.get("example_lao", "").strip()),
                        "example_vi": row.get("example_vi", "").strip(),
                    }

    def __len__(self) -> int:
        return len(self.entries)

    def contains(self, word: str) -> bool:
        """Kiểm tra từ có tồn tại trong từ điển hay không."""
        return normalize_lao(word) in self.entries

    def lookup(self, word: str) -> Optional[Dict[str, Any]]:
        """Tra cứu chi tiết một mục từ."""
        norm_word = normalize_lao(word)
        return self.entries.get(norm_word)

    def lookup_gloss(self, word: str, lang: str = "vi") -> str:
        """Lấy nghĩa ngắn gọn phục vụ chú giải từng từ."""
        entry = self.lookup(word)
        if entry:
            return entry.get(lang, "")
        return ""

    def search_partial(self, query: str, field: str = "lao") -> List[Dict[str, Any]]:
        """Tìm kiếm các từ chứa cụm từ truy vấn."""
        norm_q = normalize_lao(query).lower()
        results = []
        for entry in self.entries.values():
            val = entry.get(field, "").lower()
            if norm_q in val:
                results.append(entry)
        return results

    def get_all_words(self) -> List[str]:
        """Lấy danh sách tất cả các từ trong từ điển."""
        return list(self.entries.keys())
