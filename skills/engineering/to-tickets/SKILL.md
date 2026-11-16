---
name: to-tickets
description: 把一份计划、spec 或当前对话拆成一组曳光弹式 ticket，每个 ticket 声明自己的阻塞边，发布到已配置的 tracker（本地时边以文本形式一 ticket 一文件，真实 tracker 上用原生阻塞链接）。
disable-model-invocation: true
---

# 拆 Ticket（To Tickets）

把一份计划、spec 或对话拆成一组 **ticket**：曳光弹式的垂直切片，每个声明哪些 ticket **阻塞（block）** 它。

issue tracker 和 triage 标签词汇表应该已经提供给你了。如果没有，让用户运行 `/setup-matt-pocock-skills`。

## 流程

### 1. 收集上下文

基于对话上下文里已有的东西干活。如果用户传了引用（spec 路径、issue 编号或 URL）作为参数，取回来并读它的完整正文和评论。

### 2. 探索代码库（可选）

如果你还没有探索过代码库，现在探索，以了解代码的现状。ticket 的标题和描述应使用项目的领域术语表词汇，并尊重你所触及区域内的 ADR。

寻找预先重构（prefactor）代码以简化实现的机会。"先把改动变容易，再做那个容易的改动。"

### 3. 起草垂直切片

把工作拆成**曳光弹（tracer bullet）**式 ticket。

<vertical-slice-rules>

- 每个切片都切出一条窄但完整的路径，穿透每一层（schema、API、UI、测试）：是垂直切片，绝不是单层的横向切片
- 一个完成的切片可以独立演示或独立验证
- 每个切片的大小要能装进一个全新的上下文窗口
- 任何预先重构都应最先做

</vertical-slice-rules>

给每个 ticket 标上它的**阻塞边**：必须先完成它才能开工的其他 ticket。没有阻塞方的 ticket 可以立即开工。

**宽重构是垂直切片的例外。** **宽重构（wide refactor）**是一次机械性修改（重命名一列、改一个共享符号的类型），其**爆炸半径**扇出到整个代码库，一次编辑就让数千个调用点同时挂掉，没有任何垂直切片能保持绿色落地。不要硬塞进曳光弹；把它排成**扩张–收缩（expand–contract）**。先扩张：把新形态加在旧形态旁边，什么都不破坏。然后按爆炸半径分批（按包、按目录）迁移调用点，每批是自己的 ticket，被扩张 ticket 阻塞，批次之间 CI 保持绿色，因为旧形态还在。最后收缩：一旦没有调用方残留就删掉旧形态，放在一个被所有迁移批次阻塞的 ticket 里。当连分批都无法独自保持绿色时，保持这个顺序但让它们共享一条集成分支，全部阻塞一个最终的「集成并验证」ticket；只在那一刻承诺绿色。

### 4. 考问用户

把提议的拆分以编号列表呈现。每个 ticket 展示：

- **标题**：简短的描述性名称
- **被谁阻塞（Blocked by）**：哪些其他 ticket（如果有）必须先完成
- **它交付什么（What it delivers）**：这个 ticket 让什么端到端行为跑起来

问用户：

- 粒度感觉对吗？（太粗 / 太细）
- 阻塞边对不对：每个 ticket 是否只依赖真正卡住它的 ticket？
- 有 ticket 该合并或再拆吗？

迭代到用户认可这个拆分为止。

### 5. 把 ticket 发布到已配置的 tracker

发布认可的 ticket。**怎么发**取决于 `/setup-matt-pocock-skills` 配置的 tracker；ticket 本身两种方式都一样，只有阻塞边的形状变化：

- **本地文件** → 在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每 ticket 写一个文件，按依赖顺序（阻塞方在前）从 `01` 编号。每个文件的 "Blocked by" 列出它依赖的编号/标题。用下面的单 ticket 文件模板：一 ticket 一文件，绝不合并成单个文件。
- **真实 issue tracker（GitHub、Linear、…）** → 按依赖顺序（阻塞方在前）每 ticket 发布一个 issue，这样每个 ticket 的阻塞边能引用真实标识符。平台有原生阻塞关系就用原生；否则把每个 ticket 的 "Blocked by" 设为阻塞它的那些 issue。如果来源是一个既有 issue，让每个 ticket 成为它的子 issue（tracker 文档中的操作）。除非另有指示，打上 `ready-for-agent` triage 标签；这些 ticket 构造上就是 agent 可抓取的。

干**前沿（frontier）**：任何阻塞方全部完成的 ticket。对纯线性链条来说就是自上而下。

不要关闭或修改任何父 issue。

<local-ticket-template>

# <NN>: <Ticket 标题>

**要构建什么：** 这个 ticket 让什么端到端行为跑起来，从用户视角描述，不是逐层实现的清单。

**被谁阻塞：** 卡住这个 ticket 的那些 ticket 的编号/标题，或"无（可立即开工）"。

**Status:** ready-for-agent

- [ ] 验收标准 1
- [ ] 验收标准 2

</local-ticket-template>

<issue-template>

## 父 issue（Parent）

指向 tracker 上父 issue 的引用（如果来源是既有 issue，否则省略本节）。

## 要构建什么（What to build）

这个 ticket 让什么端到端行为跑起来，从用户视角描述，不是逐层实现。

## 验收标准（Acceptance criteria）

- [ ] 标准 1
- [ ] 标准 2

## 被谁阻塞（Blocked by）

- 每个阻塞 ticket 的引用，或"无（可立即开工）"。阻塞边已设为原生关系时省略本节。

</issue-template>

无论哪种形式，避免具体文件路径或代码片段：它们很快过期。例外：如果某个原型产出了比文字更精确地编码一个决策的片段（状态机、reducer、schema、类型形状），内联它并简要注明来自原型。裁剪到富含决策的部分，不是能跑的演示，只要重要的那几块。
