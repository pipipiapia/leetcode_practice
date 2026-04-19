#!/usr/bin/env python3
"""
LC 643. 子数组最大平均数 I
https://leetcode.com/problems/maximum-average-subarray-i/

难度: 简单 | 字节跳动: ★★★ | 快手: ★★★

给定一个整数数组 nums，找长度为 k 的连续子数组的最大平均值。
返回这个最大平均值。

示例:
  输入: nums = [1,12,-5,-6,50,3], k = 4
  输出: 12.75
  解释: 最大平均子数组是 (12-5-6+50)/4 = 51/4 = 12.75

Tags: 数组 | 滑动窗口 | 固定窗口
"""

import unittest


def find_max_average(nums: list[int], k: int) -> float:
    """
    思路拆解：

    固定窗口大小滑动窗口：
    - 先计算第一个窗口的和作为初始值
    - 窗口向右滑动：加右边新值，减左边旧值
    - 维护最大窗口和
    - 平均值 = 最大和 / k

    时间 O(n)，空间 O(1)
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestMaxAverage(unittest.TestCase):

    def test_basic(self):
        self.assertAlmostEqual(find_max_average([1, 12, -5, -6, 50, 3], 4), 12.75, places=5)

    def test_single(self):
        self.assertAlmostEqual(find_max_average([5], 1), 5.0, places=5)

    def test_negative(self):
        self.assertAlmostEqual(find_max_average([-1], 1), -1.0, places=5)


if __name__ == "__main__":
    unittest.main()
