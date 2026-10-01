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


def render_font_validation_grid(font_path: str, output_image_path: str, grid_cols: int = 15):
    """
    Render lưới các tổ hợp phụ âm x nguyên âm x dấu thanh ra ảnh PNG
    để người nghiên cứu soi trực quan phát hiện lỗi dấu (font validation).
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[LƯU Ý] Pillow chưa được cài đặt. Không thể render ảnh lưới.")
        return False

    if not os.path.exists(font_path):
        print(f"[LỖI] Không tìm thấy file font: {font_path}")
        return False

    combos = generate_lao_combinations()
    font_size = 28
    cell_w, cell_h = 75, 75
    
    n_items = len(combos)
    grid_rows = (n_items + grid_cols - 1) // grid_cols
    
    img_w = grid_cols * cell_w + 40
    img_h = grid_rows * cell_h + 100
    
    img = Image.new("RGB", (img_w, img_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(font_path, font_size)
    header_font = ImageFont.load_default()
    
    font_name = os.path.basename(font_path)
    draw.text((20, 15), f"Lao Font Validation Grid - {font_name} (Total: {n_items} combinations)", fill=(0, 0, 0))
    draw.text((20, 45), "Quy chuẩn: Phụ âm + Nguyên âm trên/dưới + Dấu thanh. Kiểm tra dấu thanh có bị lệch/đè chữ hay không.", fill=(80, 80, 80))
    
    for idx, combo in enumerate(combos):
        row = idx // grid_cols
        col = idx % grid_cols
        x = 20 + col * cell_w
        y = 80 + row * cell_h
        
        # Vẽ ô lưới
        draw.rectangle([x, y, x + cell_w - 4, y + cell_h - 4], outline=(220, 220, 220), width=1)
        # Vẽ chữ tiếng Lào
        draw.text((x + 12, y + 16), combo, font=font, fill=(0, 0, 0))
        
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    img.save(output_image_path)
    print(f"✅ Đã render thành công lưới kiểm tra font ({n_items} ô) -> {output_image_path}")
    return True


def main():
    combos = generate_lao_combinations()
    print(f"Tổng số tổ hợp tiếng Lào được sinh: {len(combos)}")
    
    # Kiểm tra các font trong thư mục data/fonts/
    fonts_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fonts")
    if os.path.exists(fonts_dir):
        font_files = [f for f in os.listdir(fonts_dir) if f.endswith((".ttf", ".otf"))]
        print(f"Tìm thấy {len(font_files)} fonts trong {fonts_dir}: {font_files}")
        for font_file in font_files:
            font_path = os.path.join(fonts_dir, font_file)
            out_img = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "results", f"grid_{font_file}.png")
            render_font_validation_grid(font_path, out_img)
    else:
        print(f"Chưa có thư mục {fonts_dir}.")


if __name__ == "__main__":
    main()

