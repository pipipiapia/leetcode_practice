#!/usr/bin/env python3
"""
LC 54. 螺旋矩阵
https://leetcode.com/problems/spiral-matrix/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个 m×n 的矩阵，按照顺时针螺旋顺序，返回矩阵中的所有元素。

示例:
  输入:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
  输出: [1, 2, 3, 6, 9, 8, 7, 4, 5]

Tags: 数组 | 矩阵 | 模拟
"""

import unittest


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    思路拆解：

    方法：收缩边界
    - 维护四个边界 top, bottom, left, right
    - 每次按方向遍历一条边后，收缩对应边界
    - 方向顺序：→ ↓ ← ↑ 循环

    终止条件：top > bottom 或 left > right
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestSpiralOrder(unittest.TestCase):

    def test_3x3(self):
        self.assertEqual(
            spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            [1, 2, 3, 6, 9, 8, 7, 4, 5]
        )

    def test_3x4(self):
        self.assertEqual(
            spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]),
            [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
        )

    def test_single_row(self):
        self.assertEqual(spiral_order([[1, 2, 3]]), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
