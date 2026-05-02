#!/usr/bin/env python3
"""
LC 128. 最长连续序列
https://leetcode.com/problems/longest-consecutive-sequence/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定一个未排序的整数数组 nums，找出数字连续的最长序列的长度。
要求 O(n) 时间复杂度。

示例:
  输入: nums = [100, 4, 200, 1, 3, 2]
  输出: 4   # [1, 2, 3, 4]

  输入: nums = [0,3,7,2,5,8,4,6,0,1]
  输出: 9   # [0,1,2,3,4,5,6,7,8]

Tags: 哈希表 | 并查集
"""

import unittest


def longest_consecutive(nums: list[int]) -> int:
    """
    思路拆解：

    O(n) 方法：哈希集合
    - 将所有数字加入 set
    - 遍历：只从序列起点开始扩展（判断 num-1 不在 set 中）
    - 向右一直扩展，记录最大长度

    关键优化：若 num-1 在 set 中，说明当前 num 不是序列起点，跳过，
    这样保证每个序列只从起点遍历一次，总体 O(n)
    """
    # ═══════════════════════════════════════════════
    record = set()
    for i in nums:
        record.add(i)
    ret = 0
    for i in range(len(nums)):
        if (nums[i] -1 ) not in record:
            tmp = nums[i]
            cnt = 0
            while tmp in record:
                cnt += 1
                tmp += 1
            ret = max(cnt, ret)
    return ret
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestLongestConsecutive(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(longest_consecutive([100, 4, 200, 1, 3, 2]), 4)

    def test_longer(self):
        self.assertEqual(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)

    def test_empty(self):
        self.assertEqual(longest_consecutive([]), 0)

    def test_single(self):
        self.assertEqual(longest_consecutive([1]), 1)


if __name__ == "__main__":
    unittest.main()
