---
name: wayfinder
description: 把一大块工作（大到单个 agent 会话装不下）规划成 issue tracker 上一张由决策 ticket 组成的共享地图，然后一次解决一个，直到通往目的地的路清晰为止。
disable-model-invocation: true
---

一个松散的想法到来了，大到单个 agent 会话装不下，而且裹在雾里：从这里到**目的地**的路还看不见。寻路（wayfinding）讲的是找到那条路，而不是朝目的地猛冲。这个 skill 把路绘制成仓库 issue tracker 上的一张**共享地图**，然后逐个处理它的**决策 ticket**（其解决是一个决策的问题，而不是待执行的构建切片），直到路线清晰。

目的地因每次努力而异，为它命名是绘图的第一步：它塑造每个 ticket。它可能是一份用来交接和迭代的 spec、一个在规划开始前要锁定的决策、或一个就地完成的变更比如数据结构迁移。地图与领域无关：工程工作、课程内容，任何符合这个形状的东西。

## 做规划，不做执行

Wayfinder 默认是**规划**：每个 ticket 解决一个决策，路清晰了地图就完成了，在有人去把事情做掉之前再无待决事项。想直接把活干了的冲动通常是你已到达地图边缘、该交接了的信号。某次努力可以在它的 **Notes** 里覆盖这一点，把执行也带进地图，但若没有那个设定，请产出决策而不是交付物。

## 按名字引用

每张地图和每个 ticket 都是 issue，所以都有一个**名字**：它的标题。在人读到的一切里（叙述、地图的 Decisions-so-far），按那个名字引用它，绝不裸用 id、编号或 slug。一墙的 `#42, #43, #44` 没法读；名字一眼可读。id 和 URL 不会消失；名字包裹着它的链接，但它们_藏在_名字里面，绝不顶替名字。

## 地图（The Map）

地图是本仓库 issue tracker 上的单个 issue，带 `wayfinder:map` 标签，是规范化工件。它的 ticket 是地图的子 issue。

地图是一个**索引**，不是存储。它列出已做的决策并指向持有细节的 ticket；一个决策只活在一个地方，它的 ticket 里，所以地图绝不重述决策，只给 gist 并附链接。

**地图、它的子 ticket、阻塞和前沿查询在物理上放在哪取决于具体 tracker。** issue tracker 应该已经提供给你了。如果没有，让用户运行 `/setup-matt-pocock-skills`。查阅 tracker 文档的「寻路操作」一节，了解_本_仓库如何表达它们。如果没有提供 tracker，默认用本地 markdown tracker。

### 地图正文

低分辨率下的整张地图，每会话加载一次。未关闭的 ticket **不**列出：它们是未关闭的子 issue，靠查询发现。

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Ticket

每个 ticket 是地图的**子 issue**；tracker 的 issue id 是它的身份。它的正文就是问题，大小以一个 100K token 的 agent 会话为限：

```markdown
## Question

<the decision or investigation this ticket resolves>
```

