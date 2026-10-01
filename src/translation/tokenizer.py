"""
Module Phân Đoạn Từ Tiếng Lào (Lao Word Tokenization).
Do tiếng Lào là chữ viết Abugida không có khoảng trắng giữa các từ,
module này triển khai giải thuật Maximum Matching (Khớp chuỗi cực đại)
kết hợp cấu trúc tiền tố Trie và từ điển giáo trình 1,200 mục từ.
Đồng thời cung cấp hàm tính toán F1-Score biên giới từ (Word Boundary Metrics).
"""
import os
import sys
import csv
from typing import List, Set, Tuple, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class LaoTokenizer:
    def __init__(self, dict_path: Optional[str] = None):
        """Khởi tạo Tokenizer với cây Trie từ điển từ vựng tiếng Lào."""
        self.root = TrieNode()
        self.vocab: Set[str] = set()
        self.max_word_len = 0
        
        default_dict = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
        path_to_load = dict_path or default_dict
        self._load_vocab(path_to_load)

    def _load_vocab(self, dict_path: str):
        if not os.path.exists(dict_path):
            return
            
        with open(dict_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = normalize_lao(row.get("lao", "").strip())
                if word:
                    self.add_word(word)

    def add_word(self, word: str):
        """Thêm một từ vào cây Trie."""
        norm_word = normalize_lao(word)
        if not norm_word:
            return
            
        self.vocab.add(norm_word)
        if len(norm_word) > self.max_word_len:
            self.max_word_len = len(norm_word)
            
        node = self.root
        for char in norm_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def tokenize(self, text: str) -> List[str]:
        """
        Phân đoạn chuỗi tiếng Lào thành danh sách từ bằng giải thuật
        Longest Matching (Khớp chuỗi cực đại từ trái qua phải).
        """
        norm_text = normalize_lao(text)
        if not norm_text:
            return []
            
        tokens = []
        i = 0
        n = len(norm_text)
        
        while i < n:
            # Bỏ qua khoảng trắng nếu có
            if norm_text[i].isspace():
                i += 1
                continue
                
            node = self.root
            longest_match_end = -1
            curr_idx = i
            
            # Quét tìm từ dài nhất trong Trie
            while curr_idx < n and norm_text[curr_idx] in node.children:
                node = node.children[norm_text[curr_idx]]
                curr_idx += 1
                if node.is_word:
                    longest_match_end = curr_idx
                    
            if longest_match_end != -1:
                # Khớp được từ trong từ điển
                token = norm_text[i:longest_match_end]
                tokens.append(token)
                i = longest_match_end
            else:
                # Ký tự OOV ngoài từ điển hoặc phụ âm lẻ
                # Gom ít nhất 1 cụm ký tự không thể tách rời (phụ âm + nguyên âm)
                step = 1
                # Kiểm tra nếu ký tự kế tiếp là nguyên âm tầng trên/dưới hoặc dấu thanh
                while (i + step < n) and (norm_text[i + step] in "່້໊໋໌ໍະາຳິີຶືຸູົຼຽ"):
                    step += 1
                tokens.append(norm_text[i:i + step])
                i += step
                
        return tokens


def compute_boundary_indices(text: str, tokens: List[str]) -> Set[int]:
    """Lấy tập vị trí chỉ số biên giới phân đoạn từ (Word Boundary Indices)."""
    boundaries = set()
    current_pos = 0
    for tok in tokens[:-1]:
        current_pos += len(tok)
        boundaries.add(current_pos)
    return boundaries


def compute_tokenization_f1(gold_tokens_list: List[List[str]], pred_tokens_list: List[List[str]]) -> Tuple[float, float, float]:
    """
    Tính Precision, Recall và F1-Score cho bài toán phân đoạn từ tiếng Lào.
    Dựa trên sự trùng khớp của các biên giới từ (Word Boundaries).
    """
    total_gold_boundaries = 0
    total_pred_boundaries = 0
    total_true_positives = 0
    
    for gold_tokens, pred_tokens in zip(gold_tokens_list, pred_tokens_list):
        full_gold_text = "".join(gold_tokens)
        full_pred_text = "".join(pred_tokens)
        
        gold_b = compute_boundary_indices(full_gold_text, gold_tokens)
        pred_b = compute_boundary_indices(full_pred_text, pred_tokens)
        
        total_gold_boundaries += len(gold_b)
        total_pred_boundaries += len(pred_b)
        total_true_positives += len(gold_b.intersection(pred_b))
        
    prec = total_true_positives / max(total_pred_boundaries, 1)
    rec = total_true_positives / max(total_gold_boundaries, 1)
    f1 = (2 * prec * rec) / max(prec + rec, 1e-6)
    
    return prec, rec, f1
