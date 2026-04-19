#!/usr/bin/env python3
"""
LC 11. 盛最多水的容器
https://leetcode.com/problems/container-with-most-water/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个长度为 n 的整数数组 height，有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i])。
找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

示例:
  输入: height = [1,8,6,2,5,4,8,3,7]
  输出: 49
  解释: 左指针指向1，右指针指向7，min(1,7)*8=56... 实际最大为 49（8*6.2 宽度）

Tags: 数组 | 双指针 | 对撞指针
"""

import unittest


def max_area(height: list[int]) -> int:
    """
    思路拆解：

    对撞指针：左右指针向中间收敛
    - 面积 = min(height[l], height[r]) * (r - l)
    - 移动较矮的那一侧才有可能增大面积（因为宽度必然减少）

    为什么移动较矮侧？
      若移动较高侧，高度不会增加（受限于较矮侧），宽度又减少，面积必然变小
      若移动较矮侧，高度可能增加，宽度减少但有机会获得更大面积
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestMaxArea(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_two_elements(self):
        self.assertEqual(max_area([1, 1]), 1)

    def test_increasing(self):
        self.assertEqual(max_area([1, 2, 3, 4, 5]), 6)


if __name__ == "__main__":
    unittest.main()
