#!/usr/bin/env python3
"""
LC 56. 合并区间
https://leetcode.com/problems/merge-intervals/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给出一个区间的集合，合并所有重叠的区间。

示例:
  输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
  输出: [[1,6],[8,10],[15,18]]
  解释: [1,3] 和 [2,6] 重叠，合并为 [1,6]

  输入: intervals = [[1,4],[4,5]]
  输出: [[1,5]]  # 端点相接也合并

Tags: 数组 | 排序 | 区间
"""

import unittest


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    思路拆解：

    1. 按区间起点排序（若起点相同则按终点）
    2. 遍历，若当前区间起点 <= 上一个合并区间的终点 → 可以合并（取终点最大值）
               否则 → 无重叠，直接加入结果
    """
    # ══════════════════════════════════════════════
    intervals.sort()
    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestMerge(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            merge([[1, 3], [2, 6], [8, 10], [15, 18]]),
            [[1, 6], [8, 10], [15, 18]]
        )

    def test_touching(self):
        self.assertEqual(merge([[1, 4], [4, 5]]), [[1, 5]])

    def test_single(self):
        self.assertEqual(merge([[1, 4]]), [[1, 4]])


if __name__ == "__main__":
    unittest.main()
