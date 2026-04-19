#!/usr/bin/env python3
"""
LC 322. 零钱兑换
https://leetcode.com/problems/coin-change/

难度: 中等 | 字节跳动: ★★★★ | 快手: ★★★

给定不同面额的硬币 coins 和一个总金额 amount。
计算凑成总金额所需的最少硬币个数。如果无法凑成，返回 -1。
每种硬币的数量无限使用。

示例:
  输入: coins = [1, 2, 5], amount = 11
  输出: 3
  解释: 11 = 5 + 5 + 1

Tags: 动态规划 | 广度优先搜索
"""

import unittest


def coin_change(coins: list[int], amount: int) -> int:
    """
    思路拆解：

    完全背包问题（每种硬币可用无限次）

    状态定义:
      dp[i] = 凑成金额 i 所需的最少硬币数

    转移方程:
      对于每种硬币 coin: dp[i] = min(dp[i], dp[i - coin] + 1)
      （用一枚 coin 后，剩余 i-coin 所需的最少硬币数 + 1）

    初始条件:
      dp[0] = 0（凑成0元需要0枚硬币）
      dp[其他] = inf（初始为无穷大，表示未凑成）

    遍历顺序:
      金额从小到大遍历（因为硬币可重复使用）

    关键点：为什么 dp 数组要初始化为 inf？dp[0] = 0 的含义？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    dp = [float('inf')]* (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if i-coin >= 0:
              dp[i] = min(dp[i-coin]+1, dp[i])

    if dp[amount] != float('inf'):
      return dp[amount]
    else:
      return -1



# ─────────────────────────────────────────────────
class TestCoinChange(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(coin_change([1, 2, 5], 11), 3)

    def test_impossible(self):
        self.assertEqual(coin_change([2], 3), -1)

    def test_zero(self):
        self.assertEqual(coin_change([1], 0), 0)

    def test_large_amount(self):
        self.assertEqual(coin_change([1], 2), 2)


if __name__ == "__main__":
    unittest.main()
