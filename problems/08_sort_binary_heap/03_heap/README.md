# 03_heap：堆

> Python 只有小顶堆（heapq），大顶堆用取负数模拟

## 解题框架

```python
import heapq

# 小顶堆
h = []
heapq.heappush(h, val)       # 入堆
heapq.heappop(h)             # 弹最小值
heapq.heapify(lst)           # 原地建堆 O(n)

# 大顶堆：取负数
heapq.heappush(h, -val)
val = -heapq.heappop(h)

# 第 K 大 = 小顶堆维持大小 K
# Top K 频率 = 堆中存 (-频率, 元素)
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 215 | 数组中的第 K 个最大元素 | 🟡 Medium | ⬜ |
| 347 | 前 K 个高频元素 | 🟡 Medium | ⬜ |

## 关键思想

**第 K 大 = 小顶堆只留 K 个：** 超过 K 就 pop 掉最小的，堆顶就是第 K 大。

**Top K 频率：** 先 Counter 计数，再堆排序，O(n logk)。
