import os
import csv
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments", "results")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")


class TestP4Outputs(unittest.TestCase):
    def test_p4_psm_scan_results(self):
        """Kiểm tra tệp p4_psm_scan_results.csv có đầy đủ các chế độ PSM quy định."""
        csv_path = os.path.join(RESULTS_DIR, "p4_psm_scan_results.csv")
        self.assertTrue(os.path.exists(csv_path), "Thiếu tệp p4_psm_scan_results.csv")
        
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            
        psms = [int(r["psm"]) for r in reader]
        self.assertIn(6, psms, "Thiếu PSM 6")
        self.assertIn(7, psms, "Thiếu PSM 7")
        self.assertIn(8, psms, "Thiếu PSM 8")
        self.assertIn(11, psms, "Thiếu PSM 11")
        self.assertIn(13, psms, "Thiếu PSM 13")
        
        # Kiểm tra PSM 7 có CER hợp lệ
        psm7_row = next(r for r in reader if int(r["psm"]) == 7)
        cer = float(psm7_row["cer_percent"])
        self.assertTrue(0 < cer < 100, f"CER của PSM 7 không hợp lệ: {cer}")

    def test_p4_engine_comparison(self):
        """Kiểm tra tệp p4_engine_comparison.csv có đủ các engine đối sánh."""
        csv_path = os.path.join(RESULTS_DIR, "p4_engine_comparison.csv")
        self.assertTrue(os.path.exists(csv_path), "Thiếu tệp p4_engine_comparison.csv")
        
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            
        engine_names = [r["engine"] for r in reader]
        self.assertTrue(any("Tesseract 5 Lao" in e for e in engine_names), "Thiếu baseline Tesseract")
        self.assertTrue(any("EasyOCR" in e for e in engine_names), "Thiếu đối sánh EasyOCR")
        self.assertTrue(any("PaddleOCR" in e for e in engine_names), "Thiếu đối sánh PaddleOCR")
        self.assertTrue(any("Cloud Vision" in e for e in engine_names), "Thiếu trần tham chiếu Cloud Vision")
        self.assertTrue(any("VLM" in e for e in engine_names), "Thiếu trần tham chiếu VLM")

    def test_p4_confusion_pairs(self):
        """Kiểm tra tệp confusion_pairs.csv trích xuất cặp ký tự thực nghiệm cho P6."""
        csv_path = os.path.join(RESULTS_DIR, "confusion_pairs.csv")
        self.assertTrue(os.path.exists(csv_path), "Thiếu tệp confusion_pairs.csv")
        
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            
        self.assertGreaterEqual(len(reader), 30, f"Số lượng cặp nhầm lẫn quá ít: {len(reader)}")
        
        for r in reader:
            cost = float(r["cost"])
            self.assertTrue(0.3 <= cost <= 1.0, f"Chi phí Levenshtein ngoài ngưỡng [0.3, 1.0]: {cost}")
            self.assertGreaterEqual(int(r["count"]), 1, "Tần suất phải >= 1")

    def test_p4_error_taxonomy(self):
        """Kiểm tra tệp p4_error_taxonomy.csv đủ 5 loại lỗi."""
        csv_path = os.path.join(RESULTS_DIR, "p4_error_taxonomy.csv")
        self.assertTrue(os.path.exists(csv_path), "Thiếu tệp p4_error_taxonomy.csv")
        
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            
        cat_ids = [r["category_id"] for r in reader]
        self.assertIn("1_geometric_similarity", cat_ids)
        self.assertIn("2_tone_mark_dropped", cat_ids)
        self.assertIn("3_vowel_order_inversion", cat_ids)
        self.assertIn("4_insertion_deletion", cat_ids)
        self.assertIn("5_complete_breakdown", cat_ids)
        
        total_pct = sum(float(r["percentage"]) for r in reader)
        self.assertTrue(99.0 <= total_pct <= 101.0, f"Tổng phần trăm lỗi phải xấp xỉ 100%, thực tế: {total_pct}")

    def test_error_analysis_doc_exists(self):
        """Kiểm tra file báo cáo phân tích lỗi docs/ERROR_ANALYSIS.md."""
        doc_path = os.path.join(DOCS_DIR, "ERROR_ANALYSIS.md")
        self.assertTrue(os.path.exists(doc_path), "Thiếu tệp docs/ERROR_ANALYSIS.md")
        
        with open(doc_path, mode="r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("BẢNG 1: QUÉT CÁC CHẾ ĐỘ PHÂN ĐOẠN TRANG TESSERACT", content)
        self.assertIn("BẢNG 2: SO SÁNH HIỆU NĂNG ĐA ENGINE", content)
        self.assertIn("HỆ THỐNG PHÂN LOẠI LỖI", content)
        self.assertIn("MA TRẬN NHẦM LẪN KÝ TỰ THỰC NGHIỆM", content)


if __name__ == "__main__":
    unittest.main()
