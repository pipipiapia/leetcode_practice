#!/usr/bin/env python3
"""
LC 21. 合并两个有序链表
https://leetcode.com/problems/merge-two-sorted-lists/

难度: 简单 | 字节跳动: ★★★★★ | 腾讯: ★★★★

将两个升序链表合并为一个新的升序链表并返回。
新链表是通过拼接给定的两个链表的所有节点组成的。

示例:
  输入: l1 = 1 -> 2 -> 4,  l2 = 1 -> 3 -> 4
  输出: 1 -> 1 -> 2 -> 3 -> 4 -> 4

Tags: 链表 | 递归
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    思路拆解：

    方法一：迭代（虚拟头节点）
      - 创建 dummy 节点作为结果链表的头
      - 比较 l1 和 l2 的当前节点，小的接入结果
      - 最后把剩下的那个链表接上

    方法二：递归
      - base case: 任意一个链表为空，直接返回另一个
      - 递归公式: 较小的那个节点.next = 递归合并(较小的.next, 另一个)

    关键点：为什么递归写法更简洁？它利用了什么性质？
    """

    # ═══════════════════════════════════════════════
    dummy = ListNode()
    p = dummy
    while l1 and l2:
        if l1.val >= l2.val:
            p.next = l2
            l2 = l2.next
        else:
            p.next = l1
            l1 = l1.next
        p = p.next
    p.next = l1 if l1 else l2 ### 注意这里掉了！！！
    return dummy.next
    # ═══════════════════════════════════════════════
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


class TestMergeTwoLists(unittest.TestCase):

    def test_basic(self):
        l1 = build_list([1, 2, 4])
        l2 = build_list([1, 3, 4])
        self.assertEqual(to_list(merge_two_lists(l1, l2)), [1, 1, 2, 3, 4, 4])

    def test_one_empty(self):
        self.assertEqual(to_list(merge_two_lists(None, build_list([0]))), [0])

    def test_both_empty(self):
        self.assertEqual(to_list(merge_two_lists(None, None)), [])


if __name__ == "__main__":
    unittest.main()
