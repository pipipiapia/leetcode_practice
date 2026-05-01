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
    """
    # ══════════════════════════════════════════════
    result = []
    candidates.sort()

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(list(path))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                           # 剪枝
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i 不 +1，可重复选
            path.pop()

    backtrack(0, [], target)
    return result
    # ══════════════════════════════════════════════


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
