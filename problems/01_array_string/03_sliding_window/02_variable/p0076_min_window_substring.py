#!/usr/bin/env python3
"""
LC 76: 最小覆盖子串
https://leetcode.com/problems/minimum-window-substring/

难度: 困难 | 字节跳动: ★★★★★ | 快手: ★★★★

给你两个字符串 s 和 t，返回 s 中涵盖 t 所有字符的最小子串。
如果 s 中不存在这样的子串，返回空字符串 ""。

示例:
  输入: s = "ADOBECODEBANC", t = "ABC"
  输出: "BANC"

Tags: 滑动窗口 | 哈希表
"""

import unittest


def min_window(s: str, t: str) -> str:
    """
    思路拆解：

    滑动窗口：
      1. 用 need 字典记录 t 中各字符的需求数量
      2. 用 window 字典记录当前窗口中各字符的数量
      3. valid 记录当前已满足需求的字符种类数
      4. right 扩展窗口 → 满足条件后 left 收缩窗口更新答案

    关键点：valid == len(need) 时代表什么？
            收缩左边界时如何维护 valid？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMinWindow(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(min_window("ADOBECODEBANC", "ABC"), "BANC")

    def test_single(self):
        self.assertEqual(min_window("a", "a"), "a")

    def test_no_match(self):
        self.assertEqual(min_window("a", "b"), "")


if __name__ == "__main__":
    unittest.main()
