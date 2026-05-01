# 生成式推荐系统面试准备：OneRec 系列深度解析

> 基于 OneRec V1 (arXiv:2502.18965)、OneRec Technical Report (arXiv:2506.13695)、OneRec-V2 (arXiv:2508.20900)、OpenOneRec (arXiv:2512.24762) 以及 OneRec-Think (arXiv:2510.11639) 整理

---

## 一、传统推荐系统的核心瓶颈

<b>Q：传统推荐系统架构有什么问题？为什么需要端到端生成式推荐？</b>

传统推荐系统采用多阶段级联架构：**召回 → 粗排 → 精排 → 重排**，存在三大核心瓶颈：

1. **前链路制约后链路上限**：召回阶段过滤掉的 item，即使精排认为收益极高也无法挽回，各阶段目标不一致导致全局次优
2. **Point-wise 建模的局限**：传统系统对每个 item 独立打分，忽略了同一 session 内 item 之间的相互影响（如推荐多个相似视频会导致用户疲劳）
3. **算力碎片化**：多阶段架构导致算子数量爆炸（快手精排模型算子 15000+），MFU（模型浮点运算利用率）长期停留在个位数，无法有效利用现代 GPU 算力，也难以应用 Scaling Law、RL 等 AI 前沿技术

OneRec 的核心思路：用一个统一的生成式模型替代整个级联架构，将推荐问题重新定义为**序列生成任务**。

---

## 二、OneRec V1 架构详解

### 2.1 整体架构：Encoder-Decoder + MoE

OneRec V1 采用类似 T5 的 **Encoder-Decoder** 结构：

- **Encoder**：压缩用户全生命周期行为序列，建模用户兴趣
- **Decoder**：基于用户兴趣，自回归地生成一个 session 内的推荐 item 序列
- **MoE（Mixture of Experts）**：在 Decoder 的 FFN 层引入稀疏 MoE，在不按比例增加 FLOPs 的前提下扩展模型参数量

```
用户行为序列 → [Encoder] → 用户兴趣表示 → [MoE Decoder] → 推荐 item 序列
                                                ↑
                                          Cross-Attention 连接
```

### 2.2 语义分词器：RQ-Kmeans

<b>Q：OneRec 如何将视频转化为模型可理解的 token？</b>

面对亿级别的视频候选池，OneRec 设计了**协同感知的多模态语义分词器**，将每个视频编码为一组离散的 **Semantic ID**：

**多模态特征融合**：
- 视频标题、标签、语音转文字（ASR）、图像识别等内容特征
- 用户协同行为信号（不仅看内容"是什么"，还看用户"怎么交互"）

**分层语义编码**：采用 **RQ-Kmeans**（而非 RQ-VAE）将每个视频编码为 **L 层**（通常 L=3）从粗到细的语义 ID：

```
视频 → 多模态特征提取 → RQ-Kmeans 量化 → (layer1_id, layer2_id, layer3_id)
```

<b>Q：RQ-Kmeans vs RQ-VAE 的优势是什么？</b>

| 指标 | RQ-VAE | RQ-Kmeans |
|------|--------|-----------|
| 重建损失 ↓ | 0.0548 | **0.0410**（降低 25.18%）|
| Codebook 利用率 ↑ | 0.9958~1.0 | **1.0000**（全部层满利用）|
| Token 分布熵 ↑ | 8.39~8.60 | **8.72~8.92**（更均匀）|

RQ-Kmeans 在所有指标上均优于 RQ-VAE：重建更准确、codebook 利用更充分、token 分布更均匀，有利于模型稳定性和泛化能力。

### 2.3 Encoder：多尺度用户建模

Encoder 通过四条**多尺度路径**捕获不同粒度的用户兴趣：

| 路径 | 输入 | 作用 |
|------|------|------|
| User Static Pathway | 用户画像（年龄、性别等） | 静态偏好 |
| Short-term Pathway | 近期行为序列 | 短期兴趣 |
| Effective View Pathway | 有效观看序列 | 真实兴趣信号 |
| Long-term / Lifetime Pathway | 全生命周期行为 | 长期偏好 |

