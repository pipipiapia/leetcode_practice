#!/usr/bin/env python3
"""
LC 46: 全排列
https://leetcode.com/problems/permutations/

难度: 中等 | 字节跳动: ★★★★ | 百度: ★★★★

给定一个不含重复数字的数组 nums，返回其所有可能的全排列。

示例:
  输入: nums = [1,2,3]
  输出: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Tags: 回溯 | 排列问题
"""

import unittest


def permute(nums: list[int]) -> list[list[int]]:
    """
    思路拆解：

    回溯（backtracking）：
      - 用 used 数组标记哪些数字已经用过
      - path 记录当前路径
      - 递归枚举每个位置可以选哪个数字
      - 选 → 递归 → 撤销选择（回溯）

    关键点：排列问题和组合/子集问题的区别是什么？
            排列用 used 数组，组合用 start 指针，为什么？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestPermute(unittest.TestCase):

    def test_basic(self):
        result = permute([1, 2, 3])
        self.assertEqual(len(result), 6)

    def test_two_elements(self):
        result = permute([0, 1])
        self.assertEqual(sorted(result), [[0, 1], [1, 0]])

    def test_single(self):
        self.assertEqual(permute([1]), [[1]])


if __name__ == "__main__":
    unittest.main()
