"""
Sinh 20 ảnh flashcard mẫu cho Phase P1 (Spike End-to-End).
Sử dụng các font tiếng Lào đã được kiểm định ở P0 và từ vựng từ mini_dict.csv.
"""
import os
import sys
import csv
import random
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Thư mục đích
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "samples", "p1_spike")
DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dictionaries", "mini_dict.csv")
FONTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "fonts")

FONTS = [
    os.path.join(FONTS_DIR, "NotoSansLao.ttf"),
    os.path.join(FONTS_DIR, "NotoSerifLao.ttf"),
    os.path.join(FONTS_DIR, "NotoSansLaoLooped.ttf")
]


def create_flashcard_image(text: str, font_path: str, output_path: str, card_idx: int):
    """Tạo 1 ảnh flashcard mô phỏng thực tế."""
    w, h = 600, 240
    # Màu nền mô phỏng giấy thẻ (trắng ngà nhẹ hoặc xám nhẹ)
    bg_color = (
        random.randint(245, 255),
        random.randint(245, 255),
        random.randint(240, 250)
    )
    img = Image.new("RGB", (w, h), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Viền thẻ flashcard
    draw.rectangle([10, 10, w - 10, h - 10], outline=(210, 210, 210), width=2)
    
    # Render chữ tiếng Lào
    font_size = random.choice([56, 62, 68])
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()
        
    # Tính tọa độ căn giữa
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (w - text_w) // 2
    y = (h - text_h) // 2 - 5
    
    # Màu mực chữ (đen tuyền hoặc xám đậm)
    ink_color = (random.randint(10, 30), random.randint(10, 30), random.randint(10, 30))
    draw.text((x, y), text, font=font, fill=ink_color)
    
    img.save(output_path, quality=95)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Đọc 20 từ đầu tiên trong từ điển
    entries = []
    with open(DICT_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 20:
                break
            entries.append(row)
            
    print(f"Đọc được {len(entries)} từ vựng từ {DICT_PATH}")
    
    labels_file = os.path.join(OUTPUT_DIR, "p1_labels.csv")
    with open(labels_file, mode="w", encoding="utf-8", newline="") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(["filename", "lao_text", "vi", "en", "romanization", "font"])
        
        for idx, row in enumerate(entries, start=1):
            font_path = FONTS[(idx - 1) % len(FONTS)]
            font_name = os.path.basename(font_path)
            img_filename = f"card_{idx:02d}.jpg"
            img_path = os.path.join(OUTPUT_DIR, img_filename)
            
            create_flashcard_image(row["lao"], font_path, img_path, idx)
            writer.writerow([img_filename, row["lao"], row["vi"], row["en"], row["romanization"], font_name])
            print(f"  [{idx:02d}/20] Tạo {img_filename} - '{row['lao']}' ({font_name})")
            
    print(f"\n✅ Đã sinh thành công 20 ảnh flashcard tại: {OUTPUT_DIR}")
    print(f"✅ File nhãn ground truth: {labels_file}")


if __name__ == "__main__":
    main()
