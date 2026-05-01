#!/usr/bin/env python3
"""
LC 49. 字母异位词分组
https://leetcode.com/problems/group-anagrams/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个字符串数组，将字母异位词分组（字母相同但顺序不同的字符串）。

示例:
  输入: strs = ["eat","tea","tan","ate","nat","bat"]
  输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

Tags: 哈希表 | 字符串 | 排序
"""

import unittest
from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    思路拆解：

    关键：互为字母异位词的字符串，排序后相同。
    以排序后的字符串作为哈希表的 key，将原字符串归入同一组。

    时间 O(n * k log k)：n 个字符串，每个长 k，排序 O(k log k)
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestGroupAnagrams(unittest.TestCase):

    def test_basic(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        result_sorted = [sorted(g) for g in result]
        self.assertIn(["ate", "eat", "tea"], result_sorted)
        self.assertIn(["nat", "tan"], result_sorted)
        self.assertIn(["bat"], result_sorted)

    def test_empty_string(self):
        self.assertEqual(group_anagrams([""]), [[""]])

    def test_single_char(self):
        self.assertEqual(group_anagrams(["a"]), [["a"]])


if __name__ == "__main__":
    unittest.main()
