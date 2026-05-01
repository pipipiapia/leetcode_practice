#!/usr/bin/env python3
"""
LC 208. 实现 Trie（前缀树）
https://leetcode.com/problems/implement-trie-prefix-tree/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

实现一个 Trie 类，支持：
- insert(word)：插入字符串
- search(word)：搜索完整字符串，存在返回 True
- startsWith(prefix)：搜索前缀，有任意单词以此前缀开头返回 True

示例:
  trie = Trie()
  trie.insert("apple")
  trie.search("apple")    → True
  trie.search("app")      → False
  trie.startsWith("app")  → True

Tags: 字符串 | 设计 | Trie
"""

import unittest


class Trie:
    """
    思路拆解：

    每个节点包含：
    - children：字典，key 是字符，value 是子节点
    - is_end：标记该节点是否是某个单词的结尾

    insert：逐字符遍历，不存在则创建节点，最后标记 is_end
    search：逐字符遍历，找不到返回 False，找到后检查 is_end
    startsWith：与 search 类似，但不检查 is_end
    """

    def __init__(self):
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestTrie(unittest.TestCase):

    def test_basic(self):
        trie = Trie()
        trie.insert("apple")
        self.assertTrue(trie.search("apple"))
        self.assertFalse(trie.search("app"))
        self.assertTrue(trie.startsWith("app"))
        trie.insert("app")
        self.assertTrue(trie.search("app"))

    def test_not_found(self):
        trie = Trie()
        trie.insert("hello")
        self.assertFalse(trie.search("world"))
        self.assertFalse(trie.startsWith("wor"))


if __name__ == "__main__":
    unittest.main()
