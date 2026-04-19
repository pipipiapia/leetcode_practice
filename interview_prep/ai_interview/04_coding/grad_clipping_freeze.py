#!/usr/bin/env python3
"""
Q: 梯度裁剪 + 参数冻结/解冻

两个独立的手撕题目合并：
1. 梯度裁剪：防止 RNN/LSTM 梯度爆炸
2. 参数冻结/解冻：fine-tuning 必备
"""

import torch
import torch.nn as nn
import numpy as np


# ─── 梯度裁剪 ───────────────────────────────────────────────────────
def gradient_clipping_demo():
    """梯度裁剪：防止梯度爆炸"""
    print("=" * 50)
    print("梯度裁剪演示")
    print("=" * 50)

    # 模拟一个 RNN/LSTM 的梯度
    grad = torch.tensor([2.5, 3.1, 4.2, -2.8, 3.5], requires_grad=True)
    max_norm = 1.0

    grad_norm = grad.norm()
    print(f"原始梯度: {grad}")
    print(f"梯度范数: {grad_norm.item():.4f}")

    if grad_norm > max_norm:
        clipped_grad = grad * (max_norm / grad_norm)
        print(f"→ 范数超限，裁剪到 {max_norm}")
        print(f"裁剪后: {clipped_grad}")
    else:
        print("→ 范数正常，无需裁剪")

    # PyTorch 写法
    print("""
# PyTorch 实现（clip by global norm）：
  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 或 clip by value：
  torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)
""")


# ─── 参数冻结/解冻 ─────────────────────────────────────────────────
class ModelWithFreeze(nn.Module):
    """演示冻结和解冻参数的完整流程"""

    def __init__(self):
        super().__init__()
        self.backbone = nn.Linear(100, 50)
        self.head = nn.Linear(50, 10)

    def freeze_backbone(self):
        """冻结 backbone"""
        for name, param in self.named_parameters():
            if 'backbone' in name:
                param.requires_grad = False
        print("Backbone 已冻结")

    def unfreeze_backbone(self):
        """解冻 backbone"""
        for name, param in self.named_parameters():
            if 'backbone' in name:
                param.requires_grad = True
        print("Backbone 已解冻")

    def print_trainable(self):
        """打印可训练参数"""
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        total = sum(p.numel() for p in self.parameters())
        print(f"可训练: {trainable:,} / 总计: {total:,}")


def freeze_unfreeze_demo():
    print("\n" + "=" * 50)
    print("参数冻结/解冻演示")
    print("=" * 50)

    model = ModelWithFreeze()

    print("初始状态（全部可训练）：")
    model.print_trainable()

    print("\n冻结 backbone 后：")
    model.freeze_backbone()
    model.print_trainable()

    # 验证：只有 head 的参数需要优化
    optimizer = torch.optim.SGD(
        filter(lambda p: p.requires_grad, model.parameters()), lr=0.1
    )
    print("→ optimizer 只包含 head 参数 ✓")

    print("\n解冻 backbone 后：")
    model.unfreeze_backbone()
    model.print_trainable()


# ─── 综合演示：分阶段冻结 ──────────────────────────────────────────
def progressive_freezing_demo():
    print("\n" + "=" * 50)
    print("分阶段冻结（迁移学习标准流程）")
    print("=" * 50)

    model = ModelWithFreeze()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    x = torch.randn(8, 100)
    y = torch.randint(0, 10, (8,))

    print("阶段1：只训练 head（backbone 冻结）")
    model.freeze_backbone()
    optimizer = torch.optim.SGD(
        filter(lambda p: p.requires_grad, model.parameters()), lr=0.1
    )
    for _ in range(3):
        out = model.head(model.backbone(x).detach())
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print("  head 训练完成")

    print("\n阶段2：解冻 backbone，低学习率微调")
    model.unfreeze_backbone()
    optimizer = torch.optim.Adam([
        {'params': model.backbone.parameters(), 'lr': 1e-5},
        {'params': model.head.parameters(), 'lr': 1e-3}
    ])
    out = model(x)
    loss = criterion(out, y)
    loss.backward()
    optimizer.step()
    print("  backbone 微调完成（学习率很小，不会破坏预训练权重）")


if __name__ == "__main__":
    gradient_clipping_demo()
    freeze_unfreeze_demo()
    progressive_freezing_demo()
