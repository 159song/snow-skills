# Design It Twice（设计两遍）

当用户想为选定的深化候选探索备选 interface 时，使用这个并行 sub-agent 模式。基于 "Design It Twice"（Ousterhout）：你的第一个想法不太可能是最好的。

使用 [SKILL.md](SKILL.md) 中的词汇：**module**、**interface**、**seam**、**adapter**、**leverage**。

## 流程

### 1. 框定问题空间

在生成 sub-agent 之前，为选定候选写一份面向用户的问题空间说明：

- 任何新 interface 都要满足的约束
- 它依赖的东西，以及它们各属哪个类别（见 [DEEPENING.md](DEEPENING.md)）
- 一个粗略的示意性代码草图，用来把约束落地——不是提案，只是让约束具体化的方式

把它展示给用户，然后立刻进入第 2 步。用户在 sub-agent 并行工作的同时阅读和思考。

### 2. 生成 sub-agent

并行生成 3 个以上 sub-agent，每个有全新的上下文窗口。每个必须为深化模块产出一个**截然不同**的 interface。

给每个 sub-agent 一份独立的技术简报（文件路径、耦合细节、来自 [DEEPENING.md](DEEPENING.md) 的依赖类别、seam 后面是什么）。简报独立于第 1 步面向用户的问题空间说明。给每个 agent 不同的设计约束：

- Agent 1："最小化 interface：最多 1–3 个入口点。最大化每个入口点的 leverage。"
- Agent 2："最大化灵活性：支持多种用例和扩展。"
- Agent 3："为最常见的调用方优化：让默认情形平凡。"
- Agent 4（如适用）："围绕 ports & adapters 设计跨 seam 依赖。"

简报中同时包含 [SKILL.md](SKILL.md) 词汇和 GLOSSARY.md 词汇，让每个 sub-agent 的命名与架构语言和项目领域语言保持一致。

每个 sub-agent 输出：

1. interface（类型、方法、参数，加上不变量、顺序、错误模式）
2. 展示调用方如何使用它的用例示例
3. 实现在 seam 后面藏了什么
4. 依赖策略与 adapter（见 [DEEPENING.md](DEEPENING.md)）
5. 权衡：leverage 在哪里高、哪里薄

### 3. 展示与比较

顺序展示各个设计让用户逐个消化，然后用文字比较。按**深度（depth）**（interface 处的 leverage）、**局部性（locality）**（变更集中在哪里）和 **seam 位置**对比。

比较之后给出你自己的推荐：你认为哪个设计最强、为什么。如果不同设计的元素能很好地组合，提出一个混合方案。要有主见：用户要的是一个鲜明的判断，不是一份菜单。
