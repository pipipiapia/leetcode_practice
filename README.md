# LeetCode 刷题 + AI 面试题库

> 配套 [interview_guide.md](./interview_guide.md) 使用，算法题与 AI 知识分目录管理，代码可直接运行验证。

## 目录结构

```
leetcode_practice/
├── README.md                          ← 你在这里
├── PROGRESS.md                        ← 刷题进度追踪
├── interview_prep/                    ← 面试准备（算法 + DL/PyTorch）
│   ├── README.md
│   ├── leetcode_interview_guide.md    ← LeetCode 高频题型分类总结
│   └── interview_prep_dl_pytorch.md   ← 深度学习 & PyTorch 核心知识点
└── problems/
    ├── 01_array_two_pointers/         ← 数组：双指针、滑动窗口、前缀和、矩阵
    ├── 02_hash_string/                ← 字符串、哈希表、Trie、KMP
    ├── 03_linked_list/                ← 链表：反转、合并、环、LRU
    ├── 04_binary_tree/                ← 二叉树：遍历、构造、BST、序列化
    ├── 05_dynamic_programming/        ← 动态规划：路径、背包、序列、字符串 DP
    ├── 06_stack_monotonic/            ← 栈、单调栈
    ├── 07_backtrack/                  ← 回溯：排列、组合、子集、网格搜索
    ├── 08_sort_binary_heap/           ← 排序、二分、堆、TopK
    ├── 09_graph_unionfind/            ← 图、BFS、拓扑排序、并查集
    ├── 10_greedy_interval/            ← 贪心、区间
    └── 03_ai_interview/               ← AI 面试题
        ├── 01_deep_learning/          ← 深度学习基础
        ├── 02_pytorch/                ← PyTorch 核心机制
        ├── 03_recommendation/         ← 推荐系统 / 搜广推
        ├── 04_coding/                 ← 高频手撕代码
        └── 05_losses/                 ← Loss 函数专题
```

## 如何刷题

### 第一步：选一道题

打开对应分类目录，找到 `pXXXX_name.py` 文件，每个文件结构如下：

```python
def solve(nums):
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass
```

文件里包含：
- LeetCode 原题链接
- 大厂出现频率（★越多越重要）
- 解题思路提示（拆解关键点）
- 自测用例

### 第二步：先自己想

1. 读题，理解题目要求
2. 看「思路拆解」和「关键点提示」
3. 在空白处写代码（先不要看答案）
4. 运行测试用例 `python pXXXX_name.py` 验证

### 第三步：跑通所有测试

```bash
cd problems/01_array_two_pointers/03_sliding_window/02_variable
python p0001_two_sum.py  # 运行单题

# 或直接运行
python p0001_two_sum.py
```

全部通过 ✅ 说明这题掌握了。

### 第四步：对比参考解法（Optional）

每道题都支持多种解法，README 中会说明进阶优化方向。
如果你用了 O(n²) 解法，试试看能不能优化到 O(n)。

---

## 推荐刷题顺序

### P0 必做（按优先级）

| 优先级 | 题号 | 题目 | 分类 | 字节频率 |
|--------|------|------|------|----------|
| 1 | 206 | 反转链表 | 链表 | ★★★★★ |
| 2 | 1 | 两数之和 | 数组/哈希 | ★★★★★ |
| 3 | 21 | 合并两个有序链表 | 链表 | ★★★★★ |
| 4 | 53 | 最大子数组和 | DP/贪心 | ★★★★★ |
| 5 | 70 | 爬楼梯 | DP | ★★★★★ |
| 6 | 102 | 二叉树层序遍历 | BFS | ★★★★ |
| 7 | 121 | 买卖股票最佳时机 | DP | ★★★★★ |
| 8 | 3 | 无重复字符最长子串 | 双指针 | ★★★★★ |
| 9 | 20 | 有效的括号 | 栈 | ★★★★ |
| 10 | 200 | 岛屿数量 | DFS | ★★★★ |
| 11 | 42 | 接雨水 | 双指针 | ★★★★★ |
| 12 | 322 | 零钱兑换 | DP | ★★★★ |
| 13 | 141 | 环形链表 | 链表 | ★★★★ |
| 14 | 300 | 最长递增子序列 | DP | ★★★★ |
| 15 | 146 | LRU 缓存 | 设计 | ★★★★★ |

### P1 进阶

