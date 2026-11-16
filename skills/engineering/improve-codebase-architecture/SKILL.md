---
name: improve-codebase-architecture
description: 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后与你一起拷问选中的那一个。
disable-model-invocation: true
---

# 改进代码库架构（Improve Codebase Architecture）

浮出架构摩擦，提出**深化机会（deepening opportunities）**：把浅模块变深模块的重构。目标是可测试性和对 AI 的可导航性。

这条命令_受_项目领域模型_滋养_，并建立在共享设计词汇上：

- 调用 Skill 工具运行 "codebase-design"，取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（删除测试、"interface 就是测试面"、"一个 adapter = 假想的 seam，两个 = 真的"）。在每条建议里精确使用这些术语，不要漂移成 "component"、"service"、"API" 或 "boundary"。
- `GLOSSARY.md` 里的领域语言为好 seam 命名；`docs/adr/` 里的 ADR 记录本命令不应重新审理的决策。

## 流程

### 1. 探索

**扫描前先定范围：YAGNI。** 深化一个模块的回报在于让它未来的变更更容易，所以给代码库里最近变过的地方加权重。先决定*去哪看*再看：

- 如果用户点名了方向（一个模块、一个子系统、一个痛点），照单全收，跳过下面的推断。
- 否则，往回走一大段 commit 历史（`git log --oneline`）找代码库的热点——反复出现的文件和区域，让这些路径先拉住你的注意力。如果变更分散、没有明确热点，把网撒大。

先读项目的领域词汇表（`GLOSSARY.md`）和你要动的区域里的任何 ADR。

然后生成一个带全新上下文窗口的 sub-agent 去走代码库。不要按死板的启发式走；有机地探索并记下你在哪里感到摩擦：

- 理解一个概念要在许多小模块之间跳来跳去的地方在哪？
- 哪里模块**浅**，interface 几乎和实现一样复杂？
- 哪里纯函数只是为了可测试性被提取出来，但真正的 bug 藏在它们被怎么调用里（没有 **locality**）？
- 哪里紧耦合的模块跨 seam 泄漏？
- 代码库哪些部分没有测试，或难以通过当前 interface 测试？

对你怀疑浅的任何东西应用**删除测试**：删掉它会集中复杂度，还是只是把它挪走？"会集中"就是你想要的信号。

### 2. 以 HTML 报告呈现候选

把一个自包含 HTML 文件写到 OS 临时目录，别让任何东西落进仓库。从 `$TMPDIR` 解析临时目录，回退到 `/tmp`（Windows 上是 `%TEMP%`），写到 `<tmpdir>/architecture-review-<timestamp>.html`，让每次运行拿到一个新文件。为用户打开它（Linux 上 `xdg-open <path>`，macOS 上 `open <path>`，Windows 上 `start <path>`）并告诉他们绝对路径。

报告用 **Tailwind（CDN）** 做布局和样式，用 **Mermaid（CDN）** 画图——当图/流程/时序能可靠传达结构时。把 Mermaid 与手工 CSS/SVG 可视化混用：关系是图形状（调用图、依赖、时序）时用 Mermaid，想要更有编辑感（质量图、剖面图、坍缩动画）时用手工 div/SVG。每个候选有一组 **before/after 可视化**。要视觉化。

每个候选渲染一张卡片：

- **文件**：涉及哪些文件/模块
- **问题**：当前架构为什么造成摩擦
- **方案**：平实语言描述会改变什么
- **收益**：用 locality 和 leverage 解释，以及测试会怎么改善
- **Before / After 图**：并排、手绘，展示浅薄与深化
- **推荐强度**：`Strong`、`Worth exploring`、`Speculative` 三选一，渲染成徽章

报告以**顶部推荐**收尾：你会先啃哪个候选、为什么。

**领域用 GLOSSARY.md 的词汇，架构用 `/codebase-design` 的词汇。** 如果 `GLOSSARY.md` 定义了 "Order"，就谈 "Order 接单模块"，不是 "FooBarHandler"，也不是 "Order service"。

**ADR 冲突**：如果某个候选与既有 ADR 矛盾，只在该摩擦真实到值得重开 ADR 时才浮出它。在卡片里清晰标注（如一个警告标注：_"与 ADR-0007 矛盾，但值得重开，因为…"）_。不要罗列 ADR 禁止的每一个理论上的重构。

完整的 HTML 脚手架、图模式和样式指引见 [HTML-REPORT.md](HTML-REPORT.md)。

先不要提出 interface。文件写完后问用户："这些里面你想探索哪一个？"

### 3. 拷问循环

用户选定候选后，调用 Skill 工具运行 "grilling"，与他们一起走决策树：约束、依赖、深化模块的形状、seam 后面是什么、哪些测试存活。

决策定型时副作用就地发生；随时调用 Skill 工具运行 "domain-modeling" 保持领域模型最新：

- **用 `GLOSSARY.md` 里没有的概念给深化模块命名？** 把该术语加进 `GLOSSARY.md`。文件不存在就惰性创建。
- **对话中打磨了一个模糊术语？** 当场更新 `GLOSSARY.md`。
- **用户以一个承重的理由否决了候选？** 提议一个 ADR，措辞如：_"要不要我把这个记成 ADR，让未来的架构 review 不再重复建议它？"_ 只有当这个理由确实会被未来的探索者需要、以避免重复建议同一件事时才提议；跳过一时性的理由（"现在不值得"）和自明的理由。
- **想为深化模块探索备选 interface？** 调用 Skill 工具运行 "codebase-design"，用它的 design-it-twice 并行 sub-agent 模式。
