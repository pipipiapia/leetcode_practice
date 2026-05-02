# 08_string_advanced：字符串进阶

> KMP 模式匹配、Trie 前缀树等字符串专用数据结构与算法

## 核心特征

- KMP：利用已匹配信息跳过重复比较，O(m+n)
- Trie：前缀树，支持 O(L) 的前缀查询（L 为字符串长度）

## 解题框架

```python
# KMP - 求 next 数组（最长公共前后缀）
def build_next(pattern):
    n = len(pattern)
    nxt = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt

# Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 28 | 找出字符串中第一个匹配项 | 🟢 Easy | ⬜ |
| 208 | 实现 Trie 前缀树 | 🟡 Medium | ⬜ |

## 关键思想

**KMP 的 next 数组是什么？**
`next[i]` 表示 `pattern[0..i]` 中最长相等前后缀的长度。失配时根据 next 回退，避免从头匹配。

**Trie 比哈希表好在哪？**
哈希表只能精确匹配，Trie 支持前缀匹配（如自动补全）。空间上，公共前缀共享节点，比存完整字符串更省。
