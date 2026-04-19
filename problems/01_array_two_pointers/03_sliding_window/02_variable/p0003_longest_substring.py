#!/usr/bin/env python3
"""
LC 3. 无重复字符的最长子串
https://leetcode.com/problems/longest-substring-without-repeating-characters/

难度: 中等 | 字节跳动: ★★★★★ | 美团: ★★★★

给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。

示例:
  输入: s = "abcabcbb"
  输出: 3
  解释: 答案 "abc"，长度为 3

  输入: s = "bbbbb"
  输出: 1
  解释: 答案 "b"

Tags: 滑动窗口 | 哈希表 | 双指针
"""

import unittest


def length_of_longest_substring(s: str) -> int:
    """
    思路拆解：

    1. 暴力：枚举所有子串 O(n²)，判断重复 O(n) → O(n³) → 跳过
    2. 滑动窗口 + 哈希集合：
       - right 指针右移，把字符加入集合
       - 出现重复？→ 左指针右移收缩，直到不重复
       - 每步更新最大长度

    关键点：何时收缩左边界？如何判断字符已存在于当前窗口？
    """

    # ══════════════════════════════════════════════
    # 请在此处填写你的答案
    # ══════════════════════════════════════════════
    n = len(s)
    if not n:
        return 0
    left, right = 0,0
    cnt = {}
    max = -1
    for right in range(n):
        if s[right] not in cnt:
            cnt[s[right]] = ""
            diff = right - left + 1
            if diff > max:
                max = diff
            continue
        else:
            while s[left] != s[right]:
                cnt.pop(s[left]) 
                left += 1
            left+=1
    return max

# ─────────────────────────────────────────────────
class TestLongestSubstring(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(length_of_longest_substring("abcabcbb"), 3)

    def test_all_same(self):
        self.assertEqual(length_of_longest_substring("bbbbb"), 1)

    def test_empty(self):
        self.assertEqual(length_of_longest_substring(""), 0)

    def test_mixed(self):
        self.assertEqual(length_of_longest_substring("pwwkew"), 3)


if __name__ == "__main__":
    unittest.main()
