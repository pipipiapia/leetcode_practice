#!/usr/bin/env python3
"""
LC 560. 和为 K 的子数组
https://leetcode.com/problems/subarray-sum-equals-k/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你一个整数数组 nums 和一个整数 k，返回子数组之和等于 k 的子数组的个数。

示例:
  输入: nums = [1, 1, 1], k = 2
  输出: 2   # [1,1]（下标0-1）和 [1,1]（下标1-2）

  输入: nums = [1, 2, 3], k = 3
  输出: 2   # [3] 和 [1,2]

前置知识：前缀和
  sum(i, j) = prefix[j+1] - prefix[i]
  找 sum(i,j) == k  ⟺  找 prefix[j+1] - k == prefix[i]
  → 边遍历边用哈希表记录 prefix 出现次数

Tags: 数组 | 前缀和 | 哈希表
"""

import unittest
from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    """
    思路拆解：

    暴力 O(n²)：枚举所有子数组，计算和 → 超时

    前缀和 + 哈希表 O(n)：
    - 遍历时维护当前前缀和 curr
    - 若 curr - k 在哈希表中，说明存在若干个子数组和为 k
    - 哈希表记录每个前缀和出现的次数

    关键：哈希表初始化 {0: 1}，处理从头开始的子数组（prefix=0 时 curr-k==0）
    """
    # ══════════════════════════════════════════════
    count = 0
    curr = 0
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # 前缀和为 0 出现 1 次（空数组）

    for num in nums:
        curr += num
        # 若 curr - k 在哈希表中，说明有 prefix_count[curr-k] 个子数组和为 k
        count += prefix_count[curr - k]
        prefix_count[curr] += 1

    return count
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestSubarraySum(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(subarray_sum([1, 1, 1], 2), 2)

    def test_basic2(self):
        self.assertEqual(subarray_sum([1, 2, 3], 3), 2)

    def test_single(self):
        self.assertEqual(subarray_sum([3], 3), 1)

    def test_negative(self):
        self.assertEqual(subarray_sum([1, -1, 1], 1), 3)


if __name__ == "__main__":
    unittest.main()
