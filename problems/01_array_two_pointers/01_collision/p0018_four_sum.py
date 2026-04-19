#!/usr/bin/env python3
"""
LC 18. 四数之和
https://leetcode.com/problems/4sum/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在
四个元素 a, b, c, d，使得 a + b + c + d = target？
找出所有满足条件且不重复的四元组。

示例:
  输入: nums = [1,0,-1,0,-2,2], target = 0
  输出: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]

Tags: 数组 | 双指针 | 对撞指针
"""

import unittest


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    思路拆解：

    三数之和的扩展：固定两个数，剩余用对撞指针
    - 排序
    - 两层循环固定 a, b
    - 双指针找 c + d ≈ target - a - b
    - 去重：跳过相邻相同值
    - 剪枝：若最小可能和 > target 或 最大可能和 < target，跳过
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestFourSum(unittest.TestCase):

    def test_basic(self):
        result = four_sum([1, 0, -1, 0, -2, 2], 0)
        self.assertEqual(sorted(result), sorted([[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]))

    def test_no_duplicates(self):
        result = four_sum([2, 2, 2, 2, 2], 8)
        self.assertEqual(result, [[2, 2, 2, 2]])


if __name__ == "__main__":
    unittest.main()
