#!/usr/bin/env python3
"""
LC 70. 爬楼梯
https://leetcode.com/problems/climbing-stairs/

难度: 简单 | 字节跳动: ★★★★★ | 快手: ★★★★

假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
每次你可以爬 1 或 2 个台阶。有多少种不同的方法可以爬到楼顶？

示例:
  输入: n = 3
  输出: 3
  解释: 有三种方法可以爬到楼顶:
       1. 1阶 + 1阶 + 1阶
       2. 1阶 + 2阶
       3. 2阶 + 1阶

Tags: 动态规划 | 记忆化 | 递归
"""

import unittest


def climb_stairs(n: int) -> int:
    """
    思路拆解：

    状态定义:
      dp[i] = 爬到第 i 阶的方法数

    转移方程:
      到达第 i 阶，只能从 i-1 爬1步，或从 i-2 爬2步
      dp[i] = dp[i-1] + dp[i-2]

    初始条件:
      dp[1] = 1,  dp[2] = 2

    优化: 只需要两个变量，不需要整个数组

    关键点：这其实就是斐波那契数列，但初始值不同。为什么？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestClimbStairs(unittest.TestCase):

    def test_n1(self):
        self.assertEqual(climb_stairs(1), 1)

    def test_n2(self):
        self.assertEqual(climb_stairs(2), 2)

    def test_n3(self):
        self.assertEqual(climb_stairs(3), 3)

    def test_n5(self):
        self.assertEqual(climb_stairs(5), 8)


if __name__ == "__main__":
    unittest.main()
