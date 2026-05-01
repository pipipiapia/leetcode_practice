#!/usr/bin/env python3
"""
LC 53. 最大子数组和
https://leetcode.com/problems/maximum-subarray/

难度: 中等 | 字节跳动: ★★★★★ | 快手: ★★★★

给定一个整数数组 nums，找到一个具有最大和的连续子数组（子数组最少包含一个元素），
返回其最大和。

示例:
  输入: nums = [-2,1,-3,4,-1,2,1,-5,4]
  输出: 6
  解释: 连续子数组 [4,-1,2,1] 的和最大，为 6

Tags: 数组 | 动态规划 | 分治
"""

import unittest


def max_subarray(nums: list[int]) -> int:
    """
    思路拆解：

    方法一：贪心（Kadane 算法）
      - 遍历数组，累加当前和
      - 如果当前和变成负数，直接扔掉，从下一个位置重新开始
      - 每步记录最大值

      为什么扔掉？当前和为负 → 无论如何继续加只会让后面的和更小

    方法二：动态规划
      - dp[i] = 以 nums[i] 结尾的最大子序和
      - dp[i] = max(nums[i], dp[i-1] + nums[i])
      - 取所有 dp 的最大值

    关键点：为什么 dp[i] 有两种可能，不能直接选大的？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMaxSubarray(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_single(self):
        self.assertEqual(max_subarray([1]), 1)

    def test_all_negative(self):
        self.assertEqual(max_subarray([-1, -2, -3]), -1)

    def test_positive(self):
        self.assertEqual(max_subarray([1, 2, 3, 4]), 10)


if __name__ == "__main__":
    unittest.main()
