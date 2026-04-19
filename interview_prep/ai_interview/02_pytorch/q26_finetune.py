#!/usr/bin/env python3
"""
Q26: PyTorch 模型微调（Fine-tuning）

面试常问：
1. 如何微调一个预训练模型？
2. 冻结部分参数怎么操作？
3. 不同层设置不同学习率怎么做？

三种常见微调策略：
  策略1：冻结 backbone，只训练新加的层
  策略2：所有层一起训练，但 backbone 用小学习率
  策略3：用较小的预训练权重初始化，再微调
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


# ─── 假设的预训练模型（模拟 ResNet18） ─────────────────────────────
class PretrainedBackbone(nn.Module):
    """
    模拟一个预训练 backbone：
    - conv1, conv2, conv3: 特征提取器（需要冻结或用小学习率）
    - fc: 分类头（替换为目标任务的输出维度）
    """
    def __init__(self, num_classes=1000):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


class NewTaskHead(nn.Module):
    """新任务的头部：替换掉原始 fc 层"""
    def __init__(self, input_dim, num_classes=10):
        super().__init__()
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(input_dim, num_classes)

    def forward(self, x):
        return self.fc(self.dropout(x))


# ─── 方式1：冻结 backbone，只训练新层 ───────────────────────────────
def freeze_backbone_only_new_head():
    print("=" * 50)
    print("方式1：冻结 backbone，只训练新层")
    print("=" * 50)

    model = PretrainedBackbone(num_classes=1000)

    # 替换分类头
    model.fc = nn.Linear(256, 10)   # 输出从1000类改为10类

    # 冻结所有参数
    for param in model.parameters():
        param.requires_grad = False

    # 只让新 fc 层可训练
    for param in model.fc.parameters():
        param.requires_grad = True

    # 验证：只有新层的参数可训练
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"可训练参数: {trainable_params:,} / {total_params:,}")

    optimizer = optim.SGD(filter(lambda p: p.requires_grad, model.parameters()), lr=0.1)
    return model, optimizer


# ─── 方式2：不同层不同学习率 ────────────────────────────────────────
def different_lr_for_layers():
    print("\n" + "=" * 50)
    print("方式2：不同层不同学习率（迁移学习推荐）")
    print("=" * 50)

    model = PretrainedBackbone(num_classes=1000)
    model.fc = nn.Linear(256, 10)

    # backbone 用小学习率（预训练权重不要被破坏）
    # head 用大学习率（从头学起）
    backbone_params = []
    head_params = []

    for name, param in model.named_parameters():
        if 'fc' in name:
            head_params.append(param)
        else:
            backbone_params.append(param)

    optimizer = optim.Adam([
        {'params': backbone_params, 'lr': 1e-5},   # backbone: 小学习率
        {'params': head_params, 'lr': 1e-3},      # head: 大学习率
    ])

    print(f"Backbone 参数学习率: {optimizer.param_groups[0]['lr']}")
    print(f"Head 参数学习率: {optimizer.param_groups[1]['lr']}")

    return model, optimizer


# ─── 方式3：逐步解冻（Gradual Unfreezing） ──────────────────────────
def gradual_unfreezing():
    print("\n" + "=" * 50)
    print("方式3：逐步解冻（先训头，再逐步解冻底层）")
    print("=" * 50)

    model = PretrainedBackbone(num_classes=1000)
    model.fc = nn.Linear(256, 10)

    # 第一阶段：只训 head
    print("阶段1：冻结所有层，只训 head")
    for param in model.parameters():
        param.requires_grad = False
    for param in model.fc.parameters():
        param.requires_grad = True

    # 第二阶段：解冻 conv3
    print("阶段2：解冻 conv3 + head")
    for param in model.conv3.parameters():
        param.requires_grad = True
    for param in model.fc.parameters():
        param.requires_grad = True

    # 第三阶段：解冻 conv2
    print("阶段3：解冻 conv2 + conv3 + head")

    # 第四阶段：全解冻
    print("阶段4：全部解冻，低学习率微调")


# ─── 完整训练循环演示 ────────────────────────────────────────────────
def full_training_loop():
    print("\n" + "=" * 50)
    print("完整训练循环（配合方式2）")
    print("=" * 50)

    model, optimizer = different_lr_for_layers()

    # 模拟数据
    x = torch.randn(32, 3, 32, 32)
    y = torch.randint(0, 10, (32,))
    criterion = nn.CrossEntropyLoss()

    model.train()
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

    print(f"Step loss: {loss.item():.4f}")
    print(f"Backbone 梯度范数: {sum(p.grad.norm().item() for p in model.parameters() if p.requires_grad and p.grad is not None):.6f}")


if __name__ == "__main__":
    freeze_backbone_only_new_head()
    different_lr_for_layers()
    gradual_unfreezing()
    full_training_loop()

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: 什么时候冻结 backbone？
A: 数据集小、预训练模型和目标任务相似度高时。
   冻结可以防止过拟合，同时加速训练。

Q: 不同学习率的原理？
A: 预训练的 backbone 已经学到了有用的特征，大学习率会破坏它。
   新加的 head 是随机初始化的，需要较大的学习率快速拟合。

Q: 怎么决定冻结哪些层？
A: 越靠近输入的层（底层），学到的特征越通用（边缘、纹理）。
   越靠近输出的层（高层），学到的特征越任务相关。
   通常冻结底层，微调高层。
""")
