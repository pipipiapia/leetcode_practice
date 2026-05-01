#!/usr/bin/env python3
"""
LC 122. 买卖股票的最佳时机 II
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你一个整数数组 prices，可以多次买卖（持有时最多只有一支股票）。
返回能获得的最大利润。

示例:
  输入: [7,1,5,3,6,4]  输出: 7  # (5-1) + (6-3) = 4 + 3
  输入: [1,2,3,4,5]    输出: 4  # (5-1)
  输入: [7,6,4,3,1]    输出: 0  # 不交易

Tags: 数组 | 贪心 | 动态规划
"""

import unittest


def max_profit(prices: list[int]) -> int:
    """
    思路拆解：

    贪心：只要明天比今天涨，就今天买明天卖（把所有上升段利润累加）
    等价于：profit = sum(max(prices[i]-prices[i-1], 0) for i in range(1, n))

    本质：每段连续上涨都完整捕获
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMaxProfit(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(max_profit([7, 1, 5, 3, 6, 4]), 7)

    def test_increasing(self):
        self.assertEqual(max_profit([1, 2, 3, 4, 5]), 4)

    def test_decreasing(self):
        self.assertEqual(max_profit([7, 6, 4, 3, 1]), 0)


if __name__ == "__main__":
    unittest.main()
