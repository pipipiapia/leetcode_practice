#!/usr/bin/env python3
"""
LC 303. 区域和检索 - 数组不可变
https://leetcode.com/problems/range-sum-query-immutable/

难度: 简单 | 字节跳动: ★★★ | 腾讯: ★★★

给定一个整数数组 nums，求索引 left 到 right（含两端）之间的元素和。
sumRange(left, right) 将被多次调用，要求每次 O(1)。

示例:
  nums = [-2, 0, 3, -5, 2, -1]
  sumRange(0, 2) -> 1   # -2+0+3
  sumRange(2, 5) -> -1  # 3-5+2-1
  sumRange(0, 5) -> -3  # 全部

核心思想（前缀和模板）:
  prefix[i] = nums[0] + nums[1] + ... + nums[i-1]  （前 i 个元素的和）
  sumRange(l, r) = prefix[r+1] - prefix[l]

Tags: 数组 | 前缀和 | 设计
"""

import unittest


class NumArray:
    """
    思路拆解：

    预处理 O(n)：构建前缀和数组 prefix，prefix[i] 表示 nums[0..i-1] 的和
    查询 O(1)：sumRange(l, r) = prefix[r+1] - prefix[l]

    为什么从 prefix[1] 开始存？
      prefix[0] = 0（哨兵，简化边界处理）
      prefix[i] = prefix[i-1] + nums[i-1]
    """

    def __init__(self, nums: list[int]):
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestNumArray(unittest.TestCase):

    def setUp(self):
        self.obj = NumArray([-2, 0, 3, -5, 2, -1])

    def test_sum_middle(self):
        self.assertEqual(self.obj.sumRange(0, 2), 1)

    def test_sum_end(self):
        self.assertEqual(self.obj.sumRange(2, 5), -1)

    def test_sum_all(self):
        self.assertEqual(self.obj.sumRange(0, 5), -3)


if __name__ == "__main__":
    unittest.main()
