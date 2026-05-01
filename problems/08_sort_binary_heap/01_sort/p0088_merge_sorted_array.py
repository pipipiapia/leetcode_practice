#!/usr/bin/env python3
"""
LC 88. 合并两个有序数组
https://leetcode.com/problems/merge-sorted-array/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你两个按非递减顺序排列的整数数组 nums1 和 nums2，
将 nums2 合并到 nums1 中，使合并后的数组同样按非递减顺序排列。
nums1 长度为 m+n，后 n 个元素为 0（占位）。要求原地操作。

示例:
  输入: nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3
  输出: [1,2,2,3,5,6]

Tags: 数组 | 双指针 | 排序
"""

import unittest


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """
    思路拆解：

    从后往前合并（避免覆盖未处理元素）：
    - 三个指针：p1=m-1（nums1有效末尾），p2=n-1（nums2末尾），p=m+n-1（填充位置）
    - 每次取 nums1[p1] 和 nums2[p2] 中较大值，从后往前填入
    - 若 nums2 还有剩余，直接补到 nums1 前部
    """
    # ══════════════════════════════════════════════
    p1, p2, p = m - 1, n - 1, m + n - 1

    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1

    # nums2 还有剩余（nums1 剩余不用处理，本来就在正确位置）
    nums1[:p2 + 1] = nums2[:p2 + 1]
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestMerge(unittest.TestCase):

    def test_basic(self):
        nums1 = [1, 2, 3, 0, 0, 0]
        merge(nums1, 3, [2, 5, 6], 3)
        self.assertEqual(nums1, [1, 2, 2, 3, 5, 6])

    def test_empty_nums2(self):
        nums1 = [1]
        merge(nums1, 1, [], 0)
        self.assertEqual(nums1, [1])

    def test_empty_nums1(self):
        nums1 = [0]
        merge(nums1, 0, [1], 1)
        self.assertEqual(nums1, [1])


if __name__ == "__main__":
    unittest.main()
