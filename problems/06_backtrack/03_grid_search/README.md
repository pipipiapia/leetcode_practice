# 03_grid_search：网格搜索

> 在二维网格上 DFS 搜索路径

## 解题框架

```python
def dfs(i, j, k):
    if 越界 or 不匹配: return False
    if k == len(word) - 1: return True
    board[i][j] = '#'          # 标记已访问
    res = dfs(i±1, j, k+1) or dfs(i, j±1, k+1)
    board[i][j] = word[k]      # 回溯，恢复
    return res
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 79 | 单词搜索 | 🟡 Medium | ⬜ |

## 关键思想

**必须原地标记+回溯恢复！** 网格搜索不能用额外 visited 数组，直接修改 board 值，回溯时恢复。
