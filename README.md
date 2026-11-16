# snow-skills

我的个人 Claude Code skill 集合，以 plugin marketplace 形式发布，全中文。

## 安装

```bash
claude plugin marketplace add 159song/snow-skills
claude plugin install snow-skills@snow-skills
```

或在 Claude Code 内执行 `/plugin marketplace add 159song/snow-skills`。

## 收录内容

| Skill | 来源 | 说明 |
|---|---|---|
| `rag-architect` | rag-architect + rag-skills 合并 | 设计、调优、评测生产级 RAG 管线：3 个确定性 Python 工具（chunking 优化 / 管线设计 / 检索评测）+ 40 余篇按需加载的专题指南 |
| `dg-piagent` | 原创 | pi-agent / @earendil-works/pi-coding-agent SDK 开发：创建 agent、自定义工具、企业内网接口接入评估等 |
| `engineering/*`（18 个） | mattpocock/skills（翻译收录） | TDD、代码评审、领域建模、诊断 bug、spec/工单流等工程方法论 |
| `productivity/*`（7 个） | mattpocock/skills（翻译收录） | grilling 追问、教学、交接、写作等生产力 skill |

## 结构

```
.claude-plugin/     # marketplace.json + plugin.json
skills/
  rag-architect/    # RAG 合并 skill（SKILL.md + 工具 + guides/）
  dg-piagent/
  engineering/      # mattpocock 工程类
  productivity/     # mattpocock 生产力类
```

## 来源与致谢

- **rag-architect / rag-skills**：RAG 专题指南合集（MIT，翻译并合并为单 skill）
- **mattpocock/skills**：Matt Pocock 的工程方法论 skill（MIT，翻译收录稳定集）

两者均为冻结副本（vendor），上游更新需手动同步。详见 `LICENSE` 中的版权声明。

## License

MIT（含上游版权声明，见 `LICENSE`）。
