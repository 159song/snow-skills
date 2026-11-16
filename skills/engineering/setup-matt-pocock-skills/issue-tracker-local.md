# Issue tracker：本地 Markdown

本仓库的 issue 和 spec 以 markdown 文件的形式存放在 `.scratch/`。

## 约定

- 每个特性一个目录：`.scratch/<feature-slug>/`
- spec 是 `.scratch/<feature-slug>/spec.md`
- 实现 issue 是每 ticket 一个文件，放在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号，绝不合并成单个 tickets 文件
- triage 状态记录在每个 issue 文件顶部附近的 `Status:` 行（角色字符串见 `triage-labels.md`）
- 评论和对话历史以 `## Comments` 标题追加到文件底部

## 当 skill 说「发布到 issue tracker」

在 `.scratch/<feature-slug>/` 下创建新文件（需要时创建目录）。

## 当 skill 说「取回相关 ticket」

读取被引用路径上的文件。用户通常会直接给路径或 issue 编号。

## 寻路操作（Wayfinding operations）

供 `/wayfinder` 使用。**map（地图）**是一个文件，每个 ticket 一个**子**文件。

- **Map**：`.scratch/<effort>/map.md`（Notes / Decisions-so-far / Fog 正文）。
- **子 ticket**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 开始编号，正文写问题。`Type:` 行记录 ticket 类型（`research`/`prototype`/`grilling`/`task`）；`Status:` 行记录 `claimed`/`resolved`。
- **Blocking（阻塞）**：顶部附近的 `Blocked by: NN, NN` 行。它列出的每个文件都 `resolved` 后，ticket 即解除阻塞。
- **前沿（Frontier）**：扫描 `.scratch/<effort>/issues/`，找未关闭、未阻塞且未被认领的文件；按编号第一个胜出。
- **认领（Claim）**：设 `Status: claimed` 并保存，然后才开始任何工作。
- **解决（Resolve）**：在 `## Answer` 标题下追加答案，设 `Status: resolved`，再向 `map.md` 中 map 的 Decisions-so-far 追加上下文指针（gist + 链接）。
