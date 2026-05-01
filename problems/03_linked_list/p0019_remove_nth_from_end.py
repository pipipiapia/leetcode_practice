#!/usr/bin/env python3
"""
LC 19. 删除链表的倒数第 N 个节点
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个链表，删除链表的倒数第 n 个节点，并返回链表的头节点。要求一次遍历。

示例:
  输入: head = [1->2->3->4->5], n = 2
  输出: [1->2->3->5]

Tags: 链表 | 双指针 | 快慢指针
"""

import unittest
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    思路拆解：

    快慢指针（一次遍历）：
    - fast 先走 n 步
    - fast 和 slow 同时走，直到 fast 到达最后一个节点
    - 此时 slow.next 就是倒数第 n 个节点，删除它

    关键：用 dummy 哨兵处理删除头节点的边界情况
    """
    # ══════════════════════════════════════════════
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    # fast 先走 n+1 步（让 slow 停在待删节点的前一个）
    for _ in range(n + 1):
        fast = fast.next

    while fast:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
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


class TestRemoveNthFromEnd(unittest.TestCase):

    def test_basic(self):
        head = list_to_nodes([1, 2, 3, 4, 5])
        self.assertEqual(nodes_to_list(remove_nth_from_end(head, 2)), [1, 2, 3, 5])

    def test_remove_head(self):
        head = list_to_nodes([1, 2])
        self.assertEqual(nodes_to_list(remove_nth_from_end(head, 2)), [2])

    def test_single(self):
        head = list_to_nodes([1])
        self.assertIsNone(remove_nth_from_end(head, 1))


if __name__ == "__main__":
    unittest.main()
