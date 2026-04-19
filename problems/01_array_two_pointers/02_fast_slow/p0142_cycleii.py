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

    数学证明：
      设起点到入口距离为 a，环入口到相遇点距离为 b，环剩余长度为 c
      慢走了 a+b，快走了 a+b+c+b = a+2b+c
      快=2*慢 → a+2b+c = 2a+2b → c = a
      即：从相遇点和起点同时出发，相遇点就是入口
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
class TestDetectCycle(unittest.TestCase):

    def test_with_cycle(self):
        # 3 -> 2 -> 0 -> -4 -> (回头到2)
        node2 = ListNode(2)
        head = ListNode(3, ListNode(2, ListNode(0, ListNode(-4, node2))))
        node2.next = head.next  # 环入口是 node2
        self.assertIs(detect_cycle(head), node2)

    def test_without_cycle(self):
        head = ListNode(1, ListNode(2, ListNode(3)))
        self.assertIsNone(detect_cycle(head))


if __name__ == "__main__":
    unittest.main()
