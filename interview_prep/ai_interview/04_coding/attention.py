#!/usr/bin/env python3
"""
Q: 手写 Attention 机制

面试常问：
1. Attention 的计算公式是什么？
2. 为什么需要缩放因子（√d_k）？
3. Self-Attention 和普通 Attention 有什么区别？

标准 Attention（Bahdanau / 加性Attention）：
  Score(h_i, s_j) = v^T · tanh(W·h_i + U·s_j)
  α_i = softmax(Score_i)
  c = Σ α_i · h_i

Self-Attention（核心！Transformer 用的就是这个）：
  Q = X · W_Q
  K = X · W_K
  V = X · W_V

  Score = Q · K^T / √d_k
  Attention(Q, K, V) = softmax(Score) · V

缩放因子原因：
  d_k 较大时，Q·K 的点积方差也会变大，
  softmax 后会进入饱和区，梯度接近 0。
  除以 √d_k 让方差稳定。
"""

import numpy as np
import unittest


def attention(query, key, value, mask=None, scale=True):
    """
    标准的 Scaled Dot-Product Attention

    参数：
      query: (batch, seq_len_q, d_k)
      key:   (batch, seq_len_k, d_k)
      value: (batch, seq_len_k, d_v)
      mask:  可选，(batch, seq_len_q, seq_len_k)，True/False 或 0/1
      scale: 是否除以 √d_k

    返回：
      output: (batch, seq_len_q, d_v)
      attention_weights: (batch, seq_len_q, seq_len_k)
    """
    d_k = query.shape[-1]

    # 1. 计算 QK^T
    scores = np.einsum('bqd,bkd->bqk', query, key)  # (batch, seq_q, seq_k)

    # 2. 缩放
    if scale:
        scores = scores / np.sqrt(d_k)

    # 3. Mask（可选）：将 mask 位置设为 -inf
    if mask is not None:
        scores = np.where(mask, scores, -1e9)

    # 4. Softmax
    scores_exp = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attention_weights = scores_exp / (np.sum(scores_exp, axis=-1, keepdims=True) + 1e-9)

    # 5. 加权求和
    output = np.einsum('bqk,bkd->bqd', attention_weights, value)  # (batch, seq_q, d_v)

    return output, attention_weights


class TestAttention(unittest.TestCase):

    def test_output_shape(self):
        """输出形状正确"""
        np.random.seed(42)
        batch, seq_len, d = 2, 5, 8

        Q = np.random.randn(batch, seq_len, d)
        K = np.random.randn(batch, seq_len, d)
        V = np.random.randn(batch, seq_len, d)

        out, attn = attention(Q, K, V)

        self.assertEqual(out.shape, (batch, seq_len, d))
        self.assertEqual(attn.shape, (batch, seq_len, seq_len))

    def test_attention_weights_sum_to_one(self):
        """每行注意力权重和为 1"""
        np.random.seed(0)
        Q = np.random.randn(1, 4, 8)
        K = np.random.randn(1, 4, 8)
        V = np.random.randn(1, 4, 8)

        _, attn = attention(Q, K, V)
        row_sums = np.sum(attn, axis=-1)

        np.testing.assert_array_almost_equal(row_sums, np.ones_like(row_sums), decimal=5)

    def test_self_vs_cross_attention(self):
        """Self-Attention（Q=K=V） vs Cross-Attention（Q≠K）"""
        np.random.seed(0)
        batch, seq_q, seq_k, d = 2, 5, 3, 8

        X = np.random.randn(batch, seq_q, d)   # encoder
        Y = np.random.randn(batch, seq_k, d)  # decoder

        # Self-Attention: Q=K=V=X
        out_self, _ = attention(X, X, X)
        self.assertEqual(out_self.shape, (batch, seq_q, d))

        # Cross-Attention: Q来自Y, K,V来自X
        out_cross, _ = attention(Y, X, X)
        self.assertEqual(out_cross.shape, (batch, seq_k, d))


if __name__ == "__main__":
    print("=" * 50)
    print("Scaled Dot-Product Attention 演示")
    print("=" * 50)

    np.random.seed(0)
    batch, seq_len, d = 1, 4, 8

    # 模拟输入序列
    x = np.random.randn(batch, seq_len, d)
    Q = x; K = x; V = x  # Self-Attention

    out, attn = attention(Q, K, V)

    print(f"输入 X shape: {x.shape}")
    print(f"输出 O shape: {out.shape}")
    print(f"\n注意力权重矩阵（第一行，即第一个 Query 对所有 Key 的注意力）：")
    print(attn[0, 0].round(3))

    print("\n" + "=" * 50)
    print("Multi-Head Attention（多头注意力）")
    print("=" * 50)
    print("""
# PyTorch 实现逻辑：
d_model = 512
num_heads = 8
d_k = d_v = d_model // num_heads  # 64

W_Q = nn.Linear(d_model, d_model)
W_K = nn.Linear(d_model, d_model)
W_V = nn.Linear(d_model, d_model)
W_O = nn.Linear(d_model, d_model)

Q = W_Q(x).view(batch, seq_len, num_heads, d_k).transpose(1, 2)   # (B, H, L, d_k)
K = W_K(x).view(batch, seq_len, num_heads, d_k).transpose(1, 2)
V = W_V(x).view(batch, seq_len, num_heads, d_v).transpose(1, 2)

attn_out, _ = attention(Q, K, V)
attn_out = attn_out.transpose(1, 2).contiguous().view(batch, seq_len, d_model)
output = W_O(attn_out)
""")

    print("多头的好处：每个头可以关注不同类型的相关性（位置、语法、语义等）")

    unittest.main(verbosity=2)
