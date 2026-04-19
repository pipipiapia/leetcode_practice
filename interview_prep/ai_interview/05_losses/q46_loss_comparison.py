"""
=============================================================================
面试题 Q46：Loss 函数全景对比（高频综合题）
=============================================================================

【题目】
面试官可能让你对比以下 Loss，不要求手写，但要求深刻理解：

  1. MSE / L2 Loss          → 回归
  2. BCE with Logits        → 二分类
  3. Cross Entropy          → 多分类
  4. Focal Loss             → 类别不平衡
  5. Triplet / Contrastive  → 表征学习
  6. BPR Loss               → 推荐排序
  7. Gumbel Softmax / Straight-Through → 离散表征

请写出每种 loss 的核心公式、适用场景、以及面试追问答案。

=============================================================================
"""

import numpy as np
import unittest


def mse_loss(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """L2 Loss：回归首选"""
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


def bce_logits_loss(logits: np.ndarray, targets: np.ndarray) -> float:
    """
    BCE with Logits（二分类，数值稳定版）。
    等价于：sigmoid(logits) 后算 BCE，但更稳定。
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestMSEBCE(unittest.TestCase):
    def test_mse_shape(self):
        np.random.seed(0)
        y_pred = np.random.randn(100)
        y_true = np.random.randn(100)
        loss = mse_loss(y_pred, y_true)
        self.assertEqual((), np.shape(loss))

    def test_bce_logits_stable(self):
        """大负值 logits 不应溢出"""
        logits = np.array([[-50.0], [50.0], [0.0]])
        targets = np.array([[0.0], [1.0], [0.5]])
        loss = bce_logits_loss(logits, targets)
        self.assertFalse(np.isnan(loss))
        self.assertFalse(np.isinf(loss))


# ═══════════════════════════════════════════════════════════════════════════
# Loss 函数对比表（面试背诵版）
# ═══════════════════════════════════════════════════════════════════════════
"""
┌──────────────────┬──────────────────────────────┬──────────────────────────┐
│ Loss             │ 核心公式                      │ 适用场景                  │
├──────────────────┼──────────────────────────────┼──────────────────────────┤
│ MSE / L2         │ (y-ŷ)² 均值                  │ 回归、VAE、重建任务       │
│ MAE / L1         │ |y-ŷ| 均值                   │ 回归、对异常值鲁棒        │
│ BCE Logits       │ -[y·logσ(x)+(1-y)·log(1-σ)]  │ 二分类、隐式反馈推荐      │
│ Cross Entropy    │ -Σ y_i·log(p_i)              │ 多分类（NLP、图像分类）   │
│ Focal Loss       │ -(1-p_t)^γ · log(p_t)         │ 类别不平衡、长尾检测      │
│ Triplet Margin   │ max(0, d+ - d- + margin)     │ 人脸识别、度量学习        │
│ InfoNCE / NT-Xent│ -log exp(sim/τ)/Σexp(sim/τ)  │ 对比学习（SimCLR/CLIP）  │
│ BPR Loss         │ -log σ(s_pos - s_neg)         │ 推荐排序、隐式反馈        │
│ Hinge / SVM      │ max(0, 1 - y·s)              │ SVM、大间隔分类           │
│ Gumbel Softmax   │ CE(q(y=argmax), p_θ)         │ 离散变量重参数化          │
│ Label Smoothing  │ CE(soft_labels)               │ 正则化、防止overconfidence│
└──────────────────┴──────────────────────────────┴──────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

【面试高频追问 + 标准答案】

Q1: MSE 和 MAE 哪个对异常值更鲁棒？为什么？
A: MAE 更鲁棒，因为 MSE 对误差的平方会放大异常点的影响。
   但 MAE 梯度处处是 ±1，优化困难（不可导点：y=ŷ）；
   实际中可做 Huber Loss：MSE + MAE 混合。

Q2: BCE 和 CE 有什么区别？
A: BCE 作用于二分类（标签 0/1），是 CE 的 C=2 特殊形式。
   CE 标签可以是 one-hot 或概率分布。

Q3: 为什么分类用 CE 而不是 MSE？
A: ① MSE 梯度在 p→0/1 时趋于零（梯度消失），收敛极慢；
   ② CE 的梯度与预测误差线性相关，收敛快；
   ③ 从概率角度：最小化 CE 等价于最大化似然估计（MLE）。

Q4: Focal Loss 的 γ 怎么选？
A: γ=2 是常用默认值。任务越不平衡、难易样本差距越大，γ 可以调高（3~5）。
   建议用验证集调参，γ=0 时退化为普通 CE。

Q5: 对比学习的负样本重要还是正样本重要？
A: 都很重要，但负样本质量和数量更关键：
   - 负样本太少→对比信号弱，学不到好表征
   - 负样本太简单（和正样本太远）→loss很快趋0，无梯度
   - MoCo/COLAS 等方法通过队列/momentum 增大负样本集

Q6: BPR vs CE，在推荐里哪个更好？
A: BPR 直接建模排序，CE 只建模点击概率。
   如果目标是优化 AUC/排序，推荐用 BPR 或 LambdaRank。
   如果是 CTR 预估（绝对概率预测），用 BCE/CE 更合适。
   实际中可两者加权组合（multi-task）。

Q7: Gumbel Softmax 的作用？
A: 让离散变量（如词表中选词）可反向传播。
   用 Gumbel(0,1) 噪声 + softmax 近似 argmax（重参数化），
   straight-through 版本直接在前向时取 argmax，反向时用 softmax 梯度。

═══════════════════════════════════════════════════════════════════════════
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
