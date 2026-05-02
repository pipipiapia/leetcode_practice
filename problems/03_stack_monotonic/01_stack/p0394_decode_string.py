#!/usr/bin/env python3
"""
LC 394. 字符串解码
https://leetcode.com/problems/decode-string/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给定一个经过编码的字符串，返回它解码后的字符串。
编码规则：k[encoded_string] 表示将 encoded_string 重复 k 次。

示例:
  输入: "3[a]2[bc]"   输出: "aaabcbc"
  输入: "3[a2[c]]"    输出: "accaccacc"
  输入: "2[abc]3[cd]ef"  输出: "abcabccdcdcdef"

Tags: 栈 | 字符串 | 递归
"""

import unittest


def decode_string(s: str) -> str:
    """
    思路拆解：

    用栈处理嵌套：
    - 遇到数字：累积当前重复次数 num
    - 遇到 '['：将当前 (num, 已构建字符串) 压栈，重置 num 和 curr_str
    - 遇到 ']'：弹出栈顶 (prev_num, prev_str)，curr_str = prev_str + prev_num * curr_str
    - 遇到字母：拼接到 curr_str
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestDecodeString(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(decode_string("3[a]2[bc]"), "aaabcbc")

    def test_nested(self):
        self.assertEqual(decode_string("3[a2[c]]"), "accaccacc")

    def test_combined(self):
        self.assertEqual(decode_string("2[abc]3[cd]ef"), "abcabccdcdcdef")


if __name__ == "__main__":
    unittest.main()