每条行为路径内部，item 序列的格式为（每个 item 有 L=3 层 semantic ID，前面加 BOS 标记）。

**具体示例**（假设用户最近看了搞笑视频 → 美食视频 → 旅游 Vlog）：

```
═══════════════════════════════════════════════════════════════
                    Encoder 输入（完整 Prompt）
═══════════════════════════════════════════════════════════════

[Pathway 1: User Static] ← 用户画像，非 SID，通过 Linear 映射为 embedding
  age=25, gender=M, city=北京, register_days=365

[Pathway 2: Short-term] ← 近 50 条行为（SID 序列）
  [BOS] 42  187  63     ← 搞笑短视频（粗粒度=42:搞笑类, 中=187:段子, 细=63:具体视频）
  [BOS] 15  203  91     ← 美食探店视频
  [BOS] 28  156  44     ← 旅游 Vlog
  ...

[Pathway 3: Effective View] ← 有效观看（完播率>50%）的子集
  [BOS] 42  187  63     ← 搞笑视频（看完了，真实兴趣）
  [BOS] 28  156  44     ← 旅游 Vlog（看完了）
  ...
  （注意：美食视频划走了，不在此路径中）

[Pathway 4: Long-term] ← 全生命周期行为（可能数千条，压缩采样）
  [BOS] 42  187  63
  [BOS] 77  12   205
  [BOS] 15  203  91
  ... (数百~数千条历史)

═══════════════════════════════════════════════════════════════
              各路径独立编码 → 拼接 → Transformer Encoder
═══════════════════════════════════════════════════════════════

Pathway 1 (Static):     [age=25, gender=M, ...] → Linear      → h_static
Pathway 2 (Short):      [BOS]42,187,63 [BOS]15,203,91 ...  → Transformer → h_short
Pathway 3 (EffView):    [BOS]42,187,63 [BOS]28,156,44 ...  → Transformer → h_effview
Pathway 4 (Long):       [BOS]42,187,63 [BOS]77,12,205 ...  → Transformer → h_long

H_user = TransformerEncoder( Concat(h_static, h_short, h_effview, h_long) )

═══════════════════════════════════════════════════════════════
                 Decoder 自回归生成（输出）
═══════════════════════════════════════════════════════════════

H_user → MoE Decoder (Cross-Attention 接入 H_user)
  → [BOS] 28  156  44     ← 生成第 1 个推荐：旅游 Vlog
  → [BOS] 42  201  17     ← 生成第 2 个推荐：搞笑合集
  → [BOS] 33  89   152    ← 生成第 3 个推荐：户外运动
  ... (session-wise 生成整个推荐序列)
```

**SID 的分层语义**（以 `42 187 63` 为例）：
- 第 1 层 `42`：粗粒度类目（如"搞笑/幽默"大类）
- 第 2 层 `187`：中粒度子类（如"搞笑段子"）
- 第 3 层 `63`：细粒度，定位到具体视频

注意：User Static Pathway 的输入是用户画像特征（非 SID 序列），其余三条路径的输入才是 SID 序列。不同路径的行为序列可能有重叠（如同一个视频出现在 Short-term 和 Effective View 中），但各路径建模目标不同。

### 2.4 Decoder：MoE + Session-wise 生成

<b>Q：Session-wise 生成 vs Point-wise 生成有什么区别？</b>

**Point-wise**：每次请求独立预测每个 item 的分数，item 之间互不影响

**Session-wise（OneRec）**：一次请求生成整个 session 的推荐序列，后续 item 的生成依赖于前面已生成的 item，自然地建模了 item 间的交互和多样性

Decoder 的 MoE 层采用 Top-K 路由策略：
- N_experts 个专家网络
- 每个 token 激活 top-k 个专家
- 稀疏激活实现参数量扩展而不线性增加计算量

### 2.5 训练：NTP + DPO 偏好对齐

#### 阶段一：Next Token Prediction（NTP）预训练

采用交叉熵损失，自回归预测下一个 semantic ID：

