"""
Unit Tests cho Phase P7: Mô hình Học Sâu & Huấn luyện OCR Tiếng Lào (LaoCRNN + CTC).
Kiểm tra:
1. LaoVocabulary: Mã hóa, giải mã, CTC greedy decode chuẩn NFC.
2. LaoCRNN: Forward pass tensor dimensions, sequence length nén H=1.
3. LaoCRNN predict_image: Hỗ trợ numpy array và PIL Image.
4. Model Checkpoint: crnn_lao.pt tải thành công và tương thích trọng số.
5. P7 Outputs: Đầy đủ 4 bảng số liệu (Table 15-18) và 2 đồ thị trực quan hóa.
"""
import os
import sys
import unittest
import torch
import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models.lao_vocab import LaoVocabulary, DEFAULT_LAO_VOCAB
from src.models.crnn import LaoCRNN
from src.preprocessing.normalize import normalize_lao


class TestP7Models(unittest.TestCase):
    def test_lao_vocab_encoding_decoding(self):
        vocab = LaoVocabulary()
        self.assertEqual(vocab.blank_idx, 0)
        self.assertEqual(vocab.unk_idx, 1)
        self.assertGreater(vocab.num_classes, 50)

        sample_text = "ສະບາຍດີ"
        encoded = vocab.encode(sample_text)
        self.assertGreater(len(encoded), 0)
        self.assertTrue(all(isinstance(idx, int) for idx in encoded))

        decoded = vocab.decode(encoded)
        self.assertEqual(decoded, normalize_lao(sample_text))

    def test_lao_vocab_ctc_greedy_decode(self):
        vocab = LaoVocabulary()
        idx_sa = vocab.char2idx["ສ"]
        idx_ba = vocab.char2idx["ບ"]

        # Mô phỏng chuỗi logits argmax có lặp và xen kẽ CTC blank (0)
        raw_sequence = [0, idx_sa, idx_sa, 0, idx_ba, idx_ba, idx_ba, 0]
        decoded_text = vocab.ctc_greedy_decode(raw_sequence)
        expected_text = normalize_lao("ສບ")
        self.assertEqual(decoded_text, expected_text)

    def test_lao_crnn_architecture_and_forward(self):
        model = LaoCRNN(hidden_size=64)  # Giảm hidden_size để test nhanh
        model.eval()

        batch_size = 2
        height = 48
        width = 160  # W phải chia hết cho 4 theo kiến trúc CNN (160 / 4 = 40)
        dummy_input = torch.randn(batch_size, 1, height, width)

        with torch.no_grad():
            logits = model(dummy_input)

        # Output logits phải có shape (T, B, num_classes) với T = width // 4 = 40
        self.assertEqual(logits.shape, (40, batch_size, model.vocab.num_classes))

    def test_lao_crnn_predict_image(self):
        model = LaoCRNN(hidden_size=64)
        model.eval()

        # Test với numpy RGB
        dummy_np_rgb = np.full((60, 200, 3), 255, dtype=np.uint8)
        pred_text = model.predict_image(dummy_np_rgb)
        self.assertIsInstance(pred_text, str)

        # Test với PIL Image
        dummy_pil = Image.fromarray(dummy_np_rgb)
        pred_pil = model.predict_image(dummy_pil)
        self.assertIsInstance(pred_pil, str)

    def test_checkpoint_loading(self):
        checkpoint_path = os.path.join(PROJECT_ROOT, "models", "crnn_lao.pt")
        if not os.path.exists(checkpoint_path):
            self.skipTest("models/crnn_lao.pt chưa được tạo.")

        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        self.assertIsInstance(checkpoint, dict)

        vocab = LaoVocabulary()
        model = LaoCRNN(vocab=vocab, hidden_size=256)
        # Checkpoint lưu trực tiếp state_dict
        if "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
        else:
            model.load_state_dict(checkpoint)
        model.eval()

        # Kiểm tra inference thử với 1 ảnh trắng
        test_img = np.full((48, 128), 255, dtype=np.uint8)
        pred = model.predict_image(test_img)
        self.assertIsInstance(pred, str)

    def test_p7_tables_and_plots_exist(self):
        results_dir = os.path.join(PROJECT_ROOT, "experiments", "results")
        required_csvs = [
            "p7_table15_multi_model_benchmark.csv",
            "p7_table16_learning_curves_data_scale.csv",
            "p7_table17_augmentation_impact.csv",
            "p7_table18_lexicon_snap_integration.csv",
        ]
        for fname in required_csvs:
            full_path = os.path.join(results_dir, fname)
            self.assertTrue(os.path.exists(full_path), f"Thiếu file: {fname}")
            with open(full_path, "r", encoding="utf-8-sig") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.assertGreaterEqual(len(lines), 3, f"{fname} có ít hơn 3 dòng.")

        required_pngs = [
            "p7_learning_curves_and_scale.png",
            "p7_model_comparison_radar_or_bars.png",
        ]
        for fname in required_pngs:
            full_path = os.path.join(results_dir, fname)
            self.assertTrue(os.path.exists(full_path), f"Thiếu đồ thị: {fname}")
            self.assertGreater(os.path.getsize(full_path), 1000, f"{fname} quá nhỏ.")


if __name__ == "__main__":
    unittest.main()
