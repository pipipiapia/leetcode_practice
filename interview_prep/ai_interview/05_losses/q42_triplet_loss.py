"""
=============================================================================
面试题 Q42：Triplet Loss（对比学习基础）
=============================================================================

【题目】
手写 Triplet Loss，用于学习有区分度的 Embedding。

给定：
  - anchor（锚样本）a
  - positive（同类别）p
  - negative（不同类别）n

要求：d(a, p) + margin < d(a, n)

即：让同类样本距离近，异类样本距离远，至少相差 margin。

公式：
    L = max(0, d(a,p) - d(a,n) + margin)

=============================================================================
"""

import numpy as np
import unittest


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """计算欧氏距离，支持批量。"""
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


def triplet_loss(a: np.ndarray, p: np.ndarray, n: np.ndarray,
                 margin: float = 1.0) -> float:
    """
    Triplet Loss，支持批量。

    Args:
        a: anchor embeddings，shape (N, D)
        p: positive embeddings，shape (N, D)
        n: negative embeddings，shape (N, D)
        margin: 间隔，默认 1.0

    Returns:
        标量 loss（仅对违反 margin 的三元组求平均）
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


def triplet_hard_mining(a: np.ndarray, p: np.ndarray, n: np.ndarray,
                         margin: float = 1.0) -> float:
    """
    Hard Triplet Loss：只对最难的三元组计算。
    - hardest positive：与 anchor 距离最远的正样本
    - hardest negative：与 anchor 距离最近的负样本

    Args:
        a, p, n: embeddings，同上
        margin: 间隔

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestTriplet(unittest.TestCase):
    def test_triplet_violation(self):
        """违反 margin 的三元组，loss 应该 > 0"""
        a = np.array([[0.0, 0.0]])
        p = np.array([[1.0, 0.0]])    # d(a,p) = 1
        n = np.array([[1.1, 0.0]])    # d(a,n) = 1.1，margin=0.5 → 违反
        loss = triplet_loss(a, p, n, margin=0.5)
        self.assertGreater(loss, 0)

    def test_triplet_satisfied(self):
        """满足 margin 的三元组，loss 应该 = 0"""
        a = np.array([[0.0, 0.0]])
        p = np.array([[1.0, 0.0]])    # d(a,p) = 1
        n = np.array([[3.0, 0.0]])    # d(a,n) = 3，满足 margin=0.5
        loss = triplet_loss(a, p, n, margin=0.5)
        self.assertEqual(loss, 0.0)

    def test_batch_shape(self):
        np.random.seed(0)
        a = np.random.randn(4, 128)
        p = np.random.randn(4, 128)
        n = np.random.randn(4, 128)
        loss = triplet_loss(a, p, n)
        self.assertEqual((), np.shape(loss))
        self.assertTrue(loss >= 0)


# ═══════════════════════════════════════════════════════════════════════════
# 思路拆解
# ═══════════════════════════════════════════════════════════════════════════
"""
【Triplet Loss 核心】
1. 先算 d(a,p) 和 d(a,n)，常用 L2 距离
2. 用 max(0, d_ap - d_an + margin) 限制，只有违反时才有梯度

【三种 Triplet 策略】
  - Easy triplet：d_ap + margin < d_an，loss=0，无需学习
  - Semi-hard：d_ap < d_an < d_ap + margin，仍有梯度但信号弱
  - Hard triplet：d_an < d_ap，最难，梯度最强

【面试追问】
Q: Triplet Loss vs Contrastive Loss？
A: Contrastive Loss（成对）用正负样本对，同类拉近/异类推开；
   Triplet Loss（三元组）显式引入 margin，约束更清晰。

Q: Hard Mining 有什么问题？
A: 极端负样本太多可能导致训练早期loss爆炸；通常用 Semi-hard 或逐步降低 margin。
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
