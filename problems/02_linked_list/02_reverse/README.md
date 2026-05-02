# 02_reverse：链表反转

> 链表最核心的指针操作技巧

## 核心特征

- 反转 = 修改 next 指针方向
- 局部反转需要记录前驱和后继
- k 组反转 = 局部反转 + 递归/迭代拼接

## 解题框架

```python
# 整体反转
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev

# 局部反转 [left, right]
# 先走到 left-1，反转 left 到 right，再拼接
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 206 | 反转链表 | 🟢 Easy | ⬜ |
| 92 | 反转链表 II | 🟡 Medium | ⬜ |
| 25 | K 个一组翻转链表 | 🔴 Hard | ⬜ |

## 关键思想

**反转的三指针是什么？**
`prev`（已反转部分的头）、`curr`（当前处理节点）、`nxt`（暂存下一个，防断链）。每轮把 `curr.next` 指向 `prev`，然后三个指针各走一步。
