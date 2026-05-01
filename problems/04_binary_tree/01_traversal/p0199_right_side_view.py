#!/usr/bin/env python3
"""
LC 199. 二叉树的右视图
https://leetcode.com/problems/binary-tree-right-side-view/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定一个二叉树，返回从右侧看到的节点值（即每层最右边的节点值）。

示例:
  输入:
      1
     / \
    2   3
     \   \
      5   4
  输出: [1, 3, 4]

Tags: 二叉树 | BFS | DFS
"""

import unittest
from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: Optional[TreeNode]) -> list[int]:
    """
    思路拆解：

    BFS 层序遍历：每层的最后一个节点即为右视图可见节点
    - 遍历每一层，取最后一个节点加入结果
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestRightSideView(unittest.TestCase):

    def test_basic(self):
        root = TreeNode(1,
                        TreeNode(2, None, TreeNode(5)),
                        TreeNode(3, None, TreeNode(4)))
        self.assertEqual(right_side_view(root), [1, 3, 4])

    def test_single(self):
        self.assertEqual(right_side_view(TreeNode(1)), [1])

    def test_empty(self):
        self.assertEqual(right_side_view(None), [])


if __name__ == "__main__":
    unittest.main()
