#!/usr/bin/env python3
"""
Q06: Softmax 原理与求导（数值稳定版本）

面试常问：
1. Softmax 的公式是什么？
2. 为什么需要数值稳定（numerical stability）？
3. Softmax + CrossEntropy 的梯度是什么？

公式：
  S(z_i) = e^{z_i} / Σ_j e^{z_j}

求导（关键！）：
  当 i == j（对角线）：∂S_i/∂z_i = S_i(1 - S_i)
  当 i != j（非对角线）：∂S_i/∂z_j = -S_i · S_j

数值稳定：
  e^{z_i} 可能溢出（如 z_i = 1000）
  技巧：所有 z 减去 max(z)，结果不变
  e^{z_i - max} / Σe^{z_j - max}

Softmax + CrossEntropy 简化梯度（最重要！）：
  CrossEntropy(L) = -Σ y_i · log(S_i)
  ∂L/∂z = S - y
  （推导见下方，非常简洁！）
"""

import numpy as np
import unittest


def softmax(z: np.ndarray) -> np.ndarray:
    """
    数值稳定的 Softmax

    原理：S_i = e^{z_i} / Σe^{z_j}
    = e^{z_i - C} / Σe^{z_j - C}   （分子分母同乘 e^{-C}）
    取 C = max(z)，保证指数不超过 0，防止溢出
    """
    z_shifted = z - np.max(z, axis=-1, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / (np.sum(exp_z, axis=-1, keepdims=True) + 1e-10)


def cross_entropy(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """
    交叉熵损失
    L = -Σ y_true[i] · log(y_pred[i])
    """
    eps = 1e-10
    return -np.mean(np.sum(y_true * np.log(y_pred + eps), axis=-1))


def softmax_ce_grad(z: np.ndarray, y_true: np.ndarray) -> np.ndarray:
    """
    Softmax + CrossEntropy 的组合梯度
    这就是为什么两者经常一起用 —— 梯度形式极其简洁！

    推导：
      L = -Σ_k y_k · log(S_k)
      ∂L/∂z_i = Σ_k ∂L/∂S_k · ∂S_k/∂z_i
              = -Σ_k y_k · (1/S_k) · ∂S_k/∂z_i

      利用 ∂S_i/∂z_j 的通式，可化简为：
      ∂L/∂z_i = S_i - y_i

    即：组合损失对 z 的梯度 = softmax输出 - 真实标签
    """
    y_pred = softmax(z)
    return y_pred - y_true


# ─── 梯度验证（用手工推导的公式对比） ─────────────────────────────
def softmax_grad_manual(z: np.ndarray) -> np.ndarray:
    """
    手工计算 Softmax 雅可比矩阵的梯度（用于对比验证）

    Jacobian: J[i][j] = ∂S_i/∂z_j
    对角线: S_i(1 - S_i)
    非对角: -S_i · S_j
    """
    S = softmax(z)                        # (n,) 或 (batch, n)
    if z.ndim == 1:
        diag = np.diag(S)
        off_diag = -np.outer(S, S)
        np.fill_diagonal(off_diag, 0)    # 对角线清零
        return diag + off_diag
    else:
        # batch 版本：对每个样本分别计算
        batch, n = S.shape
        grad = np.zeros((batch, n, n))
        for i in range(batch):
            Si = S[i]
            grad[i] = np.diag(Si) - np.outer(Si, Si)
        return grad


class TestSoftmax(unittest.TestCase):

    def test_sum_to_one(self):
        """验证 Softmax 输出和为 1"""
        z = np.array([1.0, 2.0, 3.0])
        s = softmax(z)
        self.assertAlmostEqual(np.sum(s), 1.0, places=5)

    def test_numerical_stability(self):
        """验证数值稳定性：减去 max 不影响结果"""
        z1 = np.array([1000, 1001, 1002])
        s1 = softmax(z1)
        z2 = np.array([0, 1, 2])         # 减去 1000
        s2 = softmax(z2)
        np.testing.assert_array_almost_equal(s1, s2)

    def test_combined_gradient(self):
        """验证 Softmax+CE 组合梯度公式"""
        np.random.seed(42)
        z = np.random.randn(5)
        y_true = np.zeros(5)
        y_true[2] = 1.0                   # one-hot 标签

        grad = softmax_ce_grad(z, y_true)

        # 手动验证：∂L/∂z = S - y
        s = softmax(z)
        expected = s - y_true
        np.testing.assert_array_almost_equal(grad, expected)


if __name__ == "__main__":
    # 演示
    z = np.array([2.0, 1.0, -1.0])
    s = softmax(z)
    print("z =", z)
    print("softmax(z) =", s)
    print("sum =", np.sum(s), "✓" if np.isclose(np.sum(s), 1.0) else "✗")

    print("\n数值稳定性演示：")
    z_huge = np.array([1000, 1001, 1002])
    s_huge = softmax(z_huge)
    print(f"z很大时 softmax = {s_huge}")   # 不会溢出

    print("\n组合梯度演示（Softmax + CE）：")
    y_true = np.array([0., 0., 1.])
    grad = softmax_ce_grad(z, y_true)
    print(f"∂L/∂z = {grad}")
    print("（等于 softmax(z) - y_true）")

    # 运行单元测试
    unittest.main(verbosity=2)
