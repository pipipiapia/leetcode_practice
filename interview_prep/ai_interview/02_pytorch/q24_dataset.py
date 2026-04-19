#!/usr/bin/env python3
"""
Q24: 自定义 PyTorch Dataset 与 DataLoader

面试常问：
1. Dataset 必须实现的两个方法是什么？
2. DataLoader 的关键参数及作用？
3. 如何处理不规则数据（padding）？

Dataset 三要素：
  __init__: 初始化数据
  __len__: 返回数据集大小
  __getitem__: 根据索引返回样本
"""

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np


# ─── 最基础的 Dataset ────────────────────────────────────────────────
class SimpleDataset(Dataset):
    """最简单的 Dataset 实现"""
    def __init__(self, data, labels):
        self.data = torch.FloatTensor(data)
        self.labels = torch.LongTensor(labels)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


# ─── 实际场景：变长序列（NLP 数据）──────────────────────────────────
class TextClassificationDataset(Dataset):
    """
    处理变长文本（NLP 场景）：
    - 不同句子长度不同，需要 padding 到同一长度
    - 需要返回 attention_mask 告诉模型哪些是真实 token，哪些是 padding
    """
    def __init__(self, texts, labels, tokenizer=None, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer or self._simple_tokenizer()
        self.max_length = max_length

    def _simple_tokenizer(self):
        """简易 tokenizer（演示用）"""
        vocab = {
            '<PAD>': 0, '<UNK>': 1,
            'i': 2, 'want': 3, 'to': 4, 'buy': 5,
            'a': 6, 'phone': 7, 'laptop': 8, 'the': 9
        }
        def encode(text):
            tokens = text.lower().split()
            ids = [vocab.get(w, 1) for w in tokens]  # 1=UNK
            return ids
        return encode

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # Tokenize
        token_ids = self.tokenizer(text)

        # Padding
        if len(token_ids) < self.max_length:
            padding = [0] * (self.max_length - len(token_ids))
            token_ids = token_ids + padding
        else:
            token_ids = token_ids[:self.max_length]

        # Attention mask: 1=真实token, 0=PAD
        attention_mask = [1 if t != 0 else 0 for t in token_ids]

        return {
            'input_ids': torch.tensor(token_ids),
            'attention_mask': torch.tensor(attention_mask),
            'label': torch.tensor(label, dtype=torch.long)
        }


# ─── collate_fn: 自定义批处理逻辑 ──────────────────────────────────
def custom_collate_fn(batch):
    """
    当 Dataset 返回字典时，DataLoader 的默认 collate 可能会出问题
    需要自定义 collate_fn
    """
    input_ids = torch.stack([item['input_ids'] for item in batch])
    attention_mask = torch.stack([item['attention_mask'] for item in batch])
    labels = torch.stack([item['label'] for item in batch])
    return {
        'input_ids': input_ids,
        'attention_mask': attention_mask,
        'labels': labels
    }


# ─── 数据增强 Dataset ───────────────────────────────────────────────
class AugmentedImageDataset(Dataset):
    """图像数据增强（在 __getitem__ 中实时增强）"""
    def __init__(self, images, labels, augment=True):
        self.images = images  # numpy array (N, H, W, C)
        self.labels = labels
        self.augment = augment

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = self.images[idx].copy()
        label = self.labels[idx]

        if self.augment:
            # 随机水平翻转
            if np.random.rand() > 0.5:
                img = np.fliplr(img).copy()

            # 随机裁剪（这里简化处理）
            # 实际可用 torchvision.transforms

        # (H, W, C) → (C, H, W)  并归一化
        img = torch.FloatTensor(img).permute(2, 0, 1) / 255.0

        return img, torch.tensor(label, dtype=torch.long)


# ─── 运行演示 ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Dataset 演示")
    print("=" * 50)

    # 1. 基础 Dataset
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, 100)
    dataset = SimpleDataset(X, y)
    loader = DataLoader(dataset, batch_size=8, shuffle=True)

    for batch_x, batch_y in loader:
        print(f"Batch X shape: {batch_x.shape}, Batch y shape: {batch_y.shape}")
        break

    # 2. 变长文本 Dataset
    texts = ["i want to buy a phone", "laptop the want", "a buy i to want"]
    labels = [0, 1, 0]
    text_dataset = TextClassificationDataset(texts, labels, max_length=8)

    sample = text_dataset[0]
    print(f"\n文本样本 input_ids: {sample['input_ids']}")
    print(f"attention_mask:    {sample['attention_mask']}")

    # 3. 带 collate_fn 的 DataLoader
    loader = DataLoader(text_dataset, batch_size=2, collate_fn=custom_collate_fn)
    for batch in loader:
        print(f"\nBatch input_ids shape: {batch['input_ids'].shape}")
        print(f"Batch attention_mask: {batch['attention_mask'].shape}")
        break

    print("\n" + "=" * 50)
    print("面试核心要点")
    print("=" * 50)
    print("""
Dataset 必须实现：
  __len__(): len(dataset) → 数据集大小
  __getitem__(idx): dataset[idx] → 单个样本

DataLoader 关键参数：
  batch_size: 每批样本数
  shuffle: 是否打乱顺序
  num_workers: 多进程加载（加速）
  pin_memory: 锁页内存，加速 GPU 传输
  drop_last: 丢弃最后一个不完整 batch
  collate_fn: 自定义批处理逻辑（处理变长序列时常用）
""")
