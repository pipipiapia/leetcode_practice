#!/usr/bin/env python3
"""
LC 1143: 最长公共子序列（LCS）
https://leetcode.com/problems/longest-common-subsequence/

难度: 中等 | 字节跳动: ★★★★ | 阿里: ★★★

给定两个字符串 text1 和 text2，返回它们的最长公共子序列的长度。
子序列：不要求连续，但必须保持相对顺序。

示例:
  输入: text1 = "abcde", text2 = "ace"
  输出: 3
  解释: 最长公共子序列是 "ace"

进阶：你能将算法的时间复杂度降低到 O(min(m, n)) 吗？

Tags: 字符串 | 动态规划
"""

import unittest


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    思路拆解：

    dp[i][j] = text1[:i] 和 text2[:j] 的 LCS 长度

    转移方程：
      - 若 text1[i-1] == text2[j-1]：末尾相同 → dp[i][j] = dp[i-1][j-1] + 1
      - 否则：末尾不同 → dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    Base case:
      - dp[0][j] = 0（空串和任意串的 LCS 为 0）
      - dp[i][0] = 0

    空间优化：只需要一维数组 + prev 变量保存 dp[i-1][j-1]

    关键点：为什么"末尾不同"时是 max(左, 上) 而不是左上+0？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    len1, len2 = len(text1), len(text2)
    dp = [[0]*(len2+1) for _ in range(len1+1)] ####行数 = len1+1，列数 = len2+1!!!写反犯错！！！
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            # print(i, j)
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    # print(dp)
    return dp[len1][len2]


# ─────────────────────────────────────────────────
class TestLCS(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)

    def test_same(self):
        self.assertEqual(longest_common_subsequence("abc", "abc"), 3)

    def test_no_common(self):
        self.assertEqual(longest_common_subsequence("abc", "def"), 0)

    def test_empty(self):
        self.assertEqual(longest_common_subsequence("", "abc"), 0)


if __name__ == "__main__":
    unittest.main()
