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
| `rag-lifecycle` | rag-architect + rag-skills 合并重排，融入《生产级 RAG 系统》 | RAG 全生命周期：需求分析、选型设计、构建、生产化运维：3 个确定性 Python 工具 + 43 篇指南 + 15 章生产检查清单 |
| `dg-piagent` | 原创 | pi-agent / @earendil-works/pi-coding-agent SDK 开发：创建 agent、自定义工具、企业内网接口接入评估等 |
| `engineering/*`（18 个） | mattpocock/skills（翻译收录） | TDD、代码评审、领域建模、诊断 bug、spec/工单流等工程方法论 |
| `productivity/*`（7 个） | mattpocock/skills（翻译收录） | grilling 追问、教学、交接、写作等生产力 skill |

## 结构

```
.claude-plugin/     # marketplace.json + plugin.json
skills/
  rag-lifecycle/    # RAG 全生命周期 skill（SKILL.md + 工具 + guides/ + 生产检查清单）
  dg-piagent/
  engineering/      # mattpocock 工程类
  productivity/     # mattpocock 生产力类
```

## 来源与致谢

- **rag-architect / rag-skills**：RAG 专题指南合集（MIT），其指南经翻译合并进入 `rag-lifecycle`，并按《生产级 RAG 系统——从架构到 Python 实现》的 15 章生命周期重新组织，新增数据模型、可验证引用、安全威胁模型、可观测性与生产检查清单
- **mattpocock/skills**：Matt Pocock 的工程方法论 skill（MIT，翻译收录稳定集）

mattpocock 系列为冻结副本（vendor），上游更新需手动同步；`rag-lifecycle` 为原创重设计，不再跟随上游。详见 `LICENSE` 中的版权声明。

## License

MIT（含上游版权声明，见 `LICENSE`）。
