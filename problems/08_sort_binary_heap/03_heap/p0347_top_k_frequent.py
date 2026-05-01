#!/usr/bin/env python3
"""
LC 347. 前 K 个高频元素
https://leetcode.com/problems/top-k-frequent-elements/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你一个整数数组 nums 和一个整数 k，返回出现频率前 k 高的元素。

示例:
  输入: nums=[1,1,1,2,2,3], k=2  输出: [1,2]
  输入: nums=[1], k=1             输出: [1]

要求：时间复杂度优于 O(n log n)

Tags: 哈希表 | 堆 | 桶排序
"""

import unittest
from collections import Counter
import heapq


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    思路拆解：

    方法一（最小堆，O(n log k)）：
    - 统计频次
    - 维护大小为 k 的最小堆
    - 遍历频次，若堆满且当前频次 > 堆顶 → 替换

    方法二（桶排序，O(n)）：
    - 频次范围 [1, n]，建 n+1 个桶
    - 倒序遍历桶，取前 k 个

    这里用方法一（更通用，面试常考）
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestTopKFrequent(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(sorted(top_k_frequent([1,1,1,2,2,3], 2)), [1, 2])

    def test_single(self):
        self.assertEqual(top_k_frequent([1], 1), [1])

    def test_all_same(self):
        self.assertEqual(top_k_frequent([1,1,2,2,3,3], 3), [1,2,3] or
                         sorted(top_k_frequent([1,1,2,2,3,3], 3)) == [1,2,3])


if __name__ == "__main__":
    unittest.main()
