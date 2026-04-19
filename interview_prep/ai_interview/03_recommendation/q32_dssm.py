#!/usr/bin/env python3
"""
Q32: DSSM 双塔模型（DSSM = Deep Structured Semantic Model）

面试常问：
1. DSSM 的原理是什么？
2. 用户塔和物品塔分别做什么？
3. 为什么 DSSM 适合做召回？
4. DSSM 的优缺点？

原理：
  用户塔：输入用户特征 → 输出用户向量（user embedding）
  物品塔：输入物品特征 → 输出物品向量（item embedding）
  相似度：cosine(user_vec, item_vec) 或 dot(u, v)

  训练目标：拉近（用户，正样本）的相似度，拉远（用户，负样本）的相似度

优势：
  ① 物品向量离线预计算，线上只算用户向量 → 毫秒级检索
  ② 支持海量候选集（百万/亿级）
  ③ 向量检索可近似加速（HNSW / Faiss）

劣势：
  ① 用户塔和物品塔没有特征交叉（双塔隔离）
  ② 召回和排序解耦，召回质量受限于向量表达
"""

import numpy as np


class DSSM:
    """
    简化的 DSSM 双塔实现（纯 NumPy，演示原理）

    实际生产中：
    - 用户塔：输入用户 ID、历史行为序列、用户画像
    - 物品塔：输入物品 ID、类别、标签、描述
    - 相似度：cosine similarity
    - 负采样：batch 内负采样 或 全局负采样
    """

    def __init__(self, user_dim, item_dim, embed_dim=64, hidden_dim=128):
        self.embed_dim = embed_dim

        # 用户塔
        self.user_W = self._init_weights(user_dim, hidden_dim)
        self.user_b = np.zeros(hidden_dim)
        self.user_out = self._init_weights(hidden_dim, embed_dim)
        self.user_out_b = np.zeros(embed_dim)

        # 物品塔
        self.item_W = self._init_weights(item_dim, hidden_dim)
        self.item_b = np.zeros(hidden_dim)
        self.item_out = self._init_weights(hidden_dim, embed_dim)
        self.item_out_b = np.zeros(embed_dim)

    def _init_weights(self, in_dim, out_dim):
        return np.random.randn(in_dim, out_dim) * np.sqrt(2.0 / (in_dim + out_dim))

    def tanh(self, x):
        return np.tanh(x)

    def user_tower(self, x):
        """用户塔：稀疏特征 → 密集向量"""
        h = self.tanh(x @ self.user_W + self.user_b)
        return h @ self.user_out + self.user_out_b

    def item_tower(self, x):
        """物品塔"""
        h = self.tanh(x @ self.item_W + self.item_b)
        return h @ self.item_out + self.item_out_b

    def cosine_similarity(self, u, v):
        """余弦相似度"""
        norm_u = np.linalg.norm(u, axis=-1, keepdims=True)
        norm_v = np.linalg.norm(v, axis=-1, keepdims=True)
        return np.sum(u * v, axis=-1, keepdims=True) / (norm_u * norm_v + 1e-8)

    def forward(self, user_x, pos_item_x, neg_items_x):
        """
        前向传播（batch 内负采样）

        user_x:      (batch, user_dim)    用户特征
        pos_item_x:  (batch, item_dim)    正样本物品
        neg_items_x: (batch, K, item_dim) K 个负样本

        返回:
          pos_sim: 正样本相似度
          neg_sim: 负样本相似度
        """
        # 用户向量
        user_vec = self.user_tower(user_x)                        # (batch, embed)
        # 正样本向量
        pos_vec = self.item_tower(pos_item_x)                     # (batch, embed)
        # 负样本向量
        neg_vecs = np.array([self.item_tower(neg_items_x[:, i])   # (batch, K, embed)
                              for i in range(neg_items_x.shape[1])])
        neg_vec = np.mean(neg_vecs, axis=0)                       # 平均 K 个负样本

        pos_sim = self.cosine_similarity(user_vec, pos_vec)       # (batch, 1)
        neg_sim = self.cosine_similarity(user_vec, neg_vec)      # (batch, 1)

        return pos_sim, neg_sim

    def loss(self, pos_sim, neg_sim):
        """
        DSSM Loss：最大化 pos_sim，最小化 neg_sim

        batch softmax loss:
        L = -log(exp(pos_sim) / (exp(pos_sim) + sum(exp(neg_sim))))
          = log(1 + exp(neg_sim) / exp(pos_sim))
          = log(1 + exp(neg_sim - pos_sim))
        """
        return np.mean(np.log(1 + np.exp(neg_sim - pos_sim)))


if __name__ == "__main__":
    print("=" * 50)
    print("DSSM 双塔模型演示")
    print("=" * 50)

    np.random.seed(42)

    # 参数
    batch_size, K = 32, 4
    user_dim, item_dim, embed_dim = 128, 64, 32

    model = DSSM(user_dim, item_dim, embed_dim)

    # 模拟数据
    user_x = np.random.randn(batch_size, user_dim)
    pos_item_x = np.random.randn(batch_size, item_dim)
    neg_items_x = np.random.randn(batch_size, K, item_dim)

    # 前向
    pos_sim, neg_sim = model.forward(user_x, pos_item_x, neg_items_x)
    loss = model.loss(pos_sim, neg_sim)

    print(f"正样本相似度: mean={pos_sim.mean():.4f}")
    print(f"负样本相似度: mean={neg_sim.mean():.4f}")
    print(f"DSSM Loss: {loss:.4f}")
    print(f"✓ 正样本相似度 > 负样本相似度: {'符合预期' if pos_sim.mean() > neg_sim.mean() else '需训练'}")

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: DSSM 为什么适合做召回？
A: 物品塔可以离线预计算所有物品向量并存起来，
   线上只需要跑用户塔，计算量极小 → 支持毫秒级检索。

Q: DSSM 的核心缺点是什么？
A: 用户塔和物品塔在塔内没有特征交叉。
   对比精排模型（DIN/Wide&Deep），表达能力受限。
   所以 DSSM 只用于召回，精排用更复杂的模型。

Q: 负采样怎么做？
A: ① batch 内负采样：本 batch 内其他用户交互的物品作为负样本
   ② 全局负采样：从全量物品中随机采样（需注意避免采样到正样本）
   ③ 混合采样：batch 内 + 全局随机 组合
""")
