#!/usr/bin/env python3
"""
LC 169. 多数元素（摩尔投票）
https://leetcode.com/problems/majority-element/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个大小为 n 的数组 nums，找出其中的多数元素（出现次数 > n/2 的元素）。
保证多数元素一定存在。要求时间 O(n)，空间 O(1)。

示例:
  输入: [3, 2, 3]       输出: 3
  输入: [2, 2, 1, 1, 1, 2, 2]  输出: 2

Tags: 数组 | 摩尔投票 | 分治
"""

import unittest


def majority_element(nums: list[int]) -> int:
    """
    思路拆解：

    摩尔投票法（Boyer-Moore Voting）：
    - 假设当前候选者是 candidate，票数为 count
    - 遍历数组：
        若 count == 0，更换候选者
        若当前元素 == candidate，count += 1
        否则 count -= 1
    - 最终候选者就是多数元素（因为多数元素 > n/2，"消耗"不完）

    直觉：相同的票互相抵消，最后剩下的一定是多数元素
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMajorityElement(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(majority_element([3, 2, 3]), 3)

    def test_longer(self):
        self.assertEqual(majority_element([2, 2, 1, 1, 1, 2, 2]), 2)

    def test_single(self):
        self.assertEqual(majority_element([1]), 1)


if __name__ == "__main__":
    unittest.main()
