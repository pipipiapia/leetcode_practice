# OKX English Interview Full Preparation

> **Role**: Principal / Senior Staff Algorithm Engineer, Search & Recommendation  
> **Format**: Technical deep-dive + behavioral, conducted in English  
> **Instructions**: Practice each section OUT LOUD. Sample answers are reference points — use your own words.

---

## Table of Contents

| # | Section |
|---|---------|
| 0 | [Self-Introduction (2 min)](#part-0-self-introduction) |
| 1 | [Project Introductions (STAR)](#part-1-project-introductions-star-framework) |
| 2 | [User Behavior Sequence Modeling](#part-2-user-behavior-sequence-modeling) |
| 3 | [Multi-Task Learning](#part-3-multi-task-learning) |
| 4 | [Feature Interaction — DCN](#part-4-feature-interaction--dcn) |
| 5 | [Position Encoding](#part-5-position-encoding) |
| 6 | [Listwise Ranking Loss](#part-6-listwise-ranking-loss) |
| 7 | [Causal Inference & Bias Correction](#part-7-causal-inference--bias-correction) |
| 8 | [Generative Recommendation](#part-8-generative-recommendation) |
| 9 | [User Intent & Profile System](#part-9-user-intent--profile-system) |
| 10 | [LLM Agent + Recommendation](#part-10-llm-agent--recommendation) |
| 11 | [OKX Business-Specific Questions](#part-11-okx-business-specific-questions) |
| 12 | [Engineering & System Design](#part-12-engineering--system-design) |
| 13 | [Quick-Fire Technical Q&A](#part-13-quick-fire-technical-qa) |
| 14 | [Behavioral Questions](#part-14-behavioral-questions) |
| 15 | [Delivery Tips](#part-15-delivery-tips) |

---

## Part 0: Self-Introduction

> Practice delivering this in **exactly 2 minutes**. Time yourself.

**Sample (English):**

Hi, I'm Tan Yang. I have 9 years of experience as an algorithm engineer specializing in recommendation systems and search algorithms. I hold an AI Master's degree from the University of Southampton with Distinction, and a Software Engineering Master's from USTC.

My career spans two major tech companies in China. At **Baidu**, I spent over 6 years working across user profiling, content risk control, and push recommendation. My most notable work there was building the Tieba Push recommendation system from scratch — personalized ranking with DNN-NCF, dual-tower DeepFM retrieval, and graph-based representation learning using Metapath2Vec++. The system served 500 million daily impressions, and I improved CTR by over 10% while reducing user complaint rates by 20%.

At **Tencent WeSee**, I was a senior researcher responsible for push notification ranking on both WeChat and QQ platforms. I designed multi-objective CTR models using MMoE, jointly optimizing click-through and user retention.

Currently, I'm back at **Baidu** leading the automotive vertical Feed recommendation — I built the entire dual-tower vector retrieval pipeline from zero, achieving a cumulative CTR improvement of 46%. I'm also exploring AIGC applications, including LoRA-finetuned image generation for automotive ads with 90%+ usability rate, and currently leading a generative search R&D initiative exploring LLM-based query intent generation and result re-ranking.

My research interests are at the intersection of **LLM and recommendation/search** — generative retrieval, query intent understanding, and how to bring generative paradigms into production systems. I believe this aligns well with OKX's vision of building next-generation search and recommendation for the crypto ecosystem.

---

## Part 1: Project Introductions (STAR Framework)

### Project 1: Baidu Automotive Feed Recommendation (Current, 2023–Present)

**Situation**: Baidu's automotive vertical needed a personalized Feed recommendation system. The existing system relied on rule-based and simple collaborative filtering approaches with poor relevance.

**Task**: Build the end-to-end recommendation pipeline — retrieval, pre-ranking, ranking, and re-ranking — from zero. Also explore AIGC for ad creative generation.

**Action**:
1. Designed and implemented a **dual-tower vector retrieval architecture** from scratch — user tower encoding browsing history and intent signals, item tower encoding automotive content features. Built the ANN index serving layer for real-time retrieval.
2. Iterated on ranking models incorporating user behavior sequences and cross-features, supporting millions of daily requests.
3. Led automotive search optimization — implemented semantic matching for long-tail queries in "People Also Search" and SUG (Search Suggestion), improving recall-stage CTR by ~8%.
4. Explored **AIGC**: fine-tuned SDXL with LoRA/Dreambooth for automotive ad image generation (90%+ usability), combined with SwinIR image restoration and SVD image-to-video for supplementary ad creatives.
5. Currently leading **generative search** R&D — exploring LLM for query intent generation and result re-ranking.

**Result**: Cumulative CTR +46%. Search recall CTR +8%. AIGC usability 90%+. System supports tens of millions of daily requests.

**Key Talking Points for Follow-up**:
- "How did you build dual-tower from scratch?" → Describe embedding design, negative sampling strategy (in-batch + hard negatives), ANN index choice (FAISS/HNSW), online serving architecture.
- "What was the hardest part?" → Cold-start for new car models — used content-based features (brand, price range, specs) as fallback, gradually transitioned to collaborative signals.

---

### Project 2: Baidu Tieba Push Recommendation (2019–2021)

**Situation**: Baidu Tieba Push had 500 million daily impressions but low CTR and high user complaint rate about irrelevant notifications.

**Task**: Build a personalized push ranking system that improves engagement while controlling user disturbance.

**Action**:
1. Built the push recommendation platform from zero — designed the **DNN-NCF ranking model** (user ID + post ID + category features), achieving CTR +10%.
2. Designed a **dual-tower DeepFM retrieval model** for candidate quality improvement, CTR +8%.
3. Addressed long-tail cold-start: constructed a user-forum-post click graph and applied **Metapath2Vec++ graph representation learning** to generate embeddings for low-activity forums.
4. Designed a **disturbance rate control strategy** — frequency capping + quality threshold filtering. A/B test: CTR +15%, complaint rate -20%.
5. Solved **online-offline consistency**: traced a 15% metric gap to temporal feature leakage (T+1 features in training vs real-time T features in serving). After strict point-in-time feature reconstruction, gap reduced to <5%.

**Result**: DAU improvement, complaint rate significantly reduced. Received MEG Technical Innovation Award (2020).

**Key Talking Points**:
- "How did you diagnose the online-offline gap?" → Layer-by-layer feature distribution comparison between offline dataset and online logging. Found user real-time behavior count was computed with 1-day lookahead in training.
- "Why Metapath2Vec++ over other graph methods?" → Heterogeneous graph (user-forum-post), needed to capture multi-type relationships. Metapath defines semantic paths; Vec++ extends to heterogeneous edge types.

---

### Project 3: Tencent WeSee Push Ranking (2021–2022)

**Situation**: Tencent WeSee (short video) needed push notification ranking for both WeChat plugin and QQ platforms. Challenge: optimizing click-through without hurting main app user retention — conflicting objectives.

**Task**: Design multi-objective ranking model that jointly optimizes notification clicks and main app daily active users.

**Action**:
1. Implemented **MMoE (Multi-gate Mixture of Experts)** multi-objective CTR model — shared expert networks with task-specific gating for click prediction and retention prediction.
2. On QQ: designed dual-objective (red dot impression click + content click). On WeChat: active user multi-objective joint modeling.
3. Strengthened **Cross feature engineering** — interaction features between user profile, video content, and temporal context. Applied cross-business transfer learning.

**Result**: Significant DAU improvement and main app retention lift.

---

### Project 4: Baidu Content Risk Control (2017–2019, Led 2-person team)

**Situation**: Baijiahao (Baidu's content platform) had a growing problem with spammy accounts and duplicate content.

**Task**: Build an author risk profiling system and content deduplication service.

**Action**:
1. Built author risk profiling from scratch — designed 35+ risk labels covering behavioral patterns, content quality, and account signals.
2. Designed and deployed a **content deduplication service** using SimHash, Entity Linking, pHash (for images), and N-gram similarity.
3. Filed and received a **patent** as first inventor: "A Semantic Understanding-Based Content Duplication Detection Method" (CN110162752B).

**Result**: Effective suppression of abusive accounts. Won Annual Best Project Award (2018) and NLP First-Class Patent Award (2019).

---

## Part 2: User Behavior Sequence Modeling

### Technical Knowledge Points

**Evolution**: DIN → SIM → HSTU — each solves the previous generation's core bottleneck.

**DIN (Deep Interest Network, Alibaba 2018)**
- Problem: Equal-weight pooling over user history loses the fact that different behaviors contribute differently per candidate.
- Solution: Target attention — compute attention score between each historical behavior and the candidate item via an Activation Unit (MLP on concatenated features: [e_i, e_a, e_i - e_a, e_i * e_a]).
- Limitation: Sequence length capped at ~50-200 due to computational cost.

**SIM (Search-based Interest Model, Alibaba 2020)**
- Problem: Real users have up to 54,000 behaviors over 180 days. DIN can't handle this.
- Solution: Two-stage approach — GSU (General Search Unit) filters full history to Top-K (~200), then ESU (Exact Search Unit) applies multi-head target attention.
- GSU has two **mutually exclusive** variants (not combined):
  - Hard Search: Inverted index by category — lookup same-category behaviors. No parameters (α=0 in loss).
  - Soft Search: Separate auxiliary CTR model trained on long sequences for embeddings → per-user ANN index → MIPS retrieval. (α=1 in loss).
- ESU: **Multi-Head Target Attention** — Q is candidate item (single vector), K/V from Top-K subsequence. Attention shape (1×K), NOT self-attention (K×K).
- Dual-path architecture: GSU→ESU for long-term (180 days) || DIEN for short-term (~14 days) → concat → MLP.
- Time encoding: `floor(log(Δdays + 1))` log-bucketed, concatenated to behavior embeddings.

**HSTU (Hierarchical Sequential Transduction Units, Meta 2024)**
- Problem: Unify recommendation as autoregressive sequence prediction, replacing the entire DLRM pipeline.
- Core idea: Feature sequentialization — all inputs (user attributes, item features, behaviors) serialized into one token sequence with temporal markers. Training is autoregressive with causal mask (like GPT). One sequence of length N → N-1 training samples.
- Three architectural changes from standard Transformer:
  1. **SiLU replaces softmax**: Preserves engagement intensity (clicking 100 times vs 3 is meaningful; softmax normalizes this away). Formula: `SiLU(QK^T + rab) · V / N`.
  2. **Gating replaces FFN**: `Norm(A·V) ⊙ U` — U is a fourth projected vector doing per-dimension gating. Compresses 6 linear layers to 2.
  3. **rab (relative attention bias)**: Encodes both position distance and time interval, added to Q·K^T. No separate PE needed.
- "Hierarchical" = multi-layer stacking with K/V downsampling + Stochastic Length truncation. NOT session splitting.
- General architecture: works for both retrieval (output user embedding → ANN) and ranking (candidate as input token → relevance score).

**Comparison Table** (memorize this):

| | DIN | SIM | HSTU |
|---|-----|-----|------|
| Core problem | Dynamic interest | Long sequence efficiency | Unified architecture replacing DLRM |
| Sequence length | ~50 | ~54,000 (GSU filters to 200) | >8,192 (direct) |
| Attention type | Target Attention (single-head) | Multi-Head Target Attention | Causal Self-Attention + SiLU + gating |
| Training | Impression log (1 sample per impression) | Impression log | Autoregressive (N-1 samples per sequence) |
| Applicable tasks | Ranking only | Ranking only | Retrieval + Ranking |

---

### Interview Q&A

**Q: Can you explain the evolution from DIN to SIM to HSTU?**

DIN introduced target attention — dynamically weighting user history based on the candidate item. But it only handles ~50-200 behaviors. SIM solves the long sequence problem with a two-stage approach: GSU filters 54,000 behaviors down to 200 using either category-based inverted index or ANN retrieval, then ESU applies multi-head target attention. HSTU goes further — it replaces the entire DLRM pipeline with a unified autoregressive Transformer, serializing all features into one token sequence.

**Q: What kind of attention does SIM's ESU use?**

Multi-head target attention. Q is the candidate item (single vector), K/V come from the GSU-selected subsequence. Attention shape is (1×K), not (K×K). It's a multi-head upgrade of DIN's activation unit.

**Q: Is HSTU a ranking model only?**

No, it's a general architecture for both retrieval and ranking. For retrieval, the output user representation is used for ANN search. For ranking, the candidate item is included as a token in the input.

---

## Part 3: Multi-Task Learning

### Technical Knowledge Points

**Evolution**: Shared-Bottom → MMoE → PLE

- **Shared-Bottom**: All tasks share one bottom DNN. Problem: negative transfer when tasks conflict.
- **MMoE (Multi-gate Mixture of Experts)**: K independent expert networks + per-task gating (softmax weights over experts). Each task selects its own expert mixture. Problem: all experts are shared, task-specific information can be diluted.
- **PLE (Progressive Layered Extraction)**: Introduces task-specific experts alongside shared experts. Each gate weights both shared + own task-specific experts. Supports multi-layer progressive extraction.

**ESMM (Entire Space Multi-Task Model)**:
- Problem: CVR training suffers from sample selection bias (only trained on clicked samples) and data sparsity.
- Solution: Model pCTCVR = pCTR × pCVR on the entire impression space. CVR tower is never directly supervised on click samples — it's indirectly trained through the product relationship on all impressions.

**Gradient Conflict**:
- Detection: Compute cosine similarity of gradients from different tasks on shared parameters. Negative = conflict.
- Solutions: GradNorm (dynamic loss weighting), PCGrad (project conflicting gradients), PLE (architectural isolation).

### Interview Q&A

**Q: Explain MMoE and when you'd use it over Shared-Bottom.**

MMoE uses multiple independent expert networks with per-task gating. Each task learns which experts to rely on. Use MMoE when tasks have weak or negative correlation — for example, CTR and user retention often conflict because clickbait content gets high CTR but hurts retention. Shared-Bottom would suffer from negative transfer in this case.

**Q: What is ESMM and what problem does it solve?**

ESMM addresses CVR modeling bias. Traditional CVR models only train on clicked samples, but we need to predict CVR on all impressions. ESMM models pCTCVR = pCTR × pCVR, training both on the full impression space. The CVR tower gets indirect supervision through this product relationship, avoiding selection bias.

---

## Part 4: Feature Interaction — DCN

### Technical Knowledge Points

**Why DCN**: Manual feature crossing explodes combinatorially (d² for 2nd order). MLP learns multiplicative interactions inefficiently. DCN automates explicit feature crossing.

**DCN v1 (2017)**:
- Formula: `x_{l+1} = x_0 · (w^T · x_l) + b + x_l`
- w is a **vector** (not matrix). `w^T · x_l` → scalar → multiplied by x_0.
- Cross terms emerge: `x_0[i] · x_0[j]` appears, but ALL share one scalar weight.
- **Rank-1 limitation**: Can't independently weight price×brand vs price×age.
- Performance: Cross-only worse than MLP (Criteo: 0.4565 vs 0.4508). v1's contribution is directional, not practical.

**DCN v2 (2021)**:
- Core change: w vector → W matrix. Formula: `x_{l+1} = x_0 ⊙ (W · x_l + b) + x_l`
- Each dimension of x_0 multiplies a different value from W·x_l → independent weights per feature pair.
- Low-rank: W = U·V^T (d×r), parameters from d² to 2dr.
- DCN-Mix: K experts with gating, each with own U_k, V_k.
- Stacked mode (Cross → Deep → output) usually better than Parallel (Cross || Deep → concat).

**Comparison**:
| Method | Crossing | Weights | Parameters |
|--------|----------|---------|------------|
| FM | 2nd-order explicit | Embedding inner product, static | d×k |
| DCN v1 | Multi-order, rank-1 | Shared scalar | d per layer |
| DCN v2 | Multi-order, full/low-rank | Independent per pair | d² or 2dr |
| MLP | Implicit via ReLU | Fully implicit | d² |
| Self-Attention | Dynamic, input-dependent | Q·K^T per sample | d² |

### Interview Q&A

**Q: Explain DCN v1 and v2. What's the core limitation of v1?**

*(See Part 2 of original doc for full answer — same content as before)*

**Q: What's the difference between Attention and DCN for feature interaction?**

DCN does feature-dimension crossing within a single sample — static weights shared across all inputs. Attention does token-level interaction across sequence positions — dynamic weights that depend on the input. They're orthogonal and can be stacked. HSTU's `Norm(A·V) ⊙ U` combines both: A·V is dynamic aggregation, ⊙U is adaptive feature gating.

---

## Part 5: Position Encoding

### Technical Knowledge Points

Three approaches with different injection points:

```
Sinusoidal:  x' = x + PE → Q = W_q·x' → Q·K^T/√d → softmax → ·V
             ↑ added before projection    ↑ absolute/relative positions entangled

Relative PE: x → Q = W_q·x → Q·K^T/√d + β(j-i) → softmax → ·V
                                ↑ bias added to score, only depends on j-i

RoPE:        x → Q = W_q·x → Q' = R(θm)·Q → Q'·K'^T/√d → softmax → ·V
                               ↑ rotation after projection, before dot product
```

- **Sinusoidal**: PE(pos, 2i) = sin(pos/10000^(2i/d)). Entanglement problem: expanding Q·K^T gives 4 terms where relative distance m-n can't be cleanly separated from absolute positions.
- **Relative PE**: Learnable bias β(j-i) added to attention score. Clean relative encoding. Limitation: needs parameters for each possible distance; can't extrapolate.
- **RoPE**: Rotation matrices on Q/K. Mathematical property: R(m)^T · R(n) = R(m-n), so dot product strictly depends on relative distance only. Continuous rotation supports length extrapolation. Used in LLaMA, ChatGLM.

**In RecSys**: DIN has no PE; SIM uses log-bucketed time intervals; HSTU uses rab (relative attention bias encoding both position and time).

---

## Part 6: Listwise Ranking Loss

### Technical Knowledge Points

| Type | Approach | Representative | Pros/Cons |
|------|----------|---------------|-----------|
| Pointwise | Predict score independently | CTR regression | Simple, ignores relative order |
| Pairwise | Model "which is more relevant" | BPR, RankNet | Considers relative order, O(n²) pairs |
| Listwise | Optimize entire ranking quality | ListMLE, Softmax Loss, LambdaRank | Closest to NDCG, more complex |

**Softmax Loss (most frequent in interviews)**:
- Given query + candidates (1 positive + K negatives), maximize positive's softmax probability.
- Temperature τ: smaller → sharper, more sensitive to hard negatives. Typical range: 0.07–0.2.

**LambdaRank**:
- NDCG is non-differentiable. Trick: don't define loss, define gradient directly.
- λ_ij weighted by |ΔNDCG_ij| — how much NDCG changes if you swap items i and j.
- LambdaMART = LambdaRank + gradient boosted trees. Common for offline re-ranking.

### Interview Q&A

**Q: What's the difference between Pointwise, Pairwise, and Listwise?**

Pointwise predicts each item's score independently — simple but ignores inter-item relationships. Pairwise models whether item A is more relevant than B — captures relative order but pair count is O(n²). Listwise directly optimizes the quality of the entire ranking — closest to metrics like NDCG. In practice, Softmax Loss (a listwise approach) is the most commonly used in modern recommendation because it naturally handles in-batch negatives and scales well.

---

## Part 7: Causal Inference & Bias Correction

### Technical Knowledge Points

**Bias types in RecSys**:
- **Position Bias**: Users click top-ranked items regardless of quality → top items get inflated CTR.
- **Selection Bias**: Only exposed items have labels → model only learns from "what was recommended."
- **Popularity Bias**: Popular items get over-exposed → long-tail items undiscoverable.

**Position Bias Correction**:
1. **IPW (Inverse Propensity Weighting)**: Weight each sample by 1/P(click|position). Lower-position positives get higher weight.
2. **Position-Independent Dual Tower**: Train with position as a separate tower; at inference time, zero out the position tower. Most common production approach (YouTube DNN).
3. **PAL (Position-Aware Learning)**: Explicitly model pCTR = pCTR_true × P(examine|position).

**Uplift Modeling**:
- Goal: Find "Persuadables" — users who act ONLY because of the intervention.
- T-Learner: Train separate models for treatment and control groups, uplift = difference in predicted probabilities.
- S-Learner: Single model with treatment as a feature, compute uplift by toggling treatment on/off.
- Evaluation: AUUC (Area Under Uplift Curve), Qini Coefficient.

### Interview Q&A

**Q: How would you handle position bias in a recommendation system?**

The most practical production approach is the Position-Independent Dual Tower: include position as a separate input tower during training, then zero it out at serving time. This way, the main model learns content relevance without position influence. I've seen this work well at scale — YouTube DNN uses this exact approach. For more principled correction, IPW re-weights samples by inverse propensity scores, but estimating propensity accurately is tricky in practice.

---

## Part 8: Generative Recommendation

### Technical Knowledge Points

**VQ-VAE**: Encoder → continuous z → quantize to nearest codebook vector → Decoder reconstructs. Each item becomes 1 discrete token. Gradient through quantization: Straight-Through Estimator (STE).

**RQ-VAE (Residual Quantization)**: Multi-level quantization — each level quantizes the residual from the previous level. Item represented as tuple (c1, c2, c3). Coarse-to-fine hierarchy.

**FSQ (Finite Scalar Quantization)**: No codebook at all — directly quantize each dimension to finite integer levels. Codebook size = product of levels (e.g., [8,5,5,5] → 1000). No codebook collapse issue.

**Three Paradigms**:

| | Behavior Sequentialization (HSTU) | Semantic ID (TIGER/OneSearch) | Text-to-Text (P5) |
|---|---|---|---|
| Representative | HSTU (Meta 2024) | TIGER (Google 2023), OneSearch (Kuaishou) | P5 (2022), GPT4Rec |
| Input | Behavior tokens | Semantic IDs (RQ-VAE codes) | Natural language |
| Model | Modified Decoder-only | T5 Encoder-Decoder | T5 / GPT |
| Pre-training | None, behavior data only | None (or minimal) | Yes, LLM world knowledge |
| Industrial deployment | Meta (billions DAU) | OneSearch (Kuaishou e-commerce) | Experimental |
| Strength | Training efficiency, proven at scale | Structured generation, controllable | Cold-start, cross-domain |
| Weakness | No text knowledge | Depends on tokenizer quality | Slow inference |

**TIGER specifics**: 3-level RQ-VAE, codebook size 256/level, Sentence-T5 768-dim input, tested on Amazon datasets (~50K items).

**OneSearch specifics**: Actually uses RQ-Kmeans + OPQ (not RQ-VAE — found RQ-VAE inferior). 5 layers, codebook sizes (4096, 1024, 512, 256, 256). Deployed on Kuaishou e-commerce.

### Interview Q&A

**Q: What are the main generative recommendation paradigms?**

Three paths. First, behavior sequentialization like HSTU — serialize everything into one token sequence, decoder-only autoregressive. Only one proven at industrial scale. Second, semantic ID generation like TIGER and OneSearch — encode items into discrete IDs via RQ-VAE or RQ-Kmeans, then use T5 to generate IDs autoregressively. Third, text-to-text like P5 — convert the task to natural language and leverage LLM pre-training. Good for cold-start but too slow for production.

**Q: Why do many papers use T5 for generative recommendation?**

T5's encoder-decoder architecture naturally fits "understand history → generate recommendation." The encoder uses bidirectional attention to fully comprehend user context; the decoder autoregressively generates item IDs. Plus T5 has pre-trained world knowledge useful for cold-start. HSTU chose decoder-only because it unifies input and output into one sequence, eliminating the need for a separate encoder.

---

## Part 9: User Intent & Profile System

### Technical Knowledge Points

**OKX's unique challenge**: User behavior spans three heterogeneous domains:
1. Content consumption (articles, news)
2. Feature usage (spot trading, contracts, options)
3. Search (token search, project search)

**Cross-Domain Intent Framework**:
- Each domain has its own encoder → domain intent vector
- Cross-domain Attention Fusion → unified intent vector
- Key decision: Share entity embeddings across domains (BTC = same entity everywhere) but use domain-specific attention layers.
- Temporal alignment: Different domains have very different event frequencies. Use absolute timestamps, not relative positions.

**User Lifecycle Profiling**:

| Stage | Characteristics | Strategy |
|-------|----------------|----------|
| Cold-start (<7 days) | No/few behaviors | Cluster by registration channel + device + region; show popular content |
| Exploration (7-30 days) | Diverse but unstable | Fast interest convergence; high Explore weight (UCB) |
| Stable preference (30+ days) | Clear patterns | Precise long-term modeling; reduce Explore |
| Churn risk (30 days inactive) | No recent activity | Trigger recall push; high-info, low-barrier content |

---

## Part 10: LLM Agent + Recommendation

### Technical Knowledge Points

**Why LLM Agent for OKX**: Crypto user queries are often complex multi-step intents: "I want to find DeFi projects with good yield, low risk, suitable for beginners." This requires reasoning, not keyword matching.

**ReAct Pattern (Reasoning + Acting)**:
```
User: Recommend low-risk DeFi products for current market
→ LLM Thought: Need market sentiment first, then filter low-risk
→ Action: call get_market_sentiment()
→ Observation: Fear index 72, bearish
→ LLM Thought: Bearish market → prioritize stablecoin strategies
→ Action: call recommend_defi(risk="low", market="bear", user_id=xxx)
→ Observation: [Aave USDC 4.2% APY, Curve 3pool 3.8%, ...]
→ Response: Based on current market conditions, here are low-risk options...
```

**Hybrid Retrieval**: LLM Embedding (semantic) + BM25 (keyword) → RRF Rerank → Cross-Encoder Reranker → LLM generates final answer with citations.

---

## Part 11: OKX Business-Specific Questions

### Interview Q&A

**Q: How is crypto recommendation different from traditional content recommendation?**

Four key differences. First, **behavior is highly correlated with market conditions** — when BTC drops 20%, everyone reads panic articles. The "stable preference" assumption fails; you need real-time market sentiment features (Fear & Greed Index, 24h BTC change) as context signals. Second, **risk appetite is a critical dimension** — high-risk traders and conservative investors have completely different content needs. This dimension doesn't exist in typical content recommendation. Third, **information freshness is extremely valuable** — a single news piece can move a token 30%; time decay weights need to be much more aggressive. Fourth, **regulatory compliance** is a hard constraint — different jurisdictions have different rules about what tokens can be shown.

**Q: How would you design a "feature discovery" recommendation for OKX?**

Treat platform features (spot trading, contracts, staking, etc.) as items to recommend. User features: which features already used, trading frequency, asset size, account age. Item features: feature complexity, prerequisite features, adoption rate among similar users. Optimize for CVR (shown feature → first use), not CTR. Cold-start: new users get basic features (spot buy/sell); gradually guide toward complex features (contracts, options) based on behavior.

**Q: How would you handle multi-language, multi-region recommendation?**

Use multilingual pre-trained models (XLM-R / mBERT) for content embedding — semantic space aligned across languages. Region embedding as auxiliary feature to capture regional preference differences. For compliance, maintain per-jurisdiction filtering rules applied at the re-ranking stage.

---

## Part 12: Engineering & System Design

### Technical Knowledge Points

**Real-Time Feature Pipeline**:
```
User events (click/trade/search)
  → Kafka (partitioned by user ID, preserving order)
  → Flink streaming: real-time CTR stats (5min/1h/24h windows),
    user sequence updates, item popularity computation
  → Redis / Feature Store (<10ms read latency)
  → Model inference service
```

**Common pitfalls**:
- **Feature leakage**: Training uses future data. Fix: strict event-time alignment.
- **Training-serving skew**: Different feature computation logic offline vs online. Fix: unified Feature Store with historical snapshots.

**Inference Latency Optimization** (target P99 < 100ms):

| Technique | Effect | Use Case |
|-----------|--------|----------|
| INT8 quantization | 2-4x speedup, <1% accuracy loss | Ranking models |
| Knowledge distillation | Small model ≈ large model | Retrieval / pre-ranking |
| Async pre-computation | User vectors cached in Redis | Dual-tower user side |
| ONNX + TensorRT | Cross-framework acceleration | GPU inference |
| Batch serving | Higher GPU utilization | High-concurrency |

### System Design: OKX Recommendation System (30-min interview format)

**1. Clarify Requirements (5 min)**:
- What to recommend: content articles / platform features / token pairs
- Scale: DAU, candidate pool size
- Core metrics: CTR? Retention? Trading conversion?
- Latency: real-time <100ms or pre-computation acceptable?

**2. Overall Architecture (10 min)**:
- Retrieval → Pre-ranking → Ranking → Re-ranking → Compliance filtering
- Retrieval strategies: vector retrieval (dual-tower), collaborative filtering (I2I), popularity, time-based trending
- Ranking: DIN/SIM base + market sentiment real-time features
- Multi-objective: CTR + trading conversion + retention via MMoE

**3. Core Algorithm Details (10 min)**:
- User sequence modeling (SIM or HSTU, explain why)
- Position bias: Position-Independent dual tower
- OKX-specific: market sentiment features, risk appetite modeling

**4. Cold-Start & Monitoring (5 min)**:
- New users: region + device cluster-based recommendation
- New tokens/articles: content-based features + on-chain data
- Monitoring: CTR, CVR, diversity index, real-time A/B dashboard

---

## Part 13: Quick-Fire Technical Q&A

Practice giving **concise 30-second answers**:

| # | Question | Key Points |
|---|----------|------------|
| 1 | Attention vs DCN for feature interaction? | Attention: dynamic, input-dependent, cross-token. DCN: static weights, same-sample, cross-dimension. Orthogonal, can stack. |
| 2 | Self-attention on non-sequential discrete features? | Yes — AutoInt (2019) treats each feature as a token. HSTU serializes everything. |
| 3 | What is autoregressive attention? | Causal-masked attention — each position only sees previous tokens. GPT, HSTU. One sequence → N-1 training samples. |
| 4 | Encoder vs Decoder in Transformer? | Encoder: bidirectional self-attention (BERT). Decoder: causal self-attention + cross-attention + FFN. GPT = decoder-only (no cross-attention). |
| 5 | Why did HSTU remove softmax? | Softmax normalizes to sum=1, losing engagement intensity. SiLU preserves absolute magnitude. |
| 6 | RQ-VAE vs VQ-VAE? | VQ-VAE: single codebook, one code. RQ-VAE: multiple codebooks, each quantizes residual — coarse-to-fine. |
| 7 | "Rank-1" in DCN v1? | w is vector → dot product gives scalar → multiplied by x_0 produces rank-1 outer product. All cross terms share one weight. |
| 8 | How does SIM's Hard Search work? | Inverted index by category. Look up user history with same category as candidate. No parameters, no training. Engineering-simple, widely deployed. |
| 9 | What's the ESMM trick? | pCTCVR = pCTR × pCVR. CVR tower trained indirectly through product relationship on full impression space, avoiding selection bias. |
| 10 | Position bias in production? | Position-Independent Dual Tower — train with position tower, zero it out at inference. YouTube DNN approach. |
| 11 | Gradient conflict in multi-task? | Tasks' gradients on shared params point in opposite directions (cosine < 0). Fix: PCGrad (projection), GradNorm (dynamic weighting), PLE (architectural isolation). |
| 12 | FSQ vs VQ-VAE? | FSQ has no codebook — directly quantize each dimension to finite integers. No codebook collapse. Simpler. |

---

## Part 14: Behavioral Questions

### Q: Tell me about the most impactful project you've led.

*(Use Baidu Push Recommendation — Project 2 above)*

### Q: How do you balance technical perfectionism with fast delivery?

I believe in iterative improvement with a working baseline first. For example, when building user sequence modeling, I started with a simple DIN baseline — it was fast to implement and gave us quick A/B test results to validate the direction. Only after proving business value with data did I invest in the more sophisticated SIM long-sequence version. I usually propose a two-phase plan: Phase 1 delivers business value quickly; Phase 2 pushes toward the optimal solution. This gives stakeholders confidence while keeping technical quality high.

### Q: How do you handle disagreements with product/business teams?

At Baidu, after deploying our CTR model, the business team complained that "user quality dropped." From a technical perspective, CTR was up — the model was doing its job. But from the business perspective, clicks weren't leading to deeper engagement. The root cause: we were optimizing for clicks only, ignoring depth metrics. I proposed adding CVR and dwell time as auxiliary objectives using MMoE, which aligned the algorithm's optimization target with the business's actual goal. The key lesson: explicitly surface the gap between algorithm metrics and business metrics, so both sides can see the same picture.

### Q: What's your biggest weakness / area for growth?

My experience has been primarily in traditional recommendation — user profiling, CTR prediction, and multi-objective optimization. Generative recommendation (RQ-VAE, autoregressive retrieval) and large-scale distributed training are areas I've been actively studying but haven't deployed in production yet. That's exactly why this role is exciting to me — OKX's focus on generative search and LLM-powered recommendation is the direction I want to grow into, and I'm bringing strong fundamentals in the full recommendation pipeline to build on.

### Q: Why OKX?

Three reasons. First, OKX is at the intersection of recommendation systems and a fast-evolving domain — crypto and Web3. The recommendation challenges here are unique: real-time market sensitivity, cross-domain user intent, regulatory constraints. This is technically more interesting than standard content or e-commerce recommendation. Second, the JD emphasizes generative search and LLM agents for recommendation — that's exactly the direction I'm currently researching and want to go deeper. Third, I want to work in a global product environment. My Master's at Southampton gave me comfort working in English, and OKX's global user base across 200+ countries is an environment where I can grow both technically and professionally.

---

## Part 15: Delivery Tips

1. **Structure first**: "There are three key points..." or "Let me break this into two parts..." — helps the interviewer follow.
2. **Use comparisons**: "Unlike DIN which..., SIM addresses..." — shows depth.
3. **Admit trade-offs**: "The downside is..." or "In practice, this doesn't work well because..." — shows real understanding vs textbook answers.
4. **Connect to experience**: "In my work at Baidu, we faced a similar problem where..." — makes answers concrete.
5. **Don't over-explain**: If the interviewer nods, move on. If they look confused, add more detail. Read the room.
6. **Key phrases to have ready**:
   - "The core insight of this paper is..."
   - "The practical limitation is..."
   - "In production, the bottleneck was..."
   - "We validated this through A/B testing and saw..."
   - "The trade-off between X and Y is..."
   - "Let me give you a concrete example from my experience..."
7. **Numbers matter**: Always mention specific metrics — "CTR +46%", "500 million daily impressions", "gap reduced from 15% to 5%". Interviewers remember numbers.
8. **Don't be afraid to say "I don't know"**: If asked about something unfamiliar, say "I haven't worked with that directly, but based on my understanding of [related concept]..." — shows intellectual honesty.
