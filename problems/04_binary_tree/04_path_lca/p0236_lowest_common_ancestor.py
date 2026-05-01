#!/usr/bin/env python3
"""
LC 236: 二叉树的最近公共祖先（LCA）
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

难度: 中等 | 字节跳动: ★★★★ | 百度: ★★★★

给定一个二叉树，找到该树中两个指定节点的最近公共祖先。

示例:
  输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
  输出: 3

  输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
  输出: 5（5是自身的祖先）

Tags: 树 | DFS | 二叉树
"""

import unittest


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    思路拆解：

    后序 DFS 递归：
      - 递归返回值：找到 p 或 q 就返回该节点
      - 三种情况：
        1. 左子树有、右子树有 → 当前节点就是 LCA
        2. 只有左子树有 → 返回左子树结果
        3. 只有右子树有 → 返回右子树结果
      - base case: root 为 None 或 root == p 或 root == q

    关键点：为什么要用后序遍历（左右根）？
            left and right 非空时为什么直接返回 root？
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


class TestLCA(unittest.TestCase):

    def test_basic(self):
        root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = root.left    # 5
        q = root.right   # 1
        self.assertEqual(lowest_common_ancestor(root, p, q).val, 3)

    def test_p_is_ancestor(self):
        root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = root.left      # 5
        q = root.left.right.right  # 4
        self.assertEqual(lowest_common_ancestor(root, p, q).val, 5)


if __name__ == "__main__":
    unittest.main()
