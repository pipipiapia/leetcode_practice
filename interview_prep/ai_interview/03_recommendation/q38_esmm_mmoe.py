#!/usr/bin/env python3
"""
Q38 / Q39: ESMM（Entire Space Multi-task Model）和 MMOE

面试常问：
1. ESMM 是如何解决 CVR 建模的样本选择偏差问题的？
2. MMOE 和 SharedBottom 的区别是什么？
3. 多目标学习中的负迁移是什么？

ESMM 解决的问题：
  CVR（转化率）建模的困境：
  ① 样本稀疏：点击→转化的样本远少于曝光→点击
  ② 延迟反馈：转化可能发生在未来
  ③ 选择偏差：只有被点击的样本才能观测到是否转化

ESMM 核心思路：
  同时建模 CTR 和 CTCVR（点击且转化率）
  利用 CTCVR = CTR × CVR 的数学关系
  在全样本空间（曝光）上训练，避免选择偏差

  Loss = L_ctr + L_ctcvr
  CVR = CTCVR / CTR（隐式学习，不直接用 CVR 样本训练）

MMOE（Multi-gate Mixture-of-Experts）：
  问题：SharedBottom（所有任务共享底层）会导致负迁移
  解决：多个 Expert 网络 + 每个任务独立的 Gate

  y_k = Σ_i g_k(x)_i · Expert_i(x)
  g_k(x) = softmax(W_k · x)    ← 任务专属门控
  Expert_i(x) = f_i(x)         ← 共享专家

PLE（在 MMOE 基础上改进）：
  增加了任务专属 Expert 和共享 Expert 的分层
  分离共享参数和独有参数
"""

import numpy as np


class ESMM:
    """
    ESMM（Entire Space Multi-task Model）

    三个网络：
      CTR 网络：输入曝光样本，输出 P(click | impression)
      CVR 网络：输入点击样本，输出 P(conversion | click)
      CTCVR 网络：输入曝光样本，输出 P(click & conversion)

    核心关系：P(click & conversion) = P(click) × P(conversion)
      CTCVR = CTR × CVR
      因此 CVR = CTCVR / CTR

    Loss = L_ctr + L_ctcvr（注意：没有单独的 CVR loss！）
    """

    def __init__(self, input_dim):
        self.input_dim = input_dim

        # CTR 网络（曝光 → 点击）
        self.ctr_W = np.random.randn(input_dim, 1) * 0.01
        self.ctr_b = 0.0

        # CTCVR 网络（曝光 → 点击且转化）
        self.ctcvr_W = np.random.randn(input_dim, 1) * 0.01
        self.ctcvr_b = 0.0

        # CVR 网络（点击 → 转化）— 只用于推理，不直接训练
        self.cvr_W = np.random.randn(input_dim, 1) * 0.01
        self.cvr_b = 0.0

    def forward(self, x, train_full_space=True):
        """
        x: (batch, input_dim)

        ESMM 关键：
        - 训练时，用曝光样本同时算 CTR 和 CTCVR loss
        - 不直接训练 CVR 网络，只用 CTCVR/CTR 的关系隐式学习
        """
        # CTR（曝光样本全量参与）
        ctr_pred = self._sigmoid(x @ self.ctr_W + self.ctr_b)

        # CTCVR（曝光样本全量参与）
        ctcvr_pred = self._sigmoid(x @ self.ctcvr_W + self.ctcvr_b)

        # CVR = CTCVR / CTR（由关系隐式得到）
        # 注意：实际代码中 CVR 网络的梯度由 CTCVR 反向传播得到
        cvr_pred = ctcvr_pred / (ctr_pred + 1e-8)

        return ctr_pred, ctcvr_pred, cvr_pred

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


