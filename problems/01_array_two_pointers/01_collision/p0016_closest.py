#!/usr/bin/env python3
"""
LC 16. 最接近的三数之和
https://leetcode.com/problems/3sum-closest/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★

给定一个长度为 n 的整数数组 nums 和一个目标值 target，从 nums 中选出三个整数
使它们的和与 target 最接近。返回这三个数的和。

示例:
  输入: nums = [-1,2,1,-4], target = 1
  输出: 2
  解释: -1+2+1=2，与 target 最近

Tags: 数组 | 双指针 | 对撞指针
"""

import unittest


def three_sum_closest(nums: list[int], target: int) -> int:
    """
    思路拆解：

    先排序，固定一个数，再用对撞指针找两数之和 ≈ target - nums[i]
    - 初始化 ans = 前三数之和
    - 对每个 i，双指针逼近，维护最小差值
    - 若 sum == target，直接返回
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestThreeSumClosest(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(three_sum_closest([-1, 2, 1, -4], 1), 2)

    def test_zero(self):
        self.assertEqual(three_sum_closest([0, 0, 0], 1), 0)

    def test_negative(self):
        self.assertEqual(three_sum_closest([-3, -2, 5, -4, 1], 1), -1)


if __name__ == "__main__":
    unittest.main()
