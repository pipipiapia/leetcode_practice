#!/usr/bin/env python3
"""
LC 26. 删除有序数组中的重复项
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

难度: 简单 | 字节跳动: ★★★ | 快手: ★★★

给定一个升序数组 nums，原地删除重复出现的元素，使每个元素只出现一次，
返回删除后数组的新长度。
不要使用额外的数组空间，必须原地修改输入数组。

示例:
  输入: nums = [1,1,2]
  输出: 2，nums 前两位应为 [1,2]

Tags: 数组 | 双指针 | 快慢指针
"""

import unittest


def remove_duplicates(nums: list[int]) -> int:
    """
    思路拆解：

    快慢指针：
    - slow 指向已处理区间的最后一个有效元素
    - fast 扫描整个数组
    - 若 nums[fast] != nums[slow]，说明遇到新值，slow++ 并更新 nums[slow]
    - 最终 slow+1 即为新长度
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestRemoveDup(unittest.TestCase):

    def test_basic(self):
        nums = [1, 1, 2]
        self.assertEqual(remove_duplicates(nums), 2)
        self.assertEqual(nums[:2], [1, 2])

    def test_no_duplicates(self):
        nums = [1, 2, 3]
        self.assertEqual(remove_duplicates(nums), 3)
        self.assertEqual(nums, [1, 2, 3])

    def test_all_same(self):
        nums = [1, 1, 1, 1]
        self.assertEqual(remove_duplicates(nums), 1)
        self.assertEqual(nums[0], 1)


if __name__ == "__main__":
    unittest.main()
