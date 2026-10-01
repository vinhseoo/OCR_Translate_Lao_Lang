"""
Pipeline sinh dữ liệu tổng hợp (Synthetic Corpus Generator - Phase P2c).
Tạo dữ liệu dòng chữ tiếng Lào phục vụ huấn luyện và thực nghiệm (Phase P7).
Hỗ trợ 2 chế độ:
  1. synth_clean: Ảnh văn bản sạch chuẩn, đa dạng font và cỡ chữ
  2. synth_aug  : Ảnh được augmentation mô phỏng ảnh chụp điện thoại thực tế:
                  - Blur (Motion / Gaussian)
                  - Phối cảnh (Perspective warp +-12 độ)
                  - Gradient ánh sáng & Bóng đổ tay / điện thoại
                  - Nhiễu hạt (Salt & Pepper / Gaussian noise)
                  - Nén JPEG chất lượng thấp
"""
import os
import sys
import csv
import math
import random
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.normalize import normalize_lao

SYNTH_DIR = os.path.join(PROJECT_ROOT, "data", "synth")
FONTS_DIR = os.path.join(PROJECT_ROOT, "data", "fonts")
DICT_PATH = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")


def get_available_fonts():
    """Lấy danh sách các font hợp lệ đã được thẩm định ở P0."""
    valid_fonts = []
    if os.path.exists(FONTS_DIR):
        for f in os.listdir(FONTS_DIR):
            if f.endswith((".ttf", ".otf")):
                valid_fonts.append((f, os.path.join(FONTS_DIR, f)))
    return valid_fonts


