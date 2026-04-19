#!/usr/bin/env python3
"""
Q01: 反向传播原理与链式法则

面试常问：
1. 解释反向传播的工作原理
2. 推导链式法则在反向传播中的应用
3. 为什么从后往前传播梯度？

核心概念：
- 前向传播：输入 → 逐层计算激活值 → 输出 loss
- 反向传播：根据 loss，从输出层往输入层逐层计算梯度
- 链式法则：∂L/∂W = ∂L/∂a · ∂a/∂z · ∂z/∂W

举例：两层全连接网络
  z1 = W1 @ x + b1        (第一层线性)
  a1 = ReLU(z1)           (第一层激活)
  z2 = W2 @ a1 + b2       (第二层线性)
  a2 = softmax(z2)        (输出层)
  loss = CrossEntropy(a2, y)

梯度计算：
  ∂L/∂W2 = δ2 @ a1.T       (δ2 = ∂L/∂z2)
  ∂L/∂W1 = δ1 @ x.T        (δ1 = (W2.T @ δ2) * ReLU'(z1))
"""

import numpy as np


def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    """ReLU 的梯度：正区间为1，负区间为0"""
    return (x > 0).astype(float)


def softmax(z):
    """数值稳定的 Softmax"""
    z_shifted = z - np.max(z, axis=-1, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=-1, keepdims=True)


def cross_entropy_loss(y_pred, y_true):
    """交叉熵损失"""
    eps = 1e-9
    return -np.sum(y_true * np.log(y_pred + eps)) / y_true.shape[0]


def forward(x, W1, b1, W2, b2):
    """
    前向传播
    x: (batch_size, input_dim)
    W1: (input_dim, hidden_dim)
    b1: (hidden_dim,)
    W2: (hidden_dim, output_dim)
    b2: (output_dim,)
    """
    z1 = x @ W1 + b1          # (batch, hidden)
    a1 = relu(z1)             # (batch, hidden)
    z2 = a1 @ W2 + b2        # (batch, output)
    a2 = softmax(z2)          # (batch, output) 概率分布
    return z1, a1, z2, a2


def backward(x, y_true, z1, a1, z2, a2, W2):
    """
    反向传播

    对于交叉熵 + Softmax：
      ∂L/∂z2 = a2 - y_true        (推导见 Q06)

    关键公式：
      δ2 = ∂L/∂z2 = a2 - y_true          (batch, output_dim)
      δ1 = (δ2 @ W2.T) * ReLU'(z1)        (batch, hidden_dim)

      ∂L/∂W2 = a1.T @ δ2                  (hidden, output)
      ∂L/∂b2 = sum(δ2, axis=0)             (output,)
      ∂L/∂W1 = x.T @ δ1                    (input, hidden)
      ∂L/∂b1 = sum(δ1, axis=0)             (hidden,)
    """
    batch_size = x.shape[0]

    # 输出层误差 δ2 = softmax(z2) - y_true
    delta2 = a2 - y_true          # (batch, output)

    # ∂L/∂W2 = a1.T @ δ2,  ∂L/∂b2 = sum(δ2)
    dW2 = a1.T @ delta2           # (hidden, output)
    db2 = np.sum(delta2, axis=0)  # (output,)

    # 反向传播到第一层
    # δ1 = (δ2 @ W2.T) * ReLU'(z1)
    delta1 = (delta2 @ W2.T) * relu_grad(z1)  # (batch, hidden)

    # ∂L/∂W1 = x.T @ δ1,  ∂L/∂b1 = sum(δ1)
    dW1 = x.T @ delta1            # (input, hidden)
    db1 = np.sum(delta1, axis=0)   # (hidden,)

    return dW1, db1, dW2, db2


def train_step(x, y_true, W1, b1, W2, b2, lr=0.01):
    """单步训练"""
    z1, a1, z2, a2 = forward(x, W1, b1, W2, b2)

    loss = cross_entropy_loss(a2, y_true)

    dW1, db1, dW2, db2 = backward(x, y_true, z1, a1, z2, a2, W2)

    # 梯度下降更新
    W1 -= lr * dW1
    b1 -= lr * db1
    W2 -= lr * dW2
    b2 -= lr * db2

    return loss


# ─── 运行验证 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)

    # 模拟数据
    batch_size, input_dim, hidden_dim, output_dim = 4, 10, 8, 3
    x = np.random.randn(batch_size, input_dim)
    y_true = np.zeros((batch_size, output_dim))
    y_true[np.arange(batch_size), np.random.randint(0, output_dim, batch_size)] = 1

    # 初始化参数
    W1 = np.random.randn(input_dim, hidden_dim) * 0.01
    b1 = np.zeros(hidden_dim)
    W2 = np.random.randn(hidden_dim, output_dim) * 0.01
    b2 = np.zeros(output_dim)

    print("初始 loss:", cross_entropy_loss(softmax(x @ W1 + b1 @ np.ones((batch_size, 1))) if False else
          forward(x, W1, b1, W2, b2)[3], y_true))

    for epoch in range(5):
        loss = train_step(x, y_true, W1, b1, W2, b2, lr=0.1)
        print(f"Epoch {epoch+1} | Loss: {loss:.4f}")

    # 验证梯度形状
    z1, a1, z2, a2 = forward(x, W1, b1, W2, b2)
    dW1, db1, dW2, db2 = backward(x, y_true, z1, a1, z2, a2, W2)
    print(f"\n梯度形状验证：")
    print(f"  dW1: {dW1.shape}, db1: {db1.shape}")
    print(f"  dW2: {dW2.shape}, db2: {db2.shape}")
    print(f"  ✓ 参数维度与梯度维度一致" if dW1.shape == W1.shape else "  ✗ 形状不一致!")
