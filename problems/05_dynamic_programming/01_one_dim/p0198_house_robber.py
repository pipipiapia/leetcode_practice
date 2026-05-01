#!/usr/bin/env python3
"""
LC 198. 打家劫舍
https://leetcode.com/problems/house-robber/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

每间房屋存有一定金额，相邻房屋不能同时被盗。求能偷到的最大金额。

示例:
  输入: [1,2,3,1]   输出: 4  # 偷第1、3间
  输入: [2,7,9,3,1] 输出: 12 # 偷第1、3、5间

Tags: 动态规划
"""

import unittest


def rob(nums: list[int]) -> int:
    """
    思路拆解：

    dp[i] = 前 i 间房能偷到的最大值
    dp[i] = max(dp[i-1],          # 不偷第 i 间
                dp[i-2] + nums[i]) # 偷第 i 间

    空间优化：只需维护 prev2 和 prev1 两个变量
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestRob(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(rob([1, 2, 3, 1]), 4)

    def test_basic2(self):
        self.assertEqual(rob([2, 7, 9, 3, 1]), 12)

    def test_single(self):
        self.assertEqual(rob([5]), 5)


if __name__ == "__main__":
    unittest.main()
