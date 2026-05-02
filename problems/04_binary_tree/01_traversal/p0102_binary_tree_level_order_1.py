#!/usr/bin/env python3
"""
LC 102. 二叉树的层序遍历
https://leetcode.com/problems/binary-tree-level-order-traversal/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★★

给你二叉树的根节点 root，返回其节点值的层序遍历。
（即逐层地从左到右访问所有节点）。

示例:
  输入: root = [3, 9, 20, null, null, 15, 7]
  输出: [[3], [9, 20], [15, 7]]

Tags: 树 | BFS | 二叉树
"""

import unittest
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode) -> list[list[int]]:
    """
    思路拆解：

    BFS（广度优先遍历）用队列:
      1. 根节点入队
      2. while 队列非空:
           - 记录当前层节点数 = 队列长度
           - 弹出当前层所有节点，收集值
           - 每个节点的左右孩子入队
      3. 每层结果作为一个 list 加入结果

    关键点：如何区分"当前层"和"下一层"？
            什么数据结构天然适合 BFS？
    """
    # ═══════════════════════════════════════════════
    if not root:
        return []
    ret = []
    queue = []
    queue.append(root)
    level = []
    while queue:
        level = []
        for _ in range(len(queue)):
            tmp = queue.pop(0)
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)
            level.append(tmp.val)     
        ret.append(level)
    return ret            

    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def build_tree(values: list) -> TreeNode:
    """层序数组转二叉树（LeetCode 风格）"""
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


class TestLevelOrder(unittest.TestCase):

    def test_basic(self):
        root = build_tree([3, 9, 20, None, None, 15, 7])
        result = level_order(root)
        self.assertEqual(result, [[3], [9, 20], [15, 7]])

    def test_single(self):
        root = TreeNode(1)
        self.assertEqual(level_order(root), [[1]])

    def test_empty(self):
        self.assertEqual(level_order(None), [])


if __name__ == "__main__":
    unittest.main()
