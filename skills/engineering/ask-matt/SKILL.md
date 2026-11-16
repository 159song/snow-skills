---
name: ask-matt
description: 询问哪个 skill 或 flow 适合你的处境。本仓库各 skill 的路由器。
disable-model-invocation: true
---

# Ask Matt

你记不住每个 skill，所以问。

在陈述某个 skill 的功能或建议跳过某一步之前，先读那个 skill 的 SKILL.md：这里的摘要只用于定向。

**flow（流程）**是穿过这些 skill 的一条路径。大多数路径沿一条**主流程**运行，两个**入口匝道（on-ramp）**汇入其中。其余的都是独立的，或是运行在下方的词汇层。

## 主流程：idea → ship

大多数工作走的路线。你有一个想法，想把它建出来。

1. **`/grill-with-docs`** 通过访谈打磨想法。只要你**在个工作目录里工作**就从这里开始：它是有状态的，把学到的东西保存在 `GLOSSARY.md` 和 ADR 里。（没有工作目录？改用 `/grill-me`，见「独立」一节。两者运行的是同一个 `/grilling` 原语；`grill-with-docs` 会留下书面痕迹，所以只要有仓库可留痕，它就是两者中更好的那个。）
2. **分支：能在对话中解决所有问题吗？** 如果某个问题需要可运行的答案（状态、业务逻辑、必须亲眼看的 UI），绕道原型，双向用 **`/handoff`** 桥接（原型活在它自己的目录里，这正是 `/handoff` 的用途；见「阶段边界」）：
   - **`/handoff`** 导出，然后针对那个文件开一个全新会话，
   - **`/prototype`** 用一次性代码回答问题，
   - **`/handoff`** 把你学到的东西带回，并在原始想法线程里引用它。
3. **分支：这是多会话构建吗？**
   - **是** → **`/to-spec`**（把线程变成 spec），然后 **`/to-tickets`** 拆成曳光弹 ticket，每个声明自己的**阻塞边（blocking edges）**。然后二选一地消化这些 ticket：
     - 逐 ticket **`/implement`**，**每个之间 `/clear` 上下文**。在本地 tracker 上是 `.scratch/<feature>/issues/` 下每 ticket 一个文件，按阻塞优先手工推进；在真正的 tracker 上，这些边变成原生的阻塞链接，任何阻塞已完成的 ticket 都可以被认领。每个 ticket 都自包含，所以上一个的上下文用完即弃。
     - **`/implement-spec`** 一次跑完整个 spec。它把 ticket 当作**任务图（task graph）**，在就绪的**前沿（frontier）**上并行运行多个 implementer subagent，把一切落在一个**集成分支**上。当你宁愿编排构建而不是亲自驱动每个 ticket 时用它。
   - **否** → 就在这里、同一上下文窗口里 **`/implement`**。

   无论哪条路，代码都靠 **`/tdd`** 驱动构建（一次一个红-绿切片），并以 **`/code-review`** 收尾——对 diff 的双轴 review（Standards + Spec）。`/implement` 对每个 ticket 各跑一次这两者；`/implement-spec` 的 implementer 各自驱动 `/tdd`，而它在集成分支上跑一次 `/code-review`。当你只想测试先行地构建一个具体行为、不需要完整 spec 时，单独用 **`/tdd`**；当你想把分支或 PR 对照某个固定点做 review 时，随时单独用 **`/code-review`**。

   当工作以 pull request 提交时，**`/pr`** 塑造正文：展示变更的最小可视化、证明它可用的 before/after 证据，以及单向门或双向门的判定。它是模型调用的，所以 agent 写 PR 时会自动用它。

4. **`/retro`** 闭环。一次构建之后，尤其是跑偏的构建之后，它回看会话，并对 agent 的**环境**（而非代码）提出改动建议：导航指针、自动化检查、`/code-review` 执行的编码规范、导向文件、工具。机械性错误变成确定性检查；判断题变成编码规范。下一次构建于是从更好的环境起步。

### 上下文卫生

