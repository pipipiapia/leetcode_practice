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

    ！！注意！！：dummy 就是一个"不存在的前驱"，让头节点也有了一个 prev，删除逻辑统一，不用写 if 特判。
    """
    # ═══════════════════════════════════════════════
    dummy = ListNode()
    dummy.next = head
    fast = head
    cnt = 0
    pre = dummy ## slow是多余的，要删除一个节点，需要的是上一个节点就足够了！！
    while fast:
        cnt += 1
        if cnt >= n+1:
            pre =pre.next
        fast = fast.next
    pre.next = pre.next.next
    return dummy.next

    # ═══════════════════════════════════════════════
    标准写法：
    # dummy = ListNode(0, head)
    # fast = slow = dummy        # 都从 dummy 开始
    # for _ in range(n):         # fast 先走 n 步
    #     fast = fast.next
    # while fast.next:           # fast 到最后一个节点时停
    #     fast = fast.next
    #     slow = slow.next       # slow.next 就是要删的节点
    # slow.next = slow.next.next  # 删除
    # return dummy.next
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
