#!/usr/bin/env python3
"""
LC 160. 相交链表
https://leetcode.com/problems/intersection-of-two-linked-lists/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你两个单链表的头节点 headA 和 headB，请你找出并返回两个单链表相交的起始节点。
若不相交返回 null。要求 O(m+n) 时间，O(1) 空间。

Tags: 链表 | 双指针 | 哈希表
"""

import unittest
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def get_intersection_node(headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    """
    思路拆解：

    双指针消除路径长度差：
    - pA 走完 A 后切换到 B 的头，pB 走完 B 后切换到 A 的头
    - 若相交：pA 和 pB 走过相同总路程 (len_A + len_B)，必然在交点相遇
    - 若不相交：两者同时到 None

    假设 A 长度 a，B 长度 b，公共部分长 c：
      pA 路径：a + (b-c) = a + b - c
      pB 路径：b + (a-c) = a + b - c  → 同时到达交点
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestGetIntersectionNode(unittest.TestCase):

    def test_intersect(self):
        # 公共部分 [8->4->5]
        common = ListNode(8, ListNode(4, ListNode(5)))
        headA = ListNode(4, ListNode(1, common))
        headB = ListNode(5, ListNode(6, ListNode(1, common)))
        self.assertIs(get_intersection_node(headA, headB), common)

    def test_no_intersect(self):
        headA = ListNode(2, ListNode(6, ListNode(4)))
        headB = ListNode(1, ListNode(5))
        self.assertIsNone(get_intersection_node(headA, headB))


if __name__ == "__main__":
    unittest.main()