把步骤 1–3 保持在**一个不间断的上下文窗口**里（`/to-tickets` 之前不要压缩或清空），让拷问、spec 和 ticket 建立在同一段思考上。之后每个 `/implement` 从 ticket 出发全新开始。`/retro` 要在它所回顾的那个会话里、清空之前跑；清空之后，让它指向那个会话的日志。

这件事的上限是 **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**：模型仍能敏锐推理的那个窗口（最先进模型上约 150k tokens）。如果会话在 `/to-tickets` 之前逼近上限，不要在降级状态硬撑；在最近的阶段边界 `/compact` 然后继续（见「阶段边界」）。

## 入口匝道

一种会生成工作的起点处境，随后汇入主流程。

- **Bug 和请求堆积** → **`/triage`**。它把 issue 推过分诊角色，产出 agent-ready 的 issue，稍后由 **`/implement`** 接走。

  分诊只用于**不是你创建的** issue：bug 报告、外部功能请求、任何以原始状态抵达的东西。`/to-tickets` 产出的 ticket 已经是 agent-ready，所以**不要分诊它们**。

- **有东西坏了** → **`/diagnosing-bugs`**。用于难的那些：第一眼看不服的 bug、间歇性 flake、在两个已知良好状态之间潜入的 regression。它拒绝在拿到**紧密反馈回路**（一条已经能在*这个* bug 上变红的命令）之前建立理论，然后用回归测试修复。修复落地后，在同一会话里跑 **`/retro`**，问什么本可以阻止这个 bug；如果真正的发现是没有好的 seam 把它锁死，那是 **`/improve-codebase-architecture`** 的活。

- **庞大而朦胧的工程：全新项目或超大功能构建，一个会话装不下** → **`/wayfinder`**，这里认知要求最高的 flow。当从当前位置到目的地的路径还看不见时，它在 issue tracker 上绘制一张由**决策 ticket** 组成的**共享地图**，逐个解决它们，产出**决策而非交付物**，直到迷雾被推回、路径清晰。**`/grill-with-docs`** 打磨的是一个会话装得下的想法，wayfinder 用于装不下的那个；它更慢更密，所以专为那种情况留着，永远不要用在范围清晰的功能上。

  地图清晰后，**它交接，它不构建**：在 **`/to-spec`** 处汇入主流程，把地图的关联决策收敛成可构建的计划，然后照常 `/to-tickets` 和 `/implement`。把地图直接循环进 `/implement` 会跳过这个收敛、扔掉关联细节，所以只有当工程最终确实很小时才直接 `/implement`。

## 代码库健康

不是功能工作，只是维护。

- **`/improve-codebase-architecture`** 在你有空闲时刻时运行，保持代码库对 agent 友好。它浮出**深化机会**；选中一个就_生成一个想法_，可以带进主流程的 `/grill-with-docs`。它是找出候选的勘察；**`/codebase-design`**（见下）是你设计选中之物的工作台。

## 底下的词汇

两个运行在其他 skill *之下*的模型调用参考，各自是其词汇的唯一事实来源。当问题出在**词语**而非流程上时直接用它们；或者让上面的 skill 拉它们进来。

- **`/domain-modeling`**：打磨项目的*领域*语言：挑战一个模糊术语、解决一个过载词（"account" 一词干三份工）、把一个难以逆转的决策记录为 ADR。它是 `/grill-with-docs` 驱动的主动纪律，保持 `GLOSSARY.md` 是一份干净的词汇表。
- **`/codebase-design`** 是深模块词汇（module、interface、depth、seam、adapter、leverage、locality），用于设计模块的*形状*：干净 seam 后面的小接口背后藏大量行为。`/tdd` 和 `/improve-codebase-architecture` 都说这门语言。

## 阶段边界

**阶段（phase）**是会话内的一块工作：拷问、实现、QA。在两个阶段之间的**边界**上你有五个选项，在它们之间挑选是整张地图里最模糊的决策：

