#!/usr/bin/env python3
"""
LC 72: 编辑距离
https://leetcode.com/problems/edit-distance/

难度: 困难 | 字节跳动: ★★★★ | 阿里: ★★★★

给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数。
你可以对一个单词进行以下三种操作：
  1. 插入一个字符
  2. 删除一个字符
  3. 替换一个字符

示例:
  输入: word1 = "horse", word2 = "ros"
  输出: 3
  解释: horse → rorse → rose → ros（替换→删除→插入）

Tags: 字符串 | 动态规划
"""

import unittest


def min_distance(word1: str, word2: str) -> int:
    """
    思路拆解：

    dp[i][j] = word1[:i] 转换成 word2[:j] 的最少操作数

    转移方程：
      - 若 word1[i-1] == word2[j-1]：直接继承，dp[i][j] = dp[i-1][j-1]
      - 否则：dp[i][j] = min(
              dp[i-1][j]   + 1,    # 删除 word1[i-1]
              dp[i][j-1]   + 1,    # 插入 word2[j-1]
              dp[i-1][j-1] + 1     # 替换 word1[i-1] 为 word2[j-1]
            )

    Base case:
      - dp[0][j] = j（空串变成长度j的串，需要j次插入）
      - dp[i][0] = i（长度i的串变成空串，需要i次删除）

    关键点：为什么 dp[i-1][j] 对应"删除"操作？画图理解。
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestEditDistance(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(min_distance("horse", "ros"), 3)

    def test_intention(self):
        self.assertEqual(min_distance("intention", "execution"), 5)

    def test_same(self):
        self.assertEqual(min_distance("abc", "abc"), 0)

    def test_empty(self):
        self.assertEqual(min_distance("", "abc"), 3)


if __name__ == "__main__":
    unittest.main()
