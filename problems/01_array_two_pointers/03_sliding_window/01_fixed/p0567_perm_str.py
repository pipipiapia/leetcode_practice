#!/usr/bin/env python3
"""
LC 567. 字符串的排列
https://leetcode.com/problems/permutation-in-string/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★

给你两个字符串 s1 和 s2，若 s2 包含 s1 的任意排列，返回 true；否则返回 false。
换句话说，若 s1 的排列之一是 s2 的子串，则返回 true。

示例:
  输入: s1 = "ab", s2 = "eidbaooo"
  输出: True（因为 "ba" 是 eidbaooo 的子串）

Tags: 字符串 | 滑动窗口 | 固定窗口
"""

import unittest
from collections import Counter

def check_inclusion(s1: str, s2: str) -> bool:
    """
    思路拆解：

    固定窗口大小滑动窗口：
    - 窗口大小 = len(s1)
    - 用字符计数数组（26个字母）比较
    - 维护两个计数：s1 的字符频率 和 当前窗口的字符频率
    - 若窗口计数 == s1 计数，返回 True

    技巧：Python 中用 collections.Counter 便于比较
    用长度为 26 的数组存字符频率，比 Counter 直接比较数组更高效（O(1) 比较）
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    cnt1 = Counter(s1)



# ─────────────────────────────────────────────────
class TestPermStr(unittest.TestCase):

    def test_basic(self):
        self.assertTrue(check_inclusion("ab", "eidbaooo"))

    def test_no_permutation(self):
        self.assertFalse(check_inclusion("ab", "eidboaoo"))

    def test_exact_match(self):
        self.assertTrue(check_inclusion("a", "a"))

    def test_longer(self):
        self.assertTrue(check_inclusion("abc", "ccccbbbbaaaa"))


if __name__ == "__main__":
    unittest.main()
