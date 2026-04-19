#!/usr/bin/env python3
"""
Q28: PyTorch 模型保存与加载

面试常问：
1. state_dict 和完整模型保存有什么区别？
2. 如何加载预训练模型的部分权重？
3. 保存到 GPU、加载到 CPU 怎么处理？

推荐方式：
  torch.save(model.state_dict(), 'weights.pth')
  model.load_state_dict(torch.load('weights.pth'))

不推荐：
  torch.save(model, 'model.pkl')  ← 包含整个类结构，迁移性差
"""

import torch
import torch.nn as nn


class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 16, 3, padding=1)
        self.bn = nn.BatchNorm2d(16)
        self.fc = nn.Linear(16 * 8 * 8, 10)

    def forward(self, x):
        x = torch.relu(self.bn(self.conv(x)))
        x = nn.functional.adaptive_avg_pool2d(x, (8, 8))
        return self.fc(x.flatten(1))


def save_and_load_demo():
    print("=" * 50)
    print("模型保存与加载演示")
    print("=" * 50)

    model = SimpleCNN()

    # ─── 推荐方式：只保存参数 ───────────────────────────────────────
    torch.save(model.state_dict(), 'simple_cnn_weights.pth')

    # 加载到结构相同的模型
    model2 = SimpleCNN()
    model2.load_state_dict(torch.load('simple_cnn_weights.pth', weights_only=True))
    model2.eval()

    # 验证：两个模型输出应该完全一致
    x = torch.randn(2, 3, 32, 32)
    with torch.no_grad():
        out1 = model(x)
        out2 = model2(x)

    print(f"原始模型输出:\n{out1}")
    print(f"加载后模型输出:\n{out2}")
    print(f"一致性检查: {'✓ 完全一致' if torch.allclose(out1, out2) else '✗ 不一致'}")


def partial_load_demo():
    """部分加载：加载预训练模型的部分权重"""
    print("\n" + "=" * 50)
    print("部分加载：加载部分权重（常见场景）")
    print("=" * 50)

    # 模拟预训练模型（1000类）
    pretrained = SimpleCNN()
    torch.save(pretrained.state_dict(), 'pretrained_weights.pth')

    # 当前任务（10类，需要替换 fc 层）
    model = SimpleCNN()
    model.fc = nn.Linear(16 * 8 * 8, 10)  # 输出改成10类

    # 加载权重，自动跳过不匹配的层（strict=False）
    pretrained_dict = torch.load('pretrained_weights.pth', weights_only=True)
    model_dict = model.state_dict()

    # 只加载匹配的权重（fc 层不加载，保持随机初始化）
    matched_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict and model_dict[k].shape == v.shape}
    model_dict.update(matched_dict)
    model.load_state_dict(model_dict)

    loaded_params = sum(1 for k in model.state_dict() if any(k.startswith(p) for p in ['conv', 'bn']))
    print(f"成功加载 {loaded_params} 层权重（conv 和 bn）")
    print(f"fc 层保持随机初始化（10类新输出）")


def gpu_cpu_demo():
    """GPU 存、CPU 加载 / CPU 存、GPU 加载"""
    print("\n" + "=" * 50)
    print("GPU 与 CPU 之间的保存加载")
    print("=" * 50)

    model = SimpleCNN()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 场景1: GPU保存 → CPU加载
    model = model.to(device)
    torch.save(model.state_dict(), 'gpu_weights.pth')

    model_cpu = SimpleCNN()
    state_dict = torch.load('gpu_weights.pth', map_location='cpu', weights_only=True)
    model_cpu.load_state_dict(state_dict)
    print("场景1: GPU保存 → CPU加载 ✓")

    # 场景2: CPU保存 → GPU加载
    torch.save(model.state_dict(), 'cpu_weights.pth')
    if torch.cuda.is_available():
        model_gpu = SimpleCNN()
        model_gpu.load_state_dict(torch.load('cpu_weights.pth', map_location='cuda:0', weights_only=True))
        model_gpu = model_gpu.cuda()
        print("场景2: CPU保存 → GPU加载 ✓")

    # 清理临时文件
    import os
    for f in ['simple_cnn_weights.pth', 'pretrained_weights.pth', 'gpu_weights.pth', 'cpu_weights.pth']:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    save_and_load_demo()
    partial_load_demo()
    gpu_cpu_demo()

    print("\n" + "=" * 50)
    print("面试核心要点")
    print("=" * 50)
    print("""
推荐保存方式（只存权重）：
  torch.save(model.state_dict(), 'weights.pth')

推荐加载方式：
  model.load_state_dict(torch.load('weights.pth', weights_only=True))

注意事项：
  1. weights_only=True（PyTorch 1.14+）：防止加载恶意 pickle
  2. 多 GPU 保存用 model.module.state_dict()
  3. partial load 用 strict=False + 手动过滤
  4. GPU→CPU 用 map_location='cpu'
""")
