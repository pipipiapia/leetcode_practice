# 02_fast_slow：快慢指针

> 两个指针以不同速度遍历，常用于链表判环、删除重复元素

## 核心特征

- 链表场景：快指针走两步，慢指针走一步
- 数组场景：快慢指针用于原地修改数组
- 核心思想：用不同速度"追上"或"分隔"数据

## 解题框架

**链表判环：**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # 有环
return False
```

**数组原地修改：**
```python
slow = 0
for fast in range(len(nums)):
    if nums[fast] != val:
        nums[slow] = nums[fast]
        slow += 1
return slow
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 26 | 删除有序数组中的重复项 | 🟢 Easy | ⬜ |
| 27 | 移除元素 | 🟢 Easy | ⬜ |
| 141 | 环形链表 | 🟢 Easy | ⬜ |
| 142 | 环形链表 II | 🟡 Medium | ⬜ |
