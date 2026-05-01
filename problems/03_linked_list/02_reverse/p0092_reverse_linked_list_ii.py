#!/usr/bin/env python3
"""
LC 92. 反转链表 II
https://leetcode.com/problems/reverse-linked-list-ii/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你单链表的头节点 head 和两个整数 left 和 right（left <= right），
请你反转从位置 left 到位置 right 的链表节点，返回反转后的链表。

示例:
  输入: head = [1->2->3->4->5], left=2, right=4
  输出: [1->4->3->2->5]

Tags: 链表 | 递归 | 头插法
"""

import unittest
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """
    思路拆解：

    头插法（一次遍历）：
    1. 找到 left 前一个节点 pre（用 dummy 哨兵简化边界）
    2. curr 指向 left 节点
    3. 反复将 curr.next 插到 pre.next（头插到 pre 后面）
       重复 right - left 次

    示意（left=2, right=4）：
      初始：  dummy -> 1 -> [2 -> 3 -> 4] -> 5
      step1: dummy -> 1 -> [3 -> 2] -> 4 -> 5
      step2: dummy -> 1 -> [4 -> 3 -> 2] -> 5
    """
    # ══════════════════════════════════════════════
    dummy = ListNode(0)
    dummy.next = head
    pre = dummy

    # 走到 left 前一个节点
    for _ in range(left - 1):
        pre = pre.next

    curr = pre.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt

    return dummy.next
    # ══════════════════════════════════════════════


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


class TestReverseBetween(unittest.TestCase):

    def test_basic(self):
        head = list_to_nodes([1, 2, 3, 4, 5])
        self.assertEqual(nodes_to_list(reverse_between(head, 2, 4)), [1, 4, 3, 2, 5])

    def test_full(self):
        head = list_to_nodes([1, 2, 3])
        self.assertEqual(nodes_to_list(reverse_between(head, 1, 3)), [3, 2, 1])

    def test_single(self):
        head = list_to_nodes([5])
        self.assertEqual(nodes_to_list(reverse_between(head, 1, 1)), [5])


if __name__ == "__main__":
    unittest.main()
