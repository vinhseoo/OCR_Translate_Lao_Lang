"""
Module Dịch Thuật & Hỗ Trợ Học Tập Tiếng Lào (Lao Translation Engine).
Kết hợp bộ ba:
1. Phân đoạn từ (LaoTokenizer)
2. Phiên âm Latinh (LaoRomanizer)
3. Tra cứu từ điển giáo trình (LaoDictionary)
Hỗ trợ cả cấp độ từ vựng (Word Glosses), cụm từ (Phrases) và câu văn hoàn chỉnh
sang cả hai ngôn ngữ Tiếng Việt và Tiếng Anh.
"""
import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao
from src.translation.tokenizer import LaoTokenizer
from src.translation.romanizer import LaoRomanizer
from src.translation.dictionary_lookup import LaoDictionary


@dataclass
class WordGloss:
    """Chú giải chi tiết từng từ cho người học."""
    lao: str
    vi: str
    en: str
    pos: str
    romanization: str
    in_dict: bool
    example_lao: str = ""
    example_vi: str = ""


@dataclass
class TranslationOutput:
    """Kết quả dịch thuật và hỗ trợ học tập toàn diện."""
    original_lao: str
    tokens: List[str]
    romanization: str
    translation_vi: str
    translation_en: str
    glosses: List[WordGloss]
    is_exact_phrase: bool = False


class LaoTranslator:
    def __init__(self, dict_path: Optional[str] = None):
        """Khởi tạo hệ thống dịch thuật và hỗ trợ học tập tiếng Lào."""
        self.dictionary = LaoDictionary(dict_path)
        self.tokenizer = LaoTokenizer(dict_path)
        self.romanizer = LaoRomanizer(dict_path)

    def translate(self, text: str) -> TranslationOutput:
        """
        Dịch chuỗi văn bản tiếng Lào sang Tiếng Việt và Tiếng Anh.
        Đồng thời cung cấp phân đoạn từ, phiên âm và bảng chú giải từ điển.
        """
        norm_text = normalize_lao(text).strip()
        if not norm_text:
            return TranslationOutput(
                original_lao="",
                tokens=[],
                romanization="",
                translation_vi="",
                translation_en="",
                glosses=[],
                is_exact_phrase=False
            )

        # 1. Kiểm tra trường hợp khớp nguyên cụm/từ trong từ điển (Exact Match)
        exact_entry = self.dictionary.lookup(norm_text)
        if exact_entry:
            single_gloss = WordGloss(
                lao=norm_text,
                vi=exact_entry["vi"],
                en=exact_entry["en"],
                pos=exact_entry["pos"],
                romanization=exact_entry["romanization"],
                in_dict=True,
                example_lao=exact_entry["example_lao"],
                example_vi=exact_entry["example_vi"]
            )
            return TranslationOutput(
                original_lao=norm_text,
                tokens=[norm_text],
                romanization=exact_entry["romanization"],
                translation_vi=exact_entry["vi"],
                translation_en=exact_entry["en"],
                glosses=[single_gloss],
                is_exact_phrase=True
            )

        # 2. Phân đoạn từ (Word Tokenization)
        tokens = self.tokenizer.tokenize(norm_text)
        
        # 3. Phiên âm Latinh toàn câu
        full_romanization = self.romanizer.romanize(tokens)
        
        # 4. Tra cứu chú giải từng từ (Word Glosses)
        glosses = []
        vi_pieces = []
        en_pieces = []
        
        for tok in tokens:
            entry = self.dictionary.lookup(tok)
            if entry:
                vi_meaning = entry["vi"]
                # Lấy nghĩa đầu tiên nếu có nhiều nghĩa phân tách bởi '/'
                vi_short = vi_meaning.split("/")[0].strip()
                en_short = entry["en"].split("/")[0].strip()
                
                gloss = WordGloss(
                    lao=tok,
                    vi=vi_meaning,
                    en=entry["en"],
                    pos=entry["pos"],
                    romanization=entry["romanization"],
                    in_dict=True,
                    example_lao=entry["example_lao"],
                    example_vi=entry["example_vi"]
                )
                vi_pieces.append(vi_short)
                en_pieces.append(en_short)
            else:
                # Từ ngoài từ điển OOV
                tok_rom = self.romanizer.romanize_token(tok)
                gloss = WordGloss(
                    lao=tok,
                    vi=f"[{tok}]",
                    en=f"[{tok}]",
                    pos="unknown",
                    romanization=tok_rom,
                    in_dict=False
                )
                vi_pieces.append(tok)
                en_pieces.append(tok)
                
            glosses.append(gloss)

        # 5. Lắp ráp bản dịch tổng thể (Sentence-level assembly)
        translation_vi = " ".join(vi_pieces)
        translation_en = " ".join(en_pieces)

        return TranslationOutput(
            original_lao=norm_text,
            tokens=tokens,
            romanization=full_romanization,
            translation_vi=translation_vi,
            translation_en=translation_en,
            glosses=glosses,
            is_exact_phrase=False
        )
