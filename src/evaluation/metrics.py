"""
Module đánh giá độ chính xác nhận dạng OCR (CER, WER, Word Acc, Bootstrap CI).
Tất cả các hàm tính toán đều tự động chuẩn hóa qua normalize_lao().
"""
from typing import List, Tuple, Dict, Any
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    import random
    import math

from src.preprocessing.normalize import normalize_lao


def levenshtein_distance(s1: str, s2: str) -> int:
    """Tính khoảng cách Levenshtein cơ bản giữa 2 chuỗi ký tự."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
            
    return dp[m][n]


def compute_cer(reference: str, hypothesis: str, auto_normalize: bool = True) -> float:
    """
    Tính Character Error Rate (CER) = Levenshtein(ref, hyp) / len(ref).
    Nếu reference rỗng và hyp rỗng -> 0.0; nếu ref rỗng và hyp có chữ -> 1.0.
    """
    if auto_normalize:
        ref = normalize_lao(reference)
        hyp = normalize_lao(hypothesis)
    else:
        ref = reference
        hyp = hypothesis
        
    if len(ref) == 0:
        return 0.0 if len(hyp) == 0 else 1.0
        
    dist = levenshtein_distance(ref, hyp)
    return float(dist) / len(ref)


def compute_dataset_cer(references: List[str], hypotheses: List[str]) -> float:
    """
    Tính CER vĩ mô toàn tập dữ liệu: tổng khoảng cách / tổng số ký tự reference.
    """
    total_dist = 0
    total_len = 0
    for r, h in zip(references, hypotheses):
        ref = normalize_lao(r)
        hyp = normalize_lao(h)
        total_dist += levenshtein_distance(ref, hyp)
        total_len += len(ref)
        
    return float(total_dist) / max(total_len, 1)


def compute_word_accuracy(references: List[str], hypotheses: List[str]) -> float:
    """Tính tỉ lệ từ đúng tuyệt đối (Exact Match Rate)."""
    if not references:
        return 0.0
    correct = 0
    for r, h in zip(references, hypotheses):
        if normalize_lao(r) == normalize_lao(h):
            correct += 1
    return float(correct) / len(references)


def bootstrap_cer_confidence_interval(
    references: List[str],
    hypotheses: List[str],
    n_resamples: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42
) -> Tuple[float, float, float]:
    """
    Tính khoảng tin cậy Bootstrap cho CER (Bootstrap Confidence Interval).
    Trả về: (Mean CER, Lower Bound, Upper Bound).
    """
    n = len(references)
    if n == 0:
        return 0.0, 0.0, 0.0
        
    boot_cers = []
    
    if HAS_NUMPY:
        np.random.seed(seed)
        indices = np.arange(n)
        for _ in range(n_resamples):
            sample_idx = np.random.choice(indices, size=n, replace=True)
            sample_refs = [references[i] for i in sample_idx]
            sample_hyps = [hypotheses[i] for i in sample_idx]
            boot_cers.append(compute_dataset_cer(sample_refs, sample_hyps))
            
        alpha = (1.0 - confidence_level) / 2.0
        lower = float(np.percentile(boot_cers, alpha * 100))
        upper = float(np.percentile(boot_cers, (1.0 - alpha) * 100))
        mean_val = float(np.mean(boot_cers))
    else:
        rng = random.Random(seed)
        indices = list(range(n))
        for _ in range(n_resamples):
            sample_idx = [rng.choice(indices) for _ in range(n)]
            sample_refs = [references[i] for i in sample_idx]
            sample_hyps = [hypotheses[i] for i in sample_idx]
            boot_cers.append(compute_dataset_cer(sample_refs, sample_hyps))
            
        boot_cers.sort()
        alpha = (1.0 - confidence_level) / 2.0
        lower_idx = int(alpha * len(boot_cers))
        upper_idx = int((1.0 - alpha) * len(boot_cers))
        upper_idx = min(upper_idx, len(boot_cers) - 1)
        lower = float(boot_cers[lower_idx])
        upper = float(boot_cers[upper_idx])
        mean_val = float(sum(boot_cers) / len(boot_cers))
        
    return mean_val, lower, upper

