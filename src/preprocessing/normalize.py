"""
Module chuẩn hóa chuỗi tiếng Lào (Unicode NFC + Combining Mark Canonicalization).
Tuân thủ tuyệt đối quy chuẩn trong AGENTS.md.
"""
import re
import unicodedata
from typing import Set

# Bảng mã Unicode tiếng Lào (U+0E80 - U+0EFF)
LAO_UNICODE_RANGE = (0x0E80, 0x0EFF)

# Các nhóm ký tự tiếng Lào
LAO_LEADING_VOWELS = {"ເ", "ແ", "ໂ", "ໃ", "ໄ"}  # U+0EC0 - U+0EC4
LAO_ABOVE_VOWELS = {"ັ", "ິ", "ີ", "ຶ", "ື", "ໍ"}  # U+0EB1, U+0EB4 - U+0EB7, U+0ECD
LAO_BELOW_VOWELS = {"ຸ", "ູ"}  # U+0EB8, U+0EB9
LAO_TONE_MARKS = {"່", "້", "໊", "໋"}  # U+0EC8 - U+0ECB
LAO_CANCELLATION_MARK = {"໌"}  # U+0ECC
LAO_SUB_CONSONANTS = {"ຼ"}  # U+0EBC

ALL_COMBINING_VOWELS = LAO_ABOVE_VOWELS.union(LAO_BELOW_VOWELS)
ALL_TONES_AND_SIGNS = LAO_TONE_MARKS.union(LAO_CANCELLATION_MARK)


def is_lao_char(ch: str) -> bool:
    """Kiểm tra ký tự có thuộc khối Unicode tiếng Lào hay không."""
    if not ch:
        return False
    code = ord(ch)
    return LAO_UNICODE_RANGE[0] <= code <= LAO_UNICODE_RANGE[1]


def reorder_lao_combining_marks(text: str) -> str:
    """
    Sắp xếp lại thứ tự các dấu tổ hợp trên cùng một ký tự gốc.
    Quy tắc chuẩn:
      Phụ âm gốc (+ phụ âm phụ) -> Nguyên âm tổ hợp (trên/dưới) -> Dấu thanh / Dấu hủy.
    Xử lý lỗi gõ ngược: Dấu thanh đứng trước nguyên âm trên/dưới.
    """
    chars = list(text)
    n = len(chars)
    i = 0
    result = []
    
    while i < n:
        ch = chars[i]
        result.append(ch)
        
        # Nếu gặp dấu thanh, kiểm tra xem ký tự ngay sau có phải là nguyên âm tổ hợp bị gõ ngược không
        if ch in ALL_TONES_AND_SIGNS and i + 1 < n:
            next_ch = chars[i + 1]
            if next_ch in ALL_COMBINING_VOWELS:
                # Đổi chỗ: nguyên âm đứng trước, dấu thanh đứng sau
                result.pop()  # bỏ dấu thanh vừa thêm
                result.append(next_ch)  # thêm nguyên âm
                result.append(ch)  # thêm lại dấu thanh
                i += 2
                continue
        i += 1
        
    return "".join(result)


def normalize_lao(text: str) -> str:
    """
    Chuẩn hóa toàn diện chuỗi văn bản tiếng Lào:
    1. Loại bỏ ký tự rác, khoảng trắng thừa, Zero-Width Space (U+200B).
    2. Chuẩn hóa dạng Unicode NFC.
    3. Sửa trật tự các dấu tổ hợp (Combining marks) bị gõ lộn xộn.
    4. Ép lại NFC lần cuối đảm bảo byte đồng nhất.
    """
    if not text:
        return ""
    
    # 1. Loại bỏ khoảng trắng thừa ở 2 đầu và zero-width space
    text = text.replace("\u200b", "").replace("\ufeff", "").strip()
    
    # 2. Chuẩn hóa NFC lần 1
    text = unicodedata.normalize("NFC", text)
    
    # 3. Chuẩn hóa trật tự dấu tổ hợp
    text = reorder_lao_combining_marks(text)
    
    # 4. Ép NFC lần 2 để đảm bảo canonical representation
    text = unicodedata.normalize("NFC", text)
    
    return text
