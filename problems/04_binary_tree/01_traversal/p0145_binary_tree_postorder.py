#!/usr/bin/env python3
"""
LC 145. 二叉树的后序遍历
https://leetcode.com/problems/binary-tree-postorder-traversal/

难度: 简单 | 字节跳动: ★★★★ | 美团: ★★★

给你一棵二叉树的根节点 root，返回其节点值的后序遍历。

后序遍历顺序：左 → 右 → 根

示例:
  输入: root = [1, null, 2, 3]
  输出: [3, 2, 1]

  输入: root = [1, 2, 3, 4, 5]
  输出: [4, 5, 2, 3, 1]

Tags: 树 | DFS | 二叉树 | 栈

难点: 非递归写法需要处理"右子树是否已访问"的判断（prev 指针）
"""

import unittest


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val: int = val
        self.left: "TreeNode | None" = left
        self.right: "TreeNode | None" = right


class Solution:
    # -------------------------------------------------------
    # 方法一：递归（最简单）
    # 时间 O(n)，空间 O(n)
    # -------------------------------------------------------
    def postorderTraversal_recursive(self, root: TreeNode | None) -> list[int]:
        ret = []
        def fun(root, ret):
            
        return []

    # -------------------------------------------------------
    # 方法二：非递归 - 前序变体 + 翻转（推荐，好记）
    # 思路：前序改成 根→右→左，结果反转 = 左→右→根
    # 时间 O(n)，空间 O(n)
    # -------------------------------------------------------
    def postorderTraversal_reverse(self, root: TreeNode | None) -> list[int]:
        return []

    # -------------------------------------------------------
    # 方法三：非递归 - 标准单栈（真正模拟递归）
    # 思路：用 prev 记上一个输出节点，判断右子树是否已访问
    # 时间 O(n)，空间 O(n)
    # -------------------------------------------------------
    def postorderTraversal(self, root: TreeNode | None) -> list[int]:
        return []


# -------------------------------------------------------
# 辅助函数
# -------------------------------------------------------
def build_tree(vals: list) -> TreeNode | None:
    """从列表构建二叉树（BFS 顺序，None 表示空节点）"""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue: list[TreeNode] = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


class TestPostorder(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example1(self):
        root = build_tree([1, None, 2, 3])
        self.assertEqual(self.sol.postorderTraversal(root), [3, 2, 1])

    def test_example2(self):
        root = build_tree([1, 2, 3, 4, 5])
        self.assertEqual(self.sol.postorderTraversal(root), [4, 5, 2, 3, 1])

    def test_single(self):
        root = TreeNode(1)
        self.assertEqual(self.sol.postorderTraversal(root), [1])

    def test_empty(self):
        self.assertEqual(self.sol.postorderTraversal(None), [])

    def test_left_only(self):
        root = build_tree([1, 2, None, 3])
        self.assertEqual(self.sol.postorderTraversal(root), [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
