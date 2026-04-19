#!/usr/bin/env python3
"""
Q05: ReLU vs Sigmoid

面试常问：
1. 为什么需要非线性激活函数？
2. ReLU 相比 Sigmoid 有哪些优势？
3. ReLU 的缺点是什么？有哪些改进版本？

核心：若无非线性激活函数，多层网络 = 单层线性变换
  y = W1·(W2·x + b2) + b1 = (W1·W2)·x + (W1·b2 + b1) = W·x + b
  加多少层都没用，相当于没有隐藏层。

ReLU 优势（vs Sigmoid）：
  ① 计算快：max(0,x) vs 1/(1+e^-x)  （无 exp 运算）
  ② 梯度不易消失：正区间梯度恒为 1（sigmoid 饱和区梯度→0）
  ③ 稀疏激活性：负区间直接输出 0，产生稀疏表示

ReLU 缺点：
  Dead ReLU Problem：负区间梯度为 0，神经元可能永久死亡
  （参数初始化不当或学习率过大时容易发生）
"""

import numpy as np
import unittest


def relu(x):
    """ReLU: max(0, x)"""
    return np.maximum(0, x)


def relu_grad(x):
    """ReLU 的梯度：正区间=1，负区间=0"""
    return (x > 0).astype(float)


def sigmoid(x):
    """Sigmoid: 1 / (1 + e^-x)"""
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid_grad(x):
    """Sigmoid 梯度: σ(x)(1 - σ(x))"""
    s = sigmoid(x)
    return s * (1 - s)


def leaky_relu(x, alpha=0.01):
    """Leaky ReLU: x if x > 0 else αx
    改进 Dead ReLU：负区间有小的梯度
    """
    return np.where(x > 0, x, alpha * x)


def elu(x, alpha=1.0):
    """ELU: x if x > 0 else α(e^x - 1)
    优点：负区间输出接近 0，均值接近 0（收敛更快）
    """
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))


def gelu(x):
    """GELU: 高斯误差线性单元（BERT/GPT 等常用）
    ≈ 0.5x · (1 + tanh(√(2/π)(x + 0.044715x³)))
    """
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


class TestActivations(unittest.TestCase):

    def test_relu_properties(self):
        """验证 ReLU 性质"""
        x = np.array([-2, -1, 0, 1, 2])
        self.assertTrue(np.all(relu(x) == np.array([0, 0, 0, 1, 2])))
        self.assertTrue(np.all(relu_grad(x) == np.array([0, 0, 1, 1, 1])))

    def test_sigmoid_range(self):
        """验证 Sigmoid 输出在 (0, 1)"""
        x = np.array([-10, 0, 10])
        s = sigmoid(x)
        self.assertTrue(np.all(s > 0) and np.all(s < 1))

    def test_leaky_relu_no_dead(self):
        """验证 Leaky ReLU 负区间有梯度"""
        x = np.array([-2.0, -1.0])
        grad = np.where(x > 0, 1.0, 0.01)  # LeakyReLU 的梯度
        self.assertTrue(np.all(grad > 0))  # 永远不会死


if __name__ == "__main__":
    print("=" * 50)
    print("激活函数对比")
    print("=" * 50)

    x = np.linspace(-5, 5, 100)

    print(f"\nx = {x[:5]} ... {x[-5:]}")
    print(f"\nReLU:        {relu(x)[:5].round(3)} ... {relu(x)[-5:].round(3)}")
    print(f"LeakyReLU:   {leaky_relu(x)[:5].round(3)} ... {leaky_relu(x)[-5:].round(3)}")
    print(f"Sigmoid:     {sigmoid(x)[:5].round(3)} ... {sigmoid(x)[-5:].round(3)}")
    print(f"ELU:         {elu(x)[:5].round(3)} ... {elu(x)[-5:].round(3)}")
    print(f"GELU:        {gelu(x)[:5].round(3)} ... {gelu(x)[-5:].round(3)}")

    print("\n梯度对比（x = [-2, 0, 2]）：")
    x_sample = np.array([-2.0, 0.0, 2.0])
    print(f"ReLU梯度:       {relu_grad(x_sample)}")
    print(f"Sigmoid梯度:    {sigmoid_grad(x_sample).round(4)}")
    print(f"LeakyReLU梯度:  {np.where(x_sample > 0, 1.0, 0.01)}")
    print(f"→ Sigmoid 在极端值时梯度接近 0（梯度消失）")
    print(f"→ ReLU 在负区间梯度 = 0（Dead ReLU）")
    print(f"→ LeakyReLU 负区间有小梯度，不会死")

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: 为什么需要非线性激活函数？
A: 多层线性叠加 = 单层线性，隐藏层没有意义。
   非线性让网络能拟合任意复杂函数。

Q: ReLU 的 Dead ReLU 问题怎么解决？
A: ① 用 LeakyReLU / PReLU / ELU 替代
   ② 好的权重初始化（He 初始化）
   ③ 学习率不要设太大
   ④ Batch Normalization

Q: 为什么 ReLU 收敛比 Sigmoid 快？
A: Sigmoid 的梯度在 (0, 1) 之间，链式法则乘下去会指数衰减（梯度消失）。
   ReLU 正区间梯度恒为 1，梯度传递畅通，收敛更快。

Q: ReLU 输出有什么特点？
A: 输出有稀疏性（负区间输出 0），类似生物神经元的稀疏激活。
   但也意味着负值信息完全丢失。
""")

    unittest.main(verbosity=2)
