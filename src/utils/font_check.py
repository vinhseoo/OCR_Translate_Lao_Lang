"""
Script kiểm tra khả năng render font tiếng Lào (P0 font validation).
Render tổ hợp: Phụ âm (Consonant) x Nguyên âm tổ hợp (Vowel) x Dấu thanh (Tone)
nhằm phát hiện sớm các font bị lỗi trôi dấu, đè dấu hoặc mất nét.
"""
import os
import sys
from typing import List, Tuple

# Cấu hình UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Bảng 27 phụ âm chính của tiếng Lào
LAO_CONSONANTS = [
    "ກ", "ຂ", "ຄ", "ງ", "ຈ", "ສ", "ຊ", "ຍ",
    "ດ", "ຕ", "ຖ", "ທ", "ນ", "ບ", "ປ", "ຜ",
    "ຝ", "ພ", "ຟ", "ມ", "ຢ", "ຣ", "ລ", "ວ",
    "ຫ", "ອ", "ຮ"
]

# Các nguyên âm tổ hợp trên và dưới (tầng 2 & tầng 4)
LAO_COMBINING_VOWELS = [
    "",    # Không có nguyên âm đi kèm
    "ັ",   # U+0EB1
    "ິ",   # U+0EB4
    "ີ",   # U+0EB5
    "ຶ",   # U+0EB6
    "ື",   # U+0EB7
    "ຸ",   # U+0EB8 (dưới)
    "ູ",   # U+0EB9 (dưới)
    "ໍ"    # U+0ECD
]

# Các dấu thanh (tầng 1)
LAO_TONE_MARKS = [
    "",    # Không dấu thanh
    "່",   # U+0EC8 (Mai Ek)
    "້",   # U+0EC9 (Mai Tho)
    "໊",   # U+0ECA (Mai Ti)
    "໋"    # U+0ECB (Mai Chattawa)
]


def generate_lao_combinations() -> List[str]:
    """Sinh ra ~400 tổ hợp phụ âm x nguyên âm x dấu thanh chuẩn."""
    combinations = []
    for c in LAO_CONSONANTS:
        for v in LAO_COMBINING_VOWELS:
            for t in LAO_TONE_MARKS:
                # Trật tự chuẩn: Phụ âm -> Nguyên âm -> Dấu thanh
                combo = f"{c}{v}{t}"
                combinations.append(combo)
    return combinations


def main():
    combos = generate_lao_combinations()
    print(f"Tổng số tổ hợp tiếng Lào được sinh: {len(combos)}")
    print("Mẫu 10 tổ hợp đầu tiên:")
    for i, c in enumerate(combos[:10]):
        print(f"  [{i+1}] '{c}' (Hex: {' '.join(hex(ord(ch)) for ch in c)})")
        
    print("\n[Hướng dẫn kiểm tra Font]:")
    print("1. Đặt các file font (.ttf, .otf) tiếng Lào vào thư mục `data/fonts/`.")
    print("2. Dùng Pillow + ImageFont để render lưới các tổ hợp này ra ảnh PNG.")
    print("3. Soi trực quan: Font nào bị dấu đè lên chữ hoặc dấu thanh bị lệch -> Cho vào Blacklist.")


if __name__ == "__main__":
    main()
