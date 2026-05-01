#!/usr/bin/env python3
"""
LC 739. 每日温度
https://leetcode.com/problems/daily-temperatures/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定一个整数数组 temperatures，返回一个数组 answer，其中 answer[i] 表示
第 i 天后需要等待多少天才能等到更高的温度，若不存在则为 0。

示例:
  输入: [73,74,75,71,69,72,76,73]
  输出: [1,1,4,2,1,1,0,0]

Tags: 数组 | 单调栈
"""

import unittest


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    思路拆解：

    单调栈（维护单调递减栈，存下标）：
    - 遍历每天温度，若当前温度 > 栈顶对应温度 → 找到了栈顶那天的答案
    - 弹出栈顶，answer[栈顶] = 当前下标 - 栈顶下标
    - 重复直到栈为空或栈顶温度 >= 当前温度
    - 当前下标入栈

    单调栈存储"还没找到答案的天"的下标，当遇到更高温度时结算
    """
    # ══════════════════════════════════════════════
    n = len(temperatures)
    answer = [0] * n
    stack = []  # 单调递减栈，存下标

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)

    return answer
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestDailyTemperatures(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
            [1, 1, 4, 2, 1, 1, 0, 0]
        )

    def test_decreasing(self):
        self.assertEqual(daily_temperatures([30, 20, 10]), [0, 0, 0])

    def test_increasing(self):
        self.assertEqual(daily_temperatures([30, 40, 50, 60]), [1, 1, 1, 0])


if __name__ == "__main__":
    unittest.main()
