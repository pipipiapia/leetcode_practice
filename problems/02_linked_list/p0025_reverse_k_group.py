#!/usr/bin/env python3
"""
LC 25: K 个一组翻转链表
https://leetcode.com/problems/reverse-nodes-in-k-group/

难度: 困难 | 字节跳动: ★★★★★ | 快手: ★★★★

给你链表的头节点 head，每 k 个节点一组进行翻转，返回翻转后的链表。
k 是一个正整数，且小于等于链表长度。
如果节点总数不是 k 的整数倍，则保持原有顺序。

示例:
  输入: head = [1,2,3,4,5], k = 2
  输出: [2,1,4,3,5]

  输入: head = [1,2,3,4,5], k = 3
  输出: [3,2,1,4,5]

Tags: 链表 | 递归 | 迭代
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_k_group(head: ListNode, k: int) -> ListNode:
    """
    思路拆解：

    三步走（每组反转通用模式）：
      1. 计数：检查剩余节点数够不够 k 个，不够直接返回
      2. 反转：反转当前 k 个节点（头插法）
      3. 接上：把反转后的子链表接到前后两端

    关键点：如何保存"下一组"的起始节点？
            反转后 prev 和 curr 分别指向哪里？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
def list_to_linkedlist(lst: list[int]) -> ListNode:
    if not lst:
        return None
    dummy = ListNode(0)
    cur = dummy
    for val in lst:
        cur.next = ListNode(val)
        cur = cur.next
    return dummy.next


def linkedlist_to_list(node: ListNode) -> list[int]:
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


class TestReverseKGroup(unittest.TestCase):

    def test_k2(self):
        head = list_to_linkedlist([1, 2, 3, 4, 5])
        self.assertEqual(linkedlist_to_list(reverse_k_group(head, 2)), [2, 1, 4, 3, 5])

    def test_k3(self):
        head = list_to_linkedlist([1, 2, 3, 4, 5])
        self.assertEqual(linkedlist_to_list(reverse_k_group(head, 3)), [3, 2, 1, 4, 5])

    def test_k1(self):
        head = list_to_linkedlist([1, 2, 3])
        self.assertEqual(linkedlist_to_list(reverse_k_group(head, 1)), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
