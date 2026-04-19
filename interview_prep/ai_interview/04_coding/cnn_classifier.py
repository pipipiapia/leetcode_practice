#!/usr/bin/env python3
"""
Q: 手撕 CNN 图像分类器

完整实现一个 CNN 分类器，包括：
1. 卷积层 + 池化层
2. 全连接分类层
3. 前向传播 + 训练循环
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader


class SimpleCNN(nn.Module):
    """
    简单 CNN（LeNet-5 风格）：
    Conv1 -> Pool -> Conv2 -> Pool -> FC -> FC
    """
    def __init__(self, num_classes=10):
        super().__init__()
        # Conv1: 1@28x28 -> 6@14x14
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2)
        # Conv2: 6@14x14 -> 16@5x5
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        # FC layers
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        # Conv1 + ReLU + MaxPool
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)  # 28->14

        # Conv2 + ReLU + MaxPool
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)  # 14->7->5

        # Flatten
        x = x.view(x.size(0), -1)

        # FC
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train_cnn_demo():
    """演示 CNN 训练流程（使用 MNIST）"""
    print("=" * 50)
    print("CNN 图像分类器训练演示")
    print("=" * 50)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")

    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),           # (H, W, C) -> (C, H, W), 归一化到 [0,1]
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST 均值方差
    ])

    # 加载 MNIST
    train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, download=False, transform=transform
    )
    test_dataset = torchvision.datasets.MNIST(
        root='./data', train=False, download=False, transform=transform
    )

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

    # 模型、损失、优化器
    model = SimpleCNN(num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 训练
    def train_epoch(model, loader, criterion, optimizer, device):
        model.train()
        total_loss = 0
        correct = 0
        total = 0

        for batch_idx, (data, target) in enumerate(loader):
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

            if batch_idx % 100 == 0:
                print(f"  Batch {batch_idx:3d} | Loss: {loss.item():.4f}")

        return total_loss / len(loader), 100. * correct / total

    # 测试
    def evaluate(model, loader, device):
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        return 100. * correct / total

    # 跑1个 epoch 演示
    print("\n开始训练（1 epoch）：")
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")

    test_acc = evaluate(model, test_loader, device)
    print(f"Test Acc: {test_acc:.2f}%")


if __name__ == "__main__":
    train_cnn_demo()
