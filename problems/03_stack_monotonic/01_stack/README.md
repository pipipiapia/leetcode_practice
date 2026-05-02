# 01_stack：栈

> 后进先出（LIFO），处理"最近相关性"和"嵌套结构"问题

## 核心特征

- 括号匹配：遇到左括号入栈，遇到右括号出栈匹配
- 表达式求值：用栈处理运算符优先级
- 最小栈：辅助栈同步记录当前最小值

## 解题框架

```python
# 括号匹配
stack = []
pairs = {')': '(', ']': '[', '}': '{'}
for ch in s:
    if ch in pairs.values():
        stack.append(ch)
    elif ch in pairs:
        if not stack or stack.pop() != pairs[ch]:
            return False

# 最小栈
stack = []
min_stack = []           # 同步记录每个位置的最小值
```

## 题目清单

| 题号 | 题名 | 难度 | 状态 |
|------|------|------|------|
| 20 | 有效的括号 | 🟢 Easy | ⬜ |
| 155 | 最小栈 | 🟡 Medium | ⬜ |
| 394 | 字符串解码 | 🟡 Medium | ⬜ |

## 关键思想

**最小栈为什么需要辅助栈？**
单个栈无法在 O(1) 内获取最小值。辅助栈与主栈同步 push/pop，始终在栈顶记录当前最小值。
