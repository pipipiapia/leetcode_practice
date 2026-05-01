#!/usr/bin/env python3
"""
LC 55. 跳跃游戏
https://leetcode.com/problems/jump-game/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给定一个非负整数数组 nums，最初位于数组的第一个下标。
数组中每个元素代表你在该位置可以跳跃的最大长度，判断是否能到达最后一个下标。

示例:
  输入: [2,3,1,1,4]  输出: True
  输入: [3,2,1,0,4]  输出: False  # 永远停在下标 3

Tags: 数组 | 贪心
"""

import unittest


def can_jump(nums: list[int]) -> bool:
    """
    思路拆解：

    贪心：维护当前能到达的最远下标 max_reach
    - 遍历数组，若当前下标 i > max_reach，说明无法到达 i，返回 False
    - 否则更新 max_reach = max(max_reach, i + nums[i])
    - 若 max_reach >= n-1，提前返回 True
    """
    # ══════════════════════════════════════════════
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestCanJump(unittest.TestCase):

    def test_true(self):
        self.assertTrue(can_jump([2, 3, 1, 1, 4]))

    def test_false(self):
        self.assertFalse(can_jump([3, 2, 1, 0, 4]))

    def test_single(self):
        self.assertTrue(can_jump([0]))


if __name__ == "__main__":
    unittest.main()
