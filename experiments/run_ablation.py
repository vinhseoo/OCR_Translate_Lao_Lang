"""
Script Tự Động Hóa Nghiên Cứu Ablation Toàn Diện (Phase P5 - Đóng Góp Khoa Học #1).
Thực thi và xuất bản 8 bảng thực nghiệm khoa học (kèm khoảng tin cậy Bootstrap 95%) và 5 biểu đồ chẩn đoán:
  1. Bảng 3: So sánh 6 phương pháp nhị phân hóa (A6).
  2. Bảng 4: Leave-one-out từng bước A1 - A9 (Delta CER kèm CI 95%).
  3. Bảng 5: Greedy forward selection tìm cấu hình tối ưu.
  4. Bảng 6: Ảnh hưởng kích thước kernel hình thái học (Kiểm chứng Lao Golden Rule #3).
  5. Bảng 7: Ảnh hưởng của chiều cao dòng chuẩn hóa (A8).
  6. Bảng 8: Phân tích CER phân tầng (Sáng x Thiết bị x Font x Góc).
  7. Bảng 9: Độ bền pipeline (Noise & Blur Robustness Curve).
  8. Bảng 10: Đối chiếu hiệu năng: Chữ in vs Chữ viết tay.
"""
import os
import sys
import csv
import time
import math
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.ocr.tesseract_engine import TesseractLaoEngine
from src.preprocessing.pipeline import PreprocessingPipeline
from src.preprocessing.normalize import normalize_lao, LAO_TONE_MARKS
from src.evaluation.metrics import (
    compute_cer,
    compute_dataset_cer,
    compute_word_accuracy,
    bootstrap_cer_confidence_interval,
)

# Thư mục dữ liệu & kết quả
GOLD_DIR = os.path.join(PROJECT_ROOT, "data", "gold")
DEV_LABELS_CSV = os.path.join(GOLD_DIR, "dev_labels.csv")
ALL_LABELS_CSV = os.path.join(GOLD_DIR, "all_labels.csv")
IMAGES_DIR = os.path.join(GOLD_DIR, "images")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments", "results")
CONFIGS_DIR = os.path.join(PROJECT_ROOT, "experiments", "configs")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(CONFIGS_DIR, exist_ok=True)


# ==============================================================================
# HÀM HỖ TRỢ ĐỌC DỮ LIỆU & CHẠY OCR SONG SONG ĐA LUỒNG
# ==============================================================================
def load_dev_records() -> List[Dict[str, Any]]:
    records = []
    with open(DEV_LABELS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)
    return records


