"""
Unit test kiểm định tính toàn vẹn của Dữ liệu Phase P2 (Data Integrity & Exit Gate Validation).
Kiểm tra:
  1. Từ điển >= 500 mục, không rỗng, 100% Unicode NFC.
  2. Toàn bộ ảnh trong dev_labels.csv và test_labels.csv có tồn tại trên đĩa.
  3. Không có ký tự rác hoặc trật tự dấu tổ hợp sai.
"""
import os
import sys
import csv
import unicodedata

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.preprocessing.normalize import normalize_lao

DICT_PATH = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
DEV_PATH = os.path.join(PROJECT_ROOT, "data", "gold", "dev_labels.csv")
TEST_PATH = os.path.join(PROJECT_ROOT, "data", "gold", "test_labels.csv")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "gold", "images")


def test_dictionary_integrity():
    assert os.path.exists(DICT_PATH), f"Không tìm thấy {DICT_PATH}"
    count = 0
    with open(DICT_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count += 1
            lao_text = row["lao"]
            assert len(lao_text) > 0, f"Dòng {count} có từ rỗng!"
            # Kiểm tra chuẩn hóa NFC
            assert lao_text == unicodedata.normalize("NFC", lao_text), f"Từ '{lao_text}' chưa chuẩn NFC!"
            assert lao_text == normalize_lao(lao_text), f"Từ '{lao_text}' chưa chuẩn combining marks!"
            
    assert count >= 500, f"Từ điển chỉ có {count} từ (< 500)!"
    print(f"✅ Kiểm định Từ điển: {count} entries ĐẠT 100% chuẩn NFC và toàn vẹn.")


def test_gold_dataset_integrity():
    for label_path, name in [(DEV_PATH, "Dev Set"), (TEST_PATH, "Test Set")]:
        assert os.path.exists(label_path), f"Không tìm thấy {label_path}"
        count = 0
        with open(label_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                count += 1
                img_name = row["filename"]
                img_path = os.path.join(IMAGES_DIR, img_name)
                assert os.path.exists(img_path), f"Ảnh {img_name} không tồn tại trên đĩa!"
                
                lao_text = row["lao_text"]
                assert len(lao_text) > 0, f"Nhãn rỗng tại {img_name}"
                assert lao_text == normalize_lao(lao_text), f"Nhãn {lao_text} chưa chuẩn hóa!"
                
        print(f"✅ Kiểm định {name}: {count} ảnh tồn tại đầy đủ và nhãn sạch 100%.")


if __name__ == "__main__":
    test_dictionary_integrity()
    test_gold_dataset_integrity()
    print("\n🎉 MỌI BÀI TEST TÍNH TOÀN VẸN DỮ LIỆU PHASE P2 ĐẠT XUẤT SẮC!")
