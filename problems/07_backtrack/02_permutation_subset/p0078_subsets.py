#!/usr/bin/env python3
"""
LC 78. 子集
https://leetcode.com/problems/subsets/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你一个整数数组 nums（元素互不相同），返回该数组所有可能的子集（幂集）。

示例:
  输入: [1,2,3]
  输出: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Tags: 数组 | 回溯 | 位运算
"""

import unittest


def subsets(nums: list[int]) -> list[list[int]]:
    """
    思路拆解：

    回溯（DFS）：
    - 每一层决定是否选当前元素
    - 每次递归时都将当前 path 加入结果（不像组合，每个节点都是合法子集）
    - 从 start 开始，避免重复
    """
    # ══════════════════════════════════════════════
    result = []

    def backtrack(start, path):
        result.append(list(path))
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestSubsets(unittest.TestCase):

    def test_basic(self):
        result = subsets([1, 2, 3])
        self.assertEqual(len(result), 8)
        self.assertIn([], result)
        self.assertIn([1, 2, 3], result)
        self.assertIn([1, 2], result)

    def test_empty(self):
        self.assertEqual(subsets([]), [[]])


if __name__ == "__main__":
    unittest.main()
