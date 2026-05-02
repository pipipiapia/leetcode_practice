#!/usr/bin/env python3
"""
LC 113. 路径总和 II
https://leetcode.com/problems/path-sum-ii/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你二叉树的根节点 root 和一个整数目标和 targetSum，返回所有从根节点到叶子节点
路径总和等于 targetSum 的路径。

示例:
  输入: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
  输出: [[5,4,11,2],[5,8,4,5]]

Tags: 二叉树 | DFS | 回溯
"""

import unittest
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def path_sum(root: Optional[TreeNode], targetSum: int) -> list[list[int]]:
    """
    思路拆解：

    DFS + 回溯：
    - 维护当前路径 path 和当前累积和 curr_sum
    - 到达叶子节点时，若 curr_sum == targetSum，加入结果
    - 回溯：递归返回后弹出 path 中的最后一个元素
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def build(vals, i=0):
    if i >= len(vals) or vals[i] is None:
        return None
    return TreeNode(vals[i], build(vals, 2*i+1), build(vals, 2*i+2))


class TestPathSum(unittest.TestCase):

    def test_basic(self):
        root = TreeNode(5,
            TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2)), None),
            TreeNode(8, TreeNode(13), TreeNode(4, TreeNode(5), TreeNode(1))))
        result = path_sum(root, 22)
        self.assertIn([5, 4, 11, 2], result)
        self.assertIn([5, 8, 4, 5], result)

    def test_empty(self):
        self.assertEqual(path_sum(None, 0), [])


if __name__ == "__main__":
    unittest.main()
