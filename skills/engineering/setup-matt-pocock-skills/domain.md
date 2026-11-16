# 领域文档（Domain Docs）

工程 skills 在探索代码库时应如何消费本仓库的领域文档。

## 探索之前，先读这些

- 仓库根目录的 **`GLOSSARY.md`**，或
- 仓库根目录的 **`GLOSSARY-MAP.md`**（如果存在）：它指向每个上下文一个 `GLOSSARY.md`。读与主题相关的每一个。
- **`docs/adr/`**：读触及你即将工作区域的 ADR。在多上下文仓库中，还要查 `src/<context>/docs/adr/` 里上下文范围的决策。

如果这些文件不存在，**静默继续**。不要标记它们的缺失；不要预先建议创建。`/domain-modeling` skill（经 `/grill-with-docs` 和 `/improve-codebase-architecture` 到达）会在术语或决策真正被敲定时惰性地创建它们。

## 文件结构

单一上下文仓库（大多数仓库）：

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `GLOSSARY-MAP.md` 时）：

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 使用术语表的词汇

当你的产出要命名一个领域概念时（issue 标题、重构提案、假设、测试名），使用 `GLOSSARY.md` 中定义的术语。不要漂移到术语表明确回避的同义词。

如果你需要的概念还不在术语表里，那是一个信号：要么你在发明项目不用的语言（重新考虑），要么存在真实的缺口（记下来交给 `/domain-modeling`）。

## 标记 ADR 冲突

如果你的产出与既有 ADR 矛盾，显式地摆出来，而不是静默覆盖：

> _与 ADR-0007（事件溯源订单）矛盾，但值得重启讨论，因为……_
