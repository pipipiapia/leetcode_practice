"""
=============================================================================
面试题 Q45：Label Smoothing + BPR Loss + AUC 优化
=============================================================================

【题目 1】Label Smoothing（正则化防过拟合）
题目：手写带 Label Smoothing 的 Cross Entropy。

Label Smoothing 将硬标签软化：
    y_smooth = y * (1 - ε) + ε / C
其中 ε 是平滑因子（通常 0.1），C 是类别数。

【题目 2】BPR Loss（推荐系统经典）
题目：手写 BPR（Bayesian Personalized Ranking）Loss。

BPR 用于隐式反馈推荐：最大化正样本与负样本的得分差异。
    L = - Σ log σ(r_ui - r_uj)
其中 r_ui 是用户 u 对正物品 i 的预测分，r_uj 是对负物品 j 的预测分。

【题目 3】AUC 友好的 Loss 变体
题目：解释并实现一种 AUC 可优化的损失函数。

=============================================================================
"""

import numpy as np
import unittest


# ───────────────────────────────────────────────────────────────────────────
# Q45-1: Label Smoothing Cross Entropy
# ───────────────────────────────────────────────────────────────────────────
def label_smoothing_ce(logits: np.ndarray, labels: np.ndarray,
                       epsilon: float = 0.1) -> float:
    """
    带 Label Smoothing 的 Cross Entropy Loss。

    Args:
        logits: (N, C) 未归一化分数
        labels: (N,) 整数标签，或 (N, C) one-hot
        epsilon: 平滑系数，默认 0.1

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ───────────────────────────────────────────────────────────────────────────
# Q45-2: BPR Loss
# ───────────────────────────────────────────────────────────────────────────
def bpr_loss(pos_scores: np.ndarray, neg_scores: np.ndarray) -> float:
    """
    BPR Loss for 推荐系统。

    Args:
        pos_scores: 用户对正样本的预测分，shape (N,)
        neg_scores: 用户对负样本的预测分，shape (N,)

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ───────────────────────────────────────────────────────────────────────────
# Q45-3: AUC-friendly Pairwise Loss
# ───────────────────────────────────────────────────────────────────────────
def auc_pairwise_loss(scores_pos: np.ndarray, scores_neg: np.ndarray) -> float:
    """
    AUC 友好的 Pairwise Hinge Loss。

    核心：让正样本得分比负样本高至少 1 的 margin。
    L = Σ max(0, 1 - (scores_pos - scores_neg))

    Args:
        scores_pos: shape (N,)
        scores_neg: shape (N,)

    Returns:
        标量 loss
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestLosses(unittest.TestCase):
    def test_label_smoothing_reduces_ce(self):
        """平滑后的 loss 应该比硬标签 CE 略低（不过拟合）"""
        np.random.seed(0)
        logits = np.random.randn(200, 10)
        labels = np.random.randint(0, 10, size=200)
        loss_smooth = label_smoothing_ce(logits, labels, epsilon=0.1)
        # 硬标签 CE
        probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
        ce = np.mean(-np.log(probs[np.arange(200), labels] + 1e-9))
        self.assertLessEqual(loss_smooth, ce * 1.1)  # 平滑后不应远大于硬CE

    def test_bpr_gradient_direction(self):
        """正样本得分升高，负样本得分降低时，loss 应该下降"""
        pos_scores = np.array([0.8, 0.5, 0.9])
        neg_scores = np.array([0.3, 0.2, 0.4])

        pos_higher = pos_scores - neg_scores
        neg_higher = neg_scores - pos_scores

        loss_improved = bpr_loss(pos_scores, neg_scores)
        loss_worse    = bpr_loss(neg_scores, pos_scores)
        self.assertLess(loss_improved, loss_worse)

    def test_auc_loss_non_neg(self):
        """Hinge 损失永远非负"""
        np.random.seed(0)
        pos = np.random.randn(50)
        neg = np.random.randn(50)
        loss = auc_pairwise_loss(pos, neg)
        self.assertGreaterEqual(loss, 0)


# ═══════════════════════════════════════════════════════════════════════════
# 思路拆解
# ═══════════════════════════════════════════════════════════════════════════
"""
【Label Smoothing】
把硬标签 y=[0,1,0] 变成 y_smooth=[ε/3, 1-2ε/3, ε/3]（以3分类为例）
→ 模型不会被逼到输出极端概率（p→1），减少过拟合
→ ε=0.1 是默认值（BERT 用的是 0.1）

【BPR Loss】
从贝叶斯角度推导：最大化观测数据与未观测数据的后验比值
等价于让 pos_score - neg_score 的 sigmoid 值尽可能大
→ 直接优化 pairwise ranking，不受 absolute scores 影响

【AUC-friendly Loss】
AUC = P(score_pos > score_neg)
Hinge loss max(0, 1 - (s_pos - s_neg)) 直接对标 AUC
类似 SVM 的间隔准则

【推荐系统常用 Loss 对比】
  - Pointwise（CE）：预测绝对分数，不建模排序
  - Pairwise（BPR）：建模两两相对排序
  - Listwise（LambdaMART）：直接优化 NDCG 等排序指标
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
