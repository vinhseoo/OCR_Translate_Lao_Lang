"""
Tạo hình lưới 3x3 ảnh mẫu tập dữ liệu Gold Set (P2 Deliverable & Exit Gate).
Trực quan hóa sự đa dạng: ánh sáng, góc nghiêng, thiết bị, chữ viết tay và trang sách.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "gold", "images")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "experiments", "results", "dataset_sample_grid.png")


def create_3x3_grid():
    # 9 ảnh tiêu biểu đại diện cho các điều kiện khác nhau
    sample_files = [
        ("gold_card_0001.jpg", "Natural Light (iPhone)"),
        ("gold_card_0002.jpg", "Fluorescent (Samsung)"),
        ("gold_card_0003.jpg", "Low Light / Tilt (Redmi)"),
        ("gold_card_0004.jpg", "Cast Shadow Gradient"),
        ("gold_card_0015.jpg", "NotoSansLao Font (Front)"),
        ("gold_card_0025.jpg", "NotoSerifLao Font (Tilt)"),
        ("handwritten_001.jpg", "Handwritten Sample #01"),
        ("handwritten_002.jpg", "Handwritten Sample #02"),
        ("textbook_page_01.jpg", "Multi-line Page (Book)")
    ]
    
    cell_w, cell_h = 360, 200
    grid_img = Image.new("RGB", (cell_w * 3 + 40, cell_h * 3 + 80), color=(255, 255, 255))
    draw = ImageDraw.Draw(grid_img)
    font = ImageFont.load_default()
    
    draw.text((20, 15), "LAO OCR GOLD DATASET - 3x3 REPRESENTATIVE SAMPLE GRID (PHASE P2)", fill=(20, 20, 20), font=font)
    draw.text((20, 32), "Dimensions: 3 Devices x 4 Lighting Conditions x Angles x Handwritten x Multi-line Pages", fill=(100, 100, 100), font=font)
    
    for idx, (fname, label) in enumerate(sample_files):
        row = idx // 3
        col = idx % 3
        x = 20 + col * (cell_w + 10)
        y = 55 + row * (cell_h + 10)
        
        fpath = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(fpath):
            img = Image.open(fpath).convert("RGB")
            img = img.resize((cell_w, cell_h - 22), Image.Resampling.LANCZOS)
            grid_img.paste(img, (x, y))
            draw.rectangle([x, y, x + cell_w, y + cell_h - 22], outline=(180, 180, 180), width=1)
            draw.text((x + 5, y + cell_h - 18), f"[{idx+1}] {label}", fill=(40, 40, 40), font=font)
            
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    grid_img.save(OUTPUT_PATH, quality=95)
    print(f"✅ Đã tạo thành công hình lưới 3x3 ảnh mẫu tại: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_3x3_grid()
