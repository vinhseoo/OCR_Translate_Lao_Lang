"""
Script sinh và quản lý tập dữ liệu chuẩn vàng Gold Test Set (Phase P2a).
Bao gồm:
  1. 450 - 550 ảnh flashcard in đa thiết bị x điều kiện sáng x góc nghiêng
  2. 50 ảnh flashcard viết tay (Handwritten system boundary)
  3. 30 ảnh trang sách nhiều dòng (Textbook multi-line segmentation)
  4. Phân chia tập Dev (30%) / Test (70% đóng băng)
  5. 100% nhãn được chuẩn hóa NFC.
"""
import os
import sys
import csv
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.normalize import normalize_lao

GOLD_DIR = os.path.join(PROJECT_ROOT, "data", "gold")
IMAGES_DIR = os.path.join(GOLD_DIR, "images")
FONTS_DIR = os.path.join(PROJECT_ROOT, "data", "fonts")
DICT_PATH = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")

FONTS = [
    ("NotoSansLao", os.path.join(FONTS_DIR, "NotoSansLao.ttf")),
    ("NotoSerifLao", os.path.join(FONTS_DIR, "NotoSerifLao.ttf")),
    ("NotoSansLaoLooped", os.path.join(FONTS_DIR, "NotoSansLaoLooped.ttf")),
]

DEVICES = ["iPhone_14", "Samsung_Galaxy", "Xiaomi_Redmi"]
LIGHTING_CONDITIONS = ["natural", "fluorescent", "low_light", "cast_shadow"]
ANGLES = [0, -8, 8]


def apply_lighting_and_shadow(img: Image.Image, lighting: str) -> Image.Image:
    """Mô phỏng 4 điều kiện ánh sáng thực tế."""
    w, h = img.size
    np_img = np.array(img).astype(np.float32)
    
    if lighting == "natural":
        # Ánh sáng tự nhiên đồng đều, tương phản cao nhẹ
        factor = random.uniform(0.98, 1.05)
        np_img = np.clip(np_img * factor, 0, 255)
        
    elif lighting == "fluorescent":
        # Ánh sáng đèn tuýp huỳnh quang hơi ngả xanh lạnh nhẹ
        np_img[:, :, 0] *= 0.95  # R
        np_img[:, :, 1] *= 1.02  # G
        np_img[:, :, 2] *= 1.04  # B
        np_img = np.clip(np_img, 0, 255)
        
    elif lighting == "low_light":
        # Thiếu sáng, ảnh tối và có noise nhẹ
        dark_factor = random.uniform(0.55, 0.70)
        np_img = np_img * dark_factor
        noise = np.random.normal(0, 5, np_img.shape)
        np_img = np.clip(np_img + noise, 0, 255)
        
    elif lighting == "cast_shadow":
        # Bóng đổ tay hoặc điện thoại tạo gradient sáng tối ngang qua thẻ
        gradient = np.linspace(0.45, 1.05, w).reshape(1, w, 1)
        np_img = np.clip(np_img * gradient, 0, 255)
        
    res_img = Image.fromarray(np_img.astype(np.uint8))
    return res_img


def apply_device_and_angle(img: Image.Image, device: str, angle: int) -> Image.Image:
    """Mô phỏng góc nghiêng và đặc tính cảm biến camera điện thoại."""
    # 1. Xoay góc chụp (Perspective / Rotation)
    if angle != 0:
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(235, 235, 235))
        
    # 2. Đặc tính cảm biến thiết bị
    if device == "iPhone_14":
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
    elif device == "Samsung_Galaxy":
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)
    elif device == "Xiaomi_Redmi":
        # Nhiễu nén nhẹ hoặc blur rất nhẹ
        if random.random() > 0.5:
            img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
            
    return img


def render_flashcard(text: str, font_path: str, card_w: int = 640, card_h: int = 260) -> Image.Image:
    """Render thẻ flashcard cơ bản."""
    # Nền giấy ngà
    bg_r = random.randint(248, 255)
    bg_g = random.randint(246, 253)
    bg_b = random.randint(238, 248)
    
    img = Image.new("RGB", (card_w, card_h), color=(bg_r, bg_g, bg_b))
    draw = ImageDraw.Draw(img)
    
    # Khung viền thẻ
    draw.rectangle([12, 12, card_w - 12, card_h - 12], outline=(205, 205, 205), width=2)
    
    # Font và kích cỡ
    font_size = random.choice([54, 58, 62])
    font = ImageFont.truetype(font_path, font_size)
    
    # Căn giữa chữ
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (card_w - tw) // 2
    y = (card_h - th) // 2 - 4
    
    # Mực in chữ
    ink = (random.randint(15, 35), random.randint(15, 35), random.randint(15, 35))
    draw.text((x, y), text, font=font, fill=ink)
    
    return img


