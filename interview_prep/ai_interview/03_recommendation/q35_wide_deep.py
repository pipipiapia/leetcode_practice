#!/usr/bin/env python3
"""
Q35: Wide&Deep 模型

面试常问：
1. Wide&Deep 的原理是什么？
2. Wide 部分和 Deep 部分分别负责什么？
3. Wide&Deep 和 DeepFM 的区别是什么？

Wide&Deep = Wide（记忆）+ Deep（泛化）

Wide 部分：
  输入：稀疏的原始特征 + 人工设计的特征交叉（Cross Product）
  模型：线性模型（L1 正则化 LR）
  作用：记住用户的历史行为模式（短期高频）
  典型特征：用户点击过的类别、历史安装的App

Deep 部分：
  输入：稠密 Embedding + 稀疏特征
  模型：DNN（全连接）
  作用：泛化到从未见过的特征组合
  典型特征：用户兴趣的稠密表达

联合训练：
  P(Y=1|x) = σ(W_wide^T [x, φ(x)] + W_deep^T a^{(l)} + b)
  Wide 和 Deep 的输出一起作为最终 logits，共享同一个输出层
"""

import numpy as np


class WideComponent:
    """
    Wide 部分：稀疏特征 + Cross Product 特征交叉
    核心作用：记忆（ Memorization）
    """
    def __init__(self, input_dim):
        # 实际中用 L1 正则化的 SGD/LR，这里简化为线性层
        self.w = np.random.randn(input_dim) * 0.01
        self.b = 0.0

    def forward(self, x):
        """x: (batch, input_dim)"""
        return x @ self.w + self.b


class DeepComponent:
    """
    Deep 部分：DNN 提取稠密特征
    核心作用：泛化（Generalization）
    """
    def __init__(self, embed_dim, hidden_dims=[128, 64]):
        self.embed_dim = embed_dim
        self.Ws = []
        self.bs = []

        prev_dim = embed_dim
        for h_dim in hidden_dims:
            self.Ws.append(np.random.randn(prev_dim, h_dim) * np.sqrt(2.0 / prev_dim))
            self.bs.append(np.zeros(h_dim))
            prev_dim = h_dim

        self.output_dim = prev_dim

    def forward(self, x):
        """x: (batch, embed_dim)"""
        h = x
        for W, b in zip(self.Ws, self.bs):
            h = np.tanh(h @ W + b)
        return h


class WideAndDeep:
    """
    Wide & Deep 联合模型
    """
    def __init__(self, sparse_dim, embed_dim=32, hidden_dims=[128, 64]):
        self.wide = WideComponent(sparse_dim)
        self.deep = DeepComponent(embed_dim, hidden_dims)

        # 联合输出层
        self.W_out = np.random.randn(
            self.wide.b + self.Ws[-1].shape[1] if hasattr(self, 'Ws') else 1 + hidden_dims[-1]
        ) * 0.01
        self.b_out = 0.0

    def forward(self, sparse_x, embed_x):
        """
        sparse_x: (batch, sparse_dim)  — 稀疏特征
        embed_x:  (batch, embed_dim)  — Embedding 特征
        """
        wide_out = self.wide.forward(sparse_x)       # (batch,)
        deep_out = self.deep.forward(embed_x)          # (batch, hidden_last)

        # 拼接 + sigmoid
        concat = np.concatenate([wide_out.reshape(-1, 1), deep_out], axis=1)
        logits = concat @ self.W_out + self.b_out
        probs = 1 / (1 + np.exp(-logits))             # sigmoid

        return probs, logits


# ─── 特征交叉示例 ───────────────────────────────────────────────────
def cross_product_transform(x1, x2):
    """
    Wide 部分常用的 Cross Product 特征交叉
    φ_k(x) = ∏_{i} x_i^{c_ki}   （c_ki ∈ {0, 1}）
    即：x_i 和 x_j 同时为1时，交叉特征为1

    例：用户安装了App A，同时看到App B → 交叉特征=1
    """
    return x1 * x2  # 简化：只做二阶交叉


if __name__ == "__main__":
    print("=" * 50)
    print("Wide&Deep 模型演示")
    print("=" * 50)

    np.random.seed(42)
    batch_size = 32
    sparse_dim = 128
    embed_dim = 32

    # 模拟稀疏特征（用户ID、类别ID等）
    sparse_x = np.random.randint(0, 2, (batch_size, sparse_dim)).astype(float)
    # 模拟 Embedding 特征（DNN 提取的稠密向量）
    embed_x = np.random.randn(batch_size, embed_dim)

    model = WideAndDeep(sparse_dim, embed_dim)
    probs, logits = model.forward(sparse_x, embed_x)

    print(f"稀疏特征 shape: {sparse_x.shape}")
    print(f"Embedding 特征 shape: {embed_x.shape}")
    print(f"输出概率 shape: {probs.shape}")
    print(f"概率范围: [{probs.min():.4f}, {probs.max():.4f}]")

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: Wide&Deep 和 DeepFM 的核心区别是什么？
A: Wide&Deep 的 Wide 部分需要人工设计特征交叉（如 Cross Product）。
   DeepFM 的 Wide 部分用 FM（Factorization Machine）自动学习二阶特征交叉。
   简单说：DeepFM 把"人工设计交叉"换成"自动学习交叉"。

Q: Wide 部分具体用哪些特征？
A: 稀疏的 ID 类特征、历史行为序列的计数特征。
   例如：用户过去7天安装的App类别、过去点击的类别交叉。
   这些特征高频出现，Wide 能很好记住。

Q: Deep 部分输入是什么？
A: Embedding 向量（用户/物品ID经Embedding层得到）。
   Embedding 层将高维稀疏特征压缩到低维稠密空间。

Q: 联合训练 vs 分别训练再融合？
A: Wide&Deep 必须联合训练，因为 Wide 和 Deep 共用输出层。
   分别训练再融合（stacking）也可以，但不如联合训练端到端。
""")
