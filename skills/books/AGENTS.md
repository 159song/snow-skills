# books/ — 经典软件工程书籍规则集

## 职责与边界

收录 [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books)（MIT）的 14 本书规则集，作为**冻结副本（vendor）**。每本书提炼为一套可加载的工程决策规则，供 AI 代理在设计、实现、重构、评审等任务中按需取用。规则是社区对原书的提炼而非替代品，不复述原书原文。

本目录不涉及 RAG（见 `../rag-lifecycle`）、具体工程流程方法论（见 `../engineering/`）。

## 目录结构与核心文件

```
books/<book-name>/
  SKILL.md          # 中文入口：frontmatter description + 三档加载指引（本仓库重写）
  <name>.mini.md    # 默认档：核心决策规则，多数任务够用（上游原文，英文）
  <name>.nano.md    # 精简档：上下文预算紧张时的兜底（上游原文，英文）
  <name>.md         # full 档：完整参考，仅深入权衡时查阅（上游原文，英文）
```

收录的 14 本书：软件设计哲学、整洁架构、代码整洁之道、代码大全、设计数据密集型应用（DDIA）、领域驱动设计（蓝皮书/精粹/红皮书）、企业应用架构模式（PoEAA）、重构、Refactoring.Guru、发布！（Release It!）、程序员修炼之道、修改代码的艺术。

## 对外接口与调用方式

- 每本书注册为插件内一个独立 skill，可被 Claude 按任务自动触发，也可 `/书名` 手动调用。
- 加载协议（写在每本书的 `SKILL.md` 中）：默认 mini → 预算紧张用 nano → 权衡不足才查 full。

## 关键依赖与数据流

无外部依赖，纯 Markdown。上游版本：v0.6（commit `893a88a`，2026-09-10）。

## 同步与验证

- 上游更新需手动同步：clone 上游 → 对比 `<name>.{mini,nano}.md` 与 `<name>.md` → 仅覆盖三个规则文件 → **不要**覆盖 `SKILL.md`（中文入口由本仓库维护）。
- 验证：`python3 -c "import json;json.load(open('.claude-plugin/plugin.json'))"` 确认清单合法；确认每个目录都含 4 个文件且 `SKILL.md` 的 name 与目录名一致。
- 新增/删除书时，同步更新 `.claude-plugin/plugin.json` 的 skills 数组与仓库 `README.md` 收录表。

## 本目录特有约定

- 规则正文保持英文冻结，不做翻译（370KB+ 的密集规则翻译易失真，且会破坏与上游的可比性）；中文仅用于 `SKILL.md` 入口。
- frontmatter 必须带 `license: MIT`，保留上游版权归属（见仓库 `LICENSE` 第 4 条）。
