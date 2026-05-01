#!/usr/bin/env python3
"""
LC 28. 找出字符串中第一个匹配项的下标
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/

难度: 简单/中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你两个字符串 haystack 和 needle，在 haystack 中找出 needle 第一次出现的下标，
不存在返回 -1。

示例:
  输入: haystack="sadbutsad", needle="sad"  输出: 0
  输入: haystack="leetcode",  needle="leeto" 输出: -1

Tags: 字符串 | KMP | 双指针
"""

import unittest


def str_str(haystack: str, needle: str) -> int:
    """
    思路拆解：

    方法一：暴力 O(m*n) — 面试也接受
    方法二：KMP O(m+n) — 进阶，面试加分

    KMP 核心：构建 next 数组（部分匹配表），失配时不从头匹配，
    利用已匹配的前缀信息跳跃，避免重复比较。

    这里实现 KMP，但面试中能清晰讲出思路即可，暴力也不扣分。
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestStrStr(unittest.TestCase):

    def test_found(self):
        self.assertEqual(str_str("sadbutsad", "sad"), 0)

    def test_not_found(self):
        self.assertEqual(str_str("leetcode", "leeto"), -1)

    def test_empty_needle(self):
        self.assertEqual(str_str("hello", ""), 0)

    def test_at_end(self):
        self.assertEqual(str_str("hello", "lo"), 3)


if __name__ == "__main__":
    unittest.main()
