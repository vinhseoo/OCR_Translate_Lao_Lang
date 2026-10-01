"""
Kiến trúc Mạng Nơ-ron Học Sâu CRNN (CNN + BiLSTM + CTC Loss) cho Nhận Dạng Chữ Tiếng Lào.
Thiết kế tối ưu cho ảnh dòng đơn 4 tầng độ cao (chiều cao chuẩn 48px).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional

from src.models.lao_vocab import DEFAULT_LAO_VOCAB, LaoVocabulary
from src.preprocessing.normalize import normalize_lao


class LaoCRNN(nn.Module):
    def __init__(self, vocab: Optional[LaoVocabulary] = None, in_channels: int = 1, hidden_size: int = 256):
        super().__init__()
        self.vocab = vocab or DEFAULT_LAO_VOCAB
        num_classes = self.vocab.num_classes
        
        # 1. CNN Feature Extractor (Thiết kế bất đẳng hướng theo chiều ngang W)
        # Input: (B, 1, 48, W)
        self.cnn = nn.Sequential(
            # Block 1
            nn.Conv2d(in_channels, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (B, 64, 24, W/2)
            
            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (B, 128, 12, W/4)
            
            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1)),  # (B, 256, 6, W/4)
            
            # Block 4
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1)),  # (B, 512, 3, W/4)
            
            # Block 5: Nén triệt để chiều cao H về 1
            nn.Conv2d(512, 512, kernel_size=(3, 1), stride=1, padding=0),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True)  # (B, 512, 1, W/4)
        )
        
        # 2. Sequence Modeling: 2-layer Bidirectional LSTM
        # Input features: 512, Hidden size: 256 x 2 (bidirectional) = 512
        self.rnn = nn.LSTM(
            input_size=512,
            hidden_size=hidden_size,
            num_layers=2,
            bidirectional=True,
            dropout=0.2,
            batch_first=False
        )
        
        # 3. Projection Head sang số lượng nhãn ký tự tiếng Lào
        self.fc = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Input: (B, 1, H=48, W)
        Output: Logits chuỗi thời gian (T, B, num_classes) cho CTCLoss
        """
        features = self.cnn(x)  # (B, 512, 1, W_seq)
        b, c, h, w_seq = features.size()
        assert h == 1, f"Chiều cao features phải bằng 1 sau CNN, thực tế: {h}"
        
        features = features.squeeze(2)          # (B, 512, W_seq)
        features = features.permute(2, 0, 1)    # (W_seq, B, 512) -> Sequence length là W_seq
        
        rnn_out, _ = self.rnn(features)         # (W_seq, B, hidden*2)
        logits = self.fc(rnn_out)               # (W_seq, B, num_classes)
        return logits

    def predict_image(self, image_input) -> str:
        """
        Dự đoán chuỗi text tiếng Lào từ ảnh (NumPy ndarray hoặc PIL Image).
        Tự động tiền xử lý chuyển sang ảnh xám và chuẩn hóa chiều cao 48px.
        """
        self.eval()
        
        # Chuẩn bị ảnh
        if isinstance(image_input, Image.Image):
            gray = np.array(image_input.convert("L"))
        elif isinstance(image_input, np.ndarray):
            if image_input.ndim == 3:
                import cv2
                gray = cv2.cvtColor(image_input, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_input.copy()
        else:
            raise ValueError(f"Kiểu dữ liệu không hỗ trợ: {type(image_input)}")
            
        # Chuẩn hóa chiều cao về 48px
        h, w = gray.shape[:2]
        target_h = 48
        scale = target_h / float(h)
        new_w = max(int(round(w * scale)), 32)
        
        import cv2
        resized = cv2.resize(gray, (new_w, target_h), interpolation=cv2.INTER_CUBIC)
        
        # Tensor hóa: (1, 1, 48, new_w), chuẩn hóa [-1, 1]
        tensor = torch.from_numpy(resized).float().unsqueeze(0).unsqueeze(0) / 127.5 - 1.0
        
        with torch.no_grad():
            logits = self(tensor)  # (T, 1, num_classes)
            preds = torch.argmax(logits, dim=2).squeeze(1).tolist()  # (T,)
            
        return self.vocab.ctc_greedy_decode(preds)
