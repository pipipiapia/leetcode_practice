#!/usr/bin/env python3
"""
LC 209. 长度最小的子数组
https://leetcode.com/problems/minimum-size-subarray-sum/

难度: 中等 | 字节跳动: ★★★★ | 美团: ★★★

给定一个【正】【整数数组】 nums 和一个【正整数】 target，找长度最小的连续子数组，
使该子数组的元素和 >= target。返回其长度；若不存在这样的子数组，返回 0。

进阶：你能用 O(n) 时间复杂度解决吗？

示例:
  输入: nums = [2,3,1,4,3], target = 7
  输出: 2（子数组 [4,3] 的和为 7，长度为 2）

！！！注意！！！：滑动窗口不是在做选择，而是穷举了所有可能的右端点，对每个右端点精确找到了最短窗口。
只有正整数情况，滑动窗口才成立！！！

Tags: 数组 | 滑动窗口 | 可变窗口
"""

from turtle import right
import unittest


def min_subarray_len(nums: list[int], target: int) -> int:
    """
    思路拆解：

    可变窗口滑动窗口：
    - 右指针扩展窗口，记录当前和
    - 当 sum >= target 时，尝试收缩左指针（记录最短长度）
    - 持续向右扩展，直到遍历完数组

    核心：窗口只能增大（right++）或缩小（left++），每个元素最多被访问两次
    时间 O(n)，空间 O(1)

    ！！！出错！！！：sum >= target 时只收缩一次就停了，收缩一次后 sum 可能仍然 >= target，应该持续收缩直到 sum < target，这样才能找到以当前 right 为右端点的最短窗口。
    """
    # ══════════════════════════════════════════════
    left, right = 0, 0
    n = len(nums)
    s_sum = 0
    ret = n+1
    for right in range(n):
        s_sum = s_sum + nums[right]
        while s_sum >= target:
            diff = right - left + 1
            if diff < ret:
                ret = diff
            s_sum -= nums[left]
            left += 1

    return ret if ret != n + 1 else 0
    # ══════════════════════════════════════════════
    


# ─────────────────────────────────────────────────
class TestMinSubarray(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(min_subarray_len([2, 3, 1, 4, 3], 7), 2)

    def test_no_solution(self):
        self.assertEqual(min_subarray_len([1, 1, 1], 100), 0)

    def test_single(self):
        self.assertEqual(min_subarray_len([1, 4, 4], 4), 1)

    def test_negative(self):
        self.assertEqual(min_subarray_len([-1, 2, 3], 6), 0)


if __name__ == "__main__":
    unittest.main()
