#!/usr/bin/env python3
"""
LC 34. 在排序数组中查找元素的第一个和最后一个位置
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。
找出 target 在数组中的开始位置和结束位置，不存在返回 [-1, -1]。要求 O(log n)。

示例:
  输入: nums=[5,7,7,8,8,10], target=8  输出: [3, 4]
  输入: nums=[5,7,7,8,8,10], target=6  输出: [-1, -1]

Tags: 数组 | 二分查找
"""

import unittest


def search_range(nums: list[int], target: int) -> list[int]:
    """
    思路拆解：

    两次二分：分别找左边界和右边界

    找左边界：找第一个 >= target 的位置
      - nums[mid] >= target → right = mid - 1（继续往左找）
      - nums[mid] < target  → left = mid + 1

    找右边界：找最后一个 <= target 的位置
      - nums[mid] <= target → left = mid + 1（继续往右找）
      - nums[mid] > target  → right = mid - 1
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestSearchRange(unittest.TestCase):

    def test_found(self):
        self.assertEqual(search_range([5, 7, 7, 8, 8, 10], 8), [3, 4])

    def test_not_found(self):
        self.assertEqual(search_range([5, 7, 7, 8, 8, 10], 6), [-1, -1])

    def test_empty(self):
        self.assertEqual(search_range([], 0), [-1, -1])

    def test_single_match(self):
        self.assertEqual(search_range([1], 1), [0, 0])


if __name__ == "__main__":
    unittest.main()
