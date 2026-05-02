#!/usr/bin/env python3
"""
LC 75. 颜色分类（荷兰国旗问题）
https://leetcode.com/problems/sort-colors/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个包含红色、白色和蓝色（用 0、1、2 表示）的数组 nums，
原地对它们排序，使相同颜色的元素相邻（按 0、1、2 顺序）。
要求一次扫描，O(1) 空间。

示例:
  输入: [2,0,2,1,1,0]  输出: [0,0,1,1,2,2]

Tags: 数组 | 双指针 | 排序
"""

import unittest


def sort_colors(nums: list[int]) -> None:
    """
    思路拆解：

    三指针（荷兰国旗）：
    - low：0 区的右边界（low 左边全是 0）
    - mid：当前处理指针
    - high：2 区的左边界（high 右边全是 2）

    遍历 mid：
    - nums[mid] == 0 → 与 low 交换，low++, mid++
    - nums[mid] == 1 → mid++
    - nums[mid] == 2 → 与 high 交换，high--（mid 不动，因为交换来的未处理）
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestSortColors(unittest.TestCase):

    def test_basic(self):
        nums = [2, 0, 2, 1, 1, 0]
        sort_colors(nums)
        self.assertEqual(nums, [0, 0, 1, 1, 2, 2])

    def test_single_color(self):
        nums = [2, 2, 2]
        sort_colors(nums)
        self.assertEqual(nums, [2, 2, 2])

    def test_already_sorted(self):
        nums = [0, 1, 2]
        sort_colors(nums)
        self.assertEqual(nums, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
