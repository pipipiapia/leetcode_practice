# 04_center_expand：中心扩展法

> 从中心向两侧扩展，常用于回文串问题

## 核心特征

- 每个字符（或相邻两个字符）都可以作为中心
- 分奇数长度和偶数长度两种中心
- 向左右同时扩展，直到不满足条件为止
- 时间 O(n²)，空间 O(1)

## 解题框架

```python
for i in range(len(s)):
    # 奇数长度：以 i 为中心
    expand(i, i)
    # 偶数长度：以 i, i+1 为中心
    expand(i, i + 1)

def expand(left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        记录答案
        left -= 1
        right += 1
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 5 | 最长回文子串 | 🟡 Medium | ⬜ |

## 关键思想

**为什么中心扩展比 DP 更优？**
DP 解法需要 O(n²) 空间存 dp 表，而中心扩展只需 O(1) 空间，时间复杂度同为 O(n²)。面试优先写中心扩展。
