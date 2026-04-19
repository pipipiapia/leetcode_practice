#!/usr/bin/env python3
"""
Q17: PyTorch autograd 梯度计算

面试常问：
1. PyTorch 的动态计算图是如何工作的？
2. 如何手动计算梯度？
3. torch.no_grad() 和 model.eval() 的区别？
4. 梯度为什么需要清零（optimizer.zero_grad）？

动态计算图（DAG）：
  每次 forward 时自动构建，backward 时从根到叶逐层计算梯度
  每次迭代从头重建，支持任意 Python 控制流

叶子节点：requires_grad=True 的输入张量
根节点：调用 .backward() 的输出张量
"""

import torch
import torch.nn.functional as F
import numpy as np


def demo_basic_grad():
    """最基础的梯度计算"""
    print("=" * 50)
    print("基础梯度计算")
    print("=" * 50)

    x = torch.tensor([1., 2., 3.], requires_grad=True)
    y = x ** 2 + 3 * x
    loss = y.sum()

    print(f"x = {x}")
    print(f"y = x^2 + 3x = {y}")
    print(f"loss = sum(y) = {loss}")

    loss.backward()

    print(f"\n∂loss/∂x = {x.grad}")
    print("验证: ∂(x^2+3x)/∂x = 2x + 3 = [5, 7, 9] ✓" if
          torch.allclose(x.grad, 2 * x + 3) else "验证失败")


def demo_chain_rule():
    """链式法则演示"""
    print("\n" + "=" * 50)
    print("链式法则演示")
    print("=" * 50)

    x = torch.tensor(2.0, requires_grad=True)
    # y = x^2
    y = x ** 2
    # z = y^3 = (x^2)^3
    z = y ** 3

    print(f"x = {x.item()}")
    print(f"y = x^2 = {y.item()}")
    print(f"z = y^3 = {z.item()}")

    z.backward()

    print(f"\n∂z/∂x = {x.grad.item()}")
    print("验证: dz/dx = dz/dy · dy/dx = 3y^2 · 2x = 3·4·2 = 24 ✓" if
          abs(x.grad.item() - 24.0) < 1e-6 else "验证失败")


def demo_grad_accumulation():
    """梯度累积演示（为什么需要 zero_grad）"""
    print("\n" + "=" * 50)
    print("梯度累积问题")
    print("=" * 50)

    w = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

    # 第一次前向
    loss1 = (w ** 2).sum()
    loss1.backward()
    print(f"第一次 backward 后的梯度: {w.grad}")

    # 第二次前向（不清零）
    loss2 = (w ** 2).sum()
    loss2.backward()
    print(f"不清零就第二次 backward，梯度累积: {w.grad}")
    print("→ 梯度翻倍！如果不清零，多次迭代后梯度会爆炸！")

    # 正确做法：清零
    w.grad.zero_()
    loss3 = (w ** 2).sum()
    loss3.backward()
    print(f"zero_grad() 清零后: {w.grad} ✓")


def demo_no_grad():
    """torch.no_grad() vs model.eval()"""
    print("\n" + "=" * 50)
    print("no_grad() vs eval()")
    print("=" * 50)

    model = torch.nn.Linear(3, 2)

    x = torch.randn(2, 3)

    # ❌ 推理时不用 no_grad
    model.eval()
    y1 = model(x)
    print(f"eval() 模式下输出 requires_grad: {y1.requires_grad}")
    # eval() 只改变了 BN / Dropout 行为，不影响梯度计算

    # ✓ 推理时用 no_grad
    with torch.no_grad():
        y2 = model(x)
    print(f"no_grad() 模式下输出 requires_grad: {y2.requires_grad}")
    # no_grad() 完全禁用梯度计算和图构建，节省显存

    print("\n正确做法（推理时）：")
    print("  model.eval()")
    print("  with torch.no_grad():")
    print("      output = model(x)")


def demo_backward_requires_scalar():
    """backward() 要求输出是标量"""
    print("\n" + "=" * 50)
    print("backward() 必须作用于标量（或指定 grad_tensors）")
    print("=" * 50)

    x = torch.tensor([1., 2., 3.], requires_grad=True)
    y = x * 2

    # 方式1：loss 是标量，直接 backward
    loss = y.sum()
    loss.backward()
    print(f"标量 loss backward: ∂loss/∂x = {x.grad}")

    # 方式2：loss 是向量，指定 grad_tensors
    x.grad.zero_()
    loss_vec = y  # shape (3,)
    # loss_vec.backward()  # ← 会报错！
    loss_vec.backward(torch.tensor([1., 1., 1.]))  # 等价于 sum
    print(f"向量 backward(grad_tensors): ∂loss/∂x = {x.grad}")


if __name__ == "__main__":
    demo_basic_grad()
    demo_chain_rule()
    demo_grad_accumulation()
    demo_no_grad()
    demo_backward_requires_scalar()

    print("\n" + "=" * 50)
    print("面试核心问答")
    print("=" * 50)
    print("""
Q: 为什么梯度需要清零？
A: PyTorch 默认梯度会累积（accumulate），如果不清零，
   本次梯度会加上上次的梯度，导致参数更新错误。

Q: no_grad() 和 eval() 的区别？
A: no_grad() — 完全禁用梯度计算和计算图构建，节省显存/算力。
   eval()    — 切换模型为评估模式，只影响 BN/Dropout 的行为，
               不会禁用梯度。如果在 eval() 下仍需要梯度，需配合 no_grad()。

Q: 动态图和静态图的区别？
A: PyTorch 是动态图：每次前向重新构建图，灵活，支持 Python 控制流。
   TensorFlow 1.x 是静态图：先构建图，再重复执行，适合部署和优化。
   TensorFlow 2.x / JAX 默认也是动态图。
""")
