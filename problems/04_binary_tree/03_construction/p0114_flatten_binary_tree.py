#!/usr/bin/env python3
"""
LC 114. 二叉树展开为链表
https://leetcode.com/problems/flatten-binary-tree-to-linked-list/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你二叉树的根节点 root，请你将它展开为一个单链表（使用 right 指针，left 均为 None）。
展开顺序与前序遍历顺序一致。要求原地操作。

示例:
  输入:  [1, 2, 5, 3, 4, null, 6]
  输出:  [1, null, 2, null, 3, null, 4, null, 5, null, 6]

Tags: 二叉树 | 前序遍历 | 原地操作
"""

import unittest
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def flatten(root: Optional[TreeNode]) -> None:
    """
    思路拆解：

    关键观察：前序遍历 = 根 → 左子树 → 右子树
    将左子树接到右边，原右子树接到左子树最右节点后面。

    步骤（原地，O(1) 空间）：
    对每个节点 curr：
    1. 若有左子树，找左子树最右节点 rightmost
    2. rightmost.right = curr.right（原右子树接到左子树最右边）
    3. curr.right = curr.left（左子树移到右边）
    4. curr.left = None
    5. curr = curr.right（前进）
    """
    # ══════════════════════════════════════════════
    curr = root
    while curr:
        if curr.left:
            # 找左子树的最右节点
            rightmost = curr.left
            while rightmost.right:
                rightmost = rightmost.right
            # 将原右子树接到左子树最右边
            rightmost.right = curr.right
            # 左子树移到右边
            curr.right = curr.left
            curr.left = None
        curr = curr.right
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
def nodes_to_list(root):
    result = []
    while root:
        result.append(root.val)
        root = root.right
    return result


class TestFlatten(unittest.TestCase):

    def test_basic(self):
        root = TreeNode(1,
            TreeNode(2, TreeNode(3), TreeNode(4)),
            TreeNode(5, None, TreeNode(6)))
        flatten(root)
        self.assertEqual(nodes_to_list(root), [1, 2, 3, 4, 5, 6])

    def test_single(self):
        root = TreeNode(1)
        flatten(root)
        self.assertEqual(nodes_to_list(root), [1])


if __name__ == "__main__":
    unittest.main()
