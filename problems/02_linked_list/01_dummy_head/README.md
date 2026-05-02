# 01_dummy_head：虚拟头节点

> 在链表前加一个不存数据的假节点，统一头节点的操作逻辑

## 核心特征

- 删除头节点和删除中间节点的逻辑不同，dummy 让它们统一
- 返回结果时取 `dummy.next`

## 解题框架

```python
dummy = ListNode(0, head)
prev = dummy
curr = head
while curr:
    if 需要删除 curr:
        prev.next = curr.next
    else:
        prev = curr
    curr = curr.next
return dummy.next
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 19 | 删除链表的倒数第 N 个节点 | 🟡 Medium | ⬜ |
| 21 | 合并两个有序链表 | 🟢 Easy | ⬜ |
| 23 | 合并 K 个升序链表 | 🔴 Hard | ⬜ |

## 关键思想

**为什么不用 dummy 就容易出 bug？**
不 dummy 时，删除头节点需要 `head = head.next`，删除中间节点用 `prev.next = prev.next.next`，两套逻辑。加了 dummy 后，头节点也变成了"中间节点"的删除方式。
