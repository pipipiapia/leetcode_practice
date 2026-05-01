#!/usr/bin/env python3
"""
LC 125. 验证回文串
https://leetcode.com/problems/valid-palindrome/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后，
字符串正着读和反着读都一样，则认为该字符串是一个回文串。

示例:
  输入: "A man, a plan, a canal: Panama"  输出: True
  输入: "race a car"                       输出: False

Tags: 字符串 | 双指针
"""

import unittest


def is_palindrome(s: str) -> bool:
    """
    思路拆解：

    双指针：left 从头，right 从尾，跳过非字母数字字符
    - 若两端字符不同（忽略大小写）→ False
    - 全部匹配 → True
    """
    # ══════════════════════════════════════════════
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1

    return True
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestIsPalindrome(unittest.TestCase):

    def test_true(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))

    def test_false(self):
        self.assertFalse(is_palindrome("race a car"))

    def test_empty(self):
        self.assertTrue(is_palindrome(" "))


if __name__ == "__main__":
    unittest.main()
