---
name: setup-matt-pocock-skills
description: "为本仓库配置工程 skills：设置 issue tracker、triage 标签词汇表和领域文档布局。在其他工程 skills 首次使用前运行一次。"
disable-model-invocation: true
---

# 初始化 Matt Pocock's Skills

为工程 skills 所依赖的仓库级配置搭好脚手架：

- **Issue tracker（issue 跟踪器）**：issue 存放的位置（默认 GitHub；本地 markdown 也开箱即用）
- **Triage 标签**：五个规范化 triage 角色所用的字符串
- **领域文档**：`GLOSSARY.md` 和 ADR 存放的位置，以及读取它们的消费规则

这是一个提示词驱动的 skill，不是确定性脚本。先探索，呈现发现，与用户确认，然后再写。

## 流程

### 1. 探索

查看当前仓库以了解起始状态。读实际存在的东西，不要靠假设：

- `git remote -v` 和 `.git/config`：这是 GitHub 仓库吗？是哪一个？
- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：是否存在？其中是否已有 `## Agent skills` 小节？
- 仓库根目录的 `GLOSSARY.md` 和 `GLOSSARY-MAP.md`，以及旧版的 `CONTEXT.md` / `CONTEXT-MAP.md`。如果存在旧版文件，提议用 `git mv` 改成 `GLOSSARY` 名称，并把 `docs/agents/domain.md` 里的这些名字改写过来。
- `docs/adr/` 和任何 `src/*/docs/adr/` 目录
- `docs/agents/`：这个 skill 之前的产出是否已存在？
- `.scratch/`：说明本地 markdown issue tracker 约定已在使用的信号
- `triage` skill 是否已安装？（本目录旁有 `triage` skill 文件夹，或你的可用 skills 里有 `triage`。）这决定 B 节是否运行。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 里的 `workspaces` 字段、或自带 `src/` 的成规模 `packages/*`。这些只出现在真正的大型多包仓库；没有它们就是单一上下文，而几乎每个仓库都是单一上下文。

### 2. 呈现发现并询问

总结哪些已存在、哪些缺失。然后按节依次进行。一节一个问题，答完再下一节。

每一节都以推荐答案开头，让用户一个词就能接受。只在选择真的有分叉时给一行解释；探索已经定论的小节直接跳过（没装 `triage` 时跳过 B 节，没有 monorepo 时跳过 C 节）。

**A 节：Issue tracker。**

> 解释：「issue tracker」是本仓库 issue 的存放地。`to-tickets`、`triage`、`to-spec` 等 skill 从中读写。它们需要知道该调 `gh issue create`、在 `.scratch/` 下写 markdown 文件，还是遵循你描述的其他工作流。选你实际为本仓库跟踪工作的地方。

默认姿态：这些 skill 为 GitHub 设计。如果 `git remote` 指向 GitHub，就提议 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自建主机），就提议 GitLab。否则（或用户另有偏好时），提供：

- **GitHub**：issue 存放在仓库的 GitHub Issues（使用 `gh` CLI）
- **GitLab**：issue 存放在仓库的 GitLab Issues（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 markdown**：issue 以文件形式存放在本仓库的 `.scratch/<feature>/` 下（适合单人项目或没有远端的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流；skill 会把它记录为自由格式的文字

把选择记录到 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带一个 "PRs as a request surface"（PR 作为请求面）标志，默认**关闭**。保持关闭且不要主动提起：想要外部 PR 进入 triage 队列的用户日后可以自己在文件里翻开这个标志。

GitHub 或 GitLab tracker 需要一个可达的仓库。当用户选了其一而没有任何 `git remote` 指向该主机时，向他们要仓库 URL 并接好（必要时 `git init`、`git remote add origin <url>`）再继续。在这个目录里运行 `gh repo view` / `glab repo view` 能打印出项目即算完成；打不出来就停下，告诉用户缺什么。

**B 节：Triage 标签词汇表。** 如果 `triage` skill 没安装（探索阶段已经告诉你了），整节跳过，因为未安装的 skill 不需要标签。

如果已安装，只问一个问题：

> 是否保留默认的 triage 标签？（推荐：**是**）

默认值是五个规范化角色，每个标签字符串与其名称相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。答**是**就原样写入。只有当用户说否时——通常因为他们的 tracker 已在用其他名字（例如用 `bug:triage` 对应 `needs-triage`）——才收集替换值，让 `triage` 复用既有标签而不是制造重复。

**C 节：领域文档。** 默认**单一上下文**（仓库根一个 `GLOSSARY.md` + `docs/adr/`）。这适合几乎所有仓库；直接写，不用问。

只有当探索发现了 monorepo 信号时，才提供**多上下文**（根级 `GLOSSARY-MAP.md` 指向各上下文的 `GLOSSARY.md`）。此时确认用户想要哪种布局。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要加进被编辑的 `CLAUDE.md` / `AGENTS.md`（选择规则见第 4 步）的 `## Agent skills` 块
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个仅在 `triage` 已安装时）

写之前先让用户改。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果都不存在，问用户要建哪个；不要替他们选。

`CLAUDE.md` 已存在时绝不创建 `AGENTS.md`（反之亦然）；永远编辑已在的那个。

如果所选文件里已有 `## Agent skills` 块，就地更新其内容而不是追加重复。不要覆盖用户对周围小节的修改。

该块内容：

```markdown
## Agent skills

### Issue tracker

[一句话概括 issue 跟踪在哪里]。见 `docs/agents/issue-tracker.md`。

### Triage labels

[一句话概括标签词汇表]。见 `docs/agents/triage-labels.md`。

### Domain docs

[一句话概括布局："single-context" 或 "multi-context"]。见 `docs/agents/domain.md`。
```

仅当 `triage` 已安装且 B 节运行过时，才包含 `### Triage labels` 子块并写入 `docs/agents/triage-labels.md`。否则两者都省略。

当 B 节在 GitHub 或 GitLab 上运行过时，创建 tracker 缺少的每个已配置标签（`gh label create` / `glab label create`）。

然后以本 skill 目录中的种子模板为起点写入各文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 markdown issue tracker
- [triage-labels.md](./triage-labels.md)：标签映射（仅当 `triage` 已安装）
- [domain.md](./domain.md)：领域文档消费规则 + 布局

对「其他」issue tracker，根据用户的描述从零编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户配置已完成，以及哪些工程 skills 从此会读取这些文件。提醒他们日后可以直接编辑 `docs/agents/*.md`；只有想更换 issue tracker 或从头重来时才需要重跑本 skill。
