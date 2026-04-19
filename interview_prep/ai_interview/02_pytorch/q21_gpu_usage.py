#!/usr/bin/env python3
"""
Q21: PyTorch GPU 使用与显存管理

面试常问：
1. 如何把模型和数据移动到 GPU？
2. 多 GPU 训练用 DP 还是 DDP？
3. 显存不够怎么办？
4. 混合精度训练是什么？

显存占用来源：
  模型参数、梯度、优化器状态、中间激活值
  其中：中间激活值占用最多（随 batch_size 和模型深度指数增长）
"""

import torch
import torch.nn as nn
import torch.optim as optim


def check_gpu():
    """检查 GPU 可用性"""
    print("=" * 50)
    print("GPU 环境检查")
    print("=" * 50)
    print(f"CUDA 可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU 数量: {torch.cuda.device_count()}")
        print(f"当前 GPU: {torch.cuda.current_device()}")
        print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
        print(f"显存总量: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")


def basic_gpu_demo():
    """基础 GPU 使用"""
    print("\n" + "=" * 50)
    print("基础 GPU 使用")
    print("=" * 50)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")

    model = nn.Linear(10, 5).to(device)
    x = torch.randn(4, 10).to(device)
    y = torch.randn(4, 5).to(device)

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

    print(f"Loss: {loss.item():.4f}")
    print(f"输出在 GPU 上: {output.is_cuda}")


def ddp_demo():
    """DistributedDataParallel 示例"""
    print("\n" + "=" * 50)
    print("DDP vs DP 对比")
    print("=" * 50)
    print("""
# DataParallel（DP）— 不推荐
  model = nn.DataParallel(model)  # 单进程多线程，效率低
  # 缺点：有梯度累加问题（GPU0 负担重）、速度慢

# DistributedDataParallel（DDP）— 推荐
  # 需要配合 torch.distributed.launch 或 spawn 使用
  model = nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])
  # 多进程，异步通信，效率高，推荐用

# 单机多卡 DDP 启动命令：
  torchrun --nproc_per_node=4 train.py

# DDP 训练循环骨架：
  model = MyModel()
  model = nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])
  # 其他进程共享模型结构，梯度在反向传播时自动同步
""")


def memory_optimization():
    """显存优化方法"""
    print("\n" + "=" * 50)
    print("显存优化技巧")
    print("=" * 50)
    print("""
1. 梯度清零优化
   optimizer.zero_grad(set_to_none=True)  # 比 zero_grad() 更省显存

2. 梯度累积（模拟大 batch）
   for i, (x, y) in enumerate(loader):
       loss = model(x, y) / accumulation_steps
       loss.backward()
       if (i + 1) % accumulation_steps == 0:
           optimizer.step()
           optimizer.zero_grad()

3. 混合精度训练（AMP）
   scaler = torch.cuda.amp.GradScaler()
   with torch.cuda.amp.autocast():
       output = model(x)
       loss = criterion(output, y)
   scaler.scale(loss).backward()
   scaler.step(optimizer)
   scaler.update()

4. 梯度检查点（Gradient Checkpointing）
   用计算换显存：前向传播时不保存全部中间激活，
   反向传播时重新计算。显存减少 50-70%，速度稍慢。

5. 手动释放显存
   del intermediate_tensor
   torch.cuda.empty_cache()
""")


def amp_demo():
    """混合精度训练演示"""
    print("\n" + "=" * 50)
    print("混合精度训练（AMP）")
    print("=" * 50)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # FP16 训练，显存减半，速度提升
    model = nn.Sequential(
        nn.Linear(512, 2048),
        nn.ReLU(),
        nn.Linear(2048, 512)
    ).to(device)

    x = torch.randn(32, 512).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # AMP 训练
    scaler = torch.cuda.amp.GradScaler()

    with torch.cuda.amp.autocast():
        output = model(x)
        loss = criterion(output, torch.randint(0, 512, (32,)).to(device))

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

    print(f"Loss: {loss.item():.4f}")
    print(f"使用混合精度: 是（FP16）")


if __name__ == "__main__":
    check_gpu()
    basic_gpu_demo()
    ddp_demo()
    memory_optimization()
    if torch.cuda.is_available():
        amp_demo()
    else:
        print("\n当前无 GPU，跳过 AMP 演示")
