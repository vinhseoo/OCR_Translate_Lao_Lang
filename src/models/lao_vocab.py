"""
Bộ Từ Điển Ký Tự Tiếng Lào (Lao Character Vocabulary & CTC Mapping).
Bao gồm toàn bộ phụ âm, nguyên âm, dấu thanh, chữ số và ký hiệu đặc biệt
theo chuẩn Unicode U+0E81 đến U+0EDD, với chuẩn hóa Unicode NFC bắt buộc.
"""
from typing import List, Dict, Tuple
from src.preprocessing.normalize import normalize_lao

# Danh sách đầy đủ toàn bộ ký tự tiếng Lào chuẩn Unicode
LAO_CONSONANTS = [
    "ກ", "ຂ", "ຄ", "ງ", "ຈ", "ສ", "ຊ", "ຍ", "ດ", "ຕ", "ຖ", "ທ", "ນ", "ບ", "ປ", "ຜ", "ຝ", "ພ", "ຟ", "ມ", "ຢ", "ຣ", "ລ", "ວ", "ສ", "ຫ", "ອ", "ຮ"
]
LAO_VOWELS = [
    "ະ", "າ", "ຳ", "ິ", "ີ", "ຶ", "ື", "ຸ", "ູ", "ົ", "ຼ", "ຽ", "ເ", "ແ", "ໂ", "ໃ", "ໄ"
]
LAO_TONE_MARKS = [
    "່", "້", "໊", "໋", "໌", "ໍ"
]
LAO_LIGATURES = [
    "ໜ", "ໝ"
]
LAO_DIGITS = [
    "໐", "໑", "໒", "໓", "໔", "໕", "໖", "໗", "໘", "໙"
]
LAO_PUNCTUATIONS = [
    " ", "-", "/", "(", ")", ".", ",", "?", "!", "\"", "'"
]


class LaoVocabulary:
    def __init__(self):
        """Khởi tạo từ điển ký tự với index 0 dành riêng cho CTC Blank."""
        self.blank_char = "<blank>"
        self.unk_char = "<unk>"
        
        # Gom các ký tự duy nhất
        unique_chars = []
        for ch in LAO_CONSONANTS + LAO_VOWELS + LAO_TONE_MARKS + LAO_LIGATURES + LAO_DIGITS + LAO_PUNCTUATIONS:
            norm_ch = normalize_lao(ch)
            if norm_ch and norm_ch not in unique_chars:
                unique_chars.append(norm_ch)
                
        # 0: CTC Blank, 1: Unknown, tiếp theo là bảng ký tự
        self.idx2char: List[str] = [self.blank_char, self.unk_char] + unique_chars
        self.char2idx: Dict[str, int] = {c: i for i, c in enumerate(self.idx2char)}
        
        self.blank_idx = 0
        self.unk_idx = 1
        self.num_classes = len(self.idx2char)

    def encode(self, text: str) -> List[int]:
        """Chuyển chuỗi text sang danh sách index (sau khi ép chuẩn NFC)."""
        norm_text = normalize_lao(text)
        return [self.char2idx.get(c, self.unk_idx) for c in norm_text]

    def decode(self, indices: List[int]) -> str:
        """Chuyển danh sách index về text (bỏ qua blank và unk)."""
        chars = []
        for idx in indices:
            if idx == self.blank_idx:
                continue
            if idx < len(self.idx2char):
                ch = self.idx2char[idx]
                if ch != self.unk_char:
                    chars.append(ch)
        return normalize_lao("".join(chars))

    def ctc_greedy_decode(self, logits_seq: List[int]) -> str:
        """
        Giải mã tham lam CTC (Collapses consecutive duplicates and removes blank 0).
        Input: Chuỗi nhãn có độ dài T từ argmax của logits.
        Output: Chuỗi văn bản tiếng Lào chuẩn hóa.
        """
        prev_idx = -1
        collapsed = []
        for idx in logits_seq:
            if idx != prev_idx:
                if idx != self.blank_idx:
                    collapsed.append(idx)
                prev_idx = idx
        return self.decode(collapsed)


# Khởi tạo singleton mặc định
DEFAULT_LAO_VOCAB = LaoVocabulary()
