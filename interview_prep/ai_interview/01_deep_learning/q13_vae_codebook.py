#!/usr/bin/env python3
"""
Q13: 码本（Codebook）与 VAE 的关系

面试常问：
1. VAE 和 VQ-VAE 的区别是什么？
2. 码本（Codebook）是什么？是如何训练的？
3. 为什么需要把连续 latent 变成离散的？
4. 后验塌缩（Posterior Collapse）是什么？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一、标准 VAE：连续 latent space
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VAE（Variational Autoencoder）的核心：
  encoder  输出两个向量：均值 μ 和方差 σ²
  通过重参数化技巧采样：z = μ + σ * ε（ε ~ N(0,1)）
  decoder  接收连续向量 z，重建输入

训练目标：重建损失 + KL( q(z|x) || p(z) )
  → 迫使 latent 分布接近标准正态分布 N(0,1)

问题：后验塌缩（Posterior Collapse）
  decoder 学会忽略 latent，直接重建输入
  → latent 根本没有学到有意义的信息
  GPT 里也遇到过类似问题

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
二、VQ-VAE：把连续采样换成码本查找
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VQ-VAE（Vector Quantized VAE）的核心改动：
  encoder 输出连续向量 → 去码本里找最近邻 → 用码本向量替代 → decoder

前向传播：
  x → encoder(z) → 最近邻码本向量 → decoder → x_hat
                    ↑ 离散化

所以 VQ-VAE 本质上是 VAE 框架的延续，
只是把 latent 从"连续分布"改成了"离散码本"。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三、码本（Codebook）到底是什么
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

码本是一个可学习的向量表（embedding table）：
  形状：(K, D)
  K = 码本大小（e.g. 8192）
  D = 每个码向量的维度（e.g. 256）

每个 latent 位置输出的连续向量，去码本里找最近的码向量：
  z_e(x)  = encoder(x)                          # 连续向量 (H*W, D)
  idx     = argmin_i || z_e(x) - e_i ||²       # 找最近邻
  z_q(x)  = e_idx                               # 用码向量替代

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
四、码本是如何训练的（关键：stop_gradient）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

三个损失共同作用：

① 重建损失（decoder）：
   L_recon = || x - decoder(z_q(x)) ||²

② 码本损失（更新码本）：
   L_codebook = || z_e(x) - sg(z_q(x)) ||²
   → 用 encoder 输出去靠近码本（码本为可学习参数）

③ 承诺损失（约束 encoder）：
   L_commit = || sg(z_e(x)) - z_q(x) ||²
   → 让 encoder 输出不要离码本太远

sg = stop_gradient（停止梯度回传）
→ 码本损失不传梯度给 encoder
→ 承诺损失不传梯度给码本
这样各自更新，互不干扰。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
五、关键对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                 标准 VAE              VQ-VAE
──────────────────────────────────────────────────
latent 空间      连续（实数向量）        离散（码本索引）
latent 分布      正态分布 N(μ,σ²)       码本嵌入向量 {e_i}
可导方式         重参数化技巧           stop_gradient + straight-through
生成方式         采样后解码             从码本随机采样/指定索引
典型用途         插值、生成             离散token序列（Audio/Video/图像生成）
缓解塌缩         一般                 天然缓解（decoder无法绕过latent）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
六、为什么大模型都用 VQ-VAE 的离散设计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 消除后验塌缩
   decoder 无法绕过 latent 直接重建，因为它只能接收码本中的离散向量。

2. 和 Language Model 架构兼容
   离散 token = 码本索引，可以像文本 token 一样做自回归生成。
   VAR（Visual Autoregressive）：图像 → 离散视觉 token → 自回归生成

3. 压缩信息，统一模态
   DiT / Sora：像素 → VAE 压缩 → latent 空间 → diffusion 生成
   VAE 把信息压缩到低维，diffusion 只在高压缩空间运作。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
七、代码示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class VectorQuantizer(nn.Module):
    """
    VQ-VAE 核心：码本量化层
    """
    def __init__(self, num_embeddings: int, embedding_dim: int, commitment_cost: float = 0.25):
        super().__init__()
        self.num_embeddings = num_embeddings   # K：码本大小
        self.embedding_dim = embedding_dim     # D：码向量维度
        self.commitment_cost = commitment_cost

        # 可学习的码本 (K, D)
        self.embedding = nn.Embedding(num_embeddings, embedding_dim)
        self.embedding.weight.data.uniform_(-1.0 / num_embeddings, 1.0 / num_embeddings)

    def forward(self, z: torch.Tensor):
        """
        z: (B, D, H, W) — encoder 输出的连续向量
        返回: (B, D, H, W) — 量化后的向量
        """
        B, D, H, W = z.shape

        # flatten: (B*H*W, D)
        z_flat = z.permute(0, 2, 3, 1).contiguous().view(-1, D)

        # 计算每个位置和所有码向量的欧氏距离
        # (BHW, D) @ (K, D)^T → (BHW, K)
        d = torch.sum(z_flat ** 2, dim=1, keepdim=True) + \
            torch.sum(self.embedding.weight ** 2, dim=1) - \
            2 * (z_flat @ self.embedding.weight.T)

        # 最近邻索引
        min_encoding_indices = torch.argmin(d, dim=1)  # (BHW,)
        z_q = self.embedding(min_encoding_indices)     # (BHW, D) ← 码向量

        # reshape back: (B, H, W, D) → (B, D, H, W)
        z_q = z_q.view(B, H, W, D).permute(0, 3, 1, 2).contiguous()

        # 三个损失
        # 1. 重建用量化向量（straight-through: 直接用 z_q 替代 z）
        loss_recon = F.mse_loss(z, z_q.detach())           # decoder 能看到 z_q
        # 2. 码本损失：encoder 输出靠近码本
        loss_codebook = F.mse_loss(z.detach(), z_q)         # 更新码本
        # 3. 承诺损失：encoder 不要离码本太远
        loss_commit = F.mse_loss(z, z_q.detach())

        loss = loss_recon + loss_codebook + self.commitment_cost * loss_commit

        # straight-through: 前向传播时用 z_q，反向传播时梯度跳过量化
        z_q = z + (z_q - z).detach()

        return z_q, loss, min_encoding_indices


def demo_codebook_lookup():
    """演示码本查找过程"""
    print("=" * 50)
    print("码本查找过程演示")
    print("=" * 50)

    # 假设 encoder 输出 (1, 4, 2, 2) = (B, D, H, W)
    z = torch.randn(1, 4, 2, 2)
    print(f"encoder 输出 z (B={1}, D={4}, H={2}, W={2}):\n{z}")

    codebook = nn.Embedding(num_embeddings=8, embedding_dim=4)
    print(f"\n码本形状: {codebook.num_embeddings} 个, 每维 {codebook.embedding_dim} 维")

    # flatten: (4, 4)
    z_flat = z.permute(0, 2, 3, 1).contiguous().view(-1, 4)
    print(f"\n展平后: {z_flat.shape}")

    # 最近邻查找
    d = torch.cdist(z_flat, codebook.weight)  # (4, 8)
    print(f"\n距离矩阵 (4个位置 × 8个码向量):\n{d.round(2)}")

    indices = torch.argmin(d, dim=1)
    print(f"\n每个位置的最近邻码向量索引: {indices}")
    print(f"对应的码向量:\n{codebook(indices)}")


if __name__ == "__main__":
    demo_codebook_lookup()

    print("=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: VAE 和 VQ-VAE 的核心区别？
A: VAE 的 latent 是连续向量（采样），VQ-VAE 把连续向量量化成离散的码本索引。
   离散设计让 latent 无法被 decoder 绕过，天然缓解后验塌缩。

Q: 码本是怎么训练的？
A: 和 encoder、decoder 一起端到端训练。三个损失：重建损失（decoder）、
   码本损失（更新码本）、承诺损失（约束 encoder）。用 stop_gradient
   解决离散操作不可导的问题。

Q: 为什么视觉生成模型都用 VAE？
A: VAE 把像素空间压缩到低维 latent 空间（如 8× 下采样），
   Diffusion/自回归只在 latent 空间运作，大幅降低计算量。
   VQ-VAE 进一步离散化，让 latent 可以像文本 token 一样自回归生成。

Q: stop_gradient 在 VQ-VAE 里怎么用？
A: 前向：z_q 直接替换 z（straight-through，梯度无损）
   反向：码本损失的梯度不传给 encoder，承诺损失的梯度不传给码本。
   这样码本和 encoder 各更新各的，互不干扰。
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 附：补充知识
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 码本的数学原理（信息论角度）：
# ① 率失真理论（Shannon, 1959）：连续信号无限精度无法存储，必须量化
#    码本大小 K → bitrate = log₂(K) → 更大的 K = 更低失真
# ② Lloyd-Max 算法（1957）：最优量化等价于 K-Means
#    最近邻条件 + 质心条件 → VQ-VAE 的端到端训练就是实现这两条
# ③ 离散化 = 强制信息瓶颈
#    强制模型用有限离散符号表达丰富信息，避免后验塌缩
#
# 码本不是唯一的解：
#   - VAE（连续）+ KL 约束
#   - 正则化流（NF）：可逆变换保持连续分布
#   - 扩散模型（DDPM）：逐步加噪去噪，连续 latent
# VQ 的优势：离散 token 与 LLM 架构天然兼容，组合性强，工程稳定


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 附：大模型里的实际应用
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# DiT (Diffusion Transformer):
#   VAE encoder 压缩像素 → latent 空间 → Diffusion 生成 → VAE decoder 还原
#
# VAR (Visual Autoregressive):
#   VQ-GAN（VQ + GAN + VAE decoder）→ 图像离散成视觉 token → 自回归生成
#
# Sora / Stable Diffusion:
#   VAE 架构做时空压缩（视频 → latent → diffusion → 重建）
#
# 总结：码本 = VQ-VAE 离散化 VAE 的核心组件，
#       是当前所有视觉生成模型压缩信息的关键设计。
