#!/usr/bin/env python3
"""
LC 994. 腐烂的橘子（多源 BFS）
https://leetcode.com/problems/rotting-oranges/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给定一个网格，0=空，1=新鲜橘子，2=腐烂橘子。
腐烂橘子每分钟感染上下左右的新鲜橘子，返回所有橘子腐烂的最短时间，
若不可能则返回 -1。

示例:
  输入: [[2,1,1],[1,1,0],[0,1,1]]  输出: 4
  输入: [[2,1,1],[0,1,1],[1,0,1]]  输出: -1（右下角无法被感染）
  输入: [[0,2]]                    输出: 0

Tags: 图 | BFS | 多源BFS
"""

import unittest
from collections import deque


def oranges_rotting(grid: list[list[int]]) -> int:
    """
    思路拆解：

    多源 BFS：同时从所有腐烂橘子出发向外扩散
    1. 初始化：所有腐烂橘子入队，统计新鲜橘子数 fresh
    2. BFS：每轮（每分钟）处理队列中当前所有节点，感染四邻新鲜橘子
    3. 若 fresh == 0 → 返回分钟数，否则 -1

    关键：BFS 天然保证最短路径（层序扩散）
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestOrangesRotting(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(oranges_rotting([[2,1,1],[1,1,0],[0,1,1]]), 4)

    def test_impossible(self):
        self.assertEqual(oranges_rotting([[2,1,1],[0,1,1],[1,0,1]]), -1)

    def test_no_fresh(self):
        self.assertEqual(oranges_rotting([[0,2]]), 0)


if __name__ == "__main__":
    unittest.main()
