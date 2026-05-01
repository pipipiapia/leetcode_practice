#!/usr/bin/env python3
"""
LC 27. 移除元素
https://leetcode.com/problems/remove-element/

难度: 简单 | 字节跳动: ★★★ | 腾讯: ★★★

给你一个数组 nums 和一个值 val，原地移除所有数值等于 val 的元素，
返回新的长度。元素的顺序可以改变。
不要使用额外的数组空间，必须原地修改。

示例:
  输入: nums = [3,2,2,3], val = 3
  输出: 2，nums 前两位为 [2,2]

Tags: 数组 | 双指针 | 快慢指针
"""

import unittest


def remove_element(nums: list[int], val: int) -> int:
    """
    思路拆解：

    快慢指针变体：
    - slow 指向下一个待填入的位置
    - fast 扫描数组
    - 若 nums[fast] != val，将其移到 nums[slow]，slow++
    - 最终 slow 即为新长度
    """
    # ══════════════════════════════════════════════
    slow, fast = 0, 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
    # ══════════════════════════════════════════════
    


# ─────────────────────────────────────────────────
class TestRemoveElem(unittest.TestCase):

    def test_basic(self):
        nums = [3, 2, 2, 3]
        self.assertEqual(remove_element(nums, 3), 2)
        self.assertEqual(nums[:2], [2, 2])

    def test_no_val(self):
        nums = [1, 2, 3]
        self.assertEqual(remove_element(nums, 5), 3)

    def test_all_val(self):
        nums = [3, 3, 3]
        self.assertEqual(remove_element(nums, 3), 0)


if __name__ == "__main__":
    unittest.main()
