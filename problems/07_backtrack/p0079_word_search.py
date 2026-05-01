#!/usr/bin/env python3
"""
LC 79. 单词搜索
https://leetcode.com/problems/word-search/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定一个 m×n 字符网格 board 和字符串 word，判断 word 是否存在于网格中。
单词必须按照相邻格子（水平或垂直）依次构成，同一格子不能重复使用。

示例:
  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
  word = "ABCCED"  → True
  word = "SEE"     → True
  word = "ABCB"    → False

Tags: 数组 | 回溯 | DFS
"""

import unittest


def exist(board: list[list[str]], word: str) -> bool:
    """
    思路拆解：

    DFS + 回溯：
    - 遍历每个格子作为起点
    - 每次向 4 个方向扩展，匹配 word 的下一个字符
    - 已访问的格子临时标记为 '#'，回溯时恢复
    - 越界、不匹配、已访问 → 剪枝返回 False
    """
    # ══════════════════════════════════════════════
    m, n = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= m or c < 0 or c >= n:
            return False
        if board[r][c] != word[idx]:
            return False

        tmp = board[r][c]
        board[r][c] = '#'   # 标记已访问
        found = (dfs(r+1, c, idx+1) or dfs(r-1, c, idx+1) or
                 dfs(r, c+1, idx+1) or dfs(r, c-1, idx+1))
        board[r][c] = tmp   # 回溯
        return found

    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestExist(unittest.TestCase):

    def setUp(self):
        self.board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

    def test_found1(self):
        self.assertTrue(exist([r[:] for r in self.board], "ABCCED"))

    def test_found2(self):
        self.assertTrue(exist([r[:] for r in self.board], "SEE"))

    def test_not_found(self):
        self.assertFalse(exist([r[:] for r in self.board], "ABCB"))


if __name__ == "__main__":
    unittest.main()
