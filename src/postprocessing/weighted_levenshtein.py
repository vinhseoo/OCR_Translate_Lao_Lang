"""
Thuật toán Weighted Levenshtein Distance bằng Quy Hoạch Động (Dynamic Programming).
Đóng góp khoa học #2: Tích hợp ma trận chi phí thực nghiệm từ confusion_pairs.csv
và phạt giảm trừ đặc thù cho dấu thanh / nguyên âm tầng trên dưới của tiếng Lào.
"""
import os
import csv
from typing import Dict, Tuple, Optional
from src.preprocessing.normalize import (
    normalize_lao,
    LAO_TONE_MARKS,
    LAO_ABOVE_VOWELS,
    LAO_BELOW_VOWELS,
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_CONFUSION_CSV = os.path.join(PROJECT_ROOT, "experiments", "results", "confusion_pairs.csv")


class WeightedLevenshtein:
    def __init__(
        self,
        confusion_csv_path: Optional[str] = None,
        tone_penalty: float = 0.2,
        tier_vowel_penalty: float = 0.4,
        default_sub_cost: float = 1.0,
        default_del_cost: float = 1.0,
        default_ins_cost: float = 1.0,
    ):
        """
        Khởi tạo bộ tính khoảng cách Levenshtein có trọng số:
        Args:
            confusion_csv_path: Đường dẫn tới confusion_pairs.csv (sinh từ P4).
            tone_penalty: Trọng số phạt khi mất/thừa dấu thanh tầng 4 (mặc định 0.2 thay vì 1.0).
            tier_vowel_penalty: Trọng số phạt khi mất/thừa nguyên âm tầng 1, 3 (mặc định 0.4).
            default_sub_cost: Chi phí thay thế ký tự thông thường.
        """
        self.tone_penalty = tone_penalty
        self.tier_vowel_penalty = tier_vowel_penalty
        self.default_sub_cost = default_sub_cost
        self.default_del_cost = default_del_cost
        self.default_ins_cost = default_ins_cost
        
        self.sub_costs: Dict[Tuple[str, str], float] = {}
        csv_path = confusion_csv_path or DEFAULT_CONFUSION_CSV
        if os.path.exists(csv_path):
            self._load_confusion_costs(csv_path)

    def _load_confusion_costs(self, csv_path: str):
        """Nạp chi phí thay thế từ tệp CSV ma trận nhầm lẫn thực nghiệm."""
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ref = row.get("char_ref", "")
                hyp = row.get("char_hyp", "")
                if ref and hyp:
                    try:
                        cost = float(row.get("cost", 1.0))
                        self.sub_costs[(ref, hyp)] = cost
                        # Gán đối xứng nếu chiều ngược lại chưa có
                        if (hyp, ref) not in self.sub_costs:
                            self.sub_costs[(hyp, ref)] = cost
                    except ValueError:
                        pass

    def get_insertion_cost(self, char: str) -> float:
        """Chi phí chèn ký tự char."""
        if char in LAO_TONE_MARKS:
            return self.tone_penalty
        if char in LAO_ABOVE_VOWELS or char in LAO_BELOW_VOWELS:
            return self.tier_vowel_penalty
        return self.default_ins_cost

    def get_deletion_cost(self, char: str) -> float:
        """Chi phí xóa ký tự char (mất nét)."""
        if char in LAO_TONE_MARKS:
            return self.tone_penalty
        if char in LAO_ABOVE_VOWELS or char in LAO_BELOW_VOWELS:
            return self.tier_vowel_penalty
        return self.default_del_cost

    def get_substitution_cost(self, c1: str, c2: str) -> float:
        """Chi phí thay thế ký tự c1 thành c2."""
        if c1 == c2:
            return 0.0
        # Tra cứu ma trận nhầm lẫn thực nghiệm
        if (c1, c2) in self.sub_costs:
            return self.sub_costs[(c1, c2)]
        return self.default_sub_cost

    def distance(self, s1: str, s2: str) -> float:
        """
        Tính khoảng cách Levenshtein có trọng số bằng Dynamic Programming:
        Mọi chuỗi đều được chuẩn hóa Unicode NFC trước khi tính.
        """
        s1 = normalize_lao(s1)
        s2 = normalize_lao(s2)
        
        m = len(s1)
        n = len(s2)
        
        if m == 0 and n == 0:
            return 0.0
        if m == 0:
            return sum(self.get_insertion_cost(c) for c in s2)
        if n == 0:
            return sum(self.get_deletion_cost(c) for c in s1)
            
        # Ma trận quy hoạch động (m + 1) x (n + 1)
        dp = [[0.0] * (n + 1) for _ in range(m + 1)]
        
        # Khởi tạo cột 0 (deletions)
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] + self.get_deletion_cost(s1[i - 1])
            
        # Khởi tạo hàng 0 (insertions)
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] + self.get_insertion_cost(s2[j - 1])
            
        # Điền bảng quy hoạch động
        for i in range(1, m + 1):
            c1 = s1[i - 1]
            for j in range(1, n + 1):
                c2 = s2[j - 1]
                
                cost_del = dp[i - 1][j] + self.get_deletion_cost(c1)
                cost_ins = dp[i][j - 1] + self.get_insertion_cost(c2)
                cost_sub = dp[i - 1][j - 1] + self.get_substitution_cost(c1, c2)
                
                dp[i][j] = min(cost_del, cost_ins, cost_sub)
                
        return round(dp[m][n], 4)

    def similarity(self, s1: str, s2: str) -> float:
        """
        Tính điểm tương đồng chuẩn hóa trong khoảng [0.0, 1.0]:
        1.0 - (dist / max(len(s1), len(s2)))
        """
        s1 = normalize_lao(s1)
        s2 = normalize_lao(s2)
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        dist = self.distance(s1, s2)
        return max(0.0, round(1.0 - (dist / max_len), 4))


def standard_levenshtein(s1: str, s2: str) -> int:
    """Khoảng cách Levenshtein tiêu chuẩn (đồng nhất chi phí = 1)."""
    s1 = normalize_lao(s1)
    s2 = normalize_lao(s2)
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]
