#!/usr/bin/env python3
"""
LC 142. 环形链表 II
https://leetcode.com/problems/linked-list-cycle-ii/

难度: 中等 | 字节跳动: ★★★★ | 阿里: ★★★

给定一个链表，若链表中存在环，则返回环的入口节点；否则返回 null。

Tags: 链表 | 双指针 | 快慢指针
"""

import unittest


class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


def detect_cycle(head: ListNode) -> ListNode:
    """
    思路拆解：

    Floyd 判环算法的进阶：
    1. 快慢指针判环（同 LC 141）
    2. 找到相遇点后，让一个指针从头出发，另一个留在相遇点，每次都走一步
    3. 再次相遇处即为环入口

    为什么一定会相遇：
      慢指针进入环后，快指针已经在环里。
      快指针每次比慢指针多走 1 步，相当于在环上追慢指针。
      环长有限，所以最多追一圈就一定相遇。

    为什么从 head 和相遇点同时走会到入口：
      设 head 到入口距离为 a，相遇点到入口距离为 c，环长为 L。
      可以推出 a = c + 若干个完整环长，即 a % L == c。
      所以一个从 head 走 a 步到入口；另一个从相遇点走 a 步，等价于在环里走 c 步，也到入口。

    注意：不是一定有 c == a，而是 c == a % L。若 a 大于环长，仍然成立。
    """
    # ══════════════════════════════════════════════
    slow, fast = head, head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                finder = finder.next
                slow = slow.next
            return finder

    return None
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestDetectCycle(unittest.TestCase):

    def test_with_cycle(self):
        # 3 -> 2 -> 0 -> -4 -> (回头到2)
        node2 = ListNode(2)
        head = ListNode(3, node2)
        node0 = ListNode(0)
        node4 = ListNode(-4)
        node2.next = node0
        node0.next = node4
        node4.next = node2  # 环入口是 node2
        self.assertIs(detect_cycle(head), node2)

    def test_without_cycle(self):
        head = ListNode(1, ListNode(2, ListNode(3)))
        self.assertIsNone(detect_cycle(head))


if __name__ == "__main__":
    unittest.main()