```
L_NTP = -Σ_{i=1}^{m} Σ_{j=1}^{L} log P(s_i^{j+1} | [BOS], s_1^1, ..., s_1^L, ..., [BOS], s_i^1, ..., s_i^j; Θ)
```

#### 阶段二：DPO 迭代偏好对齐（IPA）

推荐场景的特殊挑战：不像 NLP 可以对同一问题获取多个回答的偏好，推荐系统一次请求只展示一个 session，无法直接获得正负样本对。

**OneRec 的解决方案（三步流程）**：

**Step 1 — 训练 Reward Model（RM）**：
- 多任务预测：CTR、VTR（完播率）、WTR（观看时长率）、LTR（点赞率）等
- 损失函数为多目标交叉熵：

```
L_RM = -Σ_{xtr} [y^{xtr} log(r^{xtr}) + (1 - y^{xtr}) log(1 - r^{xtr})]
```

**Step 2 — 构造偏好对**：
- 用预训练好的 OneRec 对同一用户进行 **Beam Search** 生成多个候选 session
- 用 RM 对每个 session 打分
- 取最优得分 session 为 chosen（正样本），最差得分 session 为 rejected（负样本）

**Step 3 — DPO 优化**：
- 用标准 DPO 算法优化 OneRec，使模型偏好生成高分 session

<b>关键发现</b>：有限数量的 DPO 样本即可显著提升推荐质量，IPA 可以迭代进行多轮。

### 2.6 强化学习深入：挤压效应与格式奖励

<b>Q：RL 在推荐场景有什么特殊挑战？</b>

**非法生成问题**：OneRec 的词表空间远大于实际视频数量，生成的 Semantic ID 序列可能无法映射回真实视频 ID。

**挤压效应（Squeezing Effect）**：RL 优化（尤其是负向优势梯度）会将大部分概率质量挤压到当前最优输出，导致合法输出的概率被抹平 → 推理成本增大 + 多样性下降。

**OneRec 的解决方案 — 格式奖励（Format Reward）**：
- 引入额外的 Format Reward 鼓励合法输出（能映射回真实视频的 ID 序列）
- 关键实验发现：
  - 选概率最大的 k 个样本训练 → 合法性先升后降（Reward Hacking）
  - **随机选 k 个样本训练** → 合法性持续上升（推荐做法）

**三类奖励信号**：
1. 用户偏好奖励：基于 RM 打分
2. 格式奖励：鼓励生成合法 Semantic ID
3. 工业场景奖励：营销号打压、冷启视频扶持、长尾分发等

### 2.7 Scaling Laws

<b>Q：推荐系统是否遵循 Scaling Law？</b>

OneRec 是首个在推荐领域验证 Scaling Law 的工作：

- 参数量从 0.015B → 2.633B，训练损失呈现明显的 **幂律下降趋势**
- 模型 FLOPs 提升 10 倍后仍能持续获得收益
- 包括 Feature Scaling、Codebook Scaling、Infer Scaling 等多个维度的 Scaling

### 2.8 性能优化与工程实践

#### 训练优化
- MFU 从传统推荐模型的 **4.6%** 提升至 **23.7%**
- 高效并行训练、混合精度、编译优化

#### 推理优化
- Beam Size 通常为 **512**（保证多样性和覆盖率）
- **计算复用**：Encoder 对同一用户只前向一次，Cross-Attention 的 K/V 在所有 beam 间共享
- **KV Cache**：缓存历史步骤的 K/V，减少重复计算
- **算子优化**：FP16 混合精度，MoE/Attention/BeamSearch 核心算子深度 Kernel 融合
- 推理 MFU 从 **11.2%** 提升至 **28.8%**

#### 成本优化
- 运营成本降至传统方案的 **10.6%**，节省约 **90%**

### 2.9 在线实验结果

部署于**快手/快手极速版**主场景：

| 指标 | 快手主站 | 快手极速版 |
|------|---------|-----------|
| App Stay Time 提升 | **+0.54%** | **+1.24%** |
| 承接线上流量 | 25% QPS | 25% QPS |

