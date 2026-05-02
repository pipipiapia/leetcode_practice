# 01_combination：组合问题

> 元素无顺序，选或不选

## 解题框架

```python
def backtrack(start, path):
    if 满足条件:
        result.append(path[:])
        return
    for i in range(start, len(candidates)):
        path.append(candidates[i])
        backtrack(i + 1, path)      # 不重复选：i+1；可重复选：i
        path.pop()
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 22 | 括号生成 | 🟡 Medium | ⬜ |
| 39 | 组合总和 | 🟡 Medium | ⬜ |
