#!/usr/bin/env python3
"""
LC 215: 数组中的第 K 个最大元素
https://leetcode.com/problems/kth-largest-element-in-an-array/

难度: 中等 | 字节跳动: ★★★★★ | 百度: ★★★★

给定整数数组 nums 和整数 k，返回数组中第 k 大的元素。
注意：需要找的是第 k 大的元素，不是第 k 个最大的不同元素。

示例:
  输入: [3,2,1,5,6,4], k = 2
  输出: 5

进阶：你能设计一个 O(n) 时间复杂度的算法吗？

Tags: 数组 | 堆 | 快速选择 | 排序
"""

import unittest


def find_kth_largest(nums: list[int], k: int) -> int:
    """
    思路拆解：

    方法一：最小堆 O(n log k) ← 推荐
      - 维持一个大小为 k 的最小堆
      - 堆顶是 k 个最大数中的最小值（即第 k 大）
      - 遍历剩余数字，比堆顶大就替换

    方法二：快速选择 O(n) 平均
      - 把问题转成"找第 target 小的数"
      - target = len(nums) - k
      - 分区操作找到 pivot 的正确位置，递归逼近

    方法三：排序 O(n log n) ← 跳过

    堆排序来解决这个问题——建立一个大根堆，做 k−1 次删除操作后堆顶元素就是我们要找的答案。

    关键点：为什么最小堆的堆顶就是第 k 大？
            快选里 target = len - k 怎么来的？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestKthLargest(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(find_kth_largest([3, 2, 1, 5, 6, 4], 2), 5)

    def test_with_duplicates(self):
        self.assertEqual(find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)

    def test_single(self):
        self.assertEqual(find_kth_largest([1], 1), 1)


if __name__ == "__main__":
    unittest.main()
