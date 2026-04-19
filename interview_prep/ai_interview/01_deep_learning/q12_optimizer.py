#!/usr/bin/env python3
"""
Q12: SGD / Momentum / Adam 对比

面试常问：
1. SGD、Momentum、Adam 的区别是什么？
2. Adam 为什么收敛快但泛化可能不如 SGD？
3. AdamW 是什么？和 Adam 有什么区别？
4. 什么场景用什么优化器？

SGD：
  θ = θ - lr · ∇L(θ)

Momentum（动量）：
  v = γ·v + lr·∇L(θ)   （累积历史梯度）
  θ = θ - v
  原理：类似物理惯性，穿越平坦区域，加速收敛

AdaGrad：自适应学习率，大参数变小步长（稀疏特征友好）
RMSProp：AdaGrad 的改进，用指数加权移动平均解决历史累积问题

Adam = Momentum + RMSProp：
  m = β1·m + (1-β1)·∇L        ← 梯度的一阶矩估计（类似动量）
  v = β2·v + (1-β2)·(∇L)²    ← 梯度二阶矩估计（类似 RMSProp）
  θ = θ - lr·m / (√v + ε)

AdamW：Adam + 权重衰减（L2 正则化）
  Adam 的 L2 是直接在梯度上加，AdamW 把正则项独立出来
  更清晰，实际效果更好（Adam+L2 ≈ AdamW）
"""

import numpy as np


class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        """params 和 grads 都是 list of np.ndarray"""
        for p, g in zip(params, grads):
            p -= self.lr * g

    def zero_grad(self, params):
        for p in params:
            p.grad = None  # 这里简化处理


class Momentum:
    """
    Momentum 优化器

    物理直觉：
    梯度累积 → 速度 → 参数更新
    在梯度方向一致时加速，在震荡方向抵消
    """
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocity = None

    def step(self, params, grads):
        if self.velocity is None:
            self.velocity = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            self.velocity[i] = self.momentum * self.velocity[i] + self.lr * g
            p -= self.velocity[i]

    def zero_grad(self):
        self.velocity = None


class Adam:
    """
    Adam 优化器

    β1=0.9, β2=0.999, ε=1e-8 是默认值
    """
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = None   # 一阶矩
        self.v = None   # 二阶矩
        self.t = 0      # 步数

    def step(self, params, grads):
        self.t += 1

        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            # 梯度的一阶、二阶矩估计
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g ** 2

            # 偏差校正（纠正启动时向零偏移的问题）
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # 参数更新
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


def optimize_function(optimizer_class, optimizer_kwargs, n_steps=100):
    """
    在简单二次函数上测试优化器收敛速度
    最小化 f(x,y) = x² + y² → 最优解 (0,0)
    """
    x, y = 5.0, 5.0
    params = [np.array([x]), np.array([y])]

    opt = optimizer_class(**optimizer_kwargs)
    losses = []

    for _ in range(n_steps):
        # 梯度：∂(x²+y²)/∂x = 2x，∂(x²+y²)/∂y = 2y
        grads = [2 * params[0], 2 * params[1]]
        opt.step(params, grads)
        losses.append(params[0][0]**2 + params[1][0]**2)

    return losses


if __name__ == "__main__":
    print("=" * 50)
    print("优化器收敛速度对比")
    print("=" * 50)

    n_steps = 100

    losses_sgd = optimize_function(SGD, {'lr': 0.1})
    losses_momentum = optimize_function(Momentum, {'lr': 0.1, 'momentum': 0.9})
    losses_adam = optimize_function(Adam, {'lr': 0.1})

    print(f"\n收敛速度对比（loss 下降过程）：")
    for step in [0, 10, 30, 50, 99]:
        print(f"  Step {step:3d}: SGD={losses_sgd[step]:.4f} | "
              f"Momentum={losses_momentum[step]:.4f} | "
              f"Adam={losses_adam[step]:.4f}")

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: Adam 为什么收敛快但泛化可能不如 SGD？
A: Adam 自适应学习率对每个参数做精细调整 → 快速收敛到训练损失最低点。
   但这种"过拟合训练集"的能力，反而牺牲了泛化能力。
   SGD 的固定/全局学习率约束更强，有隐式正则化效果。
   实际：训练用 Adam 上得快，fine-tuning 后期切 SGD 往往效果更好。

Q: AdamW 和 Adam + L2 有什么区别？
A: Adam 的 L2 正则化是把权重衰减加到梯度里（数值上近似但不等价）。
   AdamW 把权重衰减独立出来，更符合正则化的数学定义。
   结论：AdamW 效果更好，尤其是大模型训练（BERT、ViT 等都用 AdamW）。

Q: 学习率warmup是什么？
A: 训练初期用很小的学习率，逐步增到目标值，再按策略衰减。
   目的：防止早期因参数随机初始化导致的梯度不稳定。
   常见策略：线性 warmup → 余弦退火
""")
