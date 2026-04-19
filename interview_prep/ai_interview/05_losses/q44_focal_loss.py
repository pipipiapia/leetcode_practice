"""
=============================================================================
面试题 Q44：Focal Loss（解决类别不平衡）
=============================================================================

【题目】
手写 Focal Loss，经典用于目标检测（Faster R-CNN）和长尾分布分类。

背景：
  - 大量易分类负样本主导梯度，导致模型被"淹没"
  - Focal Loss 对易分类样本降权，难分类样本提权

公式：
    FL(p_t) = -α_t · (1 - p_t)^γ · log(p_t)

其中 p_t 是模型对真实类别的预测概率：
  - 正样本：p_t = p
  - 负样本：p_t = 1 - p
γ（gamma）：聚焦参数，默认 2.0
  - γ=0：退化为普通 CE
  - γ 越大：易分类样本的权重衰减越快

α（alpha）：类别权重平衡因子。

=============================================================================
"""

import numpy as np
import unittest


def focal_loss(logits: np.ndarray, labels: np.ndarray,
              gamma: float = 2.0,
              alpha: float = None) -> float:
    """
    Binary Focal Loss（支持多类扩展）。

    Args:
        logits: 模型原始输出，shape (N,) 或 (N, C)
        labels: 真实标签，shape (N,)，值为 0/1（针对二分类）
                多分类时用 one-hot
        gamma: 聚焦参数，默认 2.0
        alpha: 正负样本权重，如 alpha=0.25 表示正样本权重

    Returns:
        标量 loss（平均）
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


class TestFocalLoss(unittest.TestCase):
    def test_high_confidence_easy_negative(self):
        """高置信度负样本应该被大幅降权"""
        # 负样本，模型预测 p=0.95（很自信），但这是错的
        logits = np.array([-3.0])  # sigmoid ≈ 0.047 → 接近0，但这里是错的？
        # 其实对于二分类，label=0 时 logit 越小越好
        # label=0, logit=-3 → p=0.047，正确，接近0
        # 如果 logit=3 → p=0.95，这是错误的预测，应该被 focal loss 降权
        wrong_logits = np.array([3.0])   # 预测 p≈0.95，但 label=0
        right_logits = np.array([-3.0])  # 预测 p≈0.05，label=0，正确
        labels = np.array([0])
        loss_wrong = focal_loss(wrong_logits, labels, gamma=2.0)
        loss_right = focal_loss(right_logits, labels, gamma=2.0)
        # focal loss 对错误的高置信样本应该惩罚更重
        self.assertGreater(loss_wrong, loss_right)

    def test_focal_degrades_to_ce(self):
        """gamma=0 时退化为普通交叉熵"""
        logits = np.array([1.0, -1.0, 2.0])
        labels = np.array([1, 0, 1])
        loss_focal = focal_loss(logits, labels, gamma=0.0)
        # 应该约等于普通 BCE
        p = 1 / (1 + np.exp(-logits))
        ce = -np.mean(labels * np.log(p + 1e-9) + (1 - labels) * np.log(1 - p + 1e-9))
        self.assertAlmostEqual(loss_focal, ce, places=4)

    def test_output_range(self):
        np.random.seed(42)
        logits = np.random.randn(100)
        labels = np.random.randint(0, 2, size=100)
        loss = focal_loss(logits, labels)
        self.assertTrue(0 <= loss <= 5)


# ═══════════════════════════════════════════════════════════════════════════
# 思路拆解
# ═══════════════════════════════════════════════════════════════════════════
"""
【Focal Loss 推导】
1. 普通 CE：-log(p_t)，对所有样本权重相同
2. 加调制因子：(1 - p_t)^γ
   - 当 p_t 高（易分类）：(1-p_t)^γ → 趋近 0，权重降低
   - 当 p_t 低（难分类）：(1-p_t)^γ → 趋近 1，权重不变
3. γ 控制衰减速度：
   - γ=0 → 无衰减（退化为 CE）
   - γ=2 → 常见默认值，p=0.95 时权重降至 0.3%

【和类别不平衡处理方法的关系】
  - Oversampling：简单但容易过拟合少数类
  - Class weighting（α）：硬降权，可能欠拟合
  - Focal Loss：自适应降权，不依赖人工设权重，更优雅

【面试追问】
Q: Focal Loss 在推荐系统有用吗？
A: 有，特别是长尾物品推荐、异常检测、稀少事件预测（如CTR中长尾广告）。
"""
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main()
