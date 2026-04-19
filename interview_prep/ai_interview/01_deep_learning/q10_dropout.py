#!/usr/bin/env python3
"""
Q10: Dropout 实现

面试常问：
1. Dropout 的原理是什么？
2. 训练时和测试时行为有何不同？
3. Dropout 和 BatchNorm 能否一起用？
4. Dropout 的变体有哪些？

原理：
  训练时：以概率 p 随机将部分神经元置零（丢弃）
  测试时：所有神经元参与，乘以 (1-p) 或使用 inverted dropout

Inverted Dropout（推荐）：
  训练时：输出 / (1-p)，测试时不变
  相当于把期望拉到 1，测试时无需额外操作

为什么有效：
  1. 类似集成学习：每次训练不同子网络
  2. 减少神经元间的共适应（co-adaptation）
  3. 增加泛化能力
"""

import numpy as np
import unittest


def dropout(x: np.ndarray, p: float, training: bool = True) -> tuple:
    """
    Dropout 前向传播

    参数:
      x: 输入
      p: 丢弃概率（保留概率 = 1 - p）
      training: 是否训练模式

    返回:
      (output, mask) — mask 用于反向传播
    """
    if p == 0:
        return x, np.ones_like(x, dtype=bool)

    if training:
        # 随机生成丢弃 mask
        mask = np.random.rand(*x.shape) > p
        # inverted dropout：缩放保证期望不变
        return x * mask / (1 - p), mask
    else:
        # 测试时所有神经元参与，无需缩放
        return x, None


def dropout_backward(dout: np.ndarray, mask: np.ndarray, p: float):
    """
    Dropout 反向传播

    结论：梯度等于上层梯度 × mask（丢弃位置梯度为0）
    """
    return dout * mask / (1 - p)


# ─── 多层 Dropout 网络演示 ─────────────────────────────────────────
class DropoutLayer:
    def __init__(self, input_dim, hidden_dim, dropout_p=0.5):
        self.W = np.random.randn(input_dim, hidden_dim) * 0.01
        self.b = np.zeros(hidden_dim)
        self.p = dropout_p
        self.mask = None
        self.training = True

    def forward(self, x):
        z = x @ self.W + self.b
        a = np.maximum(0, z)   # ReLU
        a, mask = dropout(a, self.p, training=self.training)
        self.mask = mask
        return a

    def backward(self, da):
        da = dropout_backward(da, self.mask, self.p)  # ReLU 梯度 × Dropout
        da[da < 0] = 0
        return da


class TestDropout(unittest.TestCase):

    def test_output_shape(self):
        """Dropout 不改变输出维度"""
        np.random.seed(42)
        x = np.random.randn(8, 16)
        y, mask = dropout(x, p=0.5, training=True)
        self.assertEqual(y.shape, x.shape)

    def test_mask_shape(self):
        """mask 维度与输入一致"""
        x = np.random.randn(8, 16)
        _, mask = dropout(x, p=0.5, training=True)
        self.assertEqual(mask.shape, x.shape)

    def test_inverted_dropout(self):
        """验证 inverted dropout：期望值等于原始值"""
        np.random.seed(42)
        x = np.random.randn(1000, 10)
        outputs = []
        for _ in range(100):
            y, _ = dropout(x, p=0.5, training=True)
            outputs.append(y.mean())

        avg = np.mean(outputs)
        # 多次采样的均值应该接近原始均值
        np.testing.assert_almost_equal(avg, x.mean(), decimal=1)


if __name__ == "__main__":
    print("=" * 50)
    print("Dropout 原理演示")
    print("=" * 50)

    np.random.seed(42)
    x = np.array([[1.0, 2.0, 3.0, 4.0]])

    print(f"\n原始输入: {x}")

    # 多次采样看随机性
    print("\n训练模式（随机丢弃，5次采样）：")
    for i in range(5):
        y, mask = dropout(x, p=0.5, training=True)
        print(f"  采样{i+1}: {y.round(2)} | 保留位置: {mask[0]}")

    print("\n测试模式（所有神经元参与，无缩放）：")
    y_test, _ = dropout(x, p=0.5, training=False)
    print(f"  输出: {y_test}")

    print("\n面试要点速记：")
    print("  Q: Dropout 和 BatchNorm 能一起用吗？")
    print("  A: 理论上可以，但实践中不推荐。BN 本身已有正则化效果，")
    print("     Dropout 的随机性会干扰 BN 的 batch 统计量。常见只选其一。")
    print()
    print("  Q: Dropout 变体有哪些？")
    print("  A: Spatial Dropout → 丢弃整个通道（CNN 常用）")
    print("     DropConnect → 丢弃连接权重而非激活值")
    print("     Variational Dropout → 每个样本有独立 dropout mask")

    unittest.main(verbosity=2)