class MMOE:
    """
    MMOE（Multi-gate Mixture-of-Experts）

    多个 Expert（专家）网络，每个任务有独立的 Gate（门控）
    Expert 共享参数，Gate 控制各 Expert 对任务的贡献
    """

    def __init__(self, input_dim, num_experts=4, num_tasks=2, expert_hidden=32):
        self.num_experts = num_experts
        self.num_tasks = num_tasks

        # Expert 网络们
        self.experts = []
        for _ in range(num_experts):
            W1 = np.random.randn(input_dim, expert_hidden) * np.sqrt(2 / input_dim)
            b1 = np.zeros(expert_hidden)
            W2 = np.random.randn(expert_hidden, 16)
            b2 = np.zeros(16)
            self.experts.append({'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2})

        # 每个任务一个 Gate
        self.gates = []
        for _ in range(num_tasks):
            W_g = np.random.randn(16, num_experts) * np.sqrt(2 / 16)
            b_g = np.zeros(num_experts)
            self.gates.append({'W_g': W_g, 'b_g': b_g})

    def _forward_expert(self, expert, x):
        h = np.tanh(x @ expert['W1'] + expert['b1'])
        return h @ expert['W2'] + expert['b2']

    def forward(self, x):
        """
        x: (batch, input_dim)

        流程：
        1. 所有 Expert 分别计算输出 → (batch, num_experts, expert_output)
        2. 每个任务的 Gate 算权重 → (batch, num_experts)
        3. 加权求和 → (batch, expert_output)
        """
        # 1. Expert 输出
        expert_outputs = np.stack([
            self._forward_expert(exp, x) for exp in self.experts
        ], axis=1)  # (batch, num_experts, expert_output)

        # 2. 每个任务的 Gate
        task_outputs = []
        for gate in self.gates:
            # Gate 权重（softmax）
            gate_logits = x @ gate['W_g'] + gate['b_g']
            gate_weights = np.exp(gate_logits) / np.exp(gate_logits).sum(axis=-1, keepdims=True)
            # (batch, num_experts)

            # 3. 加权求和
            task_out = np.sum(expert_outputs * gate_weights[:, :, np.newaxis], axis=1)
            task_outputs.append(task_out)

        return task_outputs  # list of (batch, expert_output), len=num_tasks


if __name__ == "__main__":
    print("=" * 50)
    print("ESMM 演示")
    print("=" * 50)

    np.random.seed(42)
    batch_size = 64
    input_dim = 32

    esmm = ESMM(input_dim)
    x = np.random.randn(batch_size, input_dim)

    ctr, ctcvr, cvr = esmm.forward(x)

    print(f"CTR:      mean={ctr.mean():.4f}")
    print(f"CTCVR:    mean={ctcvr.mean():.4f}")
    print(f"CVR(=CTCVR/CTR): mean={cvr.mean():.4f}")
    print("\nESMM 关键洞察：")
    print("  CVR 网络没有直接用 CVR 样本训练")
    print("  CVR 梯度 = CTCVR/CTR 的关系反向传播得到")
    print("  这就是解决样本选择偏差的核心！")

    print("\n" + "=" * 50)
    print("MMOE 演示")
    print("=" * 50)

    mmoe = MMOE(input_dim, num_experts=4, num_tasks=2)
    task1_out, task2_out = mmoe.forward(x)

    print(f"任务1输出 shape: {task1_out.shape}")
    print(f"任务2输出 shape: {task2_out.shape}")

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: 为什么 SharedBottom 会产生负迁移？
A: 当两个任务相关性低时，共享参数会被拉扯——优化一个任务损害另一个。
   例如：主任务优化点击率，副任务优化评论率，特征可能冲突。

Q: MMOE 如何缓解负迁移？
A: 每个任务有独立的 Gate，决定各 Expert 对该任务的权重。
   如果任务A的相关Expert是 Expert1/2，任务B的相关Expert是 Expert3/4，
   Gate 可以自动学到这一点，减少冲突。

Q: PLE 和 MMOE 的区别？
A: MMOE：所有 Expert 完全共享。
   PLE：在 MMOE 基础上，增加任务专属 Expert（不是所有任务共享）。
   效果：进一步分离共享和独有知识。

Q: ESMM 如何在全样本空间训练？
A: 所有样本（曝光）都参与 CTR 和 CTCVR loss 计算。
   曝光→点击（正）标记为CTR正例
   曝光→点击→转化（正）标记为CTCVR正例
   没有单独的CVR loss，CVR由 CTCVR/CTR 的数学关系隐式学习。
""")
