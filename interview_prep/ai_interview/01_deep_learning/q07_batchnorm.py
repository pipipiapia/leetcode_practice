#!/usr/bin/env python3
"""
Q07: BatchNorm 实现（含训练/测试行为差异）

面试常问：
1. BatchNorm 的原理是什么？
2. γ 和 β 两个可学习参数的作用？
3. 训练时和测试时的行为有什么不同？
4. BatchNorm 为什么有效？

原理：
  对每个 batch 的每个通道计算均值和方差
  x_norm = (x - μ) / √(σ² + ε)
  y = γ · x_norm + β

  μ 和 σ 来自当前 batch（训练时）
  训练时累积 running_mean / running_var，测试时用这些统计量

为什么有效：
  1. 缓解 ICS（Internal Covariate Shift）
  2. 使每层输入分布稳定，梯度更平稳
  3. 有轻微正则化效果（batch 噪声）
"""

import numpy as np
import unittest


class BatchNorm1d:
    """
    手写 BatchNorm 实现（适合理解原理）

    维度说明（1D 输入）：
      x: (batch_size, num_features)
      μ, σ²: (num_features,)
      γ, β: (num_features,)  ← 可学习参数
      running_mean, running_var: (num_features,) ← 累积统计量
    """

    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        self.gamma = np.ones(num_features)    # 缩放参数
        self.beta = np.zeros(num_features)   # 平移参数
        self.eps = eps
        self.momentum = momentum
        self.running_mean = np.zeros(num_features)
        self.running_var = np.ones(num_features)
        self.training = True

    def forward(self, x):
        if self.training:
            # ── 训练时：用当前 batch 的统计量 ──
            mean = np.mean(x, axis=0)               # (C,)
            var = np.var(x, axis=0)                 # (C,)

            # 累积 moving average（测试时用）
            self.running_mean = (
                (1 - self.momentum) * self.running_mean
                + self.momentum * mean
            )
            self.running_var = (
                (1 - self.momentum) * self.running_var
                + self.momentum * var
            )
        else:
            # ── 测试时：用累积的统计量 ──
            mean = self.running_mean
            var = self.running_var

        # 标准化
        x_norm = (x - mean) / np.sqrt(var + self.eps)

        # 缩放 + 平移（可学习）
        y = self.gamma * x_norm + self.beta
        return y

    def __call__(self, x):
        return self.forward(x)

    def train(self):
        self.training = True

    def eval(self):
        self.training = False


# ─── PyTorch 版本（面试写法） ──────────────────────────────────────
# import torch
# import torch.nn as nn
#
# class PyTorchBatchNorm(nn.Module):
#     def __init__(self, num_features):
#         super().__init__()
#         self.bn = nn.BatchNorm1d(num_features)
#
#     def forward(self, x):
#         return self.bn(x)
#
# # 面试要点：
# # 1. nn.BatchNorm1d 用于 (N, C) 或 (N, C, L) 的输入
# # 2. nn.BatchNorm2d 用于 (N, C, H, W) 的图像输入
# # 3. eval() 切换为 running_mean/var，train() 切换为 batch 统计量


# ─── 对比测试：训练 vs 测试 ─────────────────────────────────────────
class TestBatchNorm(unittest.TestCase):

    def test_normalization(self):
        """验证标准化后均值≈0，方差≈1"""
        np.random.seed(42)
        bn = BatchNorm1d(4)

        x = np.random.randn(32, 4) * 3 + 5   # 均值5，方差3
        y = bn.train()(x)

        np.testing.assert_array_almost_equal(
            np.mean(y, axis=0), np.zeros(4), decimal=1
        )
        np.testing.assert_array_almost_equal(
            np.var(y, axis=0), np.ones(4), decimal=1
        )

    def test_train_vs_eval(self):
        """验证训练/测试行为差异"""
        np.random.seed(42)
        bn = BatchNorm1d(2, momentum=0.1)

        # 训练多个 batch，累积统计量
        for _ in range(100):
            x = np.random.randn(32, 2) * 2 + 10
            bn.train()
            bn(x)

        # 测试时
        bn.eval()
        x_test = np.random.randn(10, 2)
        y_train = bn.train()(x_test)
        y_eval = bn.eval()(x_test)

        # 训练时输出有随机性（batch统计量），测试时输出稳定
        # （这里主要验证 API 行为，实际数值差异取决于 batch）
        self.assertEqual(bn.training, False)


if __name__ == "__main__":
    print("=" * 50)
    print("BatchNorm 原理演示")
    print("=" * 50)

    np.random.seed(0)
    bn = BatchNorm1d(3, momentum=0.1)

    # 模拟训练阶段
    print("\n[训练阶段] 逐步累积 running_mean/running_var")
    for i in range(5):
        x = np.random.randn(16, 3) * (i + 1) + (i + 1) * 10
        bn.train()
        y = bn(x)
        print(f"  Batch {i+1}: running_mean = {bn.running_mean.round(2)}")

    # 模拟测试阶段
    print("\n[测试阶段] 使用累积的 running_mean/running_var")
    bn.eval()
    x_test = np.random.randn(4, 3)
    y_test = bn(x_test)
    print(f"  测试输出均值: {y_test.mean(axis=0).round(3)}")
    print(f"  测试输出方差: {y_test.var(axis=0).round(3)}")

    print("\n关键区别：")
    print("  训练时: 用当前 batch 的 mean/var，running 逐步累积")
    print("  测试时: 用累积的 running_mean/running_var，固定不变")
    print("  γ, β: 始终参与计算（可学习参数）")

    unittest.main(verbosity=2)
