"""
=============================================================================
面试题 Q43：InfoNCE Loss（Contrastive Learning 核心）
=============================================================================

【题目】
手写 InfoNCE Loss（SimCLR / CLIP / 对比学习标配）。

InfoNCE 是估计互信息下界的损失函数，核心思想：
  - 给定一个 query，和 N-1 个负样本
  - 正样本与 query 的相似度要远高于负样本

公式（温度系数 τ）：
    L = - log [ exp(sim(q,k+)/τ) / Σ exp(sim(q,ki)/τ) ]

其中 k+ 是正样本，ki 包含正样本 + N-1 个负样本。

=============================================================================
"""

import numpy as np
import unittest


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """计算行向量的余弦相似度，返回 shape (N,)。"""
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


def info_nce(q: np.ndarray, k_pos: np.ndarray, k_neg: np.ndarray,
             tau: float = 0.07) -> float:
    """
    Batch-level InfoNCE Loss。

    Args:
        q:      query embeddings，shape (B, D)
        k_pos:  正样本 embeddings，shape (B, D)
        k_neg:  负样本 embeddings，shape (B, N_neg, D)
                B=batch_size，N_neg=负样本数
        tau:    温度系数，默认 0.07（SimCLR 默认值）

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestInfoNCE(unittest.TestCase):
    def test_info_nce_positive(self):
        """正样本与 query 完全相同，loss 应该 → 0"""
        np.random.seed(0)
        q = np.random.randn(4, 64)
        k_pos = q + np.random.randn(4, 64) * 0.01   # 几乎相同，加小噪声
        k_neg = np.random.randn(4, 8, 64)            # 随机负样本
        loss = info_nce(q, k_pos, k_neg, tau=0.07)
        self.assertTrue(0 <= loss < 3.0)

    def test_info_nce_numerical_stability(self):
        """大相似度时不能溢出（用 -max 技巧）"""
        np.random.seed(0)
        q = np.random.randn(4, 64) * 5.0   # 大幅值，容易产生大 exp 值
        k_pos = np.random.randn(4, 64) * 5.0
        k_neg = np.random.randn(4, 16, 64) * 5.0
        loss = info_nce(q, k_pos, k_neg, tau=0.07)
        self.assertFalse(np.isnan(loss))
        self.assertFalse(np.isinf(loss))

    def test_loss_shape(self):
        np.random.seed(0)
        q = np.random.randn(4, 64)
        k_pos = np.random.randn(4, 64)
        k_neg = np.random.randn(4, 8, 64)
        loss = info_nce(q, k_pos, k_neg)
        self.assertEqual((), np.shape(loss))


# ═══════════════════════════════════════════════════════════════════════════
# 思路拆解
# ═══════════════════════════════════════════════════════════════════════════
"""
【InfoNCE 步骤拆解】
1. 计算每个 query 和正样本的相似度：sim(q, k+)
2. 计算每个 query 和所有负样本的相似度：sim(q, k_i)
3. 拼接：[sim(q,k+), sim(q,k_1), ..., sim(q,k_N)]
4. 除以温度系数 τ，用 -max 技巧保证数值稳定
5. softmax → 取正样本位置的概率 → log → 加负号

【温度系数 τ 的影响】
  - τ 小（如 0.01~0.1）：分布更 sharp，相似度差异放大，难样本被强调
  - τ 大（如 1.0）：分布更平滑，loss 更均匀，训练更稳定
  - SimCLR 默认 τ=0.07；CLIP 用 τ=0.01~0.1 可调

【InfoNCE vs NT-Xent】
  - NT-Xent = Normalized Temperature-scaled Cross Entropy
  - 本质和 InfoNCE 一样，InfoNCE 是理论名称，NT-Xent 是工程别名

【面试追问】
Q: InfoNCE 为什么有效？
A: 它是互信息的下界估计。最小化 InfoNCE 等价于最大化正样本互信息，
   同时最小化与负样本的互信息。

Q: 负样本数量越多越好吗？
A: 在一定范围内是，但有以下trade-off：
   - 负样本越多 → 对比信号越强 → 表征越好
   - 但内存消耗和计算量线性增长
   - 负样本质量也重要（太相似的负样本没有区分度）

Q: 对比学习在推荐系统里怎么用？
A: 可以用在用户/物品表征学习（如 SimCLR 推荐、CCL），用对比loss增强
   用户行为序列或物品特征的表示学习。
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
