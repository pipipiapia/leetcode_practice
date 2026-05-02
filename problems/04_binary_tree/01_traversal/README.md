# 01_traversal：二叉树遍历

> BFS 层序遍历与 DFS 深度遍历

## 解题框架

```python
# 层序遍历（BFS）
from collections import deque
queue = deque([root])
while queue:
    level = []
    for _ in range(len(queue)):
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    处理 level

# 深度（DFS）
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 102 | 二叉树的层序遍历 | 🟡 Medium | ⬜ |
| 103 | 二叉树的锯齿形层序遍历 | 🟡 Medium | ⬜ |
| 104 | 二叉树的最大深度 | 🟢 Easy | ⬜ |
| 199 | 二叉树的右视图 | 🟡 Medium | ⬜ |
