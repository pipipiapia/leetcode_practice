#!/usr/bin/env python3
"""
LC 39. 组合总和
https://leetcode.com/problems/combination-sum/

难度: 中等 | 字节跳动: ★★★★★ | 腾讯: ★★★★

给你一个无重复元素的整数数组 candidates 和一个目标整数 target，
找出 candidates 中可以使数字和为目标数 target 的所有不同组合（同一个数可以无限次选取）。

示例:
  输入: candidates=[2,3,6,7], target=7
  输出: [[2,2,3],[7]]

Tags: 数组 | 回溯
"""

import unittest


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    思路拆解：

    回溯 + 剪枝：
    - 从当前 start 开始选（避免重复）
    - 每个数可以重复选（下一层从同一个 start 开始）
    - 若 remaining < 0：剪枝
    - 若 remaining == 0：找到一个合法组合

    排序后可以提前剪枝（当 candidates[i] > remaining 时后面都不用看）
    # 回溯的基本框架
    def backtrack(路径, 选择列表):
        if 满足结束条件:
            记录答案
            return
        for 选择 in 选择列表:
            做选择（路径加入）
            backtrack(路径, 新选择列表)   # 递归深入
            撤销选择（路径移除）
    ！！！注意！！！没有 start 的话，你得到的是排列（有顺序），不是组合（无顺序）。 题目要求的是组合，所以 start 是必须的，不是优化。
    """
    # ═════════════════════════════════════════════
    ret = []
    def traceback(candidates, start, target, trace):
        if target < 0:
            return 
        elif target == 0:
            return ret.append(trace[:])
            ####   ret.append(trace[:])        # 存拷贝
        else:
            for i in range(start, len(candidates)):
                trace.append(candidates[i])
                traceback(candidates, i, target-candidates[i], trace)
                trace.pop(-1)
        
    traceback(candidates, 0, target, [])
    return ret
    
    # ═══════════════════════════════════════════════
# ─────────────────────────────────────────────────
class TestCombinationSum(unittest.TestCase):

    def test_basic(self):
        result = combination_sum([2, 3, 6, 7], 7)
        self.assertIn([2, 2, 3], result)
        self.assertIn([7], result)

    def test_no_solution(self):
        self.assertEqual(combination_sum([2], 1), [])


if __name__ == "__main__":
    unittest.main()
