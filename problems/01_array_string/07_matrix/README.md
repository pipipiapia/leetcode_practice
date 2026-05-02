# 07_matrix：矩阵操作

> 二维数组上的原地操作、模拟遍历

## 核心特征

- 矩阵 = list 的 list，用 `len(matrix)` 取行数，`len(matrix[0])` 取列数
- 旋转 = 转置 + 翻转的组合
- 螺旋遍历 = 按层收缩边界

## 解题框架

```python
# 顺时针旋转 90° = 转置 + 左右翻转
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
for row in matrix:
    row.reverse()

# 螺旋遍历
top, bottom, left, right = 0, m-1, 0, n-1
while top <= bottom and left <= right:
    遍历上边 → 右边 → 下边 → 左边
    top += 1; bottom -= 1; left += 1; right -= 1
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 48 | 旋转图像 | 🟡 Medium | ✅ |
| 54 | 螺旋矩阵 | 🟡 Medium | ⬜ |
| 73 | 矩阵置零 | 🟡 Medium | ⬜ |

## 关键思想

**旋转为什么等价于转置+翻转？**
原位置 (i, j) 顺时针 90° 后应到 (j, n-1-i)。转置 (i,j)→(j,i)，左右翻转 (j,i)→(j, n-1-i)，两步合起来刚好。

**矩阵置零怎么 O(1) 空间？**
用第一行和第一列作为标记数组，再单独记录第一行和第一列本身是否需要置零。
