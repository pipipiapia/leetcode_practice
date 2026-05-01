#!/usr/bin/env python3
"""
LC 103: 二叉树锯齿形层序遍历
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★

给定一个二叉树，返回其节点值的锯齿形层序遍历。
即先从左到右遍历下一层，再从右到左遍历，以此类推，层间交替。

示例:
  输入: root = [3,9,20,null,null,15,7]
  输出: [[3], [20,9], [15,7]]

Tags: 树 | BFS | 双端队列
"""

import unittest
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def zigzag_level_order(root: TreeNode) -> list[list[int]]:
    """
    思路拆解：

    层序遍历 + Z 字形处理：
      - 奇数层（从0开始）：从左到右 → 正常 append
      - 偶数层：从右到左 → appendleft 或最后 reverse
      - 遍历完一层后切换方向

    关键点：用什么数据结构可以实现"从右插入"？
            left_to_right 标志怎么切换？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def build_tree(values: list) -> TreeNode:
    """层序数组转二叉树"""
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


class TestZigzagLevelOrder(unittest.TestCase):

    def test_basic(self):
        root = build_tree([3, 9, 20, None, None, 15, 7])
        self.assertEqual(zigzag_level_order(root), [[3], [20, 9], [15, 7]])

    def test_single(self):
        root = TreeNode(1)
        self.assertEqual(zigzag_level_order(root), [[1]])

    def test_empty(self):
        self.assertEqual(zigzag_level_order(None), [])


if __name__ == "__main__":
    unittest.main()
