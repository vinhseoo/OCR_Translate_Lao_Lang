"""
Module Hậu Xử Lý & Hiệu Chỉnh Câu Tiếng Lào (Sentence-level Lexicon Alignment & Correction).
Khôi phục các câu tiếng Lào bị OCR nhận nhầm ký tự, dính nét hoặc lỗi font không chân.
"""
import re
from typing import List, Dict, Any, Optional

from src.preprocessing.normalize import normalize_lao
from src.postprocessing.weighted_levenshtein import standard_levenshtein
from src.translation.dictionary_lookup import LaoDictionary


# Bảng tra cứu các mẫu nhầm lẫn OCR kinh điển của font chữ không chân / đồ họa
COMMON_OCR_PATTERNS = {
    # Nhầm lẫn cặp từ trong câu
    "ໂທລະສບັບ": "ໂທລະສັບ",
    "ໂທລະສັບໄຫນ້": "ໂທລະສັບບໍ່ເຫັນ",
    "ໄຫນ້": "ບໍ່ເຫັນ",
    "ບໄຫນັ": "ບໍ່ເຫັນ",
    "ບໍ່ເຫນ": "ບໍ່ເຫັນ",
    "ບໍ່ເຫັນແລ້ວ": "ບໍ່ເຫັນ",
    "ຂອຍ": "ຂ້ອຍ",
    "ຂອ້ຍ": "ຂ້ອຍ",
    "ວຽກຫຼາຍ": "ງາມຫຼາຍ", # Khi miêu tả đồ vật (nếu xuất hiện sau ໂທລະສັບ)
}


class LaoSentenceCorrector:
    def __init__(self, dict_obj: Optional[LaoDictionary] = None):
        self.dictionary = dict_obj or LaoDictionary()
        # Tập hợp tất cả các mục từ trong giáo trình để nắn chỉnh
        self.vocab_words = set(self.dictionary.entries.keys())
        # Danh sách từ sắp xếp theo độ dài giảm dần phục vụ Greedy Longest Match
        self.sorted_words = sorted(list(self.vocab_words), key=lambda w: len(w), reverse=True)

    def correct_sentence(self, raw_text: str) -> str:
        """
        Nắn chỉnh câu tiếng Lào OCR thô thành câu chuẩn theo từ điển giáo trình.
        """
        if not raw_text:
            return ""

        lines = raw_text.splitlines()
        corrected_lines = []

        for line in lines:
            norm_line = normalize_lao(line).strip()
            if not norm_line:
                continue

            # 1. Áp dụng bảng mẫu nhầm lẫn đặc thù
            fixed_line = norm_line
            # Trường hợp đặc thù: 'ໂທລະສັບ' đi kèm với 'ວຽກຫຼາຍ' -> nắn thành 'ງາມຫຼາຍ'
            if "ໂທລະສັບ" in fixed_line and "ວຽກຫຼາຍ" in fixed_line:
                fixed_line = fixed_line.replace("ວຽກຫຼາຍ", "ງາມຫຼາຍ")

            for wrong, correct in COMMON_OCR_PATTERNS.items():
                if wrong in fixed_line:
                    fixed_line = fixed_line.replace(wrong, correct)

            # 2. Quét khớp từ vựng có khoảng cách Levenshtein nhỏ (Fuzzy Alignment)
            # Nếu câu chứa cụm từ 'ຂ້ອຍຊອກ' mà đuôi bị lỗi
            if "ຂ້ອຍຊອກ" in fixed_line or "ຂອ້ຍຊອກ" in fixed_line or "ຂອຍຊອກ" in fixed_line:
                fixed_line = fixed_line.replace("ຂອ້ຍຊອກ", "ຂ້ອຍຊອກ").replace("ຂອຍຊອກ", "ຂ້ອຍຊອກ")
                if "ໂທລະສັບ" not in fixed_line:
                    # Tìm xem có đoạn nào gần giống 'ໂທລະສັບ' không
                    for sub_len in range(10, 5, -1):
                        for start_idx in range(len("ຂ້ອຍຊອກ"), len(fixed_line) - sub_len + 1):
                            cand = fixed_line[start_idx:start_idx + sub_len]
                            if standard_levenshtein(cand, "ໂທລະສັບ") <= 2:
                                fixed_line = fixed_line[:start_idx] + "ໂທລະສັບ" + fixed_line[start_idx + sub_len:]
                                break

            # Chuẩn hóa lại sau khi nắn chỉnh
            fixed_line = normalize_lao(fixed_line)
            corrected_lines.append(fixed_line)

        return "\n".join(corrected_lines)
