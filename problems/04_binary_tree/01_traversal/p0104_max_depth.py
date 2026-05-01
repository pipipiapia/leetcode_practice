#!/usr/bin/env python3
"""
LC 104. 二叉树的最大深度
https://leetcode.com/problems/maximum-depth-of-binary-tree/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个二叉树，返回其最大深度（从根节点到最远叶子节点的最长路径上的节点数）。

示例:
  输入:
      3
     / \
    9  20
       / \
      15   7
  输出: 3

Tags: 二叉树 | DFS | BFS
"""

import unittest
from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: Optional[TreeNode]) -> int:
    """
    思路拆解：

    递归（DFS）：
      max_depth(root) = 1 + max(max_depth(left), max_depth(right))
      base case：root 为 None 时深度为 0

    迭代（BFS 层序）：
      按层遍历，每遍历完一层 depth += 1
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestMaxDepth(unittest.TestCase):

    def test_basic(self):
        #     3
        #    / \
        #   9  20
        #      / \
        #     15   7
        root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        self.assertEqual(max_depth(root), 3)

    def test_single(self):
        self.assertEqual(max_depth(TreeNode(1)), 1)

    def test_empty(self):
        self.assertEqual(max_depth(None), 0)


if __name__ == "__main__":
    unittest.main()
