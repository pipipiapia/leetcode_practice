#!/usr/bin/env python3
"""
LC 300. 最长递增子序列
https://leetcode.com/problems/longest-increasing-subsequence/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★

给你一个整数数组 nums，找到其中最长严格递增子序列的长度。
子序列是由数组派生而来的序列，删除（或不删除）一些元素，但不改变其余元素的顺序。

示例:
  输入: nums = [10, 9, 2, 5, 3, 7, 101, 18]
  输出: 4
  解释: 最长递增子序列是 [2, 3, 7, 101] 或 [2, 3, 7, 18]，长度为 4

进阶: 你能将算法的时间复杂度降低到 O(n log n) 吗？

Tags: 数组 | 动态规划 | 二分查找
"""

import unittest


def length_of_lis(nums: list[int]) -> int:
    """
    思路拆解：

    方法一：动态规划 O(n²)
      - dp[i] = 以 nums[i] 结尾的 LIS 长度
      - dp[i] = max(dp[j] + 1) for all j < i and nums[j] < nums[i]
      - 答案 = max(dp)

    方法二：二分查找 O(n log n) ← 进阶要求
      - 维护一个 tails 数组：tails[i] = 长度为 i+1 的递增子序列的最小尾部值
      - 对于每个 num，用二分找到它应该插入的位置
      - 长度即为答案

    关键点：tails 数组为什么是有序的？如何二分？
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestLIS(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_all_decreasing(self):
        self.assertEqual(length_of_lis([3, 2, 1]), 1)

    def test_all_increasing(self):
        self.assertEqual(length_of_lis([1, 2, 3, 4, 5]), 5)


if __name__ == "__main__":
    unittest.main()
