#!/usr/bin/env python3
"""
LC 141: 环形链表
https://leetcode.com/problems/linked-list-cycle/

难度: 简单 | 字节跳动: ★★★★ | 腾讯: ★★★★

给你一个链表的头节点 head，判断链表中是否有环。
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。

示例:
  输入: head = [3,2,0,-4], pos = 1（尾节点指向索引1的节点）
  输出: true

进阶：你能用 O(1)（即常量）内存解决此题吗？

Tags: 链表 | 双指针 | Floyd 判圈
"""

import unittest


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode) -> bool:
    """
    思路拆解：

    方法：Floyd 判圈算法（快慢指针）
      - slow 每次走一步，fast 每次走两步
      - 有环：fast 和 slow 必然在某点相遇
      - 无环：fast 先到 None

    为什么 fast 走两步就够？走三步行不行？
    """

    # ═══════════════════════════════════════════════
    pass
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
def build_cycle_list(values: list[int], pos: int) -> ListNode:
    """构造带环链表，pos=-1 表示无环"""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0]


class TestHasCycle(unittest.TestCase):

    def test_has_cycle(self):
        head = build_cycle_list([3, 2, 0, -4], 1)
        self.assertTrue(has_cycle(head))

    def test_no_cycle(self):
        head = build_cycle_list([1, 2, 3], -1)
        self.assertFalse(has_cycle(head))

    def test_single_node_cycle(self):
        head = ListNode(1)
        head.next = head
        self.assertTrue(has_cycle(head))


if __name__ == "__main__":
    unittest.main()
