# 02_binary_search：二分查找

> 在有序区间上对答案进行二分

## 解题框架

```python
# 查找目标值
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

# 查找左边界
while left < right:
    mid = left + (right - left) // 2
    if nums[mid] < target:
        left = mid + 1
    else:
        right = mid
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 33 | 搜索旋转排序数组 | 🟡 Medium | ⬜ |
| 34 | 在排序数组中查找第一个和最后一个位置 | 🟡 Medium | ⬜ |

## 关键思想

**旋转数组二分：** 一半一定有序，判断 target 在哪半边，收缩到对应半边。

**边界查找：** 左边界用 `right = mid`，右边界用 `left = mid`（注意 mid 取法防死循环）。
