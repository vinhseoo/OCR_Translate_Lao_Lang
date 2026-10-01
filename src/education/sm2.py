"""
Thuật Toán Lặp Lại Ngắt Quãng SuperMemo SM-2 (Spaced Repetition System).
Phục vụ quản lý chu kỳ ôn tập flashcard cá nhân hóa cho học viên học tiếng Lào.
Tính toán hệ số dễ nhớ (Easiness Factor EF), khoảng cách ngày ôn tập (Interval)
và số lần lặp lại thành công (Repetitions).
"""
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from dataclasses import dataclass, asdict


@dataclass
class FlashcardReviewState:
    card_id: str
    lao_text: str
    vi_meaning: str
    romanization: str
    repetitions: int = 0
    interval_days: int = 1
    easiness_factor: float = 2.5
    last_reviewed: str = ""
    next_review: str = ""
    history: list = None

    def __post_init__(self):
        if not self.last_reviewed:
            self.last_reviewed = datetime.now().strftime("%Y-%m-%d")
        if not self.next_review:
            self.next_review = datetime.now().strftime("%Y-%m-%d")
        if self.history is None:
            self.history = []


def calculate_sm2(
    quality: int,
    repetitions: int,
    previous_interval: int,
    previous_ef: float
) -> Tuple[int, int, float]:
    """
    Tính toán trạng thái kế tiếp theo thuật toán SuperMemo SM-2.
    
    Args:
        quality: Đánh giá của người học từ 0 đến 5:
            5: Hoàn hảo, nhớ ngay lập tức
            4: Nhớ chính xác sau một chút đắn đo
            3: Nhớ đúng nhưng khá khó khăn
            2: Trả lời sai nhưng nhớ lại khi xem đáp án
            1: Trả lời sai hoàn toàn
            0: Hoàn toàn không có ấn tượng (Blackout)
        repetitions: Số lần lặp lại đúng liên tiếp hiện tại.
        previous_interval: Khoảng cách ngày ở lần ôn tập trước.
        previous_ef: Hệ số dễ nhớ trước đó (mặc định 2.5).
        
    Returns:
        (new_repetitions, new_interval_days, new_ef)
    """
    q = max(0, min(5, quality))
    
    # 1. Cập nhật hệ số dễ nhớ (Easiness Factor)
    # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ef = previous_ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ef = max(1.3, round(new_ef, 3))
    
    # 2. Cập nhật số lần lặp và khoảng cách ngày
    if q < 3:
        # Nếu trả lời thất bại (q < 3), đặt lại số lần lặp từ đầu
        new_repetitions = 0
        new_interval = 1
    else:
        # Trả lời đạt yêu cầu (q >= 3)
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = int(math.ceil(previous_interval * new_ef))
        new_repetitions = repetitions + 1
        
    return new_repetitions, new_interval, new_ef


def review_card(card: FlashcardReviewState, quality: int) -> FlashcardReviewState:
    """Cập nhật thẻ với kết quả đánh giá mới của học viên."""
    now = datetime.now()
    new_reps, new_int, new_ef = calculate_sm2(
        quality=quality,
        repetitions=card.repetitions,
        previous_interval=card.interval_days,
        previous_ef=card.easiness_factor
    )
    
    card.repetitions = new_reps
    card.interval_days = new_int
    card.easiness_factor = new_ef
    card.last_reviewed = now.strftime("%Y-%m-%d %H:%M:%S")
    card.next_review = (now + timedelta(days=new_int)).strftime("%Y-%m-%d")
    card.history.append({
        "timestamp": card.last_reviewed,
        "quality": quality,
        "new_interval": new_int,
        "new_ef": new_ef
    })
    return card
