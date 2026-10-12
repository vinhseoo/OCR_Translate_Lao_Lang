"""
Unit test kiểm thử module Phân đoạn dòng và Nhận dạng đoạn văn bản (Document OCR).
"""
import unittest
import numpy as np
import cv2

from src.ocr.document_ocr import detect_and_crop_lines, run_document_ocr


class TestDocumentOCR(unittest.TestCase):
    def setUp(self):
        # Tạo ảnh giả lập văn bản 3 dòng
        self.test_img = np.full((150, 300, 3), 255, dtype=np.uint8)
        # Dòng 1: y từ 20 đến 45
        cv2.putText(self.test_img, "Line 1 Lao", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        # Dòng 2: y từ 65 đến 90
        cv2.putText(self.test_img, "Line 2 Lao", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        # Dòng 3: y từ 110 đến 135
        cv2.putText(self.test_img, "Line 3 Lao", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    def test_line_detection(self):
        crops, boxes, annotated = detect_and_crop_lines(self.test_img, method="hpp")
        self.assertGreaterEqual(len(crops), 2)
        self.assertEqual(len(crops), len(boxes))
        self.assertEqual(annotated.shape, self.test_img.shape)

    def test_run_document_ocr_dummy(self):
        res = run_document_ocr(self.test_img, crnn_model=None, engine_choice="tesseract_block")
        self.assertIsNotNone(res)
        self.assertIsInstance(res.elapsed_ms, float)
        self.assertGreaterEqual(res.num_lines, 0)


if __name__ == "__main__":
    unittest.main()
