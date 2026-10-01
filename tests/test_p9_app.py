"""
Unit Tests cho Phase P9: Ứng Dụng Streamlit & Thuật Toán Ghi Nhớ Lặp Lại Ngắt Quãng SM-2.
Kiểm tra:
1. Thuật toán SuperMemo SM-2 (calculate_sm2): Cập nhật EF, repetitions và interval chuẩn toán học.
2. Quản lý trạng thái thẻ Flashcard (review_card, FlashcardReviewState).
3. Feedback Logging (save_user_correction, load_user_corrections).
4. Tính tương thích và toàn vẹn của ứng dụng app.py.
"""
import os
import sys
import unittest
import py_compile
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.education.sm2 import calculate_sm2, review_card, FlashcardReviewState
from src.education.feedback import save_user_correction, load_user_corrections
from src.preprocessing.pipeline import PreprocessingPipeline
from src.postprocessing.lexicon_matcher import LexiconMatcher
from src.translation.translator import LaoTranslator


class TestP9App(unittest.TestCase):
    def test_sm2_algorithm_perfect_response(self):
        """Kiểm tra phản hồi hoàn hảo (quality = 5): EF tăng và interval tăng lũy tiến."""
        # Lần lặp 0 -> 1
        reps, interval, ef = calculate_sm2(quality=5, repetitions=0, previous_interval=1, previous_ef=2.5)
        self.assertEqual(reps, 1)
        self.assertEqual(interval, 1)
        self.assertGreater(ef, 2.5)

        # Lần lặp 1 -> 2
        reps2, interval2, ef2 = calculate_sm2(quality=5, repetitions=1, previous_interval=interval, previous_ef=ef)
        self.assertEqual(reps2, 2)
        self.assertEqual(interval2, 6)

        # Lần lặp 2 -> 3: interval = ceil(6 * EF)
        reps3, interval3, ef3 = calculate_sm2(quality=5, repetitions=2, previous_interval=interval2, previous_ef=ef2)
        self.assertEqual(reps3, 3)
        self.assertGreater(interval3, 6)

    def test_sm2_algorithm_failure_reset(self):
        """Kiểm tra khi học viên quên (quality < 3): repetitions và interval bị reset về 0 và 1."""
        reps, interval, ef = calculate_sm2(quality=1, repetitions=5, previous_interval=30, previous_ef=2.5)
        self.assertEqual(reps, 0)
        self.assertEqual(interval, 1)
        self.assertLess(ef, 2.5)
        self.assertGreaterEqual(ef, 1.3)  # Không bao giờ thấp hơn ngưỡng 1.3

    def test_review_card_state_update(self):
        """Kiểm tra cập nhật thẻ flashcard đầy đủ lịch sử."""
        card = FlashcardReviewState(
            card_id="c_test",
            lao_text="ສະບາຍດີ",
            vi_meaning="Xin chào",
            romanization="sa-baai-dee"
        )
        self.assertEqual(card.repetitions, 0)
        updated = review_card(card, quality=4)
        self.assertEqual(updated.repetitions, 1)
        self.assertEqual(len(updated.history), 1)
        self.assertTrue(updated.next_review >= updated.last_reviewed[:10])

    def test_feedback_logging(self):
        """Kiểm tra lưu phản hồi sửa lỗi của người học."""
        res = save_user_correction(
            image_name="test_card.jpg",
            raw_ocr="ສະບາຍດ",
            corrected_text="ສະບາຍດີ",
            engine_used="LaoCRNN",
            user_note="Thiếu nguyên âm tầng trên"
        )
        self.assertTrue(res)
        corrections = load_user_corrections()
        self.assertGreater(len(corrections), 0)
        latest = corrections[-1]
        self.assertEqual(latest["corrected_text"], "ສະບາຍດີ")

    def test_app_compilation_and_dependencies(self):
        """Kiểm tra tính hợp lệ và khả năng chạy của ứng dụng app.py."""
        app_path = os.path.join(PROJECT_ROOT, "app.py")
        self.assertTrue(os.path.exists(app_path), "Không tìm thấy file app.py")
        
        # Biên dịch file app.py
        compiled = py_compile.compile(app_path)
        self.assertIsNotNone(compiled)

        # Kiểm tra khởi tạo các động cơ
        pipeline = PreprocessingPipeline(config={})
        self.assertIsNotNone(pipeline)
        matcher = LexiconMatcher()
        self.assertIsNotNone(matcher)
        translator = LaoTranslator()
        self.assertIsNotNone(translator)


if __name__ == "__main__":
    unittest.main()
