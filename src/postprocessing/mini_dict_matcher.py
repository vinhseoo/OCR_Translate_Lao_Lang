"""
Module tra cứu từ điển mini cho Phase P1 (Spike).
Khớp chuỗi chính xác sau khi đã chuẩn hóa qua normalize_lao().
"""
import os
import csv
from typing import Dict, Any, Optional
from src.preprocessing.normalize import normalize_lao
from src.evaluation.metrics import levenshtein_distance


class MiniDictMatcher:
    def __init__(self, dict_path: Optional[str] = None):
        if dict_path is None:
            dict_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "dictionaries", "mini_dict.csv"
            )
        self.dict_path = os.path.abspath(dict_path)
        self.entries: Dict[str, Dict[str, str]] = {}
        self._load_dictionary()

    def _load_dictionary(self):
        if not os.path.exists(self.dict_path):
            raise FileNotFoundError(f"Không tìm thấy file từ điển tại: {self.dict_path}")
            
        with open(self.dict_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                norm_lao = normalize_lao(row["lao"])
                self.entries[norm_lao] = {
                    "lao": norm_lao,
                    "vi": row.get("vi", "").strip(),
                    "en": row.get("en", "").strip(),
                    "romanization": row.get("romanization", "").strip(),
                    "type": row.get("type", "").strip()
                }

    def lookup(self, text: str) -> Dict[str, Any]:
        """
        Tra cứu từ vựng:
        - Ưu tiên 1: Khớp chuỗi chính xác 100% -> Confidence 1.0
        - Ưu tiên 2: Tìm từ gần nhất trong từ điển mini theo Levenshtein Distance
        """
        norm_query = normalize_lao(text)
        
        # 1. Khớp chính xác
        if norm_query in self.entries:
            res = dict(self.entries[norm_query])
            res["confidence"] = 1.0
            res["match_type"] = "exact"
            return res
            
        # 2. Khớp gần đúng (Fuzzy fallback)
        best_match = None
        min_dist = 999
        for lao_word, data in self.entries.items():
            dist = levenshtein_distance(norm_query, lao_word)
            if dist < min_dist:
                min_dist = dist
                best_match = data
                
        if best_match and len(norm_query) > 0:
            # Ước tính độ tin cậy dựa trên edit distance
            confidence = max(0.0, 1.0 - (min_dist / max(len(norm_query), len(best_match["lao"]))))
            res = dict(best_match)
            res["recognized_raw"] = norm_query
            res["confidence"] = round(confidence, 2)
            res["match_type"] = "fuzzy"
            res["edit_distance"] = min_dist
            return res
            
        return {
            "lao": norm_query,
            "vi": "Chưa có trong từ điển",
            "en": "Unknown",
            "romanization": "",
            "type": "unknown",
            "confidence": 0.0,
            "match_type": "none"
        }
