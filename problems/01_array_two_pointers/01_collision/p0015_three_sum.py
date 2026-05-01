#!/usr/bin/env python3
"""
LC 15: 三数之和
https://leetcode.com/problems/3sum/

难度: 中等 | 字节跳动: ★★★★★ | 百度: ★★★★

给你一个整数数组 nums，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k，
同时满足 nums[i] + nums[j] + nums[k] == 0。
要求返回所有不重复的三元组。

示例:
  输入: nums = [-1, 0, 1, 2, -1, -4]
  输出: [[-1, -1, 2], [-1, 0, 1]]

进阶: 你能想出一个时间复杂度为 O(n²) 的算法吗？

Tags: 数组 | 双指针 | 排序
"""

import unittest


def three_sum(nums: list[int]) -> list[list[int]]:
    """
    思路拆解：

    1. 排序：先对数组排序，方便去重和双指针
    2. 固定一个数 nums[i]，转成找两数之和 = -nums[i]
    3. 双指针：left = i+1，right = len(nums)-1，逼近目标和
    4. 去重：
       - 跳过相邻重复值（nums[i] == nums[i-1]）
       - 找到目标后同时跳过 left/right 重复

    关键点：为什么要先排序？去重的逻辑是什么？
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestThreeSum(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(sorted(three_sum([-1, 0, 1, 2, -1, -4])),
                         sorted([[-1, -1, 2], [-1, 0, 1]]))

    def test_no_solution(self):
        self.assertEqual(three_sum([1, 2, 3]), [])

    def test_zeros(self):
        self.assertEqual(three_sum([0, 0, 0]), [[0, 0, 0]])


if __name__ == "__main__":
    unittest.main()
