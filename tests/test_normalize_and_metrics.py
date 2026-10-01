"""
Unit tests cho P0: Kiểm tra chuẩn hóa Unicode NFC tiếng Lào và tính toán CER.
Cổng ra P0: cer(str1, str2) == 0 cho hai chuỗi cùng nội dung nhưng khác thứ tự dấu tổ hợp.
"""
import os
import sys
import unicodedata

# Cấu hình UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Thêm thư mục gốc của project vào sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao, is_lao_char
from src.evaluation.metrics import (
    compute_cer,
    compute_dataset_cer,
    compute_word_accuracy,
    bootstrap_cer_confidence_interval,
)


def test_is_lao_char():
    assert is_lao_char("ກ") is True
    assert is_lao_char("ລ") is True
    assert is_lao_char("A") is False
    assert is_lao_char("1") is False


def test_lao_combining_mark_canonicalization():
    """
    Trường hợp lỗi thực tế:
    - Ký tự 'ນ' (U+0E99)
    - Dấu thanh '້' (U+0EC9, Mai Tho)
    - Nguyên âm trên 'ໍາ' (hoặc 'ິ' U+0EB4)
    Nếu người gõ gõ: Phụ âm -> Dấu thanh -> Nguyên âm (sai trật tự)
    So với: Phụ âm -> Nguyên âm -> Dấu thanh (đúng trật tự chuẩn)
    Sau khi normalize, cả 2 phải bằng nhau và CER = 0!
    """
    # Đúng chuẩn: Phụ âm + Nguyên âm trên (ິ U+0EB4) + Dấu thanh (່ U+0EC8)
    standard_order = "\u0E81\u0EB4\u0EC8"  # ກ + ິ + ່
    # Gõ sai: Phụ âm + Dấu thanh (່ U+0EC8) + Nguyên âm trên (ິ U+0EB4)
    wrong_order = "\u0E81\u0EC8\u0EB4"     # ກ + ່ + ິ
    
    # Chưa normalize thì khác nhau
    assert standard_order != wrong_order
    
    # Sau normalize phải bằng nhau
    norm_std = normalize_lao(standard_order)
    norm_wrg = normalize_lao(wrong_order)
    assert norm_std == norm_wrg
    
    # CER phải trả về 0.0
    cer = compute_cer(standard_order, wrong_order)
    assert cer == 0.0, f"CER mong đợi 0.0 nhưng nhận được {cer}"


def test_nfd_to_nfc_normalization():
    """Kiểm tra chuỗi NFD được đưa về NFC và CER = 0."""
    lao_word = "ສະບາຍດີ"  # Sabaidee
    lao_nfd = unicodedata.normalize("NFD", lao_word)
    
    assert compute_cer(lao_word, lao_nfd) == 0.0
    assert compute_word_accuracy([lao_word], [lao_nfd]) == 1.0


def test_bootstrap_ci():
    """Kiểm tra hàm tính bootstrap CI."""
    refs = ["ສະບາຍດີ", "ຂອບໃຈ", "ພາສາລາວ", "ໂຮງຮຽນ"]
    hyps = ["ສະບາຍດີ", "ຂອບໃຈ", "ພາສາລາວ", "ໂຮງຮຽນ"]
    mean_val, lower, upper = bootstrap_cer_confidence_interval(refs, hyps, n_resamples=100)
    assert mean_val == 0.0
    assert lower == 0.0
    assert upper == 0.0


if __name__ == "__main__":
    test_is_lao_char()
    test_lao_combining_mark_canonicalization()
    test_nfd_to_nfc_normalization()
    test_bootstrap_ci()
    print("✅ MỌI BÀI TEST P0 ĐÃ ĐẠT 100%! CỔNG RA P0 CHUẨN XÁC.")
