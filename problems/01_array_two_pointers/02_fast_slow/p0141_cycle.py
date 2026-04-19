#!/usr/bin/env python3
"""
LC 141. 环形链表
https://leetcode.com/problems/linked-list-cycle/

难度: 简单 | 字节跳动: ★★★★ | 快手: ★★★

给定一个链表，判断链表中是否有环。
链表节点定义：
  class ListNode:
      def __init__(self, x):
          self.val = x
          self.next = None

进阶：你能用 O(1)（即常数级）额外内存解决这个问题吗？

Tags: 链表 | 双指针 | 快慢指针
"""

import unittest


class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


def has_cycle(head: ListNode) -> bool:
    """
    思路拆解：

    快慢指针（Floyd 判环算法）：
    - 慢指针每次走一步，快指针每次走两步
    - 若有环，快慢指针必然在环内相遇
    - 若无环，快指针先到达尾部（None）
    - 时间 O(n)，空间 O(1)

    为什么快慢指针一定能相遇？
      快每次进2步，慢每次进1步，相对速度=1，若有环则必然追上
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestHasCycle(unittest.TestCase):

    def test_with_cycle(self):
        # 3 -> 2 -> 0 -> -4 -> 2(回头)
        tail = ListNode(-4)
        head = ListNode(3, ListNode(2, ListNode(0, ListNode(-4, tail))))
        tail.next = head.next  # 形成环
        self.assertTrue(has_cycle(head))

    def test_without_cycle(self):
        head = ListNode(1, ListNode(2, ListNode(3)))
        self.assertFalse(has_cycle(head))

    def test_single_node_cycle(self):
        node = ListNode(1)
        node.next = node
        self.assertTrue(has_cycle(node))


if __name__ == "__main__":
    unittest.main()
