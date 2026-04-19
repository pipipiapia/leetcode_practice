#!/usr/bin/env python3
"""
LC 121. 买卖股票的最佳时机
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

难度: 简单 | 字节跳动: ★★★★★ | 美团: ★★★★

给定一个数组 prices，其中 prices[i] 是某只股票第 i 天的价格。
你只能完成一笔交易（买入一次，卖出一次）。
返回能获得的最大利润。如果没有利润则返回 0。

示例:
  输入: [7, 1, 5, 3, 6, 4]
  输出: 5
  解释: 在价格为 1 时买入，价格为 6 时卖出，利润最大

Tags: 数组 | 动态规划 | 贪心
"""

import unittest


def max_profit(prices: list[int]) -> int:
    """
    思路拆解：

    方法一：暴力 O(n²) → 跳过
    方法二：一次遍历
      - 记录遍历过的最小价格 min_price
      - 每天的利润 = prices[i] - min_price
      - 更新最大利润 max_profit

    方法三：动态规划（状态机）
      - dp[i][0] = 第 i 天持有现金时的最大利润（不持股）
      - dp[i][1] = 第 i 天持有股票时的最大利润（持股）
      - dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])  # 不动 或 卖出
      - dp[i][1] = max(dp[i-1][1], -prices[i])                # 不动 或 买入

    关键点：为什么买入时是 -prices[i] 而不是 +prices[i]？
            这道题只能交易一次，意味着什么？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案（一次遍历版本，更简洁）
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestBestTimeStock(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(max_profit([7, 1, 5, 3, 6, 4]), 5)

    def test_decline(self):
        self.assertEqual(max_profit([7, 6, 4, 3, 1]), 0)

    def test_single(self):
        self.assertEqual(max_profit([2, 4, 1]), 2)


if __name__ == "__main__":
    unittest.main()