OneRec-1B + IPA 模型：
- 总观看时长 **+1.68%**
- 人均观看时长 **+6.56%**
- 7 日留存等关键指标显著提升

---

## 三、OneRec-V2：Lazy Decoder-Only 架构

### 3.1 V1 的瓶颈

OneRec V1 的 Encoder-Decoder 架构存在严重的计算分配不均：

- **97.66%** 的 FLOPs 消耗在 Encoder 的序列编码上
- 仅 **2.34%** 用于 Decoder 的实际生成
- 这严重限制了模型的扩展性（V1 最大只到 0.5B 激活参数）

### 3.2 Lazy Decoder-Only 架构

<b>Q：什么是 Lazy Decoder-Only 架构？它和标准 Decoder-Only 有什么区别？</b>

OneRec-V2 提出了一种创新的 **Lazy Decoder-Only** 架构，核心思想是：

**将上下文（用户行为）视为静态条件信息，仅通过 Cross-Attention 访问，而非参与自注意力计算。**

与三种架构的对比：

| 架构 | 特点 | 问题 |
|------|------|------|
| Encoder-Decoder (V1) | Encoder 编码上下文，Decoder 生成 | 97.66% 算力浪费在 Encoder |
| Naive Decoder-Only | 上下文和生成序列拼接，统一自注意力 | 上下文 token 参与全部计算，冗余更严重 |
| **Lazy Decoder-Only (V2)** | 去掉 Encoder，上下文仅通过 Cross-Attention 接入 | 兼顾效率和效果 |

关键创新：
- **去掉 Encoder 组件**
- **简化 Cross-Attention**：移除 K/V 投影层（直接用上下文 embedding 作为 K/V）
- 上下文信息通过三条路径处理后，作为 Cross-Attention 的 KV 静态接入

```
用户静态特征 → User Static Linears  ─┐
短期行为序列 → Short-term Linear     ├→ Context Processor → Lazy Cross-Attention (无 K/V 投影)
长期行为序列 → Long-term Linear      ─┘
                                                    ↓
                                     [BOS] → Embedding → Causal Self-Attention → FFN → Semantic IDs
                                                    (Lazy Decoder Block × N_layer)
```

### 3.3 效果对比

| 指标 | V1 Encoder-Decoder | V2 Lazy Decoder-Only |
|------|-------------------|---------------------|
| 计算量 | 基准 | **降低 94%** |
| 训练资源 | 基准 | **降低 90%** |
| 最大模型参数 | 0.5B | **8B**（16 倍提升）|
| 生成 loss | 基准 | 更低（效果更好）|

### 3.4 Preference Alignment with Real-World User Interactions

<b>Q：V2 的偏好对齐和 V1 有什么区别？</b>

V1 仅依赖 Reward Model 进行 DPO，存在：
- 采样效率低
- 潜在的 Reward Hacking

V2 直接利用**真实用户反馈**进行偏好对齐，两大创新：

#### (1) Duration-Aware Reward Shaping

**问题**：原始观看时长存在视频时长偏差（长视频天然观看时间更长，但不代表用户更喜欢）

**解决方案**：对奖励信号进行时长归一化，确保奖励反映的是内容质量而非视频时长：

```
奖励 = f(实际观看时长, 视频总时长)  # 考虑完播率等相对指标
```

#### (2) Adaptive Ratio Clipping

**问题**：标准 PPO/DPO 中策略比率的方差过大，训练不稳定

**解决方案**：自适应裁剪策略比率，在保持收敛性的同时降低训练方差

### 3.5 V2 Scaling Laws

V2 架构的高效性使得 Scaling Law 研究成为可能：

- 密集模型和稀疏（MoE）模型都展示了清晰的 scaling 趋势
- 从 0.5B 成功扩展到 **8B** 参数，loss 持续下降
- 为未来更大规模的推荐模型提供了指导

### 3.6 V2 在线实验结果

| 指标 | 提升 |
|------|------|
| App Stay Time（快手） | **+0.467%** |
| App Stay Time（极速版） | **+0.741%** |
| 多目标平衡 | 显著改善 |

