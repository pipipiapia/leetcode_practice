# 02_permutation_subset：排列与子集

> 排列有顺序，子集无顺序

## 解题框架

```python
# 排列
def backtrack(path, used):
    if len(path) == len(nums):
        result.append(path[:])
        return
    for i in range(len(nums)):
        if used[i]: continue
        used[i] = True
        path.append(nums[i])
        backtrack(path, used)
        path.pop()
        used[i] = False

# 子集：每个元素选或不选
def backtrack(start, path):
    result.append(path[:])
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 46 | 全排列 | 🟡 Medium | ⬜ |
| 78 | 子集 | 🟡 Medium | ⬜ |
