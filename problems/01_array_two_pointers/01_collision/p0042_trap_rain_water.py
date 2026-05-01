#!/usr/bin/env python3
"""
LC 42. 接雨水
https://leetcode.com/problems/trapping-rain-water/

难度: 困难 | 字节跳动: ★★★★★ | 快手: ★★★★

给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，
计算按此排列的柱子下雨之后能接多少雨水。

示例:
  输入: height = [0,1,0,2,1,0,1,3,2,1,2,1]
  输出: 6
  解释: 6 个单位的水被接住（蓝色部分）

Tags: 数组 | 双指针 | 动态规划 | 单调栈
"""

import unittest


def trap(height: list[int]) -> int:
    """
    思路拆解：

    方法一：暴力 O(n²) → 超时，仅理解思路用

    方法二：动态规划 O(n)
      - left_max[i] = height[0..i] 中的最大值
      - right_max[i] = height[i..n-1] 中的最大值
      - 每根柱子能接的水 = min(left_max[i], right_max[i]) - height[i]

    方法三：双指针 O(n) ← 最优
      - left = 0, right = n-1, left_max = 0, right_max = 0
      - 移动较小指针那边，计算水量
      - 为什么这样可行？

    关键点：为什么移动较小边而不是较大边？直觉是什么？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestTrap(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)

    def test_no_water(self):
        self.assertEqual(trap([4, 2, 0, 3, 2, 5]), 9)

    def test_single_element(self):
        self.assertEqual(trap([0]), 0)


if __name__ == "__main__":
    unittest.main()
