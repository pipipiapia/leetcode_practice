#!/usr/bin/env python3
"""
LC 64. 最小路径和
https://leetcode.com/problems/minimum-path-sum/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个 m×n 网格，每个格子有非负整数，从左上角到右下角（只能向右或向下）的最小路径和。

示例:
  输入: [[1,3,1],[1,5,1],[4,2,1]]  输出: 7  # 路径 1→3→1→1→1

Tags: 动态规划
"""

import unittest


def min_path_sum(grid: list[list[int]]) -> int:
    """
    思路拆解：

    dp[i][j] = 到达 (i,j) 的最小路径和
    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

    原地修改 grid 即可，不需要额外空间
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMinPathSum(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(min_path_sum([[1,3,1],[1,5,1],[4,2,1]]), 7)

    def test_single(self):
        self.assertEqual(min_path_sum([[5]]), 5)


if __name__ == "__main__":
    unittest.main()
