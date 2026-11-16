---
name: code-review
description: "对自某个固定点（commit、branch、tag 或 merge-base）以来的变更沿两条轴做 review：Standards（代码是否遵循本仓库已记录的编码规范？）与 Spec（代码是否吻合原始 issue/spec 的要求？）。两条轴的 review 在并行 sub-agent 中运行，并排报告。当用户想 review 一个分支、PR、进行中的变更，或要求「review since X」时使用。"
---

对 `HEAD` 与用户提供的固定点之间的 diff 做双轴 review：

- **Standards（规范轴）**：代码是否符合本仓库已记录的编码规范？
- **Spec（需求轴）**：代码是否忠实实现了原始的 issue / spec？

两条轴作为**并行 sub-agent** 运行，以免互相污染上下文，然后由本 skill 汇总它们的发现。每个 sub-agent 都以全新上下文窗口启动。

issue tracker 应该已经提供给你。如果没有，让用户运行 `/setup-matt-pocock-skills`。

## 流程

### 1. 钉住固定点

用户说的任何东西都可以是固定点（commit SHA、分支名、tag、`main`、`HEAD~5` 等）。如果他们没有指定，问他们要。

一次性记下 diff 命令：`git diff <fixed-point>...HEAD`（三个点，这样比较的是 merge-base）。同时用 `git log <fixed-point>..HEAD --oneline` 记下 commit 列表。

在继续之前，确认固定点可解析（`git rev-parse <fixed-point>`）且 diff 非空。坏的 ref 或空 diff 应该在这里失败，而不是在两个并行 sub-agent 里面。

### 2. 找到 spec 来源

按以下顺序找原始 spec：

1. commit message 里的 issue 引用（`#123`、`Closes #45`、GitLab 的 `!67` 等），按 tracker 文档里的工作流抓取。
2. 用户作为参数传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与分支名或功能匹配的 spec 文件。
4. 什么都找不到就问用户 spec 在哪。如果他们说没有，**Spec** sub-agent 将跳过并报告"无可用 spec"。

### 3. 找到规范来源

在仓库里搜索所有记录代码该怎么写的文件。存在 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md` 时，它必须在清单上。

在仓库记录的内容之上，Standards 轴永远携带下面的**坏味道基线（smell baseline）**：一组固定的 Fowler 代码坏味道（《Refactoring》第 3 章），即使仓库什么都没记录也适用。两条规则约束它：

- **仓库优先。** 已记录的仓库规范永远赢；在仓库认可某样基线会标记的东西时，抑制该坏味道。
- **永远是判断题。** 每个坏味道都是带标签的启发式（"可能是 Feature Envy"），绝不是硬性违规。和这里的任何规范一样，工具已经强制的东西一律跳过。

每个坏味道按*是什么* → *怎么修*来读；对照 diff 匹配：

- **Mysterious Name（神秘命名）**：函数、变量或类型的名字不透露它做什么或装什么。→ 重命名；想不出诚实的名字，说明设计很浑。
- **Duplicated Code（重复代码）**：同一逻辑形状出现在变更中多个 hunk 或文件里。→ 提取共享形状，两处都调用它。
- **Feature Envy（依恋情结）**：一个方法摸别的对象的数据比摸自己的还多。→ 把方法搬到它依恋的数据上。
- **Data Clumps（数据泥团）**：同几个字段或参数总是结伴出现（一个想出生的类型）。→ 捆成一个类型，传那个类型。
- **Primitive Obsession（基本类型偏执）**：用基本类型或字符串顶替一个配得上自己类型的领域概念。→ 给概念一个自己的小类型。
- **Repeated Switches（重复 switch）**：对同一类型的同样 `switch`/`if` 级联在变更中反复出现。→ 用多态替换，或两处共享的一个映射。
- **Shotgun Surgery（霰弹式修改）**：一个逻辑变更迫使 diff 里许多文件四处挨改。→ 把一起变的东西收进一个模块。
- **Divergent Change（发散式变化）**：一个文件或模块因多个互不相关的原因被修改。→ 拆开，让每个模块只因一个原因变化。
- **Speculative Generality（夸夸其谈的通用性）**：为 spec 没有的需求添加的抽象、参数或钩子。→ 删掉；内联回去，等真实需求出现。
- **Message Chains（消息链）**：调用方不应依赖的长 `a.b().c().d()` 导航。→ 用第一个对象上的一个方法把这段路藏起来。
- **Middle Man（中间人）**：一个基本只在往后转发的类或函数。→ 砍掉，直接调用真正的目标。
- **Refused Bequest（被拒绝的遗赠）**：一个忽略或覆盖掉所继承大部分内容的子类或实现者。→ 放弃继承，用组合。

### 4. 并行生成两个 sub-agent

两个 sub-agent 调用一起发出，在前台运行，然后汇总它们返回的报告。

**Standards sub-agent 的 prompt** 应包含：

- 完整的 diff 命令和 commit 列表。
- 第 3 步找到的规范来源文件清单，**外加第 3 步的坏味道基线全文粘贴**（sub-agent 没有其他途径拿到它）。
- 任务简报："逐文件/逐 hunk（在相关处）报告：(a) diff 违反已记录规范的每一处：引用该规范（文件 + 规则）；以及 (b) 你发现的任何基线坏味道：点名并引用 hunk。区分硬性违规与判断题：已记录规范的违反可以是硬性的，但基线坏味道永远是判断题，且已记录的仓库规范覆盖基线。工具已强制的跳过。400 词以内。"

**Spec sub-agent 的 prompt** 应包含：

- diff 命令和 commit 列表。
- spec 的路径或抓取到的内容。
- 任务简报："报告：(a) spec 要求了但缺失或不完整的需求；(b) diff 里没被要求的行为（scope creep）；(c) 看起来实现了但实现看起来不对的需求。每条发现引用 spec 原句。400 词以内。"

spec 缺失时，跳过 Spec sub-agent 并在最终报告里注明。

### 5. 汇总

把两份报告放在 `## Standards` 和 `## Spec` 标题下呈现，原样或轻度清理。**不要**合并或重新排名发现，因为两条轴刻意分开（见「为什么两条轴」）。

以一行总结收尾：每条轴的发现总数，以及_每条轴内部_最严重的问题（如有）。不要跨轴选出一个总冠军：那是这套分离要防止的重排名。

## 为什么两条轴

一个变更可以通过一条轴而挂在另一条上：

- 代码符合每条规范但实现了错误的东西 → **Standards 过，Spec 挂。**
- 代码精确做了 issue 要求的事但破坏了项目惯例 → **Spec 过，Standards 挂。**

分开报告可以防止一条轴掩盖另一条。
