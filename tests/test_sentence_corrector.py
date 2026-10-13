"""
Unit test kiểm thử module Hậu Xử Lý & Hiệu Chỉnh Câu Tiếng Lào (Sentence Corrector).
"""
import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.postprocessing.sentence_corrector import LaoSentenceCorrector
from src.preprocessing.normalize import normalize_lao


class TestSentenceCorrector(unittest.TestCase):
    def setUp(self):
        self.corrector = LaoSentenceCorrector()

    def test_tone_reordering(self):
        # Kiểm tra sửa lỗi dấu thanh lệch vị trí
        raw = "ຂອ້ຍ"
        norm = normalize_lao(raw)
        self.assertEqual(norm, "ຂ້ອຍ")

    def test_correct_phone_not_found(self):
        # Kiểm tra sửa chuỗi OCR lỗi về 'Tôi không tìm thấy điện thoại'
        raw = "ຂອ້ຍຊອກໂທລະສບັບໄຫນ້"
        corrected = self.corrector.correct_sentence(raw)
        self.assertEqual(corrected, "ຂ້ອຍຊອກໂທລະສັບບໍ່ເຫັນ")

    def test_correct_phone_beautiful(self):
        # Kiểm tra sửa chuỗi nhầm 'ວຽກຫຼາຍ' thành 'ງາມຫຼາຍ' trong ngữ cảnh điện thoại
        raw = "ໂທລະສັບນີ້\nວຽກຫຼາຍ"
        corrected = self.corrector.correct_sentence(raw)
        self.assertEqual(corrected, "ໂທລະສັບນີ້\nງາມຫຼາຍ")


if __name__ == "__main__":
    unittest.main()
