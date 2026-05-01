#!/usr/bin/env python3
"""
LC 283. 移动零
https://leetcode.com/problems/move-zeroes/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个数组 nums，将所有 0 移到末尾，同时保持非零元素的相对顺序。
必须原地操作，不能拷贝额外数组。

示例:
  输入: [0, 1, 0, 3, 12]
  输出: [1, 3, 12, 0, 0]

Tags: 数组 | 双指针 | 原地操作
"""

import unittest


def move_zeroes(nums: list[int]) -> None:
    """
    思路拆解：

    快慢指针：
    - slow 指向下一个非零元素应放置的位置
    - fast 遍历数组，遇到非零元素则放到 slow 位置，slow 前进
    - 最后把 slow 到末尾全部填 0
    """
    # ══════════════════════════════════════════════
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1

    # 剩余位置填 0
    for i in range(slow, len(nums)):
        nums[i] = 0
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestMoveZeroes(unittest.TestCase):

    def test_basic(self):
        nums = [0, 1, 0, 3, 12]
        move_zeroes(nums)
        self.assertEqual(nums, [1, 3, 12, 0, 0])

    def test_all_zeros(self):
        nums = [0, 0, 0]
        move_zeroes(nums)
        self.assertEqual(nums, [0, 0, 0])

    def test_no_zeros(self):
        nums = [1, 2, 3]
        move_zeroes(nums)
        self.assertEqual(nums, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