---

## 四、OpenOneRec：开源推荐基座模型

### 4.1 定位与目标

OpenOneRec 是快手开源的推荐基座模型框架，目标是将 LLM 的能力引入推荐领域，基于 **Qwen3** 骨干构建。

**核心贡献**：
1. **RecIF-Bench**：首个全面的推荐指令遵循基准，包含 1 亿交互数据、20 万用户、跨短视频/广告/电商三个域
2. **OneRec-Foundation 模型族**：1.7B 和 8B 两种规格，Standard 和 Pro 两个版本
3. **全栈训练 Pipeline**：数据处理 → 联合预训练 → 后训练，完全开源可复现

### 4.2 架构：基于 Qwen3 的 LLM 推荐模型

与 V1/V2 的 ID-based 生成不同，OpenOneRec 将推荐重新表述为**自然语言指令遵循任务**：

- 骨干模型：**Qwen3**（保持原始架构不变，保留语言和推理能力）
- 引入 **Itemic Tokens**：为每个 item 分配特殊 token（类似新增词表），使 LLM 能"说出" item ID

### 4.3 训练流程

#### Stage 1: Itemic-Text Alignment（冻结大部分参数）

建立 itemic tokens 和 text tokens 之间的初步对齐：
- 仅训练 embedding 层和 item 相关的投影层
- 对于大模型（8B+），output projection 层的 itemic token 参数也可训练

#### Stage 2: Co-Pretraining

联合训练推荐数据和通用语料：
- 推荐数据：物品描述（Dense Caption）、用户行为序列、推荐任务数据
- 通用语料：防止灾难性遗忘（catastrophic forgetting）
- 数据去重：MinHash 算法

#### Stage 3: Post-Training（三阶段）

**(a) 多任务 SFT** — 恢复指令遵循和 thinking 能力：
- 混合通用域推理样本 + 推荐任务数据
- 使用 Qwen3 chat template
- 关键发现：通用能力的恢复也会增强推荐任务的推理能力（cross-fertilization）

**(b) On-policy Distillation** — 恢复通用推理能力：
- 原因：SFT 后通用 reasoning 仍有退化
- 采用 on-policy 蒸馏（而非 off-policy），效果更好
- 约 200K 样本

**(c) GRPO** — 针对推荐任务的强化学习：
- 使用 GRPO（Group Relative Policy Optimization）优化推荐性能
- 基于真实推荐任务的奖励信号

### 4.4 模型族

| 模型 | 骨干 | 参数量 | 训练数据 |
|------|------|--------|---------|
| OneRec-1.7B | Qwen3-1.7B | 1.7B | ~33B tokens（开源数据）|
| OneRec-8B | Qwen3-8B | 8B | ~33B tokens（开源数据）|
| OneRec-1.7B-Pro | Qwen3-1.7B | 1.7B | ~130B tokens（含快手工业数据）|
| OneRec-8B-Pro | Qwen3-8B | 8B | ~130B tokens（含快手工业数据）|

### 4.5 RecIF-Bench 评测体系

三层评测设计：

| 层级 | 任务 | 说明 |
|------|------|------|
| Layer 1: Fundamental Prediction | 短视频推荐、广告推荐、商品推荐、标签预测 | 基础推荐能力 |
| Layer 2: Instruction Following | 交互式推荐、条件推荐 | 指令遵循能力 |
| Layer 3: Reasoning | 推荐解释 | 推理能力 |

### 4.6 关键结果

- 在 RecIF-Bench 所有任务上达到 **SOTA**
- 在 10 个 Amazon 数据集上，Recall@10 平均提升 **26.8%**
- 数据 Scaling 有效：Pro 版 > Standard 版
- 模型 Scaling 有效：8B > 1.7B
- 通用能力保持较好（MATH-500、GSM8K 等退化有限）

---

## 五、OneRec-Think：推荐中的推理

OneRec-Think 将**显式推理（Chain-of-Thought）** 引入生成式推荐：

