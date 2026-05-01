#!/usr/bin/env python3
"""
LC 242. 有效的字母异位词
https://leetcode.com/problems/valid-anagram/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定两个字符串 s 和 t，编写一个函数来判断 t 是否是 s 的字母异位词
（两个字符串所含字母完全相同，顺序不同）。

示例:
  输入: s = "anagram", t = "nagaram"  输出: True
  输入: s = "rat", t = "car"          输出: False

Tags: 哈希表 | 字符串 | 排序
"""

import unittest
from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    """
    思路拆解：

    方法一：排序后比较 O(n log n)
    方法二：哈希表统计字符频次 O(n)
      - 统计 s 中每个字符出现次数
      - 遍历 t，每个字符计数 -1，若某字符变负 → False
    """
    # ══════════════════════════════════════════════
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestIsAnagram(unittest.TestCase):

    def test_true(self):
        self.assertTrue(is_anagram("anagram", "nagaram"))

    def test_false(self):
        self.assertFalse(is_anagram("rat", "car"))

    def test_diff_len(self):
        self.assertFalse(is_anagram("ab", "a"))


if __name__ == "__main__":
    unittest.main()
