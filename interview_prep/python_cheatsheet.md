# Python 面试速查：刷题必备语法

> 面试时一时想不起来就完蛋的东西，按使用频率排序

---

## 1. 字符与数字转换

```python
ord('a')          # 97，字符→ASCII码
chr(97)           # 'a'，ASCII码→字符
ord('b') - ord('a')  # 1，常用：字符映射到0-25索引

# 字母判断
'a' <= ch <= 'z'  # 小写字母，Python支持链式比较
'A' <= ch <= 'Z'  # 大写字母
'0' <= ch <= '9'  # 数字字符
```

## 2. is vs ==

```python
a is b    # 比较身份（是否同一个对象，即id(a)==id(b)）
a == b    # 比较值（调用 __eq__）

# is 是关键字，不是函数，不能重载
# 面试常用：判断链表节点是否同一个
if slow is fast:     # 同一个节点，不是值相等
if node is None:     # 判空（推荐用is，不用==）

# 小整数池陷阱（面试别踩）
a = 256; b = 256;  a is b  # True
a = 257; b = 257;  a is b  # 可能False（-5~256被缓存）
```

## 3. list 常用操作（动态数组）

底层是动态数组：连续内存存引用，自动扩容（约2倍），尾部操作O(1)，头部操作O(n)

```python
lst = [1, 2, 3, 4]

# ── 添加 ──
lst.append(5)         # 末尾加 [1,2,3,4,5]，O(1) 均摊
lst.insert(0, 0)      # 头部插入 → O(n)！后面所有引用要后移，用deque代替

# ── pop 删除（按索引） ──
lst.pop()             # 弹末尾 → 5，O(1)，返回被删的值
lst.pop(0)            # 弹头部 → 1，O(n)！后面所有引用要前移，用deque代替
lst.pop(2)            # 弹索引2 → O(n-i)，越靠前越慢

# ── remove 删除（按值） ──
lst.remove(3)         # 删除第一个值为3的元素，O(n)，遍历找+移位
                       # 不存在会ValueError
                       # 只删第一个！[1,2,1].remove(1) → [2,1]

# ── del 删除（按索引/切片） ──
del lst[2]            # 删索引2，O(n-i)，不返回值
del lst[1:3]          # 删切片范围

# ── pop vs remove vs del ──
# pop(i)：按索引删，返回被删值，O(n-i)
# remove(v)：按值删第一个，不返回，O(n)
# del lst[i]：按索引删，不返回，O(n-i)
# 需要被删的值 → 用pop；按值删 → 用remove；删完不要值 → 用del

# ── 切片（面试常用） ──
lst[1:3]              # [2,3]
lst[::-1]             # 反转 [4,3,2,1]
lst[::2]              # 隔一个取 [1,3]
lst[1:]               # [2,3,4]
lst[:-1]              # [1,2,3]，去掉最后一个

# 排序
lst.sort()            # 原地排序，返回None
sorted(lst)           # 返回新列表
lst.sort(key=lambda x: x[1], reverse=True)  # 按第二元素降序
```

## 4. 字符串常用操作

```python
s = "hello world"

s.split()             # ['hello', 'world']，默认按空白分割
s.split(',')          # 按逗号分割
','.join(['a','b'])   # 'a,b'，拼接
s.strip()             # 去首尾空白
s.lstrip()            # 去左空白
s[::-1]               # 反转字符串

# 不可变！不能 s[0] = 'H'，要用 s = 'H' + s[1:]
# 拼接多用 ''.join()，少用 + 循环拼接（性能差）
```

## 5. 字典常用操作

```python
d = {'a': 1}

d.get('b', 0)         # 0，key不存在返回默认值（不报错）
d['b']                # KeyError！key不存在会报错

# 面试高频：计数
from collections import Counter
cnt = Counter("ababc")    # Counter({'a':2,'b':2,'c':1})
cnt['a']                   # 2
cnt.most_common(2)         # [('a',2),('b',2)]

# 面试高频：默认值字典
from collections import defaultdict
d = defaultdict(int)       # 不存在的key默认0
d = defaultdict(list)      # 不存在的key默认[]
d['a'].append(1)           # 不用判空直接append

# 面试高频：setdefault
d = {}
d.setdefault('a', []).append(1)  # 和defaultdict(list)效果一样
```

## 6. 集合常用操作

```python
s = set()
s.add(1)               # 添加
1 in s                 # True，O(1)查找
s.remove(1)            # 删除，不存在会KeyError
s.discard(1)           # 删除，不存在不报错

# 集合运算
a & b                  # 交集
a | b                  # 并集
a - b                  # 差集
```

## 7. 双端队列 deque

```python
from collections import deque

q = deque()
q.append(1)            # 右端加
q.appendleft(0)        # 左端加
q.pop()                # 右端弹 → 1，O(1)
q.popleft()            # 左端弹 → 0，O(1)

# list的pop(0)是O(n)，deque的popleft()是O(1)
# BFS用deque，不用list
```

## 8. 堆 heapq

```python
import heapq

# Python只有小顶堆！
h = []
heapq.heappush(h, 3)   # 入堆
heapq.heappush(h, 1)
heapq.heappop(h)        # 1，弹出最小值

heapq.heapify(lst)      # 原地建堆，O(n)

# 大顶堆技巧：取负数
heapq.heappush(h, -val)
val = -heapq.heappop(h)
```

