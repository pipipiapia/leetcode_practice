#!/usr/bin/env python3
"""
LC 105. 从前序与中序遍历序列构造二叉树
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给定两个整数数组 preorder（前序遍历）和 inorder（中序遍历），构造并返回二叉树。

示例:
  preorder = [3, 9, 20, 15, 7]
  inorder  = [9, 3, 15, 20, 7]
  输出:
      3
     / \
    9  20
       / \
      15   7

Tags: 二叉树 | 递归 | 哈希表
"""

import unittest
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    """
    思路拆解：

    前序遍历：根 | 左子树 | 右子树
    中序遍历：左子树 | 根 | 右子树

    递归策略：
    1. preorder[0] 是当前子树的根
    2. 在 inorder 中找到根的位置 idx
    3. idx 左边是左子树（长度 = idx），右边是右子树
    4. 递归构建左右子树

    优化：用哈希表记录 inorder 中每个值的索引，避免每次 O(n) 查找
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def tree_to_list(root):
    """层序遍历输出（None 表示空节点）"""
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # 去掉末尾 None
    while result and result[-1] is None:
        result.pop()
    return result


class TestBuildTree(unittest.TestCase):

    def test_basic(self):
        root = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
        self.assertEqual(tree_to_list(root), [3, 9, 20, None, None, 15, 7])

    def test_single(self):
        root = build_tree([-1], [-1])
        self.assertEqual(root.val, -1)


if __name__ == "__main__":
    unittest.main()
