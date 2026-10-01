"""
Module Phiên Âm Chữ Latinh Tiếng Lào (Lao Romanization / Phonetics Converter).
Hỗ trợ chuyển đổi văn bản chữ Lào sang hệ chữ Latinh phiên âm (như 'sa-baai-dee', 'khop-chai')
nhằm hỗ trợ học viên quốc tế học cách phát âm chính xác.
Kết hợp giữa:
1. Tra cứu trực tiếp từ điển giáo trình (ưu tiên cao nhất, độ chuẩn xác 100%).
2. Hệ thống quy tắc phiên âm ngữ âm cho từ vựng mới / OOV.
"""
import os
import sys
import csv
from typing import Dict, Optional, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao

# Bảng phiên âm phụ âm đầu (Initial Consonants)
INITIAL_CONSONANTS: Dict[str, str] = {
    "ກ": "k", "ຂ": "kh", "ຄ": "kh", "ງ": "ng",
    "ຈ": "ch", "ສ": "s", "ຊ": "x", "ຍ": "ny",
    "ດ": "d", "ຕ": "t", "ຖ": "th", "ທ": "th",
    "ນ": "n", "ບ": "b", "ປ": "p", "ຜ": "ph",
    "ຝ": "f", "ພ": "ph", "ຟ": "f", "ມ": "m",
    "ຢ": "y", "ຣ": "r", "ລ": "l", "ວ": "v",
    "ຫ": "h", "ອ": "o", "ຮ": "h", "ໜ": "n", "ໝ": "m"
}

# Bảng phiên âm nguyên âm và tổ hợp nguyên âm (Vowels)
VOWEL_PATTERNS: Dict[str, str] = {
    "ະ": "a", "າ": "aa", "ຳ": "am",
    "ິ": "i", "ີ": "ee", "ຶ": "ue", "ື": "uee",
    "ຸ": "u", "ູ": "uu", "ົ": "o", "ຼ": "l",
    "ຽ": "ia", "ເ": "e", "ແ": "ae", "ໂ": "oo",
    "ໃ": "ai", "ໄ": "ai"
}


class LaoRomanizer:
    def __init__(self, dict_path: Optional[str] = None):
        """Khởi tạo Romanizer với bộ nhớ đệm từ điển phiên âm."""
        self.dict_cache: Dict[str, str] = {}
        default_dict = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
        path_to_load = dict_path or default_dict
        self._load_cache(path_to_load)

    def _load_cache(self, dict_path: str):
        if not os.path.exists(dict_path):
            return
            
        with open(dict_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lao_word = normalize_lao(row.get("lao", "").strip())
                rom = row.get("romanization", "").strip()
                if lao_word and rom:
                    self.dict_cache[lao_word] = rom

    def romanize_token(self, token: str) -> str:
        """Phiên âm một từ đơn lẻ (kiểm tra từ điển trước, fallback sang quy tắc)."""
        norm_tok = normalize_lao(token)
        if not norm_tok:
            return ""
            
        if norm_tok in self.dict_cache:
            return self.dict_cache[norm_tok]
            
        # Fallback phiên âm theo quy tắc ký tự
        rom_parts = []
        for char in norm_tok:
            if char in INITIAL_CONSONANTS:
                rom_parts.append(INITIAL_CONSONANTS[char])
            elif char in VOWEL_PATTERNS:
                rom_parts.append(VOWEL_PATTERNS[char])
            elif char in "່້໊໋໌ໍ":
                # Bỏ qua dấu thanh trong phiên âm Latinh cơ bản
                continue
            elif char.isspace() or char in "-_":
                rom_parts.append(" ")
            else:
                rom_parts.append(char)
                
        result = "".join(rom_parts).strip()
        return result or norm_tok

    def romanize(self, tokens: List[str]) -> str:
        """
        Phiên âm toàn bộ danh sách các từ trong câu.
        Nối các từ bằng dấu gạch ngang hoặc dấu cách ngữ âm.
        """
        if not tokens:
            return ""
            
        rom_list = [self.romanize_token(tok) for tok in tokens if tok.strip()]
        return " ".join(rom_list)
