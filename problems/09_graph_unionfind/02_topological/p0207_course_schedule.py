#!/usr/bin/env python3
"""
LC 207. 课程表（拓扑排序）
https://leetcode.com/problems/course-schedule/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

你这学期必须选修 numCourses 门课程，courses[i] = [a, b] 表示选 a 之前必须先选 b。
返回是否能完成所有课程（即判断是否存在环）。

示例:
  输入: numCourses=2, prerequisites=[[1,0]]       输出: True
  输入: numCourses=2, prerequisites=[[1,0],[0,1]] 输出: False（环）

核心：有向图判环 = 拓扑排序（Kahn 算法 BFS）

Tags: 图 | 拓扑排序 | BFS | DFS
"""

import unittest
from collections import deque


def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    """
    思路拆解：

    Kahn 算法（BFS 拓扑排序）：
    1. 建图（邻接表） + 统计每个节点的入度
    2. 将所有入度为 0 的节点入队
    3. BFS：每次弹出一个节点，将其邻居入度 -1，若邻居入度变 0 则入队
    4. 若最终处理的节点数 == numCourses → 无环 → True

    有向图有环 ⟺ 拓扑排序无法处理所有节点
    """
    # ══════════════════════════════════════════════
    graph = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses

    for a, b in prerequisites:
        graph[b].append(a)      # b → a（先修 b 才能选 a）
        in_degree[a] += 1

    queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1
        for nxt in graph[course]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    return completed == numCourses
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestCanFinish(unittest.TestCase):

    def test_no_cycle(self):
        self.assertTrue(can_finish(2, [[1, 0]]))

    def test_cycle(self):
        self.assertFalse(can_finish(2, [[1, 0], [0, 1]]))

    def test_no_prereqs(self):
        self.assertTrue(can_finish(3, []))

    def test_chain(self):
        self.assertTrue(can_finish(4, [[1,0],[2,1],[3,2]]))


if __name__ == "__main__":
    unittest.main()
