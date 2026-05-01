#!/usr/bin/env python3
"""
LC 5. 最长回文子串
https://leetcode.com/problems/longest-palindromic-substring/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你一个字符串 s，找到 s 中最长的回文子串。

示例:
  输入: "babad"   输出: "bab"（"aba" 也可以）
  输入: "cbbd"    输出: "bb"

Tags: 字符串 | 动态规划 | 中心扩展
"""

import unittest


def longest_palindrome(s: str) -> str:
    """
    思路拆解：

    中心扩展法 O(n²)：
    - 回文串有两种形式：奇数长度（中心是单字符）、偶数长度（中心是两字符）
    - 对每个位置，分别尝试以 s[i] 和 s[i]/s[i+1] 为中心向两端扩展
    - 记录最长的回文串

    比 DP O(n²) 空间更优（O(1) 空间），面试推荐此方法
    """
    # ══════════════════════════════════════════════
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestLongestPalindrome(unittest.TestCase):

    def test_odd(self):
        result = longest_palindrome("babad")
        self.assertIn(result, ["bab", "aba"])

    def test_even(self):
        self.assertEqual(longest_palindrome("cbbd"), "bb")

    def test_single(self):
        self.assertEqual(longest_palindrome("a"), "a")

    def test_all_same(self):
        self.assertEqual(longest_palindrome("aaaa"), "aaaa")


if __name__ == "__main__":
    unittest.main()
