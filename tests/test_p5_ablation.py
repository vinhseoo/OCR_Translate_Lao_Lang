import os
import csv
import unittest
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments", "results")
CONFIGS_DIR = os.path.join(PROJECT_ROOT, "experiments", "configs")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")


class TestP5AblationOutputs(unittest.TestCase):
    def test_all_8_csv_tables_exist(self):
        """Kiểm tra sự tồn tại và tính hợp lệ của đủ 8 bảng số liệu Ablation Study."""
        expected_tables = [
            "p5_table3_binarization.csv",
            "p5_table4_leave_one_out.csv",
            "p5_table5_forward_selection.csv",
            "p5_table6_morphology_kernel.csv",
            "p5_table7_line_height.csv",
            "p5_table8_stratified.csv",
            "p5_table9_noise_robustness.csv",
            "p5_table10_printed_vs_handwritten.csv"
        ]
        for tbl in expected_tables:
            path = os.path.join(RESULTS_DIR, tbl)
            self.assertTrue(os.path.exists(path), f"Thiếu tệp bảng số liệu: {tbl}")
            with open(path, mode="r", encoding="utf-8") as f:
                reader = list(csv.DictReader(f))
                self.assertGreaterEqual(len(reader), 2, f"Bảng {tbl} có quá ít dữ liệu: {len(reader)}")

    def test_all_5_plots_exist(self):
        """Kiểm tra sự tồn tại của đủ 5 biểu đồ chẩn đoán khoa học."""
        expected_plots = [
            "ablation_table3_binarization.png",
            "ablation_table4_leave_one_out.png",
            "ablation_table6_morphology_kernel.png",
            "ablation_table8_stratified.png",
            "ablation_table9_noise_robustness.png"
        ]
        for plt_name in expected_plots:
            path = os.path.join(RESULTS_DIR, plt_name)
            self.assertTrue(os.path.exists(path), f"Thiếu tệp biểu đồ: {plt_name}")
            self.assertGreater(os.path.getsize(path), 10000, f"Biểu đồ {plt_name} quá nhỏ hoặc rỗng")

    def test_optimal_pipeline_yaml(self):
        """Kiểm tra cấu hình tối ưu đã được khóa trong optimal_pipeline.yaml."""
        yaml_path = os.path.join(CONFIGS_DIR, "optimal_pipeline.yaml")
        self.assertTrue(os.path.exists(yaml_path), "Thiếu tệp optimal_pipeline.yaml")
        with open(yaml_path, mode="r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
            
        self.assertIn("binarization", cfg)
        self.assertIn("border_padding", cfg)
        self.assertIn("height_normalization", cfg)
        self.assertEqual(cfg["height_normalization"]["target_height"], 48)
        self.assertEqual(cfg["morphology"]["kernel_size"], [1, 1])

    def test_ablation_study_document(self):
        """Kiểm tra báo cáo khoa học docs/ABLATION_STUDY.md."""
        doc_path = os.path.join(DOCS_DIR, "ABLATION_STUDY.md")
        self.assertTrue(os.path.exists(doc_path), "Thiếu tệp docs/ABLATION_STUDY.md")
        with open(doc_path, mode="r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("BẢNG 3: SO SÁNH 6 GIẢI THUẬT NHỊ PHÂN HÓA", content)
        self.assertIn("BẢNG 4: THỰC NGHIỆM LEAVE-ONE-OUT", content)
        self.assertIn("BẢNG 5: GREEDY FORWARD SELECTION", content)
        self.assertIn("BẢNG 6: KIỂM CHỨNG QUY TẮC BẤT DI BẤT DỊCH #3", content)
        self.assertIn("BẢNG 7: ẢNH HƯỞNG CỦA CHIỀU CAO DÒNG CHUẨN HÓA", content)
        self.assertIn("BẢNG 8: PHÂN TÍCH CER PHÂN TẦNG", content)
        self.assertIn("BẢNG 9: ĐỘ BỀN PIPELINE TRƯỚC NHIỄU VÀ MỜ", content)
        self.assertIn("BẢNG 10: ĐỐI CHIẾU HIỆU NĂNG: CHỮ IN VS CHỮ VIẾT TAY", content)


if __name__ == "__main__":
    unittest.main()
