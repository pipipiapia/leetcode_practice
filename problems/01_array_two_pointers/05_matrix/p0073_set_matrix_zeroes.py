#!/usr/bin/env python3
"""
LC 73. 矩阵置零
https://leetcode.com/problems/set-matrix-zeroes/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个 m×n 的整数矩阵，如果一个元素为 0，则将其所在行和列全部设为 0。
要求原地操作，空间复杂度 O(1)。

示例:
  输入:  [[1,1,1],[1,0,1],[1,1,1]]
  输出:  [[1,0,1],[0,0,0],[1,0,1]]

Tags: 数组 | 矩阵 | 原地操作
"""

import unittest


def set_zeroes(matrix: list[list[int]]) -> None:
    """
    思路拆解：

    O(1) 空间：用第一行和第一列作为标记位
    - 先检查第一行/第一列本身是否有 0（用两个 bool 记录）
    - 扫描矩阵，把需要置零的信息记在第一行/第一列
    - 根据第一行/第一列标记，置零对应行列
    - 最后根据最初的 bool，处理第一行/第一列

    注意：先处理内部，再处理第一行和第一列（否则会互相影响）
    """
    # ══════════════════════════════════════════════
    m, n = len(matrix), len(matrix[0])

    # 记录第一行/列是否本身有 0
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # 用第一行、第一列记录其余位置是否含 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # 根据标记置零（跳过第一行和第一列）
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # 处理第一行
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    # 处理第一列
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestSetZeroes(unittest.TestCase):

    def test_basic(self):
        m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        set_zeroes(m)
        self.assertEqual(m, [[1, 0, 1], [0, 0, 0], [1, 0, 1]])

    def test_two_zeros(self):
        m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
        set_zeroes(m)
        self.assertEqual(m, [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])


if __name__ == "__main__":
    unittest.main()
