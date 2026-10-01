"""
Module Huấn Luyện Mô Hình CRNN cho Nhận Dạng Văn Bản Tiếng Lào.
Hỗ trợ nạp dữ liệu tổng hợp (synth_clean / synth_aug), CTCLoss,
tối ưu hóa Adam và theo dõi hàm mất mát & CER.
"""
import os
import csv
import time
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import cv2
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from src.models.crnn import LaoCRNN
from src.models.lao_vocab import DEFAULT_LAO_VOCAB, LaoVocabulary
from src.preprocessing.normalize import normalize_lao
from src.evaluation.metrics import compute_dataset_cer, compute_word_accuracy


class LaoOCRDataset(Dataset):
    def __init__(self, img_dir: str, csv_path: str, vocab: Optional[LaoVocabulary] = None, target_height: int = 48, max_samples: Optional[int] = None):
        self.img_dir = img_dir
        self.vocab = vocab or DEFAULT_LAO_VOCAB
        self.target_height = target_height
        self.samples: List[Tuple[str, str]] = []
        
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for idx, r in enumerate(reader):
                    if max_samples and idx >= max_samples:
                        break
                    fn = r.get("filename", "")
                    txt = r.get("text") or r.get("lao_text") or ""
                    if fn and txt:
                        self.samples.append((fn, normalize_lao(txt)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fn, text = self.samples[idx]
        img_path = os.path.join(self.img_dir, fn)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            img = np.full((self.target_height, 100), 255, dtype=np.uint8)
            
        h, w = img.shape[:2]
        scale = self.target_height / float(h)
        new_w = max(int(round(w * scale)), 32)
        resized = cv2.resize(img, (new_w, self.target_height), interpolation=cv2.INTER_CUBIC)
        
        # Tensor hóa [-1.0, 1.0]
        tensor = torch.from_numpy(resized).float().unsqueeze(0) / 127.5 - 1.0
        encoded = self.vocab.encode(text)
        return tensor, encoded, text


def collate_fn_crnn(batch):
    """Gộp batch với độ rộng biến thiên (Width Padding) và căn chỉnh nhãn CTC."""
    tensors, encodeds, texts = zip(*batch)
    batch_size = len(tensors)
    max_w = max(t.shape[2] for t in tensors)
    # Làm tròn max_w để chia hết cho 4 (CNN downsampling)
    max_w = int(np.ceil(max_w / 4.0) * 4)
    
    padded_tensors = torch.zeros(batch_size, 1, 48, max_w)
    target_lengths = []
    all_targets = []
    
    for i, t in enumerate(tensors):
        w = t.shape[2]
        padded_tensors[i, :, :, :w] = t
        enc = encodeds[i]
        target_lengths.append(len(enc))
        all_targets.extend(enc)
        
    targets_tensor = torch.tensor(all_targets, dtype=torch.long)
    target_lengths_tensor = torch.tensor(target_lengths, dtype=torch.long)
    
    # Input lengths sau khi qua 4 lần downsampling chiều ngang của CNN
    # Block 1 (/2), Block 2 (/2), Block 3 (/1), Block 4 (/1), Block 5 (/1) -> W_seq = W / 4
    input_lengths_tensor = torch.full((batch_size,), max_w // 4, dtype=torch.long)
    
    return padded_tensors, targets_tensor, input_lengths_tensor, target_lengths_tensor, texts


def train_crnn_epoch(model: LaoCRNN, dataloader: DataLoader, optimizer: torch.optim.Optimizer, criterion: nn.CTCLoss, device: torch.device) -> float:
    model.train()
    total_loss = 0.0
    num_batches = 0
    
    for images, targets, input_lengths, target_lengths, _ in dataloader:
        images = images.to(device)
        targets = targets.to(device)
        input_lengths = input_lengths.to(device)
        target_lengths = target_lengths.to(device)
        
        optimizer.zero_grad()
        logits = model(images)  # (T, B, C)
        log_probs = logits.log_softmax(2)
        
        loss = criterion(log_probs, targets, input_lengths, target_lengths)
        if torch.isfinite(loss):
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()
            total_loss += loss.item()
            num_batches += 1
            
    return total_loss / max(num_batches, 1)


def evaluate_crnn(model: LaoCRNN, images: List[np.ndarray], references: List[str]) -> Tuple[float, float]:
    """Đánh giá nhanh CER và Word Accuracy trên danh sách ảnh."""
    model.eval()
    hyps = [model.predict_image(im) for im in images]
    cer = compute_dataset_cer(references, hyps)
    acc = compute_word_accuracy(references, hyps)
    return cer, acc
