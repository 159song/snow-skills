# Issue tracker：GitLab

本仓库的 issue 和 spec 以 GitLab issues 的形式存放。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行描述用 heredoc。传 `--description -` 可打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。机器可读输出用 `-F json`。
- **列出 issues**：`glab issue list -O json`，搭配适当的 `--label` 过滤。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 把评论叫 "notes"。
- **添加 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可以用逗号分隔或重复该标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，所以先用 `glab issue note <number> --message "..."` 发说明，再关闭。
- **合并请求**：GitLab 把 PR 叫 "merge requests"。使用 `glab mr create`、`glab mr view`、`glab mr note` 等，形状与 `gh pr ...` 相同，只是 `pr` 换成 `mr`、`comment`/`--body` 换成 `note`/`--message`。

从 `git remote -v` 推断仓库；在克隆内部运行时 `glab` 自动完成。

## 把合并请求作为 triage 面

**MRs as a request surface: No.** _（如果本仓库把外部合并请求当作功能请求处理，则设为 `yes`；`/triage` 会读这个标志。）_

设为 `yes` 时，MR 走与 issue 相同的标签和状态，使用 `glab mr` 等价命令：

- **读取 MR**：`glab mr view <number> --comments`，diff 用 `glab mr diff <number>`。
- **列出待 triage 的外部 MR**：`glab mr list -O json`，然后只保留作者不是项目成员/所有者的 MR（贡献者的 MR，而非维护者进行中的工作）。
- **评论 / 打标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 的 issue 和 MR 编号是分开的，所以只要知道维护者指的是哪个面，`#42` 就没有歧义。

## 当 skill 说「发布到 issue tracker」

创建一个 GitLab issue。

## 当 skill 说「取回相关 ticket」

运行 `glab issue view <number> --comments`。

## 寻路操作（Wayfinding operations）

供 `/wayfinder` 使用。**map（地图）**是单个 issue，ticket 作为其**子** issue。

- **Map**：单个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`glab issue create --label wayfinder:map`。（在有原生 epic 的 GitLab 版本上，也可以用 epic 承载 map；带标签的 issue 到处可用。）
- **子 ticket**：描述顶部带 `Part of #<map>`、链接到 map（`glab issue create --linked-issues <map> --link-type relates_to`）并带 `wayfinder:<type>` 标签（`research`/`prototype`/`grilling`/`task`）的 issue。一旦被认领，ticket 就分配给推进的开发者。
- **Blocking（阻塞）**：GitLab 的**原生阻塞链接**，规范化、UI 可见的表达。用 `/blocked_by #<n>` 快速操作添加，以 note 形式发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接是 Premium/Ultimate 功能；在免费版（或不可用之处）回退到描述顶部的 `Blocked by: #<n>, #<n>` 行。每个阻塞方都关闭后，ticket 即解除阻塞。
- **前沿查询（Frontier query）**：用 `glab api projects/:id/issues/<map>/links` 列出 map 的子 issue，保留带 `wayfinder:<type>` 标签的未关闭 issue；去掉任何带未关闭阻塞方的：指向未关闭 issue 的原生 `blocked_by` 链接（`glab api projects/:id/issues/<child-iid>/links`）、`Blocked by` 行中的未关闭 issue、或有受理人的；按 map 顺序第一个胜出。
- **认领（Claim）**：`glab issue update <n> --assignee @me`，这是会话的第一个写操作。
- **解决（Resolve）**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再向 map 的 Decisions-so-far 追加上下文指针（gist + 链接）。
