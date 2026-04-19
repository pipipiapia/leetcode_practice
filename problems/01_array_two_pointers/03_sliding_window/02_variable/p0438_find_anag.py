#!/usr/bin/env python3
"""
LC 438. 找到字符串中所有字母异位词
https://leetcode.com/problems/find-all-anagrams-in-a-string/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★

给定两个字符串 s 和 p，找到 s 中所有 p 的异位词（字母排列）起始索引。
返回这些起始索引的列表，顺序无所谓。

异位词：字母相同但排列顺序不同的字符串。

示例:
  输入: s = "cbaebabacd", p = "abc"
  输出: [0, 6]（"cba" 和 "bac"）

Tags: 字符串 | 滑动窗口 | 可变窗口
"""

import unittest


def find_anagrams(s: str, p: str) -> list[int]:
    """
    思路拆解：

    固定窗口大小滑动窗口：
    - 窗口大小 = len(p)
    - 用字符计数数组比较窗口和 p 的字符频率是否一致
    - 若一致则记录起始位置
    - 窗口向右滑动一位，同时更新计数

    Python 技巧：用 Counter 或数组比较
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestFindAnagrams(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(sorted(find_anagrams("cbaebabacd", "abc")), [0, 6])

    def test_no_anagram(self):
        self.assertEqual(find_anagrams("hello", "xyz"), [])

    def test_overlap(self):
        self.assertEqual(sorted(find_anagrams("abab", "ab")), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
