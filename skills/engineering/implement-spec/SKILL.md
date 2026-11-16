---
name: implement-spec
description: "用代码实现 /to-spec 与 /to-tickets 的产物。"
disable-model-invocation: true
---

你已拿到一份 spec。这份 spec 应该带有与之关联的 ticket，描述如何实现它。

issue tracker 应该已经提供给你。如果没有，让用户运行 `/setup-matt-pocock-skills`。

目标是整个 spec 落在一个**集成分支**上实现完毕，每个 ticket 都以 issue tracker 关闭工作的方式解决。

这些 ticket 不是一份步骤清单。它们是一张带阻塞关系的**任务图（task graph）**。这意味着永远存在一个可以认领的**前沿（frontier）**。

每个 subagent 都以全新上下文窗口启动。

与 subagent 的往来沟通应该稀疏。主要通过**上下文指针**沟通：指向 spec、ticket、研究笔记和既往 commit。不要复制指针已能拿到的信息。

**Implementer subagent** 应尽可能在后台运行，以获得最大并发。

## 步骤

1. 读 spec 和 ticket，理解任务图。

2.（可选）用一个**探索 subagent** 完成 ticket 所需的任何探索——相关代码库文件或外部文档。确保探索 subagent 能保存文件——它应把 markdown 笔记保存在仓库之外的一个目录里，供后续所有 subagent 访问。这让 **implementer subagent** 专注于实现而非探索。

3. 创建集成分支。如果 issue tracker 通过 PR 关闭工作，或用户要求 PR，在步骤 5 第一次合并之后开一个 draft PR（领先 main 零个 commit 的分支开不了 PR），标记为关闭该 spec 和这些 ticket。

4. 每个 ticket 用一个全新的 **implementer subagent**，各自在自己的 worktree、自己的分支上。每个 implementer subagent：
   - 开始前确认自己的 worktree 基于集成分支，不是就 reset 到它上面；
   - 调用 Skill 工具运行 `tdd` 来构建该 ticket；
   - 报告完成前把集成分支顶端 merge 进自己的分支

5. 一个 **implementer subagent** 完成后，用一个 **merger subagent** 把它的工作 merge 到集成分支。

6. 如果这改变了可认领 ticket 的**前沿**，再启动更多 **implementer subagent** 处理新 ticket。这带来最大并发。

7. 所有 ticket 完成后，在集成分支上调用 Skill 工具运行 `code-review`。用一个全新的 **implementer subagent** 一次性修复 code review 提出的所有问题。

8. 如果存在 draft PR，把它标记为可 review。否则，以 issue tracker 关闭工作的方式逐个解决 ticket，并报告集成分支。

9. 清理所有 **implementer subagent** 的 worktree。