def generate_gold_dataset():
    random.seed(42)
    np.random.seed(42)
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 1. Đọc từ điển để lấy 150 từ vựng tiêu biểu
    vocab_list = []
    with open(DICT_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            vocab_list.append(r)
            
    # Lấy 150 từ vựng trải đều qua 12 bài
    step = len(vocab_list) // 150
    selected_vocab = [vocab_list[i * step] for i in range(150)]
    print(f"Đã chọn {len(selected_vocab)} từ vựng giáo trình cho Gold Test Set.")
    
    # 2. Sinh tập Flashcard Chữ In (480 ảnh: 150 từ x các tổ hợp)
    # Phân phối thiết bị, ánh sáng, góc để có 480 ảnh đa dạng
    gold_records = []
    card_id = 1
    
    for word_idx, entry in enumerate(selected_vocab):
        lao_word = normalize_lao(entry["lao"])
        # Mỗi từ sinh từ 3 - 4 biến thể điều kiện chụp
        num_variants = 3 if word_idx % 2 == 0 else 4
        
        for v in range(num_variants):
            font_name, font_path = FONTS[(word_idx + v) % len(FONTS)]
            device = DEVICES[(word_idx + v) % len(DEVICES)]
            lighting = LIGHTING_CONDITIONS[(v) % len(LIGHTING_CONDITIONS)]
            angle = ANGLES[(word_idx + v) % len(ANGLES)]
            
            # Render thẻ
            base_card = render_flashcard(lao_word, font_path)
            # Áp dụng ánh sáng và thiết bị
            lit_card = apply_lighting_and_shadow(base_card, lighting)
            final_card = apply_device_and_angle(lit_card, device, angle)
            
            filename = f"gold_card_{card_id:04d}.jpg"
            save_path = os.path.join(IMAGES_DIR, filename)
            final_card.save(save_path, quality=random.randint(88, 95))
            
            gold_records.append({
                "filename": filename,
                "lao_text": lao_word,
                "vi": entry["vi"],
                "en": entry["en"],
                "romanization": entry["romanization"],
                "pos": entry["pos"],
                "lesson": entry["lesson"],
                "font": font_name,
                "lighting": lighting,
                "device": device,
                "angle": angle,
                "type": "printed_flashcard"
            })
            card_id += 1
            
    print(f"✅ Đã sinh thành công {len(gold_records)} ảnh flashcard in.")
    
    # 3. Sinh 50 ảnh Flashcard Chữ Viết Tay (Handwritten boundary test)
    handwritten_records = []
    hand_font_name, hand_font_path = FONTS[0]  # Dùng NotoSans kết hợp jitter nét vẽ
    
    for h_idx in range(1, 51):
        entry = selected_vocab[h_idx % len(selected_vocab)]
        lao_word = normalize_lao(entry["lao"])
        
        # Mô phỏng nét viết tay: góc nghiêng ngẫu nhiên, độ mờ nhẹ, nét mảnh/dày tự nhiên
        base_card = render_flashcard(lao_word, hand_font_path, card_w=580, card_h=230)
        # Jitter và góc ngẫu nhiên
        rot_angle = random.randint(-6, 6)
        hw_card = base_card.rotate(rot_angle, resample=Image.BICUBIC, fillcolor=(245, 245, 245))
        hw_card = hw_card.filter(ImageFilter.SMOOTH_MORE)
        
        filename = f"handwritten_{h_idx:03d}.jpg"
        save_path = os.path.join(IMAGES_DIR, filename)
        hw_card.save(save_path, quality=85)
        
        handwritten_records.append({
            "filename": filename,
            "lao_text": lao_word,
            "vi": entry["vi"],
            "en": entry["en"],
            "romanization": entry["romanization"],
            "pos": entry["pos"],
            "lesson": entry["lesson"],
            "font": "simulated_handwritten",
            "lighting": "natural",
            "device": "Samsung_Galaxy",
            "angle": rot_angle,
            "type": "handwritten"
        })
        
    print(f"✅ Đã sinh thành công {len(handwritten_records)} ảnh flashcard viết tay.")
    
    # 4. Sinh 30 ảnh Trang Sách Nhiều Dòng (Multi-line textbook pages for P3)
    page_records = []
    page_font_name, page_font_path = FONTS[1]  # NotoSerifLao
    
    for p_idx in range(1, 31):
        pw, ph = 700, 950
        page_img = Image.new("RGB", (pw, ph), color=(252, 250, 245))
        draw = ImageDraw.Draw(page_img)
        p_font = ImageFont.truetype(page_font_path, 30)
        title_font = ImageFont.truetype(page_font_path, 38)
        
        # Tiêu đề bài
        draw.text((60, 50), f"ບົດຮຽນທີ {p_idx:02d} (Lesson {p_idx})", font=title_font, fill=(20, 20, 20))
        draw.line([(60, 105), (pw - 60, 105)], fill=(180, 180, 180), width=2)
        
        # Chọn 6-8 câu/dòng tiếng Lào
        lines_text = []
        cur_y = 135
        for line_no in range(8):
            v_item = vocab_list[(p_idx * 8 + line_no) % len(vocab_list)]
            ex_line = normalize_lao(v_item["example_lao"])
            if not ex_line:
                ex_line = normalize_lao(v_item["lao"])
            draw.text((70, cur_y), f"{line_no + 1}. {ex_line}", font=p_font, fill=(30, 30, 30))
            lines_text.append(ex_line)
            cur_y += 75
            
        filename = f"textbook_page_{p_idx:02d}.jpg"
        save_path = os.path.join(IMAGES_DIR, filename)
        page_img.save(save_path, quality=92)
        
        page_records.append({
            "filename": filename,
            "lao_text": " | ".join(lines_text),
            "vi": f"Trang giáo trình bài {p_idx}",
            "en": f"Textbook page lesson {p_idx}",
            "romanization": "",
            "pos": "multi_line",
            "lesson": f"Bài {p_idx}",
            "font": page_font_name,
            "lighting": "natural",
            "device": "scanner_simulated",
            "angle": 0,
            "type": "textbook_page"
        })
        
    print(f"✅ Đã sinh thành công {len(page_records)} ảnh trang sách nhiều dòng.")
    
    # 5. Phân chia Dev Set (30%) và Test Set (70% - Đóng Băng Tuyệt Đối)
    # Chỉ chia trên tập 480 flashcard in chính
    indices = list(range(len(gold_records)))
    random.shuffle(indices)
    
    split_idx = int(0.30 * len(gold_records))
    dev_indices = set(indices[:split_idx])
    
    dev_records = []
    test_records = []
    
    for i, rec in enumerate(gold_records):
        if i in dev_indices:
            rec["split"] = "dev"
            dev_records.append(rec)
        else:
            rec["split"] = "test"
            test_records.append(rec)
            
    print(f"\nPhân chia Gold Set: Dev Set = {len(dev_records)} ảnh (30.0%) | Test Set = {len(test_records)} ảnh (70.0%) [ĐÓNG BĂNG]")
    
    # 6. Ghi các file nhãn CSV chuẩn hóa NFC 100%
    fieldnames = [
        "filename", "lao_text", "vi", "en", "romanization", "pos", "lesson",
        "font", "lighting", "device", "angle", "type", "split"
    ]
    
    # Dev labels
    with open(os.path.join(GOLD_DIR, "dev_labels.csv"), mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dev_records)
        
    # Test labels (Frozen)
    with open(os.path.join(GOLD_DIR, "test_labels.csv"), mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_records)
        
    # Full master labels
    all_combined = gold_records + handwritten_records + page_records
    for r in handwritten_records:
        r["split"] = "handwritten_eval"
    for r in page_records:
        r["split"] = "page_eval"
        
    with open(os.path.join(GOLD_DIR, "all_labels.csv"), mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_combined)
        
    print(f"✅ Ghi thành công toàn bộ nhãn:")
    print(f"  • dev_labels.csv : {len(dev_records)} mẫu")
    print(f"  • test_labels.csv: {len(test_records)} mẫu (FROZEN)")
    print(f"  • all_labels.csv : {len(all_combined)} mẫu (Tổng cộng)")
    return len(dev_records), len(test_records), len(handwritten_records), len(page_records)


if __name__ == "__main__":
    generate_gold_dataset()
