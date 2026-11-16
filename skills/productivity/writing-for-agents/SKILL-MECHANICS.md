# Skill 机制

[`writing-for-agents`](SKILL.md) 的 skill 专属分支：当文档是 skill 时会有什么变化（frontmatter、调用方式的选择、路由式 skill）。其余写作要点都在 `SKILL.md` 的通用参考里。

## 调用方式

两种选择，权衡的是那两种负载：

- **模型调用（model-invoked）**的 skill 保留 `description`，因此 agent 可以自主触发它，其他 skill 也能触达它。你仍然可以手动输入它的名字：模型调用永远_包含_用户触达；description 只会增加 agent 的可发现性，从不会夺走人的那一份。description 是 skill 的顶层上下文指针，被迫常驻加载：用永久的上下文负载换可发现性。内容全是参考的模型调用 skill，还是共享参考的一个落脚点：其他 skill 可以调用它，于是多个 skill 都需要的参考就集中在一处。做法：省略 `disable-model-invocation`，并写一段面向模型的、携带触发分支的 description（`SKILL.md` 中的指针写作规则完全适用）。
- **用户调用（user-invoked）**的 skill 把 description 从 agent 的触达范围里剥掉：只有手动输入名字的人能调用它，其他任何 skill 都不能。上下文负载为零，但花的是认知负载：你就是那个必须记得它存在的索引。做法：设置 `disable-model-invocation: true`；`description` 变为面向人：一行摘要，剥掉触发词列表。

只有当 agent 必须能自主触达这个 skill，或其他 skill 必须触达它时，才选模型调用。如果它只会被手动触发，就做成用户调用，不付上下文负载。

两个用户调用 skill 都需要的共享参考，哪一边都放不下：没有 description，谁也触发不了谁。把它推到 skill 体系之外的普通文件里：变成任何 skill 都能指向的外部参考。

## 按调用方式拆分

拆分中的调用切分（序列切分见 `SKILL.md`）：当你有一个应当独立触发它的独特引导词（一个你确实会在 prompt 里用到的触发词），或另一个 skill 必须触达它时，拆出一个模型调用的 skill。你要为新的常驻 description 支付上下文负载，所以这份独立触达必须物有所值。

## 路由式 skill

当用户调用的 skill 多到记不过来，堆积的认知负载用**路由式 skill（router skill）**来治：一个用户调用的 skill，列明其他 skill 各是什么、何时用哪个，让人只需记住一个而不是很多个。它只能提示，永远不能触发它们：用户调用的 skill 没有 description，除了人以外谁也触达不了它们。
