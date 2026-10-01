import os
import sys
import csv
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments", "results")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

from src.postprocessing.weighted_levenshtein import WeightedLevenshtein, standard_levenshtein
from src.postprocessing.lexicon_matcher import LexiconMatcher
from src.preprocessing.normalize import normalize_lao


class TestP6Postprocessing(unittest.TestCase):
    def setUp(self):
        self.weighted = WeightedLevenshtein()
        self.matcher = LexiconMatcher()

    def test_weighted_levenshtein_identical(self):
        """Khoảng cách giữa hai chuỗi giống nhau phải là 0.0."""
        text = "ສະບາຍດີ"
        self.assertEqual(self.weighted.distance(text, text), 0.0)
        self.assertEqual(self.weighted.similarity(text, text), 1.0)

    def test_tone_penalty_discount(self):
        """Mất dấu thanh phải bị phạt nhẹ hơn mất phụ âm (0.2 vs 1.0)."""
        ref = "ແມ່ນ"   # Có dấu Mai Ek
        hyp_drop_tone = "ແມນ"  # Rụng dấu Mai Ek
        hyp_sub_consonant = "ແກ່ນ"  # Thay phụ âm 'ມ' bằng 'ກ'
        
        dist_drop_tone = self.weighted.distance(ref, hyp_drop_tone)
        dist_sub_consonant = self.weighted.distance(ref, hyp_sub_consonant)
        
        # Mất dấu thanh chỉ bị phạt 0.2
        self.assertAlmostEqual(dist_drop_tone, 0.2, places=2)
        # Thay phụ âm bị phạt 1.0
        self.assertGreater(dist_sub_consonant, dist_drop_tone)

    def test_confusion_pair_cost_discount(self):
        """Cặp nhầm lẫn thực nghiệm trong confusion_pairs.csv (າ -> ໂ) phải có chi phí thấp."""
        cost_empirical = self.weighted.get_substitution_cost("າ", "ໂ")
        cost_unseen = self.weighted.get_substitution_cost("າ", "X")
        
        self.assertLess(cost_empirical, 0.5)
        self.assertEqual(cost_unseen, 1.0)

    def test_lexicon_matcher_exact_match(self):
        """Khớp chính xác từ trong từ điển giáo trình."""
        res = self.matcher.match("ກະລຸນາ", method="weighted_levenshtein")
        self.assertTrue(res.is_exact)
        self.assertEqual(res.best_lao, "ກະລຸນາ")
        self.assertEqual(res.confidence, 1.0)
        self.assertIn("Làm ơn", res.best_vi)

    def test_lexicon_matcher_fuzzy_recovery(self):
        """Khôi phục đúng từ khi OCR bị rụng dấu thanh."""
        # OCR nhận dạng mất dấu thanh Mai Ek: 'ແມນ' thay vì 'ແມ່ນ'
        res = self.matcher.match("ແມນ", method="weighted_levenshtein", top_k=3)
        self.assertEqual(res.best_lao, "ແມ່ນ")
        self.assertTrue(res.confidence > 0.8)
        self.assertTrue(res.is_confident)

    def test_lexicon_matcher_topk_ordering(self):
        """Danh sách Top-k phải sắp xếp theo khoảng cách tăng dần với truy vấn không khớp chính xác."""
        res = self.matcher.match("ສະບາຍດ", method="weighted_levenshtein", top_k=5)
        self.assertEqual(len(res.top_candidates), 5)
        distances = [c.distance for c in res.top_candidates]
        self.assertEqual(distances, sorted(distances))

    def test_p6_result_tables_exist(self):
        """Kiểm tra đủ các bảng CSV kết quả của Phase P6."""
        tables = [
            "p6_table11_accuracy_and_topk.csv",
            "p6_table12_standard_vs_weighted_levenshtein.csv",
            "p6_table13_dictionary_size_effect.csv",
            "p6_table14_ngram_vs_levenshtein.csv",
            "p6_cumulative_pipeline_summary.csv"
        ]
        for tbl in tables:
            path = os.path.join(RESULTS_DIR, tbl)
            self.assertTrue(os.path.exists(path), f"Thiếu bảng kết quả: {tbl}")

    def test_p6_plots_exist(self):
        """Kiểm tra đủ các biểu đồ PNG chẩn đoán của Phase P6."""
        plots = [
            "p6_topk_and_methods_comparison.png",
            "p6_precision_coverage_curve.png"
        ]
        for plt_file in plots:
            path = os.path.join(RESULTS_DIR, plt_file)
            self.assertTrue(os.path.exists(path), f"Thiếu biểu đồ: {plt_file}")
            self.assertGreater(os.path.getsize(path), 10000, "Biểu đồ quá nhỏ hoặc rỗng")

    def test_p6_documentation_exists(self):
        """Kiểm tra tài liệu docs/POSTPROCESSING_LEXICON.md."""
        doc_path = os.path.join(DOCS_DIR, "POSTPROCESSING_LEXICON.md")
        self.assertTrue(os.path.exists(doc_path), "Thiếu docs/POSTPROCESSING_LEXICON.md")
        with open(doc_path, mode="r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("BẢNG 11: ĐỘ CHÍNH XÁC TỪ & TOP-1 / TOP-3 / TOP-5", content)
        self.assertIn("BẢNG 12: SO SÁNH ĐỐI ĐẦU LEVENSHTEIN TIÊU CHUẨN", content)
        self.assertIn("BẢNG 13: ẢNH HƯỞNG CỦA QUY MÔ TỪ ĐIỂN", content)
        self.assertIn("BẢNG TỔNG KẾT LUỒNG TĂNG TIẾN TOÀN DIỆN", content)


if __name__ == "__main__":
    unittest.main()
