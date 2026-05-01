#!/usr/bin/env python3
"""
LC 238. 除自身以外数组的乘积
https://leetcode.com/problems/product-of-array-except-self/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个整数数组 nums，返回数组 answer，其中 answer[i] 等于 nums 中除 nums[i] 之外
其余各元素的乘积。不能使用除法，且时间复杂度为 O(n)。

示例:
  输入: nums = [1, 2, 3, 4]
  输出: [24, 12, 8, 6]
  解释: answer[0]=2*3*4=24, answer[1]=1*3*4=12 ...

进阶: 额外空间复杂度为 O(1)（输出数组不计入空间）

Tags: 数组 | 前缀积 | 前后缀分解
"""

import unittest


def product_except_self(nums: list[int]) -> list[int]:
    """
    思路拆解：

    answer[i] = 左边所有元素的乘积 × 右边所有元素的乘积

    两次遍历（O(n) 空间版）：
      left[i]  = nums[0] * nums[1] * ... * nums[i-1]
      right[i] = nums[i+1] * ... * nums[n-1]
      answer[i] = left[i] * right[i]

    空间优化（O(1) 版）：
      第一次正向遍历：answer[i] = 左侧乘积（复用 answer 数组）
      第二次反向遍历：answer[i] *= 右侧乘积（用一个变量 R 滚动）
    """
    # ══════════════════════════════════════════════
    n = len(nums)
    answer = [1] * n

    # 第一次：answer[i] = nums[0..i-1] 的乘积
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # 第二次：answer[i] *= nums[i+1..n-1] 的乘积
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
    # ══════════════════════════════════════════════


# ─────────────────────────────────────────────────
class TestProductExceptSelf(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_with_zero(self):
        self.assertEqual(product_except_self([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])

    def test_two_elements(self):
        self.assertEqual(product_except_self([2, 3]), [3, 2])


if __name__ == "__main__":
    unittest.main()
