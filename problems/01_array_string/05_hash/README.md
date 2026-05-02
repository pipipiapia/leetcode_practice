# 05_hash：哈希表

> 利用哈希表 O(1) 查找的特性，解决计数、去重、配对问题

## 核心特征

- 查找/插入/删除均为 O(1) 均摊
- 常见用法：查补数、计数、分组、去重
- Python 中用 `dict` 或 `set` 实现

## 解题框架

```python
# 查补数（Two Sum 模式）
seen = set()
for num in nums:
    if target - num in seen:
        找到答案
    seen.add(num)

# 计数
from collections import Counter
cnt = Counter(nums)

# 分组（异位词模式）
groups = defaultdict(list)
for word in strs:
    key = ''.join(sorted(word))   # 排序作 key
    groups[key].append(word)
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 1 | 两数之和 | 🟢 Easy | ⬜ |
| 49 | 字母异位词分组 | 🟡 Medium | ⬜ |
| 128 | 最长连续序列 | 🟡 Medium | ⬜ |
| 242 | 有效的字母异位词 | 🟢 Easy | ⬜ |

## 关键思想

**Two Sum 为什么不用排序+双指针？**
排序会打乱原始索引，而题目要求返回下标。哈希表一遍扫描即可，O(n) 时间 O(n) 空间。

**最长连续序列为什么用 set 而不是排序？**
排序 O(n logn) 不满足题目 O(n) 要求。用 set + 只从序列起点扩展，保证每个数最多访问两次。
