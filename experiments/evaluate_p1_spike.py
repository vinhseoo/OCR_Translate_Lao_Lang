"""
Script đánh giá toàn diện Phase P1 (Spike End-to-End Evaluation).
Chạy kiểm thử trên toàn bộ 20 ảnh flashcard mẫu, tính toán CER mốc số 0 (Baseline Zero),
độ chính xác cấp từ, khoảng tin cậy Bootstrap 95% CI và xuất báo cáo CSV.
"""
import os
import sys
import csv
import time
from typing import List, Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image
from src.preprocessing.pipeline import preprocess_image_p1
from src.ocr.tesseract_engine import TesseractLaoEngine
from src.postprocessing.mini_dict_matcher import MiniDictMatcher
from src.preprocessing.normalize import normalize_lao
from src.evaluation.metrics import (
    compute_cer,
    compute_dataset_cer,
    compute_word_accuracy,
    bootstrap_cer_confidence_interval,
    levenshtein_distance,
)

LABELS_CSV = os.path.join(PROJECT_ROOT, "data", "samples", "p1_spike", "p1_labels.csv")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "samples", "p1_spike")
OUTPUT_CSV = os.path.join(PROJECT_ROOT, "experiments", "results", "p1_spike_results.csv")


def run_spike_evaluation():
    print("=" * 70)
    print("⚡ BẮT ĐẦU ĐÁNH GIÁ THỰC NGHIỆM PHASE P1: LÁT CẮT DỌC (VERTICAL SPIKE)")
    print("=" * 70)
    
    if not os.path.exists(LABELS_CSV):
        raise FileNotFoundError(f"Không tìm thấy nhãn P1 tại: {LABELS_CSV}")
        
    engine = TesseractLaoEngine()
    matcher = MiniDictMatcher()
    
    records = []
    with open(LABELS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)
            
    print(f"Tổng số mẫu đánh giá: {len(records)} ảnh")
    
    results = []
    references = []
    hypotheses = []
    
    correct_count = 0
    total_time = 0.0
    
    for idx, row in enumerate(records, start=1):
        filename = row["filename"]
        ref_text = normalize_lao(row["lao_text"])
        img_path = os.path.join(IMAGES_DIR, filename)
        
        t0 = time.time()
        # 1. Tiền xử lý (Grayscale + Otsu)
        raw_img = Image.open(img_path)
        proc_img = preprocess_image_p1(raw_img)
        
        # 2. OCR Tesseract
        pred_text = engine.recognize(proc_img)
        t_cost = time.time() - t0
        total_time += t_cost
        
        # 3. Tra từ điển
        dict_res = matcher.lookup(pred_text)
        
        # 4. Tính toán CER & Exact Match
        sample_cer = compute_cer(ref_text, pred_text)
        is_exact = (ref_text == pred_text)
        if is_exact:
            correct_count += 1
            
        references.append(ref_text)
        hypotheses.append(pred_text)
        
        results.append({
            "idx": idx,
            "filename": filename,
            "font": row.get("font", "unknown"),
            "reference": ref_text,
            "hypothesis": pred_text,
            "cer": round(sample_cer, 4),
            "exact_match": is_exact,
            "dict_vi": dict_res["vi"],
            "dict_en": dict_res["en"],
            "confidence": dict_res["confidence"],
            "match_type": dict_res["match_type"],
            "latency": round(t_cost, 3)
        })
        
        status_sym = "✅" if is_exact else "❌"
        print(f"  [{idx:02d}/20] {status_sym} Ref: '{ref_text}' | Hyp: '{pred_text}' | CER: {sample_cer:.2f} | Nghĩa: {dict_res['vi']}")

    # Tính toán các chỉ số vĩ mô toàn tập P1
    macro_cer = compute_dataset_cer(references, hypotheses)
    word_acc = compute_word_accuracy(references, hypotheses)
    mean_ci, lower_ci, upper_ci = bootstrap_cer_confidence_interval(
        references, hypotheses, n_resamples=1000, confidence_level=0.95, seed=42
    )
    
    # Ghi file kết quả CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, mode="w", encoding="utf-8", newline="") as out_f:
        fieldnames = [
            "idx", "filename", "font", "reference", "hypothesis",
            "cer", "exact_match", "dict_vi", "dict_en", "confidence", "match_type", "latency"
        ]
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    print("\n" + "=" * 70)
    print("📊 TỔNG KẾT KẾT QUẢ THỰC NGHIỆM PHASE P1 (BASELINE ZERO)")
    print("=" * 70)
    print(f"  • Tổng số ảnh kiểm thử          : {len(records)}")
    print(f"  • Số ảnh nhận dạng chính xác 100%: {correct_count}/{len(records)} ({word_acc * 100:.1f}%)")
    print(f"  • CER thô trung bình (Mốc số 0) : {macro_cer * 100:.2f}%")
    print(f"  • Khoảng tin cậy Bootstrap 95% CI: [{lower_ci * 100:.2f}% - {upper_ci * 100:.2f}%]")
    print(f"  • Thời gian xử lý trung bình/ảnh: {total_time / len(records):.3f} giây")
    print(f"  • File chi tiết lưu tại         : {OUTPUT_CSV}")
    print("=" * 70)
    
    # Kiểm tra cổng ra Phase P1 (Exit Gate: >= 5/20 ảnh đúng)
    pass_gate = correct_count >= 5
    if pass_gate:
        print(f"🎉 CỔNG RA PHASE P1: ĐẠT! ({correct_count} >= 5 ảnh đúng theo quy chuẩn)")
    else:
        print(f"⚠️ CỔNG RA PHASE P1: CHƯA ĐẠT! (Chỉ đúng {correct_count}/20 ảnh)")
    return pass_gate, macro_cer, word_acc


if __name__ == "__main__":
    run_spike_evaluation()
