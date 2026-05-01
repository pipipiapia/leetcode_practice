#!/usr/bin/env python3
"""
LC 206. 反转链表
https://leetcode.com/problems/reverse-linked-list/

难度: 简单 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你单链表的头节点 head，请你反转链表，并返回反转后的链表。

示例:
  输入: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
  输出: 5 -> 4 -> 3 -> 2 -> 1 -> NULL

Tags: 链表 | 递归
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: ListNode) -> ListNode:
    """
    思路拆解：

    方法一：迭代（双指针）
      - prev = None, cur = head
      - while cur:
          nxt = cur.next   # 先保存下一个
          cur.next = prev  # 反转指向
          prev = cur       # prev 前移
          cur = nxt        # cur 前移
      - return prev

    方法二：递归
      - 递归反转 head 之后的链表，返回新头
      - 处理 head.next.next = head，完成局部反转

    关键点：递归的终止条件是什么？最后一步怎么接？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案（迭代版）
    # ══════════════════════════════════════════════
    pass


def reverse_list_recursive(head: ListNode) -> ListNode:
    """
    递归版本 - 请在这里实现
    """
    # ══════════════════════════════════════════════
    # 请在此处填写你的答案（递归版）
    # ══════════════════════════════════════════════
    pass


# ─────────────────────────────────────────────────
def build_list(values: list[int]) -> ListNode:
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def to_list(head: ListNode) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


class TestReverseList(unittest.TestCase):

    def test_basic(self):
        head = build_list([1, 2, 3, 4, 5])
        result = to_list(reverse_list(head))
        self.assertEqual(result, [5, 4, 3, 2, 1])

    def test_two_elements(self):
        head = build_list([1, 2])
        self.assertEqual(to_list(reverse_list(head)), [2, 1])

    def test_single(self):
        head = build_list([1])
        self.assertEqual(to_list(reverse_list(head)), [1])


if __name__ == "__main__":
    unittest.main()