- 在生成推荐 item 之前，模型先生成可解释的推理过程
- 桥接了"可解释性"和"生成式推荐"的鸿沟
- 基于 GRPO/DAPO/VAPO 等技术优化推理行为

---

## 六、OneRec 系列演进总结

```
OneRec V1 (2025.02)
  架构: Encoder-Decoder + MoE
  分词: RQ-Kmeans Semantic ID
  训练: NTP + DPO/IPA
  规模: ~0.5B (activated)
  部署: 快手主站 25% 流量
     ↓
OneRec V2 (2025.08)
  架构: Lazy Decoder-Only (去掉 Encoder)
  改进: 算力降 94%, 训练资源降 90%
  训练: Duration-Aware Reward + Adaptive Ratio Clipping
  规模: 扩展至 8B
  部署: App Stay Time +0.47%~0.74%
     ↓
OneRec Technical Report (2025.06)
  完整工业实践: Scaling Laws, RL 框架, 格式奖励
  MFU: 训练 23.7%, 推理 28.8%
  成本: 降至传统方案的 10.6%
     ↓
OpenOneRec (2025.12)
  开源: 基于 Qwen3 的推荐基座模型
  路线: LLM + 推荐融合, 文本化推荐
  规模: 1.7B / 8B, Standard / Pro
  Benchmark: RecIF-Bench
     ↓
OneRec-Think (2025.10)
  创新: 显式推理 + 生成式推荐
  可解释性: CoT for Recommendation
```

---

## 七、面试高频问题与回答要点

### Q1：OneRec 和传统推荐系统的本质区别是什么？

**要点**：
- 传统：多阶段级联（召回→粗排→精排→重排），point-wise 打分
- OneRec：端到端单模型，session-wise 自回归生成
- 核心转变：从"给 item 打分排序"变为"直接生成推荐序列"
- 类比 LLM：用户行为序列 ≈ prompt，推荐结果 ≈ 生成的 response

### Q2：为什么选择 Encoder-Decoder 而不是 Decoder-Only？（V1）

**要点**：
- V1 选择 Encoder-Decoder 是因为用户行为序列很长（终身行为），需要 Encoder 压缩
- 但后来发现 97.66% 算力浪费在编码上
- V2 因此转向 Lazy Decoder-Only，用 Cross-Attention 静态接入上下文

### Q3：RQ-Kmeans 是什么？为什么不用 RQ-VAE？

**要点**：
- 两者都是残差量化方法，将连续 embedding 量化为多层离散 ID
- RQ-Kmeans 直接用 K-Means 聚类，不需要 VAE 的编解码器训练
- 实验证明 RQ-Kmeans 重建损失更低（-25%）、codebook 利用率更高（100%）、分布更均匀

### Q4：OneRec 的 DPO 和 NLP 中的 DPO 有什么区别？

**要点**：
- NLP DPO：对同一 prompt 可以生成多个 response，直接让人标注偏好
- 推荐 DPO：一次请求只展示一个 session，无法同时获得正负样本
- OneRec 解决方案：训练 RM → Beam Search 生成多个候选 → RM 打分构造偏好对 → DPO 优化
- V2 进一步改进：直接用真实用户反馈替代 RM，避免 Reward Hacking

### Q5：什么是挤压效应？如何解决？

**要点**：
- RL 的负向优势梯度将概率质量集中到少数"最优"输出
- 导致大部分合法输出概率被抹平 → 非法生成增多 + 多样性下降
- 解决：引入 Format Reward 鼓励合法输出
- 关键实验：随机采样 k 个样本训练（而非 top-k）效果更好，避免 Reward Hacking

### Q6：Lazy Decoder-Only 架构的核心思想是什么？

**要点**：
- 核心洞察：上下文（用户行为）是静态信息，不需要参与自注意力计算
- 做法：去掉 Encoder，上下文通过简单线性变换后作为 Cross-Attention 的 KV
- 进一步简化：移除 Cross-Attention 的 K/V 投影层
- 效果：计算量降 94%，资源降 90%，模型从 0.5B 扩展到 8B

### Q7：OneRec 如何实现近 90% 的成本节省？

