#!/usr/bin/env python3
"""
LC 22. 括号生成
https://leetcode.com/problems/generate-parentheses/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

数字 n 代表生成括号的对数，设计一个函数，用于能够生成所有可能的并且有效的括号组合。

示例:
  输入: n=3
  输出: ["((()))","(()())","(())()","()(())","()()()"]

Tags: 字符串 | 回溯 | 动态规划
"""

import unittest


def generate_parenthesis(n: int) -> list[str]:
    """
    思路拆解：

    回溯：维护当前已放的左括号数 open 和右括号数 close
    - 可放左括号的条件：open < n
    - 可放右括号的条件：close < open（右括号不能比左括号多）
    - 终止条件：open == close == n，加入结果

    剪枝：close >= open 时不能放右括号（无效路径）
    """
    # ══════════════════════════════════════════════
    result = []

    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if open_count < n:
            path.append("(")
            backtrack(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:
            path.append(")")
            backtrack(path, open_count, close_count + 1)
            path.pop()

    backtrack([], 0, 0)
    return result
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestGenerateParenthesis(unittest.TestCase):

    def test_n3(self):
        result = sorted(generate_parenthesis(3))
        expected = sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])
        self.assertEqual(result, expected)

    def test_n1(self):
        self.assertEqual(generate_parenthesis(1), ["()"])


if __name__ == "__main__":
    unittest.main()
