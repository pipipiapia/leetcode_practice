# 01_one_dim：一维动态规划

> 状态为一维数组的 DP 问题

## 解题框架

```python
# 一维 DP 模板
dp = [0] * (n + 1)
dp[0] = 初始值
for i in range(1, n + 1):
    dp[i] = 转移方程(dp, i)
return dp[n]
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 53 | 最大子数组和 | 🟡 Medium | ⬜ |
| 70 | 爬楼梯 | 🟢 Easy | ⬜ |
| 121 | 买卖股票的最佳时机 | 🟢 Easy | ⬜ |
| 139 | 单词拆分 | 🟡 Medium | ⬜ |
| 198 | 打家劫舍 | 🟡 Medium | ⬜ |
| 322 | 零钱兑换 | 🟡 Medium | ⬜ |

## 关键思想

**最大子数组和：** dp[i] = max(dp[i-1] + nums[i], nums[i])，要么接上去，要么重新开始。

**零钱兑换：** dp[i] = min(dp[i - coin] + 1 for coin in coins)，完全背包问题。
