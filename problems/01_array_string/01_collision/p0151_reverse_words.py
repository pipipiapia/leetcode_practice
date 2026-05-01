#!/usr/bin/env python3
"""
LC 151. 反转字符串中的单词
https://leetcode.com/problems/reverse-words-in-a-string/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你一个字符串 s，请你反转字符串中单词的顺序。
单词间可能有多余空格，输出结果中单词间只留一个空格，首尾无空格。

示例:
  输入: "the sky is blue"        输出: "blue is sky the"
  输入: "  hello world  "        输出: "world hello"
  输入: "a good   example"       输出: "example good a"

Tags: 字符串 | 双指针
"""

import unittest


def reverse_words(s: str) -> str:
    """
    思路拆解：

    Python 简洁版：split() 自动处理多余空格，reverse 后 join

    进阶（面试考原地操作思路）：
    1. 去除首尾和中间多余空格
    2. 反转整个字符串
    3. 反转每个单词
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestReverseWords(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(reverse_words("the sky is blue"), "blue is sky the")

    def test_extra_spaces(self):
        self.assertEqual(reverse_words("  hello world  "), "world hello")

    def test_middle_spaces(self):
        self.assertEqual(reverse_words("a good   example"), "example good a")


if __name__ == "__main__":
    unittest.main()