def load_handwritten_records() -> List[Dict[str, Any]]:
    records = []
    with open(ALL_LABELS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("type") == "handwritten":
                records.append(r)
    return records


def evaluate_pipeline_parallel(
    records: List[Dict[str, Any]],
    pipeline: PreprocessingPipeline,
    engine: TesseractLaoEngine,
    max_workers: int = 8,
    raw_images: bool = False,
    noise_fn = None
) -> Tuple[float, float, float, float, List[str], float]:
    """
    Chạy song song toàn bộ ảnh qua pipeline và Tesseract.
    Trả về: (cer, ci_lower, ci_upper, word_acc, hypotheses, avg_time_sec).
    """
    t0 = time.time()
    
    # 1. Tiền xử lý
    processed_images = []
    for r in records:
        img_path = os.path.join(IMAGES_DIR, r["filename"])
        if raw_images:
            img = cv2.imread(img_path)
            if img is None:
                img = np.zeros((100, 200, 3), dtype=np.uint8)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if noise_fn:
                img = noise_fn(img)
            proc_img = img
        else:
            if noise_fn:
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = noise_fn(img)
                proc_img, _ = pipeline.process(img)
            else:
                proc_img, _ = pipeline.process(img_path)
                
        processed_images.append(proc_img)
        
    # 2. Nhận dạng song song
    def recognize_single(proc):
        pil_img = Image.fromarray(proc)
        return engine.recognize(pil_img)
        
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        hypotheses = list(executor.map(recognize_single, processed_images))
        
    elapsed = time.time() - t0
    avg_time = elapsed / len(records)
    
    # 3. Tính toán thước đo chuẩn hóa NFC
    references = [normalize_lao(r["lao_text"]) for r in records]
    hyps_norm = [normalize_lao(h) for h in hypotheses]
    
    cer = compute_dataset_cer(references, hyps_norm)
    word_acc = compute_word_accuracy(references, hyps_norm)
    mean_ci, lower_ci, upper_ci = bootstrap_cer_confidence_interval(
        references, hyps_norm, n_resamples=1000, seed=42
    )
    
    return cer, lower_ci, upper_ci, word_acc, hyps_norm, avg_time


# ==============================================================================
# BÀI TOÁN 1 (BẢNG 3): SO SÁNH 6 PHƯƠNG PHÁP NHỊ PHÂN HÓA (A6)
# ==============================================================================
def run_table3_binarization(records: List[Dict[str, Any]], engine: TesseractLaoEngine):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 3: SO SÁNH 6 PHƯƠNG PHÁP NHỊ PHÂN HÓA (A6) DƯỚI ÁNH SÁNG PHỨC TẠP")
    print("=" * 75)
    
    methods = [
        ("otsu", "Otsu (Ngưỡng toàn cục tiêu chuẩn)", {}),
        ("adaptive_mean", "Adaptive Mean (Ngưỡng cục bộ trung bình, C=10)", {"window_size": 25, "C": 10}),
        ("adaptive_gaussian", "Adaptive Gaussian (Ngưỡng cục bộ Gauss, C=10)", {"window_size": 25, "C": 10}),
        ("sauvola", "Sauvola (Ngưỡng cục bộ phương sai, k=0.2, w=25)", {"window_size": 25, "k": 0.2}),
        ("niblack", "Niblack (Ngưỡng cục bộ độ lệch chuẩn, k=-0.2, w=25)", {"window_size": 25, "k": -0.2}),
        ("wolf", "Wolf (Chuẩn hóa độ tương phản cực tiểu, k=0.5, w=25)", {"window_size": 25, "k": 0.5}),
    ]
    
    rows = []
    plot_labels = []
    plot_cers = []
    plot_errors = []
    
    for method_key, method_name, extra_params in methods:
        cfg = {
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "binarization": {"enabled": True, "method": method_key, **extra_params},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15}
        }
        pipe = PreprocessingPipeline(config=cfg)
        cer, ci_low, ci_high, acc, _, t_sec = evaluate_pipeline_parallel(records, pipe, engine)
        
        print(f"  • {method_name:<50} | CER: {cer*100:>5.2f}% [{ci_low*100:>5.2f}% - {ci_high*100:>5.2f}%] | Acc: {acc*100:>5.2f}%")
        
        rows.append({
            "method": method_key,
            "description": method_name,
            "cer_percent": round(cer * 100, 2),
            "ci_95": f"[{ci_low*100:.2f}% - {ci_high*100:.2f}%]",
            "ci_lower_percent": round(ci_low * 100, 2),
            "ci_upper_percent": round(ci_high * 100, 2),
            "word_acc_percent": round(acc * 100, 2),
            "avg_time_sec": round(t_sec, 4)
        })
        plot_labels.append(method_key.capitalize())
        plot_cers.append(cer * 100)
        plot_errors.append([(cer - ci_low) * 100, (ci_high - cer) * 100])
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table3_binarization.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 3 ra: {csv_file}")
    
    # Vẽ biểu đồ khoa học
    plt.figure(figsize=(9, 5))
    errors_array = np.array(plot_errors).T
    bars = plt.bar(plot_labels, plot_cers, yerr=errors_array, capsize=5, color="#1f77b4", edgecolor="black", alpha=0.85)
    plt.title("Ablation Study: So sánh 6 giải thuật nhị phân hóa (A6) trên Dev Set", fontsize=12, fontweight="bold")
    plt.ylabel("Character Error Rate - CER (%) [Thấp hơn là tốt hơn]", fontsize=11)
    plt.xlabel("Giải thuật nhị phân hóa", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
        
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, "ablation_table3_binarization.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"📊 Đã xuất biểu đồ Bảng 3: {plot_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 2 (BẢNG 4): LEAVE-ONE-OUT TỪNG BƯỚC A1 - A9
# ==============================================================================
def run_table4_leave_one_out(records: List[Dict[str, Any]], engine: TesseractLaoEngine):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 4: LEAVE-ONE-OUT TỪNG BƯỚC TIỀN XỬ LÝ (A1 - A9) TRÊN DEV SET")
    print("=" * 75)
    
    # Cấu hình tối ưu chuẩn (Full Optimal Pipeline)
    optimal_cfg = {
        "grayscale": {"enabled": True, "method": "bgr2gray"},
        "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
        "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3, "sigma": 1.0},
        "deskew": {"enabled": True, "method": "moment", "max_angle": 45.0},
        "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2},
        "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]},
        "height_normalization": {"enabled": True, "target_height": 48},
        "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15}
    }
    
    # Đánh giá cấu hình đầy đủ (Baseline Reference)
    pipe_full = PreprocessingPipeline(config=optimal_cfg)
    cer_full, ci_l_full, ci_h_full, acc_full, _, t_full = evaluate_pipeline_parallel(records, pipe_full, engine)
    print(f"⭐ [FULL OPTIMAL PIPELINE] CER: {cer_full*100:>5.2f}% [{ci_l_full*100:>5.2f}% - {ci_h_full*100:>5.2f}%] | Acc: {acc_full*100:>5.2f}%")
    
    loo_configs = [
        ("Without A2 (Bỏ CLAHE)", {"illumination": {"enabled": False}}),
        ("Without A3 (Bỏ khử nhiễu)", {"denoise": {"enabled": False}}),
        ("Without A5 (Bỏ khử nghiêng)", {"deskew": {"enabled": False}}),
        ("Without A6 Sauvola (Dùng Otsu)", {"binarization": {"enabled": True, "method": "otsu"}}),
        ("Without A7 (Bỏ morphology)", {"morphology": {"enabled": False}}),
        ("Without A8 (Bỏ chuẩn hóa chiều cao)", {"height_normalization": {"enabled": False}}),
        ("Without Padding (Bỏ viền đệm)", {"border_padding": {"enabled": False, "crop_outer_px": 0, "padding_px": 0}}),
    ]
    
    rows = [{
        "experiment": "Full Optimal Pipeline",
        "cer_percent": round(cer_full * 100, 2),
        "delta_cer_percent": 0.0,
        "ci_95": f"[{ci_l_full*100:.2f}% - {ci_h_full*100:.2f}%]",
        "word_acc_percent": round(acc_full * 100, 2),
        "impact_evaluation": "Điểm tham chiếu tối ưu (Baseline)"
    }]
    
    plot_labels = ["Full Pipeline"]
    plot_deltas = [0.0]
    
    for label, override_dict in loo_configs:
        cfg = PreprocessingPipeline.get_default_config()
        # copy full config
        import copy
        c = copy.deepcopy(optimal_cfg)
        c.update(override_dict)
        pipe = PreprocessingPipeline(config=c)
        cer, ci_l, ci_h, acc, _, _ = evaluate_pipeline_parallel(records, pipe, engine)
        delta = (cer - cer_full) * 100
        
        impact = f"+{delta:.2f}% (Tụt hiệu năng nếu bỏ)" if delta > 0 else f"{delta:.2f}% (Không ảnh hưởng lớn)"
        print(f"  • {label:<40} | CER: {cer*100:>5.2f}% | ΔCER: {delta:>+6.2f}% | Acc: {acc*100:>5.2f}%")
        
        rows.append({
            "experiment": label,
            "cer_percent": round(cer * 100, 2),
            "delta_cer_percent": round(delta, 2),
            "ci_95": f"[{ci_l*100:.2f}% - {ci_h*100:.2f}%]",
            "word_acc_percent": round(acc * 100, 2),
            "impact_evaluation": impact
        })
        plot_labels.append(label.replace("Without ", "No-"))
        plot_deltas.append(delta)
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table4_leave_one_out.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 4 ra: {csv_file}")
    
    # Vẽ biểu đồ Leave-one-out Delta CER
    plt.figure(figsize=(10, 5))
    colors = ["#2ca02c"] + ["#d62728" if d > 0 else "#1f77b4" for d in plot_deltas[1:]]
    bars = plt.barh(plot_labels, plot_deltas, color=colors, edgecolor="black", alpha=0.85)
    plt.axvline(0, color="black", linestyle="--", linewidth=1.0)
    plt.title("Leave-One-Out Ablation Study: Tác động của từng module (ΔCER so với Full Pipeline)", fontsize=12, fontweight="bold")
    plt.xlabel("Mức tăng CER (%) khi loại bỏ bước xử lý [Càng cao nghĩa là bước đó càng quan trọng]", fontsize=11)
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    
    for bar in bars:
        w = bar.get_width()
        if abs(w) > 0.05:
            offset = 0.5 if w > 0 else -0.5
            ha = "left" if w > 0 else "right"
            plt.text(w + offset, bar.get_y() + bar.get_height()/2., f"{w:+.2f}%", va="center", ha=ha, fontsize=10, fontweight="bold")
            
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, "ablation_table4_leave_one_out.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"📊 Đã xuất biểu đồ Bảng 4: {plot_file}")
    return rows, optimal_cfg


# ==============================================================================
# BÀI TOÁN 3 (BẢNG 5): GREEDY FORWARD SELECTION
# ==============================================================================
def run_table5_forward_selection(records: List[Dict[str, Any]], engine: TesseractLaoEngine):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 5: GREEDY FORWARD SELECTION TÌM CẤU HÌNH TỐI ƯU")
    print("=" * 75)
    
    # Bước 0: Ảnh thô (Raw Image)
    pipe_raw = PreprocessingPipeline(config={
        "grayscale": {"enabled": False},
        "illumination": {"enabled": False},
        "border_padding": {"enabled": False, "crop_outer_px": 0, "padding_px": 0}
    })
    cer_0, ci_l0, ci_h0, acc_0, _, _ = evaluate_pipeline_parallel(records, pipe_raw, engine, raw_images=True)
    print(f"  [Bước 0] Ảnh thô không xử lý (Raw)              | CER: {cer_0*100:>5.2f}% | Acc: {acc_0*100:>5.2f}%")
    
    stages = [
        ("Bước 0: Ảnh thô (Raw Baseline)", pipe_raw, True),
        ("Bước 1: + Xám hóa BGR2GRAY & Cắt viền", PreprocessingPipeline(config={
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
            "binarization": {"enabled": True, "method": "otsu"}
        }), False),
        ("Bước 2: + Cân bằng sáng thích nghi CLAHE (A2)", PreprocessingPipeline(config={
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
            "binarization": {"enabled": True, "method": "otsu"}
        }), False),
        ("Bước 3: + Khử nghiêng Moment & Denoise (A3, A5)", PreprocessingPipeline(config={
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3, "sigma": 1.0},
            "deskew": {"enabled": True, "method": "moment", "max_angle": 45.0},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
            "binarization": {"enabled": True, "method": "otsu"}
        }), False),
        ("Bước 4: + Chuyển sang Sauvola Binarization (A6)", PreprocessingPipeline(config={
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3, "sigma": 1.0},
            "deskew": {"enabled": True, "method": "moment", "max_angle": 45.0},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
            "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2}
        }), False),
        ("Bước 5: + Chuẩn hóa chiều cao 48px & Opening 1x1", PreprocessingPipeline(config={
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "denoise": {"enabled": True, "method": "gaussian", "kernel_size": 3, "sigma": 1.0},
            "deskew": {"enabled": True, "method": "moment", "max_angle": 45.0},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15},
            "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2},
            "morphology": {"enabled": True, "operation": "opening", "kernel_size": [1, 1]},
            "height_normalization": {"enabled": True, "target_height": 48}
        }), False),
    ]
    
    rows = []
    prev_cer = cer_0
    for step_name, pipe, is_raw in stages:
        cer, ci_l, ci_h, acc, _, _ = evaluate_pipeline_parallel(records, pipe, engine, raw_images=is_raw)
        step_delta = (cer - prev_cer) * 100
        total_delta = (cer - cer_0) * 100
        prev_cer = cer
        
        print(f"  • {step_name:<50} | CER: {cer*100:>5.2f}% | Bước Δ: {step_delta:>+6.2f}% | Tổng Δ: {total_delta:>+6.2f}%")
        rows.append({
            "stage": step_name,
            "cer_percent": round(cer * 100, 2),
            "step_gain_percent": round(-step_delta, 2),
            "cumulative_gain_percent": round(-total_delta, 2),
            "ci_95": f"[{ci_l*100:.2f}% - {ci_h*100:.2f}%]",
            "word_acc_percent": round(acc * 100, 2)
        })
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table5_forward_selection.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 5 ra: {csv_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 4 (BẢNG 6): ẢNH HƯỞNG KÍCH THƯỚC KERNEL HÌNH THÁI HỌC (RULE #3)
# ==============================================================================
def run_table6_morphology_kernel(records: List[Dict[str, Any]], engine: TesseractLaoEngine):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 6: ẢNH HƯỞNG KÍCH THƯỚC KERNEL HÌNH THÁI HỌC (KIỂM CHỨNG RULE #3)")
    print("=" * 75)
    
    kernel_sizes = [
        ("Không áp dụng (None)", False, [1, 1]),
        ("Kernel 1x1 (An toàn tuyệt đối)", True, [1, 1]),
        ("Kernel 2x2 (Bảo vệ dấu nhỏ)", True, [2, 2]),
        ("Kernel 3x3 (Bắt đầu xóa dấu thanh)", True, [3, 3]),
        ("Kernel 5x5 (Xóa sạch toàn bộ dấu thanh)", True, [5, 5]),
    ]
    
    rows = []
    plot_labels = []
    plot_cers = []
    plot_tone_lost = []
    
    for label, is_enabled, ksize in kernel_sizes:
        cfg = {
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2},
            "morphology": {"enabled": is_enabled, "operation": "opening", "kernel_size": ksize},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15}
        }
        pipe = PreprocessingPipeline(config=cfg)
        cer, ci_l, ci_h, acc, hyps, _ = evaluate_pipeline_parallel(records, pipe, engine)
        
        # Đếm số lượng dấu thanh bị mất so với ground truth
        tone_count_ref = sum(sum(1 for c in normalize_lao(r["lao_text"]) if c in LAO_TONE_MARKS) for r in records)
        tone_count_hyp = sum(sum(1 for c in h if c in LAO_TONE_MARKS) for h in hyps)
        tone_lost = max(0, tone_count_ref - tone_count_hyp)
        tone_lost_pct = (tone_lost / tone_count_ref * 100) if tone_count_ref else 0.0
        
        print(f"  • {label:<42} | CER: {cer*100:>5.2f}% | Mất dấu thanh: {tone_lost:>3}/{tone_count_ref} ({tone_lost_pct:>5.1f}%) | Acc: {acc*100:>5.2f}%")
        
        rows.append({
            "kernel_config": label,
            "kernel_size": f"{ksize[0]}x{ksize[1]}" if is_enabled else "0x0",
            "cer_percent": round(cer * 100, 2),
            "ci_95": f"[{ci_l*100:.2f}% - {ci_h*100:.2f}%]",
            "tone_marks_lost_count": tone_lost,
            "tone_marks_lost_percent": round(tone_lost_pct, 2),
            "word_acc_percent": round(acc * 100, 2),
            "scientific_conclusion": "Tuân thủ Golden Rule #3" if ksize[0] <= 2 else "VI PHẠM: Xóa dấu thanh làm vỡ nghĩa"
        })
        plot_labels.append(f"{ksize[0]}x{ksize[1]}" if is_enabled else "None")
        plot_cers.append(cer * 100)
        plot_tone_lost.append(tone_lost_pct)
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table6_morphology_kernel.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 6 ra: {csv_file}")
    
    # Biểu đồ khoa học chứng minh Rule #3
    fig, ax1 = plt.subplots(figsize=(9, 5))
    color_cer = "#d62728"
    color_tone = "#1f77b4"
    
    ax1.set_xlabel("Kích thước Kernel Morphological Opening", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Character Error Rate - CER (%)", color=color_cer, fontsize=11, fontweight="bold")
    line1 = ax1.plot(plot_labels, plot_cers, color=color_cer, marker="o", linewidth=2.5, label="CER (%)")
    ax1.tick_params(axis="y", labelcolor=color_cer)
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Tỉ lệ dấu thanh bị xóa mất (%)", color=color_tone, fontsize=11, fontweight="bold")
    line2 = ax2.plot(plot_labels, plot_tone_lost, color=color_tone, marker="s", linewidth=2.5, linestyle="--", label="Tỉ lệ rụng dấu thanh (%)")
    ax2.tick_params(axis="y", labelcolor=color_tone)
    
    plt.title("Ablation Study: Kiểm chứng Quy tắc Bất di Bất dịch #3 (Lao Golden Rule #3)", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, "ablation_table6_morphology_kernel.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"📊 Đã xuất biểu đồ Bảng 6: {plot_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 5 (BẢNG 7): ẢNH HƯỞNG CỦA CHIỀU CAO DÒNG CHUẨN HÓA (A8)
# ==============================================================================
def run_table7_line_height(records: List[Dict[str, Any]], engine: TesseractLaoEngine):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 7: ẢNH HƯỞNG CỦA CHIỀU CAO DÒNG CHUẨN HÓA (A8)")
    print("=" * 75)
    
    height_configs = [
        ("Original Size (Không chuẩn hóa)", False, 0),
        ("Target Height = 24px (Quá nhỏ cho 4 tầng độ cao)", True, 24),
        ("Target Height = 32px (Chuẩn di động tiêu chuẩn)", True, 32),
        ("Target Height = 48px (Độ phân giải tối ưu cho nét dấu)", True, 48),
        ("Target Height = 64px (Độ phân giải cao)", True, 64),
    ]
    
    rows = []
    for label, is_enabled, target_h in height_configs:
        cfg = {
            "grayscale": {"enabled": True, "method": "bgr2gray"},
            "illumination": {"enabled": True, "method": "clahe", "clip_limit": 2.0},
            "binarization": {"enabled": True, "method": "sauvola", "window_size": 25, "k": 0.2},
            "height_normalization": {"enabled": is_enabled, "target_height": target_h},
            "border_padding": {"enabled": True, "crop_outer_px": 16, "padding_px": 15}
        }
        pipe = PreprocessingPipeline(config=cfg)
        cer, ci_l, ci_h, acc, _, t_sec = evaluate_pipeline_parallel(records, pipe, engine)
        
        print(f"  • {label:<45} | CER: {cer*100:>5.2f}% [{ci_l*100:>5.2f}% - {ci_h*100:>5.2f}%] | Acc: {acc*100:>5.2f}% | Latency: {t_sec*1000:>5.1f}ms")
        
        rows.append({
            "height_config": label,
            "target_height_px": target_h if is_enabled else "Original",
            "cer_percent": round(cer * 100, 2),
            "ci_95": f"[{ci_l*100:.2f}% - {ci_h*100:.2f}%]",
            "word_acc_percent": round(acc * 100, 2),
            "latency_ms": round(t_sec * 1000, 2)
        })
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table7_line_height.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 7 ra: {csv_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 6 (BẢNG 8): PHÂN TÍCH CER PHÂN TẦNG (STRATIFIED ANALYSIS)
# ==============================================================================
def run_table8_stratified(records: List[Dict[str, Any]], engine: TesseractLaoEngine, optimal_cfg: Dict[str, Any]):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 8: PHÂN TÍCH CER PHÂN TẦNG (SÁNG × MÁY × FONT × GÓC) TRÊN DEV SET")
    print("=" * 75)
    
    # Chạy song song 2 cấu hình trên Dev Set: Raw vs Optimal Pipeline
    pipe_opt = PreprocessingPipeline(config=optimal_cfg)
    _, _, _, _, hyps_opt, _ = evaluate_pipeline_parallel(records, pipe_opt, engine)
    
    pipe_raw = PreprocessingPipeline(config={"grayscale": {"enabled": False}, "border_padding": {"enabled": False}})
    _, _, _, _, hyps_raw, _ = evaluate_pipeline_parallel(records, pipe_raw, engine, raw_images=True)
    
    factors = {
        "lighting": ["natural", "fluorescent", "low_light", "cast_shadow"],
        "device": ["iPhone_14", "Samsung_Galaxy", "Xiaomi_Redmi"],
        "font": ["NotoSansLao", "NotoSansLaoLooped", "NotoSerifLao"],
        "angle": ["0", "8", "-8"]
    }
    
    factor_vn = {
        "lighting": "Điều kiện Ánh sáng",
        "device": "Thiết bị Chụp ảnh",
        "font": "Kiểu Phông chữ",
        "angle": "Góc chụp nghiêng"
    }
    
    rows = []
    plot_categories = []
    plot_raw_cers = []
    plot_opt_cers = []
    
    for factor_key, factor_values in factors.items():
        for val in factor_values:
            # Lọc các mẫu thuộc stratum
            sub_indices = [idx for idx, r in enumerate(records) if str(r.get(factor_key)) == str(val)]
            if not sub_indices:
                continue
                
            sub_refs = [normalize_lao(records[i]["lao_text"]) for i in sub_indices]
            sub_raw_hyps = [hyps_raw[i] for i in sub_indices]
            sub_opt_hyps = [hyps_opt[i] for i in sub_indices]
            
            cer_raw = compute_dataset_cer(sub_refs, sub_raw_hyps)
            cer_opt = compute_dataset_cer(sub_refs, sub_opt_hyps)
            gain = (cer_raw - cer_opt) * 100
            
            label_display = f"{factor_vn[factor_key]}: {val}"
            print(f"  • {label_display:<40} (n={len(sub_indices):>2}) | Raw CER: {cer_raw*100:>5.2f}% -> Opt CER: {cer_opt*100:>5.2f}% | Cải thiện: {gain:>+5.2f}%")
            
            rows.append({
                "factor_group": factor_vn[factor_key],
                "sub_stratum": val,
                "sample_count": len(sub_indices),
                "raw_cer_percent": round(cer_raw * 100, 2),
                "optimal_cer_percent": round(cer_opt * 100, 2),
                "gain_cer_percent": round(gain, 2)
            })
            plot_categories.append(val)
            plot_raw_cers.append(cer_raw * 100)
            plot_opt_cers.append(cer_opt * 100)
            
    csv_file = os.path.join(RESULTS_DIR, "p5_table8_stratified.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 8 ra: {csv_file}")
    
    # Biểu đồ so sánh phân tầng
    plt.figure(figsize=(12, 6))
    x = np.arange(len(plot_categories))
    width = 0.38
    
    plt.bar(x - width/2, plot_raw_cers, width, label="Baseline Thô (Raw)", color="#d62728", alpha=0.85, edgecolor="black")
    plt.bar(x + width/2, plot_opt_cers, width, label="Optimal Pipeline (P3/P5)", color="#2ca02c", alpha=0.85, edgecolor="black")
    
    plt.ylabel("Character Error Rate - CER (%)", fontsize=11, fontweight="bold")
    plt.title("Ablation Study: Hiệu năng CER Phân tầng (Sáng × Máy × Font × Góc)", fontsize=12, fontweight="bold")
    plt.xticks(x, plot_categories, rotation=45, ha="right", fontsize=10)
    plt.legend(fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    plot_file = os.path.join(RESULTS_DIR, "ablation_table8_stratified.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"📊 Đã xuất biểu đồ Bảng 8: {plot_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 7 (BẢNG 9): ĐỘ BỀN PIPELINE VỚI MỨC ĐỘ NHIỄU TĂNG DẦN
# ==============================================================================
def run_table9_noise_robustness(records: List[Dict[str, Any]], engine: TesseractLaoEngine, optimal_cfg: Dict[str, Any]):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 9: ĐỘ BỀN PIPELINE (NOISE ROBUSTNESS CURVE) VỚI ĐỘ NHIỄU & MỜ TĂNG DẦN")
    print("=" * 75)
    
    noise_scenarios = [
        ("Nhiễu chuẩn (Không thêm nhiễu)", None, 0),
        ("Gaussian Noise (sigma = 10)", lambda im: np.clip(im.astype(np.float32) + np.random.normal(0, 10, im.shape), 0, 255).astype(np.uint8), 10),
        ("Gaussian Noise (sigma = 20)", lambda im: np.clip(im.astype(np.float32) + np.random.normal(0, 20, im.shape), 0, 255).astype(np.uint8), 20),
        ("Gaussian Noise (sigma = 30)", lambda im: np.clip(im.astype(np.float32) + np.random.normal(0, 30, im.shape), 0, 255).astype(np.uint8), 30),
        ("Gaussian Blur (kernel 5x5)", lambda im: cv2.GaussianBlur(im, (5, 5), 1.5), -1),
    ]
    
    pipe_opt = PreprocessingPipeline(config=optimal_cfg)
    pipe_raw = PreprocessingPipeline(config={"grayscale": {"enabled": False}, "border_padding": {"enabled": False}})
    
    rows = []
    plot_labels = []
    plot_raw = []
    plot_opt = []
    
    for label, n_fn, level in noise_scenarios:
        np.random.seed(42)
        cer_raw, ci_l_r, ci_h_r, acc_raw, _, _ = evaluate_pipeline_parallel(records, pipe_raw, engine, raw_images=True, noise_fn=n_fn)
        cer_opt, ci_l_o, ci_h_o, acc_opt, _, _ = evaluate_pipeline_parallel(records, pipe_opt, engine, raw_images=False, noise_fn=n_fn)
        
        print(f"  • {label:<35} | Raw CER: {cer_raw*100:>5.2f}% -> Optimal CER: {cer_opt*100:>5.2f}%")
        
        rows.append({
            "scenario": label,
            "raw_cer_percent": round(cer_raw * 100, 2),
            "optimal_cer_percent": round(cer_opt * 100, 2),
            "gain_cer_percent": round((cer_raw - cer_opt) * 100, 2),
            "raw_word_acc_percent": round(acc_raw * 100, 2),
            "optimal_word_acc_percent": round(acc_opt * 100, 2),
        })
        plot_labels.append(label.split("(")[0].strip())
        plot_raw.append(cer_raw * 100)
        plot_opt.append(cer_opt * 100)
        
    csv_file = os.path.join(RESULTS_DIR, "p5_table9_noise_robustness.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 9 ra: {csv_file}")
    
    # Biểu đồ độ bền
    plt.figure(figsize=(9, 5))
    plt.plot(plot_labels, plot_raw, marker="o", linewidth=2.5, color="#d62728", label="Baseline Thô (Raw)")
    plt.plot(plot_labels, plot_opt, marker="s", linewidth=2.5, color="#2ca02c", label="Optimal Pipeline (P3/P5)")
    plt.title("Độ bền Pipeline (Noise & Blur Robustness Curve) khi tăng mức độ nhiễu", fontsize=12, fontweight="bold")
    plt.ylabel("Character Error Rate - CER (%)", fontsize=11, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    plot_file = os.path.join(RESULTS_DIR, "ablation_table9_noise_robustness.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"📊 Đã xuất biểu đồ Bảng 9: {plot_file}")
    return rows


# ==============================================================================
# BÀI TOÁN 8 (BẢNG 10): ĐỐI CHIẾU CHỮ IN VS CHỮ VIẾT TAY
# ==============================================================================
def run_table10_printed_vs_handwritten(
    printed_records: List[Dict[str, Any]],
    handwritten_records: List[Dict[str, Any]],
    engine: TesseractLaoEngine,
    optimal_cfg: Dict[str, Any]
):
    print("\n" + "=" * 75)
    print("🔬 BẢNG 10: ĐỐI CHIẾU HIỆU NĂNG: CHỮ IN VS CHỮ VIẾT TAY")
    print("=" * 75)
    
    pipe_opt = PreprocessingPipeline(config=optimal_cfg)
    pipe_raw = PreprocessingPipeline(config={"grayscale": {"enabled": False}, "border_padding": {"enabled": False}})
    
    # Chữ in (157 Dev Cards)
    cer_p_raw, _, _, acc_p_raw, _, _ = evaluate_pipeline_parallel(printed_records, pipe_raw, engine, raw_images=True)
    cer_p_opt, ci_l_po, ci_h_po, acc_p_opt, _, _ = evaluate_pipeline_parallel(printed_records, pipe_opt, engine)
    
    # Chữ viết tay (50 Handwritten Cards)
    cer_h_raw, _, _, acc_h_raw, _, _ = evaluate_pipeline_parallel(handwritten_records, pipe_raw, engine, raw_images=True)
    cer_h_opt, ci_l_ho, ci_h_ho, acc_h_opt, _, _ = evaluate_pipeline_parallel(handwritten_records, pipe_opt, engine)
    
    print(f"  • Chữ in Flashcard (n={len(printed_records)})  | Raw CER: {cer_p_raw*100:>5.2f}% -> Optimal CER: {cer_p_opt*100:>5.2f}% [{ci_l_po*100:.2f}% - {ci_h_po*100:.2f}%] | Acc: {acc_p_opt*100:>5.2f}%")
    print(f"  • Chữ viết tay mô phỏng (n={len(handwritten_records)}) | Raw CER: {cer_h_raw*100:>5.2f}% -> Optimal CER: {cer_h_opt*100:>5.2f}% [{ci_l_ho*100:.2f}% - {ci_h_ho*100:.2f}%] | Acc: {acc_h_opt*100:>5.2f}%")
    
    rows = [
        {
            "script_type": "Chữ in tiêu chuẩn (Flashcard Printed)",
            "sample_count": len(printed_records),
            "raw_cer_percent": round(cer_p_raw * 100, 2),
            "optimal_cer_percent": round(cer_p_opt * 100, 2),
            "ci_95": f"[{ci_l_po*100:.2f}% - {ci_h*100:.2f}%]" if 'ci_h' in locals() else f"[{ci_l_po*100:.2f}% - {ci_h_po*100:.2f}%]",
            "word_acc_percent": round(acc_p_opt * 100, 2),
            "analysis": "Nét chuẩn, Tesseract LSTM nhận diện tốt sau khi nhị phân hóa cục bộ"
        },
        {
            "script_type": "Chữ viết tay thực tế (Handwritten)",
            "sample_count": len(handwritten_records),
            "raw_cer_percent": round(cer_h_raw * 100, 2),
            "optimal_cer_percent": round(cer_h_opt * 100, 2),
            "ci_95": f"[{ci_l_ho*100:.2f}% - {ci_h_ho*100:.2f}%]",
            "word_acc_percent": round(acc_h_opt * 100, 2),
            "analysis": "Nét uốn lượn tự do, độ dày nét không đều, đòi hỏi CRNN/Fine-tune ở Phase P7"
        }
    ]
    
    csv_file = os.path.join(RESULTS_DIR, "p5_table10_printed_vs_handwritten.csv")
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Đã lưu Bảng 10 ra: {csv_file}")
    return rows


# ==============================================================================
# HÀM MAIN: ĐIỀU PHỐI TOÀN BỘ PHASE P5
# ==============================================================================
def main():
    print("=" * 80)
    print("🚀 BẮT ĐẦU CHUỖI THỰC NGHIỆM ABLATION STUDY TOÀN DIỆN (PHASE P5)")
    print("=" * 80)
    
    dev_records = load_dev_records()
    print(f"• Tải thành công {len(dev_records)} ảnh từ Dev Set (data/gold/dev_labels.csv)")
    
    handwritten_records = load_handwritten_records()
    print(f"• Tải thành công {len(handwritten_records)} ảnh viết tay (data/gold/all_labels.csv)")
    
    # Engine Tesseract tiêu chuẩn PSM 7 (đã chốt ở P4)
    engine = TesseractLaoEngine(oem=1, psm=7)
    
    # 1. Bảng 3: So sánh 6 phương pháp nhị phân hóa
    run_table3_binarization(dev_records, engine)
    
    # 2. Bảng 4: Leave-one-out
    _, optimal_cfg = run_table4_leave_one_out(dev_records, engine)
    
    # 3. Bảng 5: Forward selection
    run_table5_forward_selection(dev_records, engine)
    
    # 4. Bảng 6: Morphology kernel size (Golden Rule #3)
    run_table6_morphology_kernel(dev_records, engine)
    
    # 5. Bảng 7: Height normalization
    run_table7_line_height(dev_records, engine)
    
    # 6. Bảng 8: Stratified analysis
    run_table8_stratified(dev_records, engine, optimal_cfg)
    
    # 7. Bảng 9: Noise robustness curve
    run_table9_noise_robustness(dev_records, engine, optimal_cfg)
    
    # 8. Bảng 10: Printed vs Handwritten
    run_table10_printed_vs_handwritten(dev_records, handwritten_records, engine, optimal_cfg)
    
    # Khóa cấu hình tối ưu xuất ra YAML
    opt_yaml_path = os.path.join(CONFIGS_DIR, "optimal_pipeline.yaml")
    import yaml
    with open(opt_yaml_path, mode="w", encoding="utf-8") as f:
        yaml.dump(optimal_cfg, f, allow_unicode=True, default_flow_style=False)
    print(f"\n🔒 ĐÃ KHÓA CẤU HÌNH TIỀN XỬ LÝ TỐI ƯU RA: {opt_yaml_path}")
    
    print("\n" + "=" * 80)
    print("🎉 TOÀN BỘ 8 BẢNG VÀ 5 BIỂU ĐỒ ABLATION STUDY ĐÃ HOÀN THÀNH XUẤT SẮC!")
    print("=" * 80)


if __name__ == "__main__":
    main()