- **Continue（继续）**：原地不动。零成本，零损失。
- **`/clear`**：清空窗口，当这里的内容对接下来无关时。
- **`/handoff`** 写一个可移植的 markdown 文件。窄用：只为**新 harness**、**新目录**、**同事**，或在**阶段中途**分叉支线任务。它买到的是可移植性。
- **Subagent（子代理）**：把范围收紧的任务送进它自己的窗口，拿回一份报告。
- **`/compact`** 压缩当前上下文并以此播种新会话。**默认项**，在树底而非第一选择。

读 [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) 看有序决策树：五个问题、每个分支背后的理由，以及为什么一手来源的成本让 **Continue** 成为要先决断的选项。决策在边界**处**做；阶段中途，要么继续，要么把剩余拆给 subagent。

## 独立

完全不在主流程上。

- **`/grill-me`**：与 `/grill-with-docs` 同样的无情访谈，但**无状态**：不在本地保存任何东西，也不建 `GLOSSARY.md`。当你**不在工作目录中工作**（打磨一个计划、一个设计、一篇文章，任何底下没有仓库的东西）时用它。如果你在工作目录里，改用 `/grill-with-docs`：它跑同样的访谈且留下书面痕迹，所以严格更好。
- **`/grilling`** 是访谈原语本身：一轮轮、前沿、事实归 agent 决策归你。`/grill-me` 和 `/grill-with-docs` 是两个具名入口，而 `/triage`、`/wayfinder` 和 `/improve-codebase-architecture` 都在内部运行它。只有当你想要不带任何包装的访谈时才直接用它。
- **`/prototype`** 是一个一次性的小程序，回答一个设计问题：这个状态模型对不对，或这个 UI 该长什么样。一次性是对代码写法的约束，不是销毁它的承诺：答案折进真正的代码，原型本身作为**一手来源**保存在 main 之外的 `prototype/<name>` 分支上，从实现 issue 指向它。它是主流程第 2 步的绕道，但任何时候设计问题在纸面上难以敲定时都可以用。
- **`/research`**：把阅读跑腿委托给**后台 agent**：它针对**一手来源**调查一个问题，然后在仓库里留下一份带引用的 Markdown 文件。它读书时你继续工作。它产出的文件是要*带进*主流程 `/grill-with-docs` 的东西，因为研究喂养思考而非替代思考。
- **`/to-questionnaire`** 出现在阻碍你的东西不在你脑子里、也不在代码库里、而在**别人**脑子里时，它写一份让对方填的问卷。它是 `/grill-me` 的反向：不是就主题访谈你，而是就**发送**访谈你（发给谁、需要拿回什么），并把问题对准缺口。回来的东西是 `/grill-with-docs` 或 `/to-spec` 的素材。
- **`/wizard`** 用于只有**人**能做的步骤：开通基础设施、配置凭据或 CI secrets、在不熟的第三方 dashboard 里点选、跑一次性迁移或割接。它生成一个交互式 bash 脚本，打开每个 URL、捕获每个值、写进 `.env` 和 GitHub secrets，让这套流程不再是你每次都要向 agent 重新解释的东西。模型调用，所以 agent 一碰到只有你能过的墙就会用它。如果 agent 自己能做，它就该自己做；这是真正需要人在环里的地方。
- **`/wait-what`** 是没听懂的消息的纠偏。在对话中途、任何其他 skill 内部使用，agent 用你缺失的上下文、以平实的语言、用 `GLOSSARY.md` 的词汇重新表述它刚说的话。它在事后起作用；`/grill-with-docs` 是事前解药，因为早先达成一致的语言才是让行话根本不出现的办法。
- **`/teach`**：跨多个会话学习一个概念，把当前目录当有状态的工作区。
- **`/writing-for-agents`** 是写 agent 消费的文档的参考：skills、AGENTS.md、被指向的文档。

## 前置条件

**`/setup-matt-pocock-skills`**：在你的第一个工程 flow 之前运行，配置其他 skill 默认依赖的 issue tracker、分诊标签和文档布局。自定义 issue tracker 也可以。