每个 ticket 带一个 `wayfinder:<type>` 标签，取值为 `research`、`prototype`、`grilling`、`task` 之一（见 [Ticket 类型](#ticket-类型)）。`wayfinder:` 标签是地图及其 ticket 携带的仅有标签，绝不带 `ready-for-agent` 之类的 triage 标签：它们是决策，不是实现工作。

会话**认领** ticket 的方式是把它分配给推进地图的开发者，而且**最先**做，先于任何工作，这样并发会话就会跳过它。受理人_就是_认领：一个未关闭、无受理人的 ticket 就是未被认领。

阻塞用 tracker 的**原生**依赖关系：这很关键，因为它让前沿在 tracker 自己的 UI 里_可视化_呈现，人不打开地图就能看见什么可拿。只有缺乏原生阻塞的 tracker 才回退到正文约定。每个阻塞它的 ticket 都关闭后，一个 ticket 即**解除阻塞**；**前沿（frontier）**是未关闭、未阻塞、未被认领的子 issue，已知世界的边缘。

答案不是正文的一部分；它在解决时记录（见[走通地图](#走通地图)）。解决 ticket 期间创建的资产从 issue 链接过去，不粘贴进来。

## Ticket 类型

每个 ticket 要么是 **HITL**（human in the loop，人在环中，_与_一个代表自己说话的人一起干），要么是 **AFK**，由 agent 独自驱动。HITL ticket 只能通过那场活的交流解决；agent 绝不替人代言（一个自问自答的 grilling agent 就破坏了这一点）。

- **Research（调研）**（AFK）：阅读文档、第三方 API 或本地资源（如知识库），把某个决策正在等待的事实挖出来。由一个调用 Skill 工具加载 "research" 的子 agent 解决。当需要当前工作目录之外的知识时使用。
- **Prototype（原型）**（HITL）：通过调用 Skill 工具加载 "prototype"，做一个廉价、粗糙、具体可供反应的工件（提纲、粗稿、stub、或 UI/逻辑代码）来提高讨论的保真度。把原型作为资产链接。"应该长什么样"或"应该怎么表现"是关键问题时使用。
- **Grilling（拷问）**（HITL）：对话。默认情形。永远调用 Skill 工具两次，加载 "grilling" 和 "domain-modeling"。
- **Task（任务）**（HITL 或 AFK）：在能做某个_决策_之前必须发生的手工工作：没有可决策、可原型、可调研的东西，但讨论被卡住直到它完成。注册一个服务好评估它的 API、开通权限、搬运数据好看清它的形状。这是唯一一个_做事_而不是_做决策_的类型，它靠解锁一个决策挣得自己的位置，而不是靠交付目的地。agent 能独跑就独跑（AFK）；否则给人类一张精确的清单（HITL）。工作完成即解决；答案记录做了什么以及后续 ticket 依赖的任何由此产生的事实（凭据位置、新 URL、行数）。

## 战争之雾（Fog of war）

地图_刻意_不完整：看不清的就不要绘。活着的 ticket 之外是**战争之雾**：那些你料得到会来、却还钉不下来的决策和调研的模糊视野，因为它们悬在仍开放的问题上。解决一个 ticket 会清掉它前方的雾，把现在变得可指定的东西逐个毕业成新 ticket，直到通往目的地的路清晰、ticket 一个不剩。

地图的 **Not yet specified** 小节就是写下那片模糊视野的地方：疑点问题、日后要重访的区域。它是_通向_目的地的未发现前沿：这里的一切都在范围内，只是还没锐利到能开 ticket。视野允许就写得松，视野够好就写得满；它同时是给读这份努力走向的协作者看的路标。

**雾还是 ticket？** 判据是你现在能不能把问题陈述得足够精确，_而不是_你现在能不能回答它。

- **开 ticket 当**问题已经锐利，即使它被阻塞、暂时动不了。
- **写进 Not yet specified 当**你还没法把话说得那么锐。不要预先把雾切成 ticket 大小的块：它比 ticket 粗，一片雾在前沿到达时可能毕业成多个 ticket，也可能一个都没有。

**Not yet specified** 排除已决定的（Decisions so far）、已是活 ticket 的、和范围外的（下一节）。

## 范围外（Out of scope）

雾只朝目的地聚集。目的地固定了范围，所以它之外的工作是**范围外**：它不是雾，也不属于 **Not yet specified**。它在地图上有自己的 **Out of scope** 小节：你有意识排除在_这次_努力之外的工作。是范围，不是锐度，把它放在这里。

范围外的工作永远不会毕业（前沿止步于目的地），所以只有目的地被重画时它才会回来，而且那时是全新的努力，不是恢复。

把某事划为范围外是一次框定行为，不是路线上的一步。当一个已存在的 ticket 结果坐在目的地之外（绘图时误框进来的，或被某个解决暴露出来的），**关闭它**（关闭的 ticket 毫无歧义地在前沿之外），并在 **Out of scope** 小节留下一行：gist 加上为什么出范围，链接那个已关闭的 ticket。它不进 **Decisions so far**，那里记录实际走过的路线；范围边界不是路线上的一步。

## 调用

两种模式。无论哪种，**每会话解决的 ticket 绝不超过一个**，research ticket 是例外。

### 绘制地图

用户带着一个松散的想法调用。

1. **为目的地命名。** 调用 Skill 工具两次，加载 "grilling" 和 "domain-modeling"，敲定这张地图在寻路去往什么：spec、决策、还是变更。目的地固定范围，所以先定它。
2. **绘制前沿。** 再次拷问，这次**广度优先**：在整个空间上扇开，而不是在单条线索上深挖，把开放的决策和现在就能迈出的第一步都翻出来。**如果这没有翻出任何雾**（通往目的地的路已经清晰，整段旅程小到一个会话装得下），你不需要地图。停下来问用户想怎么继续。
3. **创建地图**（标签 `wayfinder:map`）：填好 Destination 和 Notes，Decisions-so-far 留空，雾勾勒进 **Not yet specified**。
4. **创建你现在能指定的 ticket** 作为地图的子 issue，然后在**第二遍**里接阻塞边（issue 要先有 id 才能互相引用）。也在那一遍里写交叉引用，用真实 id：占位的 `#<n>` 会自动链接到一个不相干的 issue。接线把它们分进前沿和被阻塞的；你还指定不了的一切留在雾里：**Not yet specified** 小节。
5. **发射 research 子 agent。** 对你刚创建的每个 `research` ticket，启动一个带全新上下文窗口的子 agent，调用 Skill 工具加载 "research" 并行解决它，把发现捕获到一次性 `research/<name>` 分支上，并从 ticket 留下上下文指针。推送分支但不开 PR：它永远不会被合并。
6. 停：绘图是一个会话的工作量；它不亲手解决任何东西。

### 走通地图

用户带着一张地图（URL 或编号）调用。ticket 是**可选的**：没有的话，由你而不是用户挑下一个决策。

1. 加载**地图**：低分辨率视图，不是每个 ticket 的正文。
2. 选 ticket。如果用户点了名，就用它。否则按顺序取第一个前沿 ticket。**认领它**：做任何工作之前先分配给自己。
3. 按其 `wayfinder:<type>` 标签命名的类型解决它（见 [Ticket 类型](#ticket-类型)）。读标签，别只读正文：正文从不陈述类型。**按需缩放**：按需取任何相关或已关闭 ticket 的完整正文；`## Notes` 块点到哪些 skill 就对哪些调用 Skill 工具。拿不准时，调用 Skill 工具两次，加载 "grilling" 和 "domain-modeling"。
4. 记录解决：把答案作为**解决评论**发布，**关闭** issue，并向地图的 Decisions-so-far **追加上下文指针**。
5. 加上新翻出来的 ticket（先创建后接线）；让答案使其变得可指定的任何雾毕业，并从 **Not yet specified** 清掉每片毕业的雾，让它只以新 ticket 的形式存在。如果答案揭示某个 ticket（这个或另一个）坐在目的地之外，**把它划为范围外**而不是在路线上解决它。如果该决策使地图的其他部分失效，更新或删除那些 ticket。

用户可以并行跑多个未阻塞的 ticket，所以要有其他会话并发编辑 tracker 的预期。