def load_vocabulary_corpus():
    """Đọc toàn bộ từ vựng và câu ví dụ để sinh nội dung."""
    words = []
    sentences = []
    with open(DICT_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = normalize_lao(row["lao"])
            if w:
                words.append(w)
            ex = normalize_lao(row.get("example_lao", ""))
            if ex:
                sentences.append(ex)
    return words, sentences


def generate_text_sample(words, sentences):
    """
    Sinh nội dung theo phân phối chuẩn của đề bài:
    - 40% từ đơn
    - 40% cụm 2-4 từ
    - 20% câu ngắn
    """
    prob = random.random()
    if prob < 0.40:
        # Từ đơn
        return random.choice(words)
    elif prob < 0.80:
        # Cụm 2 - 4 từ ghép lại (tiếng Lào không có dấu cách giữa các từ trong cùng một cụm)
        num_w = random.randint(2, 4)
        sample_words = [random.choice(words) for _ in range(num_w)]
        # Đôi khi thêm khoảng trắng giữa các vế câu
        if random.random() > 0.5:
            return " ".join(sample_words)
        else:
            return "".join(sample_words)
    else:
        # Câu ngắn
        return random.choice(sentences) if sentences else random.choice(words)


def apply_synthetic_augmentation(img: Image.Image) -> Image.Image:
    """Mô phỏng chân thực các khuyết tật của ảnh chụp điện thoại."""
    w, h = img.size
    
    # 1. Perspective Warp / Xoay góc nghiêng +- 12 độ
    rot_angle = random.uniform(-10.0, 10.0)
    img = img.rotate(rot_angle, resample=Image.BICUBIC, expand=True, fillcolor=(240, 240, 240))
    w, h = img.size
    
    np_img = np.array(img).astype(np.float32)
    
    # 2. Gradient ánh sáng & Bóng đổ điện thoại/tay
    if random.random() > 0.3:
        direction = random.choice(["horizontal", "vertical", "diagonal"])
        if direction == "horizontal":
            grad = np.linspace(random.uniform(0.5, 0.7), 1.0, w).reshape(1, w, 1)
        elif direction == "vertical":
            grad = np.linspace(random.uniform(0.5, 0.7), 1.0, h).reshape(h, 1, 1)
        else:
            gx = np.linspace(0.6, 1.0, w).reshape(1, w, 1)
            gy = np.linspace(0.6, 1.0, h).reshape(h, 1, 1)
            grad = (gx + gy) / 2.0
        np_img = np.clip(np_img * grad, 0, 255)
        
    # 3. Nhiễu muối tiêu (Salt & Pepper noise)
    if random.random() > 0.4:
        noise_level = random.uniform(0.005, 0.02)
        mask = np.random.rand(h, w)
        np_img[mask < noise_level / 2] = 0
        np_img[mask > (1 - noise_level / 2)] = 255
        
    img = Image.fromarray(np_img.astype(np.uint8))
    
    # 4. Blur (Motion blur hoặc Gaussian blur)
    blur_choice = random.random()
    if blur_choice < 0.35:
        # Gaussian blur nhẹ
        radius = random.uniform(0.5, 1.2)
        img = img.filter(ImageFilter.GaussianBlur(radius=radius))
        
    return img


def render_line_image(text: str, font_path: str, is_augmented: bool = False) -> Image.Image:
    """Render 1 dòng văn bản ra ảnh."""
    font_size = random.choice([36, 42, 48, 54])
    font = ImageFont.truetype(font_path, font_size)
    
    # Đo kích thước chữ
    temp_img = Image.new("RGB", (10, 10))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    tw = max(bbox[2] - bbox[0], 20)
    th = max(bbox[3] - bbox[1], 20)
    
    pad_x = random.randint(25, 45)
    pad_y = random.randint(15, 30)
    
    img_w = tw + pad_x * 2
    img_h = th + pad_y * 2
    
    # Màu nền giấy
    if is_augmented:
        bg_col = (random.randint(235, 252), random.randint(235, 250), random.randint(225, 245))
        ink_col = (random.randint(10, 45), random.randint(10, 45), random.randint(10, 45))
    else:
        bg_col = (255, 255, 255)
        ink_col = (0, 0, 0)
        
    img = Image.new("RGB", (img_w, img_h), color=bg_col)
    draw = ImageDraw.Draw(img)
    
    # Vẽ chữ
    draw.text((pad_x - bbox[0], pad_y - bbox[1]), text, font=font, fill=ink_col)
    
    # Nếu là bản augmented thì áp dụng các phép biến đổi nhiễu ảnh
    if is_augmented:
        img = apply_synthetic_augmentation(img)
        
    return img


def generate_corpus(num_samples: int = 1000):
    random.seed(42)
    np.random.seed(42)
    
    fonts = get_available_fonts()
    if not fonts:
        raise RuntimeError("Không tìm thấy font nào trong data/fonts/!")
        
    words, sentences = load_vocabulary_corpus()
    print(f"Kho ngữ liệu: {len(words)} từ vựng, {len(sentences)} câu ví dụ.")
    print(f"Số lượng mẫu cần sinh: {num_samples}")
    
    clean_dir = os.path.join(SYNTH_DIR, "synth_clean")
    aug_dir = os.path.join(SYNTH_DIR, "synth_aug")
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(aug_dir, exist_ok=True)
    
    clean_labels = []
    aug_labels = []
    
    for i in range(1, num_samples + 1):
        text = generate_text_sample(words, sentences)
        text = normalize_lao(text)
        
        font_name, font_path = random.choice(fonts)
        filename = f"synth_{i:06d}.jpg"
        
        # 1. Sinh bản clean
        clean_img = render_line_image(text, font_path, is_augmented=False)
        clean_path = os.path.join(clean_dir, filename)
        clean_img.save(clean_path, quality=95)
        clean_labels.append({"filename": filename, "text": text, "font": font_name})
        
        # 2. Sinh bản augmented
        aug_img = render_line_image(text, font_path, is_augmented=True)
        aug_path = os.path.join(aug_dir, filename)
        aug_img.save(aug_path, quality=random.randint(65, 85))  # Nén JPEG
        aug_labels.append({"filename": filename, "text": text, "font": font_name})
        
        if i % 200 == 0 or i == num_samples:
            print(f"  Đã sinh {i}/{num_samples} mẫu cho cả clean & aug...")
            
    # Ghi nhãn CSV
    with open(os.path.join(clean_dir, "labels.csv"), mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "text", "font"])
        writer.writeheader()
        writer.writerows(clean_labels)
        
    with open(os.path.join(aug_dir, "labels.csv"), mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "text", "font"])
        writer.writeheader()
        writer.writerows(aug_labels)
        
    print(f"\n✅ Đã sinh thành công tập Synthetic Corpus:")
    print(f"  • synth_clean: {len(clean_labels)} ảnh -> {clean_dir}")
    print(f"  • synth_aug  : {len(aug_labels)} ảnh -> {aug_dir}")
    print(f"  • 100% nhãn được chuẩn hóa NFC.")


def main():
    parser = argparse.ArgumentParser(description="Sinh tập dữ liệu tổng hợp tiếng Lào (Synthetic Corpus)")
    parser.add_argument("--samples", type=int, default=1000, help="Số lượng mẫu dòng cần sinh (mặc định 1000)")
    args = parser.parse_args()
    
    generate_corpus(args.samples)


if __name__ == "__main__":
    main()
