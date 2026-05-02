# 02_topological：拓扑排序

> 有向无环图的线性排序，常用于依赖关系问题

## 解题框架

```python
# Kahn 算法（BFS + 入度表）
from collections import deque, defaultdict
indegree = [0] * n
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    indegree[v] += 1

queue = deque([i for i in range(n) if indegree[i] == 0])
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for neighbor in graph[node]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)
# len(order) == n → 无环，否则有环
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 207 | 课程表 | 🟡 Medium | ⬜ |

## 关键思想

**课程表 = 判环问题：** 能完成拓扑排序（所有节点入队）则无环，可以完成所有课程；否则有环，不可能。