**要点**：
- 统一模型替代多阶段架构，消除重复计算和中间存储
- MFU 从 4.6%/11.2% 提升至 23.7%/28.8%（训练/推理），GPU 算力利用率大幅提升
- Encoder 只算一次 + Cross-Attention KV 共享 + KV Cache
- Beam Search 算子深度融合优化
- 运营成本降至传统方案的 10.6%

### Q8：OneRec 的 Scaling Law 有什么发现？

**要点**：
- 首次在推荐领域验证了 Scaling Law 的存在
- 0.015B → 2.633B（V1）→ 8B（V2），训练 loss 持续幂律下降
- 密集模型和 MoE 稀疏模型都遵循 Scaling 趋势
- 含义：推荐模型和 LLM 一样，"大力出奇迹"在一定范围内成立

### Q9：OpenOneRec 和 V1/V2 的关系是什么？

**要点**：
- V1/V2：ID-based 生成式推荐（生成 Semantic ID 序列）
- OpenOneRec：LLM-based 推荐基座（基于 Qwen3，文本化推荐）
- OpenOneRec 是 OneRec 理念的 LLM 化延伸，面向更通用的推荐场景
- 训练关键：分阶段 alignment（Itemic-Text Alignment → Co-Pretraining → Post-Training），防止灾难性遗忘

### Q10：生成式推荐的局限性和未来方向？

**要点**：
- 当前局限：互动指标（如点赞）提升有限，多目标优化仍需改进
- 非法生成问题：Semantic ID 可能映射不到真实 item
- 推理成本：大 Beam Size（512）的实时推理仍有挑战
- 未来方向：OneRec-Think（推理+推荐）、更大规模 Scaling、多模态理解、跨域迁移

---

## 八、核心概念速查表

| 概念 | 含义 |
|------|------|
| Semantic ID | 视频的离散语义标识，由 RQ-Kmeans 分层量化得到（通常 3 层） |
| RQ-Kmeans | 残差量化 + K-Means 聚类，替代 RQ-VAE 的分词方法 |
| Session-wise Generation | 一次生成整个推荐 session，而非逐个 item 独立预测 |
| MoE (Mixture of Experts) | 稀疏专家混合，Top-K 路由，扩参数不扩 FLOPs |
| NTP (Next Token Prediction) | 自回归预训练目标，预测下一个 Semantic ID |
| IPA (Iterative Preference Alignment) | 迭代式偏好对齐，V1 基于 RM+DPO |
| Lazy Decoder-Only | V2 架构，上下文仅通过 Cross-Attention 静态接入 |
| Duration-Aware Reward Shaping | 消除视频时长偏差的奖励设计 |
| Adaptive Ratio Clipping | 自适应裁剪策略比率，稳定 RL 训练 |
| Format Reward | 鼓励生成合法 Semantic ID 的奖励信号 |
| Squeezing Effect | RL 负向梯度导致概率集中的现象 |
| MFU (Model FLOPs Utilization) | GPU 算力实际利用率 |
| RecIF-Bench | OpenOneRec 提出的推荐指令遵循基准 |
| GRPO | Group Relative Policy Optimization，OpenOneRec 用于推荐 RL |

---

## 九、论文列表

1. **OneRec V1**: *OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment* (arXiv:2502.18965, 2025.02)
2. **OneRec Tech Report**: *OneRec Technical Report* (arXiv:2506.13695, 2025.06) — 完整工业实践
3. **OneRec-V2**: *OneRec-V2 Technical Report* (arXiv:2508.20900, 2025.08) — Lazy Decoder-Only
4. **OneRec-Think**: *OneRec-Think: In-Text Reasoning for Generative Recommendation* (arXiv:2510.11639, 2025.10)
5. **OpenOneRec**: *OpenOneRec Technical Report* (arXiv:2512.24762, 2025.12) — 开源基座模型
6. **OneMall**: *OneMall: One Model, More Scenarios — End-to-End Generative Recommender Family at Kuaishou E-Commerce* (arXiv:2601.21770, 2026.01) — 电商场景扩展
