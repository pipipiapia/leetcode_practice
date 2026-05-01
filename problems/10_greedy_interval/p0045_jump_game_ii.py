#!/usr/bin/env python3
"""
LC 45. 跳跃游戏 II
https://leetcode.com/problems/jump-game-ii/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给定一个非负整数数组，返回到达最后一个下标所需的最少跳跃次数（保证一定可以到达）。

示例:
  输入: [2,3,1,1,4]  输出: 2  # 0→1→4
  输入: [2,3,0,1,4]  输出: 2  # 0→1→4

Tags: 数组 | 贪心
"""

import unittest


def jump(nums: list[int]) -> int:
    """
    思路拆解：

    贪心（BFS 思想）：
    - 把跳跃看作 BFS，每次跳跃是一层
    - curr_end：当前跳跃可到达的最远边界
    - far：在当前层内，能到达的最远下标
    - 到达 curr_end 时，必须跳一次（count+1），更新 curr_end = far
    """
    # ══════════════════════════════════════════════
    count = 0
    curr_end = 0  # 当前轮能到达的最远位置
    far = 0       # 下一轮能到达的最远位置

    for i in range(len(nums) - 1):  # 不需要从最后一个位置跳
        far = max(far, i + nums[i])
        if i == curr_end:           # 到达当前轮边界，必须跳
            count += 1
            curr_end = far

    return count
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestJump(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(jump([2, 3, 1, 1, 4]), 2)

    def test_basic2(self):
        self.assertEqual(jump([2, 3, 0, 1, 4]), 2)

    def test_single(self):
        self.assertEqual(jump([0]), 0)


if __name__ == "__main__":
    unittest.main()
