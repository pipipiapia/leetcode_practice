# 02_interval：区间问题

> 几乎都要先排序，然后贪心处理

## 解题框架

```python
# 合并区间
intervals.sort(key=lambda x: x[0])
result = [intervals[0]]
for start, end in intervals[1:]:
    if start <= result[-1][1]:
        result[-1][1] = max(result[-1][1], end)   # 重叠则合并
    else:
        result.append([start, end])                # 不重叠则新增
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 56 | 合并区间 | 🟡 Medium | ⬜ |
| 435 | 无重叠区间 | 🟡 Medium | ⬜ |

## 关键思想

**无重叠区间 = 合并区间的反面：** 按右端点排序，贪心保留结束最早的区间，冲突的都删掉。
