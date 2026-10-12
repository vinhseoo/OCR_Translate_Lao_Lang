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
from typing import List, Dict, Any, Optional, Tuple
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

    def translate_full_paragraph(self, paragraph_text: str) -> Tuple[str, str, List[WordGloss]]:
        """
        Dịch toàn bộ đoạn văn bản tiếng Lào sang Tiếng Việt và Tiếng Anh trôi chảy theo ngữ cảnh.
        Đồng thời bóc tách toàn bộ từ vựng giáo trình có trong bài để phục vụ học tập.
        """
        norm_para = normalize_lao(paragraph_text).strip()
        if not norm_para:
            return "", "", []

        lines = [l.strip() for l in norm_para.splitlines() if l.strip()]
        vi_results = []
        en_results = []
        all_glosses: List[WordGloss] = []
        seen_words = set()

        import requests

        for line in lines:
            line_vi = ""
            line_en = ""

            # 1. Thử dịch câu trôi chảy qua Machine Translation API
            try:
                res_vi = requests.get(
                    "https://clients5.google.com/translate_a/t",
                    params={"client": "dict-chrome-ex", "sl": "lo", "tl": "vi", "q": line},
                    timeout=4
                )
                if res_vi.status_code == 200:
                    data = res_vi.json()
                    line_vi = data[0] if isinstance(data, list) and len(data) > 0 else ""
            except Exception:
                pass

            try:
                res_en = requests.get(
                    "https://clients5.google.com/translate_a/t",
                    params={"client": "dict-chrome-ex", "sl": "lo", "tl": "en", "q": line},
                    timeout=4
                )
                if res_en.status_code == 200:
                    data = res_en.json()
                    line_en = data[0] if isinstance(data, list) and len(data) > 0 else ""
            except Exception:
                pass

            # 2. Bóc tách từ vựng qua từ điển nội bộ
            line_out = self.translate(line)
            if not line_vi:
                line_vi = line_out.translation_vi
            if not line_en:
                line_en = line_out.translation_en

            vi_results.append(line_vi)
            en_results.append(line_en)

            for g in line_out.glosses:
                if g.in_dict and g.lao not in seen_words:
                    all_glosses.append(g)
                    seen_words.add(g.lao)

        full_vi = "\n".join(vi_results)
        full_en = "\n".join(en_results)
        return full_vi, full_en, all_glosses