## 9. 枚举与并行遍历

```python
# 带下标遍历
for i, val in enumerate(nums):
    pass

# 并行遍历
for a, b in zip(list1, list2):
    pass

# 带下标并行
for i, (a, b) in enumerate(zip(list1, list2)):
    pass
```

## 10. 排序高级用法

```python
# 按多个key排序
lst.sort(key=lambda x: (x[0], -x[1]))   # 先按第一元素升序，再按第二元素降序

# 二维矩阵按行排序
intervals.sort(key=lambda x: x[0])       # 区间题按左端点排序

# 稳定排序：相同key保持原顺序
```

## 11. 位运算

```python
n & 1              # 判断奇偶，1是奇数
n >> 1             # 除以2（向下取整）
n << 1             # 乘以2
n & (n-1)          # 消去最低位的1
bin(n).count('1')  # 1的个数

# 异或：a^a=0, a^0=a
# 只出现一次的数字：所有数异或一遍
```

## 12. 数学常量与运算

```python
float('inf')       # 正无穷
float('-inf')      # 负无穷
abs(x)             # 绝对值
max(a, b)          # 最大值
min(a, b)          # 最小值

# 整除与取模
7 // 2             # 3，整除（向下取整）
-7 // 2            # -4！Python整除向负无穷取整
7 % 2              # 1
-7 % 2             # 1！Python取模结果同号

import math
math.gcd(a, b)     # 最大公约数
```

## 13. 链表节点定义

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 构建链表
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)

# 虚拟头节点（链表题常用技巧）
dummy = ListNode(0, head)
curr = dummy
# ... 操作后
return dummy.next
```

## 14. 二叉树节点定义

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## 15. 类型转换

```python
int('123')          # 123
str(123)            # '123'
list("abc")         # ['a','b','c']
''.join(['a','b'])  # 'ab'

# 数字各位
n = 123
digits = list(str(n))     # ['1','2','3']
int_digits = [int(d) for d in str(n)]  # [1,2,3]
```

## 16. 列表推导式

```python
[x*x for x in range(10)]           # [0,1,4,9,...]
[x for x in range(10) if x%2==0]   # [0,2,4,6,8]
{c: i for i, c in enumerate("abc")}  # {'a':0,'b':1,'c':2}

# 矩阵初始化
matrix = [[0]*n for _ in range(m)]   # m行n列，正确！
# 错误写法：[[0]*n]*m  → 所有行是同一个引用！改一行全变！

# 矩阵基础操作（矩阵 = list 的 list，没有 .size()，用 len()）
rows = len(matrix)          # 行数
cols = len(matrix[0])       # 列数
matrix[i][j]                # 访问第i行第j列
matrix[i]                   # 取第i行（引用，改它原矩阵也变）
[row[j] for row in matrix]  # 取第j列（没有直接语法）

# 矩阵旋转（核心：转置 + 翻转的组合）
# 顺时针90° = 转置 + 每行左右翻转
# 逆时针90° = 每行翻转 + 转置（或转置 + 上下翻转）
# 180° = 上下翻转 + 左右翻转
```

## 17. 迭代器与 yield

```python
# ── 迭代器 ──
# 实现 __iter__ + __next__ 的对象，惰性求值，不存储数据
# 核心特点：按需生产，用一次少一次，耗尽后为空

r = reversed([1, 2, 3])   # 返回迭代器，不复制数据
list(r)                    # [3, 2, 1]  消耗掉了
list(r)                    # []         已空，不能重复用

# for 循环底层就是迭代器协议：iter() 拿迭代器，反复 __next__() 直到 StopIteration
# range, dict, 文件对象, zip, enumerate 等都走这套协议

# ── yield（生成器函数）──
# yield 是写迭代器最便捷的方式，函数里有 yield 就自动变成迭代器
# yield = 生产端，定义怎么一个一个给值
# for  = 消费端，遍历已有的值

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a           # 算出一个就交出去，暂停，下次从这里继续
        a, b = b, a + b

for x in fib(10):         # 和遍历列表用法一样，但省内存
    print(x)

# ── 原地操作 vs 非原地 ──
# 原地操作（修改原数据，返回 None，不能赋值）：
lst.reverse()              # 原地翻转，返回 None
lst.sort()                 # 原地排序，返回 None
# 错误：lst = lst.reverse()  → lst 变成 None！

# 非原地操作（返回新对象）：
lst[::-1]                  # 返回新列表
reversed(lst)              # 返回迭代器
sorted(lst)                # 返回新列表
```

## 18. 面试易错陷阱

```python
# 1. list的*复制是浅拷贝
a = [[0]] * 3        # 三个元素是同一个列表！
a[0][0] = 1          # a变成[[1],[1],[1]]

# 2. 函数默认参数只创建一次
def foo(lst=[]):     # 危险！lst在调用间共享
    lst.append(1)
    return lst
foo()  # [1]
foo()  # [1,1]  不是[1]！

# 3. 整除负数
-3 // 2              # -2，不是-1
# 要向0取整用 int(-3/2)  # -1

# 4. 闭包变量
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]  # [2,2,2] 不是[0,1,2]！
# 修正：lambda i=i: i

# 5. 删除列表元素时倒着删
# 正序删会跳过元素，因为删后索引变了
for i in range(len(lst)-1, -1, -1):
    if condition:
        del lst[i]
```
