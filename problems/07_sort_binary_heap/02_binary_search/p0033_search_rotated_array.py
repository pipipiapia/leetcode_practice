#!/usr/bin/env python3
"""
LC 33. 搜索旋转排序数组
https://leetcode.com/problems/search-in-rotated-sorted-array/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

整数数组 nums 在某个下标处旋转了（如 [4,5,6,7,0,1,2]），搜索目标值 target。
存在返回下标，不存在返回 -1。要求 O(log n)。

示例:
  输入: nums=[4,5,6,7,0,1,2], target=0  输出: 4
  输入: nums=[4,5,6,7,0,1,2], target=3  输出: -1

Tags: 数组 | 二分查找
"""

import unittest


def search(nums: list[int], target: int) -> int:
    """
    思路拆解：

    旋转数组中二分的关键：每次确定哪半边是有序的
    - 若 nums[mid] >= nums[left]，左半有序
        - target 在 [nums[left], nums[mid]) → right = mid - 1
        - 否则 left = mid + 1
    - 否则右半有序
        - target 在 (nums[mid], nums[right]] → left = mid + 1
        - 否则 right = mid - 1
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestSearch(unittest.TestCase):

    def test_found(self):
        self.assertEqual(search([4, 5, 6, 7, 0, 1, 2], 0), 4)

    def test_not_found(self):
        self.assertEqual(search([4, 5, 6, 7, 0, 1, 2], 3), -1)

    def test_single(self):
        self.assertEqual(search([1], 0), -1)


if __name__ == "__main__":
    unittest.main()
