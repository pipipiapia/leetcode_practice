#!/usr/bin/env python3
"""
LC 155. 最小栈
https://leetcode.com/problems/min-stack/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

设计一个支持 push、pop、top 和 getMin 操作的栈，其中 getMin 需 O(1) 时间复杂度。

Tags: 栈 | 设计
"""

import unittest


class MinStack:
    """
    思路拆解：

    用两个栈：
    - stack：正常存数据
    - min_stack：辅助栈，每次 push 时同步 push 当前最小值
    - pop 时两个栈同步 pop

    保证 min_stack 栈顶始终是当前 stack 的最小值。
    """

    def __init__(self):
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMinStack(unittest.TestCase):

    def test_basic(self):
        s = MinStack()
        s.push(-2)
        s.push(0)
        s.push(-3)
        self.assertEqual(s.getMin(), -3)
        s.pop()
        self.assertEqual(s.top(), 0)
        self.assertEqual(s.getMin(), -2)


if __name__ == "__main__":
    unittest.main()
