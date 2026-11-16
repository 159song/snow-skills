# Issue tracker：GitHub

本仓库的 issue 和 spec 以 GitHub issues 的形式存放。所有操作使用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文用 heredoc。
- **读取 issue**：`gh issue view <number> --json number,title,body,labels,comments`。
- **列出 issues**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，搭配适当的 `--label` 和 `--state` 过滤。
- **把 issue 设为父 issue 的子 issue**：`gh issue create --parent <parent> ...`，或事后 `gh issue edit <parent> --add-sub-issue <child>`（`gh` 2.94+）。较老的 `gh`：`gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`（数据库 id，见下方 **Blocking**）。没有子 issue 功能时，在子 issue 正文顶部放一行 `Part of #<parent>`。
- **Blocking（阻塞）**：GitHub 的**原生 issue 依赖**，规范化、UI 可见的表达。加一条边用 `gh issue create --blocked-by <n>,<n> ...` 或 `gh issue edit <child> --add-blocked-by <blocker>`（`gh` 2.94+）。较老的 `gh`：`gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`，其中 `<blocker-db-id>` 是阻塞方的数字**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，_不是_ `#number` 也不是 `node_id`）。依赖不可用时，回退到子 issue 正文顶部的 `Blocked by: #<n>, #<n>` 行。每个阻塞方都关闭后，ticket 即解除阻塞。
- **统计未关闭的阻塞方**：`gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by`（只算未关闭的阻塞方；0 表示可以开工）。`gh issue view <n> --json blockedBy` 也会列出已关闭的阻塞方，所以要过滤：`--jq '[.blockedBy.nodes[] | select(.state == "OPEN")] | length'`。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **添加 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：先用 `gh issue comment <number> --body "..."` 发说明，再 `gh issue close <number>`。对已关闭的 issue，`gh issue close --comment` 会丢弃评论但仍然退出码为 0。

从 `git remote -v` 推断仓库；在克隆内部运行时 `gh` 自动完成。

只向用户自己的仓库提 issue。绝不向 `mattpocock/skills`（这些 skill 的来源仓库）提 issue，除非用户拥有它。在 fork 中，`gh` 可能默认指向上游父仓库，所以会话里第一次 `gh issue create` 之前，用 `gh repo view --json nameWithOwner` 检查目标，如果不是用户的仓库就与用户确认。

## 把 pull request 作为 triage 面

**PRs as a request surface: No.** _（如果本仓库把外部 PR 当作功能请求处理，则设为 `yes`；`/triage` 会读这个标志。）_

设为 `yes` 时，PR 走与 issue 相同的标签和状态，使用 `gh pr` 等价命令：

- **读取 PR**：`gh pr view <number>`，然后 `gh pr view <number> --comments`（非 TTY 下 `--comments` 只打印评论，不含正文），diff 用 `gh pr diff <number>`。
- **列出待 triage 的外部 PR**：`gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`。
- **评论 / 打标签 / 关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 和 PR 共用一个编号空间，所以光一个 `#42` 可能是两者之一：用 `gh pr view 42` 解析，失败再回退 `gh issue view 42`。

## 当 skill 说「发布到 issue tracker」

创建一个 GitHub issue。

## 当 skill 说「取回相关 ticket」

按上方**读取 issue**的方式读取。

## 寻路操作（Wayfinding operations）

供 `/wayfinder` 使用。**map（地图）**是单个 issue，ticket 作为其**子** issue。

- **Map**：单个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`gh issue create --label wayfinder:map`。
- **子 ticket**：作为 GitHub 子 issue 链接到 map 的 issue（见**把 issue 设为父 issue 的子 issue**）。子 issue 功能不可用时，把子 issue 加进 map 正文的任务列表，并在子 issue 正文顶部放 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。一旦被认领，ticket 就分配给推进的开发者。
- **Blocking**：见「约定」下的 **Blocking**。
- **前沿查询（Frontier query）**：列出 map 的未关闭子 issue（`gh issue list --state open`，限定在 map 的子 issue / 任务列表内），去掉任何带未关闭阻塞方（见**统计未关闭的阻塞方**，或 `Blocked by` 行中的未关闭 issue）或有受理人的；按 map 顺序第一个胜出。
- **认领（Claim）**：`gh issue edit <n> --add-assignee @me`，这是会话的第一个写操作。
- **解决（Resolve）**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，再向 map 的 Decisions-so-far 追加上下文指针（gist + 链接）。
