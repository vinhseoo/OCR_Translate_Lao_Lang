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
        return translate_full_paragraph(paragraph_text, translator=self)


def translate_full_paragraph(paragraph_text: str, translator: Optional[LaoTranslator] = None) -> Tuple[str, str, List[WordGloss]]:
    """
    Hàm độc lập dịch toàn bộ đoạn văn bản tiếng Lào sang Tiếng Việt và Tiếng Anh trôi chảy theo ngữ cảnh.
    Tự động tương thích ngược, không phụ thuộc vào trạng thái cache của Streamlit instance.
    """
    norm_para = normalize_lao(paragraph_text).strip()
    if not norm_para:
        return "", "", []

    if translator is None or not hasattr(translator, "translate"):
        translator = LaoTranslator()

    lines = [l.strip() for l in norm_para.splitlines() if l.strip()]
    vi_results = []
    en_results = []
    all_glosses: List[WordGloss] = []
    seen_words = set()

    import requests

    # 1. Thử dịch toàn bộ đoạn văn bản cùng lúc để bảo toàn ngữ cảnh toàn bài
    full_vi = ""
    full_en = ""

    try:
        res_vi = requests.get(
            "https://clients5.google.com/translate_a/t",
            params={"client": "dict-chrome-ex", "sl": "lo", "tl": "vi", "q": norm_para},
            timeout=4
        )
        if res_vi.status_code == 200:
            data = res_vi.json()
            full_vi = data[0] if isinstance(data, list) and len(data) > 0 else ""
    except Exception:
        pass

    try:
        res_en = requests.get(
            "https://clients5.google.com/translate_a/t",
            params={"client": "dict-chrome-ex", "sl": "lo", "tl": "en", "q": norm_para},
            timeout=4
        )
        if res_en.status_code == 200:
            data = res_en.json()
            full_en = data[0] if isinstance(data, list) and len(data) > 0 else ""
    except Exception:
        pass

    # 2. Duyệt từng dòng để bóc tách từ vựng & làm dự phòng (fallback) nếu dịch toàn bài chưa có
    fallback_vi_lines = []
    fallback_en_lines = []

    for line in lines:
        line_vi = ""
        line_en = ""

        # Nếu chưa có bản dịch toàn bài, thử dịch từng dòng
        if not full_vi:
            try:
                r_vi = requests.get(
                    "https://clients5.google.com/translate_a/t",
                    params={"client": "dict-chrome-ex", "sl": "lo", "tl": "vi", "q": line},
                    timeout=3
                )
                if r_vi.status_code == 200:
                    d = r_vi.json()
                    line_vi = d[0] if isinstance(d, list) and len(d) > 0 else ""
            except Exception:
                pass

        if not full_en:
            try:
                r_en = requests.get(
                    "https://clients5.google.com/translate_a/t",
                    params={"client": "dict-chrome-ex", "sl": "lo", "tl": "en", "q": line},
                    timeout=3
                )
                if r_en.status_code == 200:
                    d = r_en.json()
                    line_en = d[0] if isinstance(d, list) and len(d) > 0 else ""
            except Exception:
                pass

        line_out = translator.translate(line)
        if not line_vi:
            line_vi = line_out.translation_vi
        if not line_en:
            line_en = line_out.translation_en

        fallback_vi_lines.append(line_vi)
        fallback_en_lines.append(line_en)

        for g in line_out.glosses:
            if g.in_dict and g.lao not in seen_words:
                all_glosses.append(g)
                seen_words.add(g.lao)

    if not full_vi:
        full_vi = "\n".join(fallback_vi_lines)
    if not full_en:
        full_en = "\n".join(fallback_en_lines)

    return full_vi, full_en, all_glosses

