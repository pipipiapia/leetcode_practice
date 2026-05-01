#!/usr/bin/env python3
"""
LC 146: LRU 缓存
https://leetcode.com/problems/lru-cache/

难度: 中等 | 字节跳动: ★★★★★ | 美团: ★★★★

请你设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构。
- get(key)：如果 key 存在于缓存中，则获取值并将该 key 标记为最近使用；否则返回 -1。
- put(key, value)：如果 key 已存在，则更新其值并标记为最近使用；
  如果不存在，则插入；当缓存达到容量时，应在插入新条目之前驱逐最久未使用的条目。

示例:
  LRUCache(2)
  put(1, 1)
  put(2, 2)
  get(1)    → 1
  put(3, 3) → 淘汰 key=2
  get(2)    → -1（已淘汰）
  put(4, 4) → 淘汰 key=1
  get(1)    → -1
  get(3)    → 3
  get(4)    → 4

Tags: 设计 | 哈希表 | 链表
"""

import unittest


class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    思路拆解：

    数据结构：哈希表 + 双向链表
      - 哈希表：O(1) 查找 key 对应的节点
      - 双向链表：O(1) 插入/删除节点，头部是最久未使用，尾部是最新

    两种实现方式：
      1. Python OrderedDict（面试不推荐：没展示设计能力）
      2. 手写双向链表（推荐：展示数据结构设计能力）

    核心操作：
      - get：找到节点 → 移到尾部（标记为最新）
      - put：存在则更新值并移到尾部；不存在则插入尾部，超容量则删除头部节点
    """

    def __init__(self, capacity: int):
        # ══════════════════════════════════════════════
        # 请在此处填写 __init__ 实现
        # ══════════════════════════════════════════════
        pass

    def get(self, key: int) -> int:
        # ══════════════════════════════════════════════
        # 请在此处填写 get 实现
        # ══════════════════════════════════════════════
        pass

    def put(self, key: int, val: int) -> None:
        # ══════════════════════════════════════════════
        # 请在此处填写 put 实现
        # ══════════════════════════════════════════════
        pass


# ─────────────────────────────────────────────────
class TestLRUCache(unittest.TestCase):

    def test_basic(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.put(3, 3)
        self.assertEqual(cache.get(2), -1)
        cache.put(4, 4)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)


if __name__ == "__main__":
    unittest.main()
