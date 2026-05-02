# 06_prefix_sum：前缀和

> 预处理前缀信息，将区间查询从 O(n) 降为 O(1)

## 核心特征

- 用额外空间预处理，换取查询加速
- 前缀和：区间求和；前缀积：区间求积
- 常配合哈希表使用（如和为 K 的子数组）

## 解题框架

```python
# 一维前缀和
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + nums[i]
# 区间 [l, r] 的和 = prefix[r+1] - prefix[l]

# 前缀和 + 哈希表（子数组和为 K）
count = defaultdict(int)
count[0] = 1
cur_sum = 0
for num in nums:
    cur_sum += num
    if cur_sum - k in count:
        累加答案
    count[cur_sum] += 1
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 238 | 除自身以外数组的乘积 | 🟡 Medium | ⬜ |
| 303 | 区域和检索 | 🟢 Easy | ⬜ |
| 560 | 和为 K 的子数组 | 🟡 Medium | ⬜ |

## 关键思想

**前缀积怎么做？**
类似前缀和，用 `prefix[i+1] = prefix[i] * nums[i]`。除自身以外的乘积 = 左侧前缀积 × 右侧后缀积，可用 O(1) 额外空间（输出数组不算）。

**前缀和 + 哈希表的直觉？**
`sum[l..r] = K` 等价于 `prefix[r+1] - prefix[l] = K`，即找之前出现过多少个 `prefix[r+1] - K`，用哈希表 O(1) 查。
