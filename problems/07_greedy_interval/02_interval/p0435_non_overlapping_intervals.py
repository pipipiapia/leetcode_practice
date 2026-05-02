#!/usr/bin/env python3
"""
LC 435. 无重叠区间
https://leetcode.com/problems/non-overlapping-intervals/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个区间的集合，找到需要移除区间的最小数量，使剩余区间互不重叠。

示例:
  输入: [[1,2],[2,3],[3,4],[1,3]]  输出: 1  # 移除 [1,3]
  输入: [[1,2],[1,2],[1,2]]        输出: 2  # 保留一个

Tags: 数组 | 贪心 | 区间调度
"""

import unittest


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    思路拆解：

    等价问题：最多保留多少不重叠区间（贪心经典：活动安排问题）
    - 按区间结束时间排序（早结束的先选，为后面留更多空间）
    - 遍历：若当前区间的起点 >= 上一个选中区间的终点 → 可以选
    - 移除数 = 总数 - 最多保留数

    贪心正确性：总选结束最早的不重叠区间，能最大化保留数量
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestEraseOverlapIntervals(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1)

    def test_all_overlap(self):
        self.assertEqual(erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]), 2)

    def test_no_overlap(self):
        self.assertEqual(erase_overlap_intervals([[1, 2], [2, 3]]), 0)


if __name__ == "__main__":
    unittest.main()
