---
name: domain-modeling
description: 构建并打磨项目的领域模型。当讨论代码库术语、编写或编辑 GLOSSARY.md、记录或编辑 ADR 时使用。
---

# 领域建模（Domain Modeling）

在设计的同时主动构建和打磨项目的领域模型。这是*主动*纪律：挑战术语、发明边界场景、在术语和决策定型的当下把它们写进词汇表和决策记录。（仅仅*读* `GLOSSARY.md` 取词不是这个 skill：那是任何 skill 都能做的一行习惯。这个 skill 用于你要改模型的时刻，而不只是消费模型。）

## 文件结构

大多数仓库只有一个上下文：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `GLOSSARY-MAP.md`，仓库就有多个上下文。地图指出每个上下文住哪：

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

惰性创建文件：只在有东西可写时创建。不存在 `GLOSSARY.md` 就在第一个术语敲定时创建。不存在 `docs/adr/` 就在第一个 ADR 需要时创建。

## 会话期间

### 对照词汇表挑战

当用户使用的术语与 `GLOSSARY.md` 既有语言冲突时，立刻指出。"你的词汇表把 'cancellation' 定义为 X，但你似乎在说 Y。是哪一个？"

### 打磨模糊语言

当用户使用含糊或过载的术语时，提出一个精确的规范术语。"你在说 'account'：你指 Customer 还是 User？它们是不同的东西。"

### 讨论具体场景

当领域关系被讨论时，用具体场景压测它们。发明探边界的场景，逼用户对概念之间的边界保持精确。

### 与代码交叉核对

当用户陈述某样东西如何工作时，检查代码是否同意。发现矛盾就浮出它："你的代码取消的是整个 Order，但你刚说部分取消是可能的。哪个对？"

### 就地更新 GLOSSARY.md

术语敲定时，当场更新 `GLOSSARY.md`。不要攒批：发生即捕获。使用 [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) 的格式。

`GLOSSARY.md` 应当完全不含实现细节。不要把 `GLOSSARY.md` 当 spec、草稿本或实现决策的仓库。它是词汇表，仅此而已。

### 节制地提议 ADR

只有以下三条全真时才提议创建 ADR：

1. **难以逆转**：之后改主意的成本可观
2. **没有上下文会让人惊讶**：未来的读者会问"他们为什么这么搞？"
3. **真实权衡的结果**：存在真实的备选，你出于具体理由选了其中一个

缺任何一条，跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 的格式。
