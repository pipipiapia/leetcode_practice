# 01_bfs_dfs：广度优先与深度优先搜索

> BFS 求最短路径，DFS 求所有路径

## 解题框架

```python
# BFS（网格）
from collections import deque
queue = deque([(i, j)])
visited = set([(i, j)])
while queue:
    x, y = queue.popleft()
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited:
            visited.add((nx, ny))
            queue.append((nx, ny))

# DFS（网格）
def dfs(x, y):
    if 越界 or 已访问: return
    visited.add((x, y))
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        dfs(x + dx, y + dy)
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 200 | 岛屿数量 | 🟡 Medium | ⬜ |
| 994 | 腐烂的橘子 | 🟡 Medium | ⬜ |

## 关键思想

**岛屿数量：** 遍历网格，遇到 1 就 DFS/BFS 把相连的 1 全标记，计数+1。

**腐烂橘子：** 多源 BFS，所有初始腐烂橘子同时入队，逐层扩展记录轮次。
