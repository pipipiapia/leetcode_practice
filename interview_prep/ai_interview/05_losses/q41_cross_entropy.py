"""
=============================================================================
面试题 Q41：手写 Cross Entropy Loss（含数值稳定版）
=============================================================================

【题目】
不使用任何库，手写 Cross Entropy Loss，并解释为什么要做数值稳定处理。

【背景】
Cross Entropy 是分类任务最常用的损失函数，公式：
    CE(y, p) = - Σ y_i * log(p_i)

面试高频追问：
  - CE 和 BCE 有什么区别？
  - Softmax + CE 为什么要一起用？
  - 数值不稳定是怎么发生的？

=============================================================================
"""

import numpy as np
import unittest


def cross_entropy_one_hot(logits: np.ndarray, labels: np.ndarray) -> float:
    """
    使用 one-hot 标签的 CE Loss，手写版本（不稳定版）。

    Args:
        logits: 模型输出，shape (N, C)，未归一化的原始分数
        labels: one-hot 标签，shape (N, C)

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


def cross_entropy_stable(logits: np.ndarray, labels: np.ndarray) -> float:
    """
    数值稳定的 Cross Entropy Loss。

    技巧：对 logit 减去 max(logits)，避免 exp(logit) 溢出。

    Args:
        logits: 模型输出，shape (N, C)，未归一化的原始分数
        labels: one-hot 标签，shape (N, C)

    Returns:
        标量 loss（平均）
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestCrossEntropy(unittest.TestCase):
    def test_ce_output_shape(self):
        np.random.seed(42)
        logits = np.random.randn(8, 10).astype(np.float64)
        labels = np.eye(10)[np.random.randint(0, 10, size=8)]
        loss = cross_entropy_stable(logits, labels)
        self.assertEqual((), np.shape(loss))
        self.assertTrue(0 <= loss <= 10)

    def test_ce_numerical_stability(self):
        """大 logits 时也不能溢出"""
        logits = np.array([[100.0, 90.0, 80.0]])   # 大 logits，容易溢出
        labels = np.array([[1.0, 0.0, 0.0]])
        loss = cross_entropy_stable(logits, labels)
        self.assertFalse(np.isnan(loss))
        self.assertFalse(np.isinf(loss))
        self.assertTrue(loss >= 0)

    def test_ce_perfect_prediction(self):
        """正确预测时 loss → 0"""
        logits = np.array([[10.0, 0.0, 0.0]])   # 正确类别 logits 最高
        labels = np.array([[1.0, 0.0, 0.0]])
        loss = cross_entropy_stable(logits, labels)
        self.assertTrue(loss < 0.1)


# ═══════════════════════════════════════════════════════════════════════════
# 思路拆解
# ═══════════════════════════════════════════════════════════════════════════
"""
【不稳定版思路】
1. 对 logits 做 softmax：p_i = exp(logit_i) / Σ exp(logit_j)
2. 取正确类别的 p：p_correct
3. 返回 -log(p_correct)

【不稳定的原因】
当 logit 很大（如 100），exp(100) 直接溢出 → inf → log(inf) = inf

【稳定版思路】
在 softmax 内部，对所有 logit 减去 max(logits)：
    exp(logit_i - max) / Σ exp(logit_j - max)

数学上等价，但每个 exp 的输入 ≤ 0，不会溢出。

【面试追问回答】
Q: CE 和 BCE 区别？
A: CE 用在多分类（标签 one-hot），BCE 用在二分类/多标签（标签是 0/1 向量）。
   BCE 可以看作 CE 的特例（多分类 C=2）。

Q: 多分类为什么不用 MSE？
A: MSE 梯度在概率接近 0 或 1 时趋于平坦（梯度消失），收敛慢；
   CE 的梯度与预测误差直接相关，训练更高效。
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
