#!/usr/bin/env python3
"""
LC 20. 有效的括号
https://leetcode.com/problems/valid-parentheses/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个只包含字符 '('，')'，'{'，'}'，'[' 和 ']' 的字符串 s，
判断字符串是否有效。

有效字符串需满足：
  1. 左括号必须用相同类型的右括号闭合。
  2. 左括号必须以正确的顺序闭合。

示例:
  输入: s = "()[]{}"
  输出: True

  输入: s = "(]"
  输出: False

Tags: 栈 | 字符串
"""

import unittest


def is_valid(s: str) -> bool:
    """
    思路拆解：

    使用栈:
      - 遍历字符串
      - 遇到左括号 → 入栈
      - 遇到右括号 → 栈顶是否匹配？匹配则弹出，不匹配则失败
      - 遍历结束后 → 栈空则有效，非空则无效

    关键数据结构: 栈（可以用 list 模拟）
    关键点: 如何判断匹配？用什么做对照？
    """

    # ═══════════════════════════════════════════════
    stack = []
    for i in s:
        if i in ['(','[','{']:
            stack.append(i)
        elif i == ')' and (not stack or stack[-1] != '('):
                return False
        elif  i == ']' and (not stack or stack[-1] != '['):
            return False
        elif  i == '}'and (not stack or stack[-1] != '{'):
            return False
        else:
            stack.pop() ### 掉了这个逻辑！！！
    if not stack:
        return True
    else:
        return False
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestValidParentheses(unittest.TestCase):

    def test_basic(self):
        self.assertTrue(is_valid("()"))

    def test_multiple(self):
        self.assertTrue(is_valid("()[]{}"))

    def test_nested(self):
        self.assertTrue(is_valid("{[]}"))

    def test_invalid(self):
        self.assertFalse(is_valid("(]"))

    def test_unclosed(self):
        self.assertFalse(is_valid("(["))

    def test_empty(self):
        self.assertTrue(is_valid(""))


if __name__ == "__main__":
    unittest.main()
