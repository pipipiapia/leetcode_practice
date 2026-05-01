#!/usr/bin/env python3
"""
LC 48. 旋转图像
https://leetcode.com/problems/rotate-image/

难度: 中等 | 字节跳动: ★★★★ | 微软: ★★★★

给定一个 n×n 的矩阵，将其顺时针旋转 90 度。必须原地旋转。

示例:
  输入:
    [[1,2,3],
     [4,5,6],
     [7,8,9]]
  输出:
    [[7,4,1],
     [8,5,2],
     [9,6,3]]

Tags: 数组 | 矩阵 | 原地操作
"""

import unittest


def rotate(matrix: list[list[int]]) -> None:
    """
    思路拆解：

    顺时针旋转 90° = 先沿主对角线转置 + 再左右翻转

    转置：matrix[i][j] ↔ matrix[j][i]
    左右翻转：每行 reverse

    为什么这个等价于旋转？
      原位置 (i, j) → 旋转后 → (j, n-1-i)
      先转置 (i,j)→(j,i)，再左右翻转 (j,i)→(j,n-1-i) ✓
    """
    # ═══════════════════════════════════════════════
    row, col = len(matrix), len(matrix[0])
    for i in range(row):
        for j in range(i+1, col):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = tmp
    
    for i in range(row):
        matrix[i].reverse()
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestRotate(unittest.TestCase):

    def test_3x3(self):
        m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        rotate(m)
        self.assertEqual(m, [[7, 4, 1], [8, 5, 2], [9, 6, 3]])

    def test_4x4(self):
        m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
        rotate(m)
        self.assertEqual(m, [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])


if __name__ == "__main__":
    unittest.main()
