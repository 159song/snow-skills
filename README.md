# snow-skills

仓库根目录是一个名为 `snow-skills` 的插件。Claude Code 和 Codex 共用 `skills/` 中的全部技能。

## 安装

### Claude Code

从当前仓库根目录运行 `claude --plugin-dir .` 可直接加载工作区版本。安装已发布的版本可运行以下命令。

```bash
claude plugin marketplace add 159song/snow-skills
claude plugin install snow-skills@snow-skills
```

或在 Claude Code 内执行 `/plugin marketplace add 159song/snow-skills`。

### Codex CLI

安装 GitHub 已发布版本，然后新开 Codex 会话：

```bash
codex plugin marketplace add 159song/snow-skills
codex plugin add snow-skills@snow-skills
```

测试本地已提交版本时，从仓库根目录导出插件文件到独立目录。Codex 会将本地安装源复制到缓存；保留导出目录供后续刷新。

```bash
mkdir -p ~/.local/share/snow-skills
plugin_src=$(mktemp -d ~/.local/share/snow-skills/local.XXXXXXXX)
git archive HEAD .claude-plugin .codex-plugin skills output-styles README.md LICENSE | tar -x -C "$plugin_src"
codex plugin marketplace add "$plugin_src"
codex plugin add snow-skills@snow-skills
```

输入 `$`，在技能列表中选择 snow-skills 的 explain 并输入主题。两端共用四级菜单。若当前模式无法显示四项单选框，回复 L1 到 L4 即可。

要在 Codex 自动使用 `ste-80`，通过 `/hooks` 查看并信任 snow-skills 的 SessionStart 钩子，再开启新会话。该钩子通过 `sed` 读取插件内的同一份风格正文。技能可以独立于该钩子使用。

## 默认输出风格

启用插件后，Claude Code 自动使用 `ste-80`，覆盖当前选择的输出风格。日常回答默认使用中文，审查和排障优先给出结论与证据。头脑风暴、产品命名和架构备选探索先展开不同方向，要求选型时再给建议。需要展开时可以直接说“详细解释”。原有的 Claude Code 工程指令继续生效。

在 Claude Code 中想理解某个问题时，输入 `/snow-skills:explain 为什么重试会导致重复下单？`。在支持的界面中先弹出单选框，选择 L1 简明文本、L2 静态图解、L3 交互 HTML 或 L4 讲解动画后再开始。

## 收录内容

| Skill | 来源 | 说明 |
|---|---|---|
| `explain` | 原创 | 手动调用，从四种形式中选择本次讲解的级别 |
| `rag-lifecycle` | rag-architect + rag-skills 合并重排，融入《生产级 RAG 系统》 | RAG 全生命周期：需求分析、选型设计、构建、生产化运维：3 个确定性 Python 工具 + 43 篇指南 + 15 章生产检查清单 |
| `dg-piagent` | buchidonggua/dg-ai-notes（冻结副本） | pi-agent / @earendil-works/pi-coding-agent SDK 开发：创建 agent、自定义工具、企业内网接口接入评估等 |
| `engineering/*`（20 个） | mattpocock/skills（翻译收录） | TDD、代码评审、领域建模、诊断 bug、spec/工单流等工程方法论 |
| `productivity/*`（7 个） | mattpocock/skills（翻译收录） | grilling 追问、教学、交接、写作等生产力 skill |
| `books/*`（14 个） | ciembor/agent-rules-books（冻结副本） | 14 本经典软件工程书提炼的规则集（mini/nano/full 三档）：整洁代码、整洁架构、DDD 三部曲、重构、DDIA、PoEAA、发布！、程序员修炼之道等 |

## 结构

```
.claude-plugin/     # 共享 marketplace 和 Claude Code 清单
.codex-plugin/      # Codex 插件清单与启动钩子
output-styles/      # 两端共用的表达规则
skills/
  rag-lifecycle/    # RAG 全生命周期 skill（SKILL.md + 工具 + guides/ + 生产检查清单）
  dg-piagent/
  explain/          # 四级讲解
  engineering/      # mattpocock 工程类
  productivity/     # mattpocock 生产力类
  books/            # agent-rules-books 经典书籍规则集（14 本，mini/nano/full 三档）
```

## 来源与致谢

- **rag-architect / rag-skills**：RAG 专题指南合集（MIT），其指南经翻译合并进入 `rag-lifecycle`，并按《生产级 RAG 系统——从架构到 Python 实现》的 15 章生命周期重新组织，新增数据模型、可验证引用、安全威胁模型、可观测性与生产检查清单
- **mattpocock/skills**：Matt Pocock 的工程方法论 skill（MIT，翻译收录稳定集）
- **buchidonggua/dg-ai-notes**：`dg-piagent` 即其 `skills/dg-piagent`（MIT，冻结副本）；其 references 内含 Pi-Agent 教程的 Python 改写版与 `earendil-works/pi`（MIT）SDK 文档摘编
- **ciembor/agent-rules-books**：`books/*` 即其 14 本书规则集（MIT，冻结副本 v0.6）；规则正文（mini/nano/full）保持英文原文，`SKILL.md` 入口重写为中文 description 以统一触发体验。规则为社区提炼、非原书替代品

mattpocock 系列与 `dg-piagent` 为冻结副本（vendor），上游更新需手动同步；`rag-lifecycle` 为原创重设计，不再跟随上游。详见 `LICENSE` 中的版权声明。

## License

MIT（含上游版权声明，见 `LICENSE`）。
