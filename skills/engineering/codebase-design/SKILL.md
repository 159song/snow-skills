---
name: codebase-design
description: 设计深模块的共享词汇。当用户想设计或改进模块的 interface、寻找深化机会、决定 seam 放哪里、让代码更可测试或对 AI 更可导航，或其他 skill 需要深模块词汇时使用。
---

# 代码库设计（Codebase Design）

设计**深模块（deep module）**：小接口背后的大量行为，放在干净的 seam 处，可通过该 interface 测试。在任何设计或重构代码的地方使用这套语言和这些原则。目标是给调用方 leverage，给维护者 locality，给所有人可测试性。

## 词汇表

精确使用这些术语：不要换成 "component"、"service"、"API" 或 "boundary"。语言一致就是全部意义所在。

**Module（模块）**：任何有 interface 和实现的东西。刻意不限定规模：一个函数、类、包，或跨层切片。_避免_：unit、component、service。

**Interface（接口）**：调用方要正确使用模块必须知道的一切：类型签名，以及不变量、顺序约束、错误模式、必需配置和性能特征。_避免_：API、signature（太窄，它们只指类型层面的表面）。

**Implementation（实现）**：模块内部的东西，它的代码体。区别于 **Adapter**：一个东西可以是小 adapter 配大 implementation（Postgres 仓库），也可以是大 adapter 配小 implementation（内存 fake）。当话题是 seam 时用 "adapter"，否则用 "implementation"。

**Depth（深度）**：interface 处的 leverage。调用方（或测试）每学一个单位的 interface 所能驱动的行为量。大量行为藏在小 interface 后时模块是**深**的；interface 几乎和实现一样复杂时是**浅**的。

**Seam（缝）**_(Michael Feathers)_：一个你无需在原地编辑就能改变行为的地方；模块 interface 所在的那个*位置*。seam 放哪里本身是一个独立的设计决策，与它后面放什么无关。_避免_：boundary（与 DDD 的 bounded context 撞义）。

**Adapter（适配器）**：在 seam 处满足 interface 的具体事物。描述*角色*（填哪个槽），而非实体（里面是什么）。

**Leverage（杠杆）**：调用方从深度得到的东西。每学一个单位的 interface 换来更多能力。一份实现在 N 个调用点和 M 个测试上收回成本。

**Locality（局部性）**：维护者从深度得到的东西。变更、bug、知识和验证集中在一个地方，而不是散落在各调用方。修一次，处处修好。

## 深与浅

**深模块** = 小 interface + 大量实现：

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**浅模块** = 大 interface + 少量实现（避免）：

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

设计 interface 时问自己：

- 我能减少方法数量吗？
- 我能简化参数吗？
- 我能把更多复杂度藏进里面吗？

## 原则

- **深度是 interface 的属性，不是实现的属性。** 深模块内部可以由小的、可 mock、可替换的部分组成；它们只是不属于 interface。模块可以有**内部 seam**（对其实现私有、由它自己的测试使用），以及 interface 处的**外部 seam**。
- **删除测试（deletion test）。** 想象删掉这个模块。如果复杂度消失了，它就是个透传层。如果复杂度在 N 个调用方那里重新出现，它就在挣自己的饭钱。
- **interface 就是测试面。** 调用方和测试穿过同一个 seam。如果你想测到 interface *之内*，这个模块的形状大概率不对。
- **一个 adapter 意味着假想的 seam。两个 adapter 才是真 seam。** 除非真有东西跨它变化，否则不要引入 seam。

## 为可测试性设计

好的 interface 让测试变得自然：

1. **接受依赖，不要创建依赖。**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不要产生副作用。**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **小表面积。** 更少的方法 = 更少的测试。更少的参数 = 更简单的测试准备。

## 关系

- 一个 **Module** 恰好有一个 **Interface**（它呈现给调用方和测试的表面）。
- **Depth** 是 **Module** 的属性，相对其 **Interface** 度量。
- **Seam** 是 **Module** 的 **Interface** 所在之处。
- 一个 **Adapter** 坐在 **Seam** 上并满足 **Interface**。
- **Depth** 为调用方产出 **Leverage**，为维护者产出 **Locality**。

## 被否决的框架

- **把深度当作实现行数与 interface 行数之比**（Ousterhout）：会奖励给实现注水。我们改用深度即 leverage。
- **把 "interface" 当作 TypeScript 的 `interface` 关键字或类的公开方法**：太窄：这里的 interface 包括调用方必须知道的每一个事实。
- **"boundary"**：与 DDD 的 bounded context 撞义。说 **seam** 或 **interface**。

## 走得更深

- **在给定依赖的情况下深化一组模块**，见 [DEEPENING.md](DEEPENING.md)：依赖类别、seam 纪律、替换而非叠层的测试法。
- **探索备选 interface**，见 [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)：起一组并行 sub-agent，用几种截然不同的方式设计 interface，然后按深度、局部性和 seam 位置比较。
