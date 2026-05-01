#!/usr/bin/env python3
"""
LC 143. 重排链表
https://leetcode.com/problems/reorder-list/

难度: 中等 | 字节跳动: ★★★★ | 腾讯: ★★★★

给定链表 L0 → L1 → ... → Ln-1 → Ln
将其重排为：L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...
不能修改节点的值，只能修改节点的 next 指针。

示例:
  输入: [1->2->3->4]   输出: [1->4->2->3]
  输入: [1->2->3->4->5] 输出: [1->5->2->4->3]

Tags: 链表 | 快慢指针 | 反转链表
"""

import unittest
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reorder_list(head: Optional[ListNode]) -> None:
    """
    思路拆解：

    三步走：
    1. 快慢指针找中点（slow 停在前半段末尾）
    2. 反转后半段链表
    3. 交叉合并前半段和反转后的后半段

    示例 [1->2->3->4->5]：
      找中点：前半 [1->2->3]，后半 [4->5]
      反转后半：[5->4]
      合并：1->5->2->4->3
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def list_to_nodes(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def nodes_to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


class TestReorderList(unittest.TestCase):

    def test_even(self):
        head = list_to_nodes([1, 2, 3, 4])
        reorder_list(head)
        self.assertEqual(nodes_to_list(head), [1, 4, 2, 3])

    def test_odd(self):
        head = list_to_nodes([1, 2, 3, 4, 5])
        reorder_list(head)
        self.assertEqual(nodes_to_list(head), [1, 5, 2, 4, 3])


if __name__ == "__main__":
    unittest.main()
