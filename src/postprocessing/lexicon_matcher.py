"""
Bộ Khớp Từ Điển Thông Minh (Lexicon Snap Engine).
Tận dụng không gian từ vựng đóng của giáo trình tiếng Lào (528 mục từ)
để khôi phục các từ bị biến dạng nét hoặc mất dấu thanh qua Weighted Levenshtein.
"""
import os
import csv
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

from src.preprocessing.normalize import normalize_lao
from src.postprocessing.weighted_levenshtein import WeightedLevenshtein, standard_levenshtein

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DICT_PATH = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")


@dataclass
class Candidate:
    lao: str
    distance: float
    confidence: float
    vi: str
    en: str
    romanization: str
    pos: str
    lesson: str


@dataclass
class MatchResult:
    query: str
    best_lao: str
    best_vi: str
    best_en: str
    best_romanization: str
    confidence: float
    is_exact: bool
    is_confident: bool
    top_candidates: List[Candidate]


class LexiconMatcher:
    def __init__(
        self,
        dict_path: Optional[str] = None,
        confusion_csv_path: Optional[str] = None,
        max_entries: Optional[int] = None,
        confidence_threshold: float = 0.55
    ):
        """
        Khởi tạo Lexicon Matcher:
        Args:
            dict_path: Đường dẫn tệp từ điển CSV.
            confusion_csv_path: Đường dẫn tệp confusion_pairs.csv cho Weighted Levenshtein.
            max_entries: Giới hạn số mục từ (phục vụ Ablation Study Bảng 13: 100, 250, 528 từ).
            confidence_threshold: Ngưỡng tin cậy tối thiểu để chấp nhận từ (dưới ngưỡng -> cảnh báo).
        """
        self.dict_path = dict_path or DEFAULT_DICT_PATH
        self.confidence_threshold = confidence_threshold
        self.weighted_engine = WeightedLevenshtein(confusion_csv_path=confusion_csv_path)
        
        self.entries: List[Dict[str, str]] = []
        self.exact_map: Dict[str, Dict[str, str]] = {}
        self._load_dictionary(self.dict_path, max_entries=max_entries)

    def _load_dictionary(self, path: str, max_entries: Optional[int] = None):
        """Nạp dữ liệu từ điển CSV với chuẩn hóa Unicode NFC."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Không tìm thấy tệp từ điển: {path}")
            
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, r in enumerate(reader):
                if max_entries and idx >= max_entries:
                    break
                clean_entry = {k: (v.strip() if v else "") for k, v in r.items()}
                lao_norm = normalize_lao(clean_entry.get("lao", ""))
                clean_entry["lao"] = lao_norm
                self.entries.append(clean_entry)
                self.exact_map[lao_norm] = clean_entry

    def match(
        self,
        query: str,
        method: str = "weighted_levenshtein",
        top_k: int = 5
    ) -> MatchResult:
        """
        Thực hiện khớp mờ từ OCR thô vào từ điển giáo trình:
        Các phương pháp hỗ trợ:
          - 'weighted_levenshtein' (Đề xuất chính trong nghiên cứu - P6)
          - 'standard_levenshtein' (Đối chứng Baseline không trọng số)
          - 'ngram' (Đối chứng mô hình ngôn ngữ n-gram)
        """
        q_norm = normalize_lao(query.strip())
        
        # 1. Kiểm tra khớp chính xác tuyệt đối (Exact Match - O(1))
        if q_norm in self.exact_map:
            e = self.exact_map[q_norm]
            cand = Candidate(
                lao=e["lao"],
                distance=0.0,
                confidence=1.0,
                vi=e.get("vi", ""),
                en=e.get("en", ""),
                romanization=e.get("romanization", ""),
                pos=e.get("pos", ""),
                lesson=e.get("lesson", "")
            )
            return MatchResult(
                query=query,
                best_lao=e["lao"],
                best_vi=e.get("vi", ""),
                best_en=e.get("en", ""),
                best_romanization=e.get("romanization", ""),
                confidence=1.0,
                is_exact=True,
                is_confident=True,
                top_candidates=[cand]
            )
            
        # 2. Khớp mờ theo phương pháp chỉ định
        scored_candidates: List[Tuple[float, float, Dict[str, str]]] = []
        # (distance, confidence, entry)
        
        for e in self.entries:
            target = e["lao"]
            max_len = max(len(q_norm), len(target)) or 1
            
            if method == "weighted_levenshtein":
                dist = self.weighted_engine.distance(q_norm, target)
                conf = max(0.0, round(1.0 - (dist / max_len), 4))
                scored_candidates.append((dist, conf, e))
                
            elif method == "standard_levenshtein":
                dist = float(standard_levenshtein(q_norm, target))
                conf = max(0.0, round(1.0 - (dist / max_len), 4))
                scored_candidates.append((dist, conf, e))
                
            elif method == "ngram":
                # Tính độ tương đồng n-gram Jaccard (n=2)
                sim = self._ngram_similarity(q_norm, target, n=2)
                dist = round(1.0 - sim, 4)
                conf = sim
                scored_candidates.append((dist, conf, e))
            else:
                raise ValueError(f"Không hỗ trợ phương pháp khớp: {method}")
                
        # Sắp xếp: khoảng cách nhỏ nhất trước, độ tin cậy cao nhất trước
        scored_candidates.sort(key=lambda item: (item[0], -item[1]))
        
        top_list: List[Candidate] = []
        for dist, conf, e in scored_candidates[:top_k]:
            top_list.append(Candidate(
                lao=e["lao"],
                distance=dist,
                confidence=conf,
                vi=e.get("vi", ""),
                en=e.get("en", ""),
                romanization=e.get("romanization", ""),
                pos=e.get("pos", ""),
                lesson=e.get("lesson", "")
            ))
            
        best = top_list[0] if top_list else None
        best_lao = best.lao if best else q_norm
        best_vi = best.vi if best else ""
        best_en = best.en if best else ""
        best_rom = best.romanization if best else ""
        best_conf = best.confidence if best else 0.0
        is_confident = best_conf >= self.confidence_threshold
        
        return MatchResult(
            query=query,
            best_lao=best_lao,
            best_vi=best_vi,
            best_en=best_en,
            best_romanization=best_rom,
            confidence=best_conf,
            is_exact=False,
            is_confident=is_confident,
            top_candidates=top_list
        )

    @staticmethod
    def _ngram_similarity(s1: str, s2: str, n: int = 2) -> float:
        """Độ đo Jaccard cấp n-gram ký tự."""
        if s1 == s2:
            return 1.0
        if len(s1) < n or len(s2) < n:
            return 1.0 if s1 == s2 else 0.0
            
        ngrams1 = Counter([s1[i:i+n] for i in range(len(s1) - n + 1)])
        ngrams2 = Counter([s2[i:i+n] for i in range(len(s2) - n + 1)])
        
        intersection = sum((ngrams1 & ngrams2).values())
        union = sum((ngrams1 | ngrams2).values())
        
        return round(intersection / union, 4) if union > 0 else 0.0
