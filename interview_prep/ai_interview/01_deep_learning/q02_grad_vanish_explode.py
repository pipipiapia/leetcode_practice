#!/usr/bin/env python3
"""
Q02: 梯度消失与梯度爆炸

面试常问：
1. 什么是梯度消失/爆炸？什么原因导致的？
2. 如何检测？（观察 loss 是否下降、梯度值大小）
3. 解决方法是？
4. 为什么 LSTM 能缓解梯度消失？

梯度消失（Vanishing Gradient）：
  深层网络中，梯度从后往前传，每层乘以激活函数的梯度
  Sigmoid: max=0.25，10层后 0.25^10 ≈ 10^-6 → 底层参数几乎不更新
  ReLU: 正区间梯度=1，但负区间=0 也可能导致死亡

梯度爆炸（Exploding Gradient）：
  梯度乘积越来越大，参数更新量过大，导致震荡或 NaN
  常见于 RNN/LSTM 等序列模型中

解决方案：
  ① 合适的初始化：He init（W ~ N(0, 2/n)），Xavier init（N(0, 1/n)）
  ② 激活函数：ReLU 替代 Sigmoid/Tanh
  ③ Batch Normalization：稳定每层输入分布
  ④ 残差连接（ResNet）：梯度跳跃传递
  ⑤ 梯度裁剪：max_norm 防止爆炸
  ⑥ LSTM/GRU：门控机制缓解
"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1 - s)


def simulate_gradient_flow_deep():
    """
    模拟深层网络中的梯度流
    梯度在每一层乘以激活函数导数，逐层衰减/增长
    """
    print("=" * 50)
    print("梯度消失演示：深层网络")
    print("=" * 50)

    n_layers = 10
    x = 1.0  # 输入

    # Sigmoid 网络（梯度消失）
    grad_sigmoid = 1.0
    for i in range(n_layers):
        # 假设每层输出在合理范围，sigmoid 导数 ≈ 0.25
        grad_sigmoid *= 0.25  # sigmoid 饱和区梯度

    print(f"10层后梯度（sigmod）: {grad_sigmoid:.2e} ← 接近0，梯度消失！")

    # ReLU 网络（梯度保持）
    grad_relu = 1.0
    for i in range(n_layers):
        grad_relu *= 1.0  # ReLU 正区间梯度恒为1

    print(f"10层后梯度（ReLU）:  {grad_relu:.2f} ← 梯度稳定")


def weight_init_comparison():
    """不同初始化方法的方差对比"""
    print("\n" + "=" * 50)
    print("权重初始化对比")
    print("=" * 50)

    def variance_before(x):
        return np.var(x)

    # Xavier (N(0, 2/(n_in + n_out)))
    # He init (N(0, 2/n)) — 更适合 ReLU
    # Normal init (N(0, 0.01)) — 不推荐

    print("""
前向传播时，输出的方差需要和输入相近才能稳定训练：
  Xavier:  N(0, 1/n_in)  — 适合 Sigmoid/Tanh（输入输出方差一致）
  He init: N(0, 2/n_in)  — 适合 ReLU（ReLU 把一半信号置零，需补偿）

如果用 He init 初始化 Sigmoid 网络会怎样？
→ 方差偏大，激活值饱和 → 梯度消失
如果用 Xavier 初始化 ReLU 网络会怎样？
→ 方差偏小，一半信号被 ReLU 置零后更小 → 梯度可能消失

结论：初始化方法和激活函数要匹配。
""")


def gradient_clipping_demo():
    """梯度裁剪防止爆炸"""
    print("\n" + "=" * 50)
    print("梯度裁剪（Gradient Clipping）")
    print("=" * 50)

    # 模拟一个爆炸的梯度
    grad = np.array([2.5, 3.1, 4.2, -2.8, 3.5])

    max_norm = 1.0
    grad_norm = np.linalg.norm(grad)

    if grad_norm > max_norm:
        clipped_grad = grad * (max_norm / grad_norm)
        print(f"原始梯度: {grad}")
        print(f"梯度范数: {grad_norm:.4f} > {max_norm} → 裁剪！")
        print(f"裁剪后:   {clipped_grad.round(4)}")
        print(f"裁剪后范数: {np.linalg.norm(clipped_grad):.4f}")
    else:
        print("梯度正常，无需裁剪")

    print("""
# PyTorch 实现：
  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
  # 所有梯度裁剪到 max_norm 以内

# RNN/LSTM 中梯度裁剪尤为重要：
  sequence 越长，梯度爆炸风险越大。
  LSTM 的门控机制能缓解（遗忘门决定保留多少历史信息）。
""")


def residual_gradient_flow():
    """ResNet 残差连接为什么能缓解梯度消失"""
    print("\n" + "=" * 50)
    print("残差连接（ResNet）原理")
    print("=" * 50)

    print("""
普通网络（每层梯度连乘）：
  ∂L/∂x_l = ∂L/∂x_L · Π ∂F(x_i)/∂x_{i-1}
           → 乘积越小（激活函数<1），梯度消失

残差网络（增加跳跃连接）：
  x_{l+1} = F(x_l) + x_l

  ∂L/∂x_l = ∂L/∂x_L · (∂F/∂x_l + 1)
           → 至少 +1，保证梯度不消失！

即使 F(x) 的梯度为 0，x_l 本身仍然有梯度传递下去。
这就是 ResNet 能训练上千层的核心原因。
""")


if __name__ == "__main__":
    simulate_gradient_flow_deep()
    weight_init_comparison()
    gradient_clipping_demo()
    residual_gradient_flow()

    print("=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: 如何发现梯度消失/爆炸？
A: ① 观察 loss：几乎不变（消失）或 NaN（爆炸）
   ② 打印每层梯度范数：接近 0（消失）或极大（爆炸）
   ③ 使用 torch.nn.utils.clip_grad_norm_ 观察裁剪频率

Q: 为什么 LSTM 能缓解梯度消失？
A: LSTM 的遗忘门控制信息保留：f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
   过去信息可以无衰减地传递下去（门=1时），不像普通 RNN 每次都乘激活函数。
   本质上，LSTM 将"乘法链"变成了"加法+门控"，缓解了梯度消失。

Q: BatchNorm 为什么有效？
A: 将每层输入标准化到均值0方差1，激活函数工作在梯度较大的区间，
   减少梯度消失/爆炸。同时加速收敛。
""")
