#!/usr/bin/env python3
"""
LC 139. 单词拆分
https://leetcode.com/problems/word-break/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定字符串 s 和字典 wordDict，判断 s 是否可以由字典中的单词拼接而成（可重复使用）。

示例:
  输入: s="leetcode", wordDict=["leet","code"]  输出: True
  输入: s="applepenapple", wordDict=["apple","pen"]  输出: True
  输入: s="catsandog", wordDict=["cats","dog","sand","and","cat"]  输出: False

Tags: 动态规划 | 字符串 | 哈希表
"""

from types import TracebackType
import unittest


def word_break(s: str, wordDict: list[str]) -> bool:
    """
    思路拆解：

    dp[i] = s[0..i-1] 能否被字典中的单词拼接

    转移：dp[i] = any(dp[j] and s[j:i] in wordDict for j in range(i))
    初始化：dp[0] = True（空字符串）

    优化：将 wordDict 转为 set，查询 O(1)

    ！！注意！！！！不管切片怎么写，第一个词永远需要一个"空前缀"的状态来启动，所以dp长度要是n+1且dp0=True
    """
    # ═══════════════════════════════════════════════
    n = len(s)
    dp = [False]*(n+1)
    record = set(wordDict)
    dp[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if dp[j] and s[j: i] in record:
                dp[i] = True
                break
    return dp[n]
            
# ─────────────────────────────────────────────────
class TestWordBreak(unittest.TestCase):

    def test_basic(self):
        self.assertTrue(word_break("leetcode", ["leet", "code"]))

    def test_repeat(self):
        self.assertTrue(word_break("applepenapple", ["apple", "pen"]))

    def test_false(self):
        self.assertFalse(word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))


if __name__ == "__main__":
    unittest.main()
