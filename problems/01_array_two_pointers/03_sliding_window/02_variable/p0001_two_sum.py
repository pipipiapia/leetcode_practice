#!/usr/bin/env python3
"""
LC 1. 两数之和
https://leetcode.com/problems/two-sum/

难度: 简单 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定一个整数数组 nums 和一个整数目标值 target，
请你在该数组中找出和为目标值 target 的两个整数，并返回它们的数组下标。

示例:
  输入: nums = [2, 7, 11, 15], target = 9
  输出: [0, 1]
  解释: nums[0] + nums[1] == 9

进阶: 你能想出一个时间复杂度小于 O(n²) 的算法吗？

Tags: 数组 | 哈希表
"""

import unittest


def two_sum(nums: list[int], target: int) -> list[int]:
    """
    思路拆解：

    1. 暴力的 O(n²) 解法：双重循环枚举所有数对 → 跳过
    2. 哈希表：遍历时把 (值, 下标) 存起来，查「target - 当前值」是否在表中
       - 时间: O(n)  空间: O(n)

    关键点：为什么要查「target - nums[i]」？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestTwoSum(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_same_values(self):
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])

    def test_negative(self):
        self.assertEqual(two_sum([-1, -2, -3, -4, -5], -8), [2, 4])


if __name__ == "__main__":
    unittest.main()