| 题号 | 题目 | 分类 |
|------|------|------|
| 25 | K 个一组翻转链表 | 链表 |
| 72 | 编辑距离 | DP |
| 1143 | 最长公共子序列 | DP |
| 103 | 二叉树锯齿形层序遍历 | BFS |
| 76 | 最小覆盖子串 | 滑动窗口 |
| 15 | 三数之和 | 双指针 |
| 236 | 二叉树最近公共祖先 | 树 |
| 215 | 数组第 K 大元素 | 堆/快排 |
| 46 | 全排列 | 回溯 |

---

## 自测命令

```bash
# 运行单个文件
python problems/01_array_two_pointers/03_sliding_window/02_variable/p0001_two_sum.py

# 运行某个分类下的所有题目
python -m unittest discover -s problems/01_array_two_pointers

# 运行全部题目
python -m unittest discover -s problems
```

## 进度追踪

每完成一道题，手动在 `PROGRESS.md` 中打勾，或运行：

```bash
python update_progress.py
```

---

## 常见问题

**Q: 看到题目没有思路怎么办？**
A: 先看「思路拆解」，按提示一步步想。如果还是卡住，说明前置知识不够，回去看该分类的知识点。

**Q: 面试时怎么描述解题思路？**
A: 套用四步框架：
1. 「我会用 X 方法解决，时间 O(X)，空间 O(X)」
2. 「因为 ...（问题分析）」
3. 「具体做法是 ...（核心逻辑）」
4. 「优化方向是 ...（如果有）」

**Q: 一道题要做多久？**
A: 简单题 15-20 分钟，中等题 25-40 分钟，超时了就看答案学习，别死磕。

---

## AI 面试题（03_ai_interview/）

> 配套 `interview_prep/interview_prep_dl_pytorch.md` 使用，每道题含题目描述 + 可运行代码 + 面试追问提示。

### 运行方式

```bash
cd leetcode_practice/problems/03_ai_interview
python3 01_deep_learning/q06_softmax.py        # 单题
python3 02_pytorch/q26_finetune.py             # 单题
```

### 快速导航

**深度学习基础（01_deep_learning/）**

| 题号 | 内容 | 面试频率 |
|------|------|----------|
| Q01 | 反向传播原理与链式法则 | ★★★★★ |
| Q02 | 梯度消失/爆炸及解决方案 | ★★★★★ |
| Q06 | Softmax 原理与求导 | ★★★★★ |
| Q07 | BatchNorm 原理与实现 | ★★★★★ |
| Q12 | SGD / Momentum / Adam 对比 | ★★★★★ |

**PyTorch 核心（02_pytorch/）**

| 题号 | 内容 | 面试频率 |
|------|------|----------|
| Q17 | autograd 梯度计算 | ★★★★ |
| Q21 | GPU 使用与显存管理 | ★★★★ |
| Q24 | 自定义 Dataset / DataLoader | ★★★★ |
| Q26 | 模型微调方法 | ★★★★★ |
| Q28 | 模型保存与加载 | ★★★★ |

**推荐系统（03_recommendation/）**

| 题号 | 内容 | 面试频率 |
|------|------|----------|
| Q32 | DSSM 双塔模型 | ★★★★ |
| Q35 | Wide&Deep | ★★★★ |
| Q38 | ESMM + MMOE + PLE | ★★★★ |

**高频手撕代码（04_coding/）**

| 文件 | 内容 |
|------|------|
| attention.py | Scaled Dot-Product Attention |
| cnn_classifier.py | CNN 图像分类器（MNIST） |
| grad_clipping_freeze.py | 梯度裁剪 + 参数冻结 |

**Loss 函数专题（05_losses/）**

| 题号 | 内容 | 面试频率 |
|------|------|----------|
| Q41 | Cross Entropy（含数值稳定版） | ★★★★★ |
| Q42 | Triplet Loss + Hard Mining | ★★★★★ |
| Q43 | InfoNCE / NT-Xent（SimCLR/CLIP） | ★★★★★ |
| Q44 | Focal Loss（类别不平衡） | ★★★★ |
| Q45 | Label Smoothing + BPR + AUC Loss | ★★★★ |
| Q46 | Loss 全景对比表 + 高频追问 | ★★★★★ |

### 常见追问

- **BatchNorm 训练和测试的区别？** → 测试用 running_mean/var
- **Adam 为什么收敛快但泛化可能不如 SGD？** → 自适应学习率过拟合训练集
- **Wide&Deep 和 DeepFM 的区别？** → Wide 部分是否需要人工设计
- **ESMM 如何解决样本选择偏差？** → 在全样本空间训练 CTR 和 CVR
