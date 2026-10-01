"""
Unit Tests cho Phase P8: Tầng Ngôn Ngữ & Hỗ Trợ Dịch (Lao NLP & Educational Translation).
Kiểm tra:
1. LaoTokenizer: Cây Trie phân đoạn từ, Longest Matching, xử lý OOV.
2. Tokenization F1 Metric: Precision, Recall, F1 biên giới từ.
3. LaoRomanizer: Phiên âm Latinh qua từ điển và quy tắc ngữ âm.
4. LaoDictionary: Tra cứu từ điển 1,200 từ, tra cứu chú giải, tìm kiếm bộ phận.
5. LaoTranslator: Dịch toàn câu, tách từ, phiên âm, sinh danh sách WordGloss.
6. P8 Artifacts: Tính toàn vẹn của Bảng 19, 20, 21 và đồ thị PNG.
"""
import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.translation.tokenizer import LaoTokenizer, compute_tokenization_f1
from src.translation.romanizer import LaoRomanizer
from src.translation.dictionary_lookup import LaoDictionary
from src.translation.translator import LaoTranslator, TranslationOutput


class TestP8LanguageLayer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = LaoTokenizer()
        self.romanizer = LaoRomanizer()
        self.dictionary = LaoDictionary()
        self.translator = LaoTranslator()

    def test_lao_tokenizer_trie(self):
        """Kiểm tra giải thuật Trie Longest Matching trên câu ghép tiếng Lào."""
        text = "ສະບາຍດີຕອນເຊົ້າ"
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("ສະບາຍດີ", tokens)
        self.assertIn("ຕອນເຊົ້າ", tokens)

    def test_compute_tokenization_f1(self):
        """Kiểm tra hàm đo F1 biên giới từ."""
        gold = [["ສະບາຍດີ", "ຕອນເຊົ້າ"]]
        pred = [["ສະບາຍດີ", "ຕອນເຊົ້າ"]]
        p, r, f1 = compute_tokenization_f1(gold, pred)
        self.assertEqual(p, 1.0)
        self.assertEqual(r, 1.0)
        self.assertEqual(f1, 1.0)

    def test_lao_romanizer(self):
        """Kiểm tra bộ sinh phiên âm Latinh ngữ âm."""
        rom_sabaidee = self.romanizer.romanize_token("ສະບາຍດີ")
        self.assertTrue(len(rom_sabaidee) > 0)
        self.assertIn("sa", rom_sabaidee.lower())

        # Test phiên âm chuỗi token
        full_rom = self.romanizer.romanize(["ສະບາຍດີ", "ຕອນເຊົ້າ"])
        self.assertTrue(len(full_rom.split()) >= 2)

    def test_lao_dictionary_lookup(self):
        """Kiểm tra kho từ điển giáo trình mở rộng (> 1,000 mục từ)."""
        self.assertGreaterEqual(len(self.dictionary), 1000)

        # Kiểm tra tra cứu từ quen thuộc
        entry = self.dictionary.lookup("ຂອບໃຈ")
        self.assertIsNotNone(entry)
        self.assertIn("Cảm ơn", entry["vi"])
        self.assertIn("Thank", entry["en"])
        self.assertTrue(self.dictionary.contains("ຂອບໃຈ"))

    def test_lao_translator_end_to_end(self):
        """Kiểm tra luồng dịch thuật và tạo flashcard giáo dục."""
        # Test 1: Khớp chính xác cụm từ từ điển
        res_exact = self.translator.translate("ສະບາຍດີ")
        self.assertIsInstance(res_exact, TranslationOutput)
        self.assertTrue(res_exact.is_exact_phrase)
        self.assertEqual(len(res_exact.glosses), 1)

        # Test 2: Dịch câu ghép nhiều từ
        sentence = "ຂ້ອຍຮຽນພາສາລາວ"
        res_sent = self.translator.translate(sentence)
        self.assertGreaterEqual(len(res_sent.tokens), 2)
        self.assertTrue(len(res_sent.translation_vi) > 0)
        self.assertTrue(len(res_sent.translation_en) > 0)
        self.assertTrue(len(res_sent.romanization) > 0)
        self.assertEqual(len(res_sent.glosses), len(res_sent.tokens))

    def test_p8_tables_and_plots_exist(self):
        """Kiểm tra sự tồn tại và tính hợp lệ của Bảng 19, 20, 21 và đồ thị."""
        results_dir = os.path.join(PROJECT_ROOT, "experiments", "results")
        required_csvs = [
            "p8_table19_word_segmentation_comparison.csv",
            "p8_table20_translation_quality.csv",
            "p8_table21_latency_breakdown.csv",
        ]
        for fname in required_csvs:
            fpath = os.path.join(results_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Thiếu file CSV: {fname}")
            with open(fpath, "r", encoding="utf-8-sig") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.assertGreaterEqual(len(lines), 3, f"{fname} quá ngắn.")

        png_path = os.path.join(results_dir, "p8_translation_and_segmentation.png")
        self.assertTrue(os.path.exists(png_path), "Thiếu biểu đồ PNG: p8_translation_and_segmentation.png")
        self.assertGreater(os.path.getsize(png_path), 5000, "File PNG quá nhỏ.")


if __name__ == "__main__":
    unittest.main()
