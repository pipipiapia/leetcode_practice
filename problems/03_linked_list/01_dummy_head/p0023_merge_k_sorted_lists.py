#!/usr/bin/env python3
"""
LC 23. 合并 K 个升序链表
https://leetcode.com/problems/merge-k-sorted-lists/

难度: 困难 | 字节跳动: ★★★★★ | 腾讯: ★★★★★

给你一个链表数组，每个链表都已经按升序排列，请你将所有链表合并到一个升序链表中。

示例:
  输入: [[1->4->5], [1->3->4], [2->6]]
  输出: 1->1->2->3->4->4->5->6

方法一（推荐）：最小堆 O(N log k)，N 为总节点数，k 为链表数
方法二：分治合并 O(N log k)
方法三：逐一合并 O(Nk) —— 不推荐

Tags: 链表 | 堆 | 分治
"""

import unittest
import heapq
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val  # 让 heapq 可以比较节点


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    思路拆解：

    最小堆：始终从 k 个链表的头节点中取最小值
    - 初始化：将所有非空链表头节点入堆
    - 每次 pop 最小节点，加入结果链表，并把该节点的 next 入堆
    - 直到堆为空

    时间 O(N log k)：每个节点入堆/出堆各一次，每次操作 O(log k)
    空间 O(k)：堆中最多 k 个节点
    """
    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
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


class TestMergeKLists(unittest.TestCase):

    def test_basic(self):
        lists = [list_to_nodes([1, 4, 5]), list_to_nodes([1, 3, 4]), list_to_nodes([2, 6])]
        self.assertEqual(nodes_to_list(merge_k_lists(lists)), [1, 1, 2, 3, 4, 4, 5, 6])

    def test_empty(self):
        self.assertIsNone(merge_k_lists([]))

    def test_single(self):
        self.assertEqual(nodes_to_list(merge_k_lists([list_to_nodes([1, 2])])), [1, 2])


if __name__ == "__main__":
    unittest.main()
