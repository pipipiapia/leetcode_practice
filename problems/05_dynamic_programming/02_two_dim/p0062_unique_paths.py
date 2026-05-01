#!/usr/bin/env python3
"""
LC 62. 不同路径
https://leetcode.com/problems/unique-paths/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

一个机器人从 m×n 网格左上角出发，每次只能向右或向下移动，到达右下角有多少条不同路径？

示例:
  输入: m=3, n=7  输出: 28
  输入: m=3, n=2  输出: 3

Tags: 动态规划 | 数学
"""

import unittest


def unique_paths(m: int, n: int) -> int:
    """
    思路拆解：

    dp[i][j] = 到达 (i,j) 的路径数 = dp[i-1][j] + dp[i][j-1]
    初始化：第一行和第一列全为 1（只能一路向右/向下）

    空间优化：只需一维数组滚动更新
    """
    # ══════════════════════════════════════════════
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestUniquePaths(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(unique_paths(3, 7), 28)

    def test_small(self):
        self.assertEqual(unique_paths(3, 2), 3)

    def test_one_row(self):
        self.assertEqual(unique_paths(1, 5), 1)


if __name__ == "__main__":
    unittest.main()
