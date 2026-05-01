#!/usr/bin/env python3
"""
LC 98. 验证二叉搜索树
https://leetcode.com/problems/validate-binary-search-tree/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你一个二叉树的根节点 root，判断其是否是一个有效的二叉搜索树（BST）。
BST：左子树所有节点 < 根，右子树所有节点 > 根，左右子树也均为 BST。

示例:
  输入: [2,1,3]         输出: True
  输入: [5,1,4,null,null,3,6]  输出: False（根5的右子节点4 < 5）

Tags: 二叉树 | DFS | BST
"""

import unittest
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    思路拆解：

    传递上下界（递归）：
    - 每个节点需满足 low < node.val < high
    - 左子树：上界更新为当前节点值（left_child < root）
    - 右子树：下界更新为当前节点值（right_child > root）

    注意：不能只比较父子节点，必须用上下界传递（经典陷阱题）
    错误示例：[5,4,6,null,null,3,7] → 3 < 5 但在右子树，不合法
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestIsValidBST(unittest.TestCase):

    def test_valid(self):
        root = TreeNode(2, TreeNode(1), TreeNode(3))
        self.assertTrue(is_valid_bst(root))

    def test_invalid(self):
        root = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
        self.assertFalse(is_valid_bst(root))

    def test_trap(self):
        # [5,4,6,null,null,3,7] — 3 在右子树但小于根 5
        root = TreeNode(5, TreeNode(4), TreeNode(6, TreeNode(3), TreeNode(7)))
        self.assertFalse(is_valid_bst(root))


if __name__ == "__main__":
    unittest.main()
