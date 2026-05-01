#!/usr/bin/env python3
"""
LC 297. 二叉树的序列化与反序列化
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

难度: 困难 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

设计一个算法，将二叉树序列化为字符串，并能将该字符串反序列化为原始二叉树结构。

示例:
  序列化: [1,2,3,null,null,4,5] → "1,2,N,N,3,4,N,N,5,N,N"
  反序列化: "1,2,N,N,3,4,N,N,5,N,N" → 原始二叉树

Tags: 二叉树 | DFS | 设计
"""

import unittest
from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """
    思路拆解：

    前序遍历序列化（DFS）：
    - 按前序遍历输出节点值，null 用 "N" 表示，逗号分隔
    - 反序列化：按前序重建，遇到 "N" 返回 None
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        # ══════════════════════════════════════════════
        tokens = []

        def dfs(node):
            if not node:
                tokens.append("N")
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(tokens)
        # ══════════════════════════════════════════════

    def deserialize(self, data: str) -> Optional[TreeNode]:
        # ══════════════════════════════════════════════
        tokens = deque(data.split(","))

        def dfs():
            val = tokens.popleft()
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
        # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestCodec(unittest.TestCase):

    def test_basic(self):
        codec = Codec()
        root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
        result = codec.deserialize(codec.serialize(root))
        # 验证结构：层序遍历对比
        def level_order(node):
            if not node:
                return []
            q, res = deque([node]), []
            while q:
                n = q.popleft()
                res.append(n.val)
                if n.left: q.append(n.left)
                if n.right: q.append(n.right)
            return res
        self.assertEqual(level_order(result), [1, 2, 3, 4, 5])

    def test_empty(self):
        codec = Codec()
        self.assertIsNone(codec.deserialize(codec.serialize(None)))

    def test_single(self):
        codec = Codec()
        root = TreeNode(1)
        result = codec.deserialize(codec.serialize(root))
        self.assertEqual(result.val, 1)


if __name__ == "__main__":
    unittest.main()
