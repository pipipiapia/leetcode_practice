# 03_fast_slow：快慢指针

> 两个指针以不同速度遍历链表，用于判环、找中间节点

## 核心特征

- 慢指针走 1 步，快指针走 2 步
- 有环则快慢指针必相遇；无环则快指针先到终点
- 找中间节点：快指针到终点时，慢指针恰在中间

## 解题框架

```python
# 判环
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        return True

# 找入环点：相遇后，一个从 head 走，一个从相遇点走，再相遇即为入环点
entry = head
while entry is not slow:
    entry = entry.next
    slow = slow.next
return entry
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 141 | 环形链表 | 🟢 Easy | ✅ |
| 142 | 环形链表 II | 🟡 Medium | ✅ |
| 160 | 相交链表 | 🟢 Easy | ⬜ |

## 关键思想

**为什么快指针走 2 步一定能追上？**
每轮快慢指针的距离缩短 1，有环内有限步必相遇。走 3 步则可能跳过（距离不单调递减）。

**找入环点的数学证明？**
相遇时 slow 走了 a+b 步，fast 走了 a+b+c+b 步。因为 2(a+b)=a+2b+c，得 a=c。所以一个从 head 走 a 步，一个从相遇点走 c 步，恰在入环点相遇。
