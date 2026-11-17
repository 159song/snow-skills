---
name: rag-lifecycle
description: RAG 全生命周期：需求分析与选型设计、从零构建、生产化与上线后运维。用户要设计 RAG 管线、选 chunking/embedding/向量库、搭企业级 RAG（多租户、ACL、版本化、引用可信）、RAG 上生产或上线后的安全、可观测、评测回归、排障降本时使用。内含 3 个确定性 Python 工具、43 篇指南与 15 章生产检查清单。
---

# RAG Lifecycle

覆盖 RAG 从需求到运维的完整生命周期。**先判断阶段，再动手**：阶段决定用工具、查哪章指南、以什么收尾。

> 出处：本 skill 由 rag-architect / rag-skills（MIT，翻译合并的冻结内容）与《生产级 RAG 系统——从架构到 Python 实现》重新设计合并而成。

## 第 0 步：判断阶段

| 用户处境 | 阶段 | 动作 |
|---|---|---|
| 还没有系统，或要推翻重来 | **设计期** | 走下方「工具工作流」，产出架构与评测基线 |
| 架构已定，在实现具体环节 | **构建期** | 查「章节地图」对应章，逐环节落地 |
| 已上线或准备上线 | **生产期** | 过 `references/production_checklist.md` 相关章；变更类需求按章节地图查对应章（权限 → 02/13，质量 → 12/14，发布 → 15） |
| 任何阶段的质量疑问 | **评测** | 用 `retrieval_evaluator.py` 拿数字，定位到章再改 |

**完成判据**：你能用一句话说出用户处于哪个阶段、下一步打开哪一章。说不出来就先问需求八问（见 `guides/01-requirements/requirements-and-query-taxonomy.md`）。

## 硬规则

1. **绝不把模型名或厂商价格当作现行事实。** Embedding 模型和向量库报价几个月就过期。推荐*档位*（见下表），点名一个当前世代候选，并要求用户去供应商页面核实。
2. **每个设计以一次评测收尾。** 没跑过 `retrieval_evaluator.py` 的 RAG 设计只是假设，不是交付物。
3. **Chunking 由语料决定。** 选策略前先在真实文档上跑 `chunking_optimizer.py`。
4. **权限与版本只存事实层。** 多租户/ACL 需求一旦出现，ACL 存 System of Record（Postgres 类），检索时过滤；向量索引是可整体重建的派生物，永不当权限的事实来源。

## Embedding 模型档位（模式，不是价格表）

| 档位 | 当前世代示例（用前核实） | 适用 |
|---|---|---|
| 快速 / 自托管 | `all-MiniLM-L6-v2`、`bge-small` | 成本敏感、小规模、实时 |
| 均衡开源 | `all-mpnet-base-v2`、`bge-large`、`e5-large` | 不依赖 API 的质量型检索 |
| 质量 API | `text-embedding-3-large`、`voyage-3-large` | 精度优先的通用检索 |
| 代码 | `voyage-code-3`、CodeBERT 系 | 代码搜索语料 |

**报价纪律：** 成本模型用占位表——列 `模型 | $/1M tokens（待核实）| 维度 | 截至日期`——
让用户填实时数字。向量库同理（Pinecone/Weaviate/Qdrant/Chroma/pgvector）：选型标准
（托管 vs 自托管、规模、过滤、现有 Postgres）是耐用的，美元数字不是。

## 设计期：工具工作流

产出链：语料分析 → 设计 → 评测。所有路径相对本 skill 目录。

### 1. 分析语料并选 chunking

```bash
python3 chunking_optimizer.py /path/to/docs --extensions .md .txt -o chunking.json
```

输出 `chunking.json`：`corpus_info`、各策略 `strategy_results`、`recommendation`（含
`best_strategy`、`best_score`、`all_scores`、`reasoning`）和 `sample_chunks`。采用
`recommendation.best_strategy` 及其配置；给用户看 2-3 个 `sample_chunks`
以人工核对边界。

**完成判据**：`chunking.json` 存在，且用户已看过样本块并认可边界。

### 2. 按需求设计管线

写需求 JSON（全部必填）：`document_types[]`、`document_count`、`avg_document_size`（字符）、
`queries_per_day`、`query_patterns[]`、`latency_requirement`、`budget_monthly`、
`accuracy_priority`（0-1）、`cost_priority`（0-1）、`maintenance_complexity`。

```bash
python3 rag_pipeline_designer.py requirements.json -o design.json
```

输出 `design.json`：`chunking`、`embedding`、`vector_db`、`retrieval`、`reranking`、
`evaluation`、`total_cost`、`architecture_diagram`（mermaid）、`config_templates`。
展示架构图；每个 `cost_monthly` 数字标注"估算，待核实"（硬规则 1）。

**完成判据**：架构图已展示给用户，且需求八问（第 1 章指南）每一问都有对应设计决策。

### 3. 评测检索质量

准备 `queries.json`（`{id, query}` 列表或 `{"queries": [...]}`）和
`ground_truth.json`（`{query_id: [相关文档id]}`），然后：

```bash
python3 retrieval_evaluator.py queries.json /path/to/docs ground_truth.json --k-values 3 5 10 -o eval.json
```

报告 precision@k、recall@k、MRR、NDCG@k，以及用于失败分析的
`poor_precision_examples` / `poor_recall_examples`。

### 4. 验证循环

设计只在满足以下条件时算完成：

1. `eval.json` 达标——常见下限：precision@5 ≥ 0.8，recall@10 ≥ 0.85（按用例与用户商定）。
2. 未达标：检查 poor-example 列表，**每次只改一个变量**（chunking 策略 → 重跑步骤 1；
   embedding 档位；加重排；混合检索），重跑步骤 3。循环。
3. 交付物中每个推荐模型/价格都带"核实当前报价/模型可用性"注记和截至日期。

**完成判据**：`eval.json` 达标，或已循环到用户接受当前数字并记录了已知短板。

## 构建期与生产期：章节地图

实现或排查具体环节时，按章打开指南。编号即 PDF《生产级 RAG 系统》的 15 章生命周期。

**01 需求**（`guides/01-requirements/`）
- `requirements-and-query-taxonomy.md` — 需求八问；查询分类（语义/精确/结构化/时序/多文档/多跳）路由到 Dense/BM25/API

**02 数据模型**（`guides/02-data-model/`）
- `rag-data-model.md` — Document/Version/Section/Chunk/ACL/lineage 实体设计；事实层与检索层分离

**03 摄取**（`guides/03-ingestion/`）
- `datatypes-overview.md` — 按数据类型路由的摄取入口
- `rag-for-code-documentation.md` — 代码、API、示例与技术文档
- `rag-for-multimodal-content.md` — 图片、表格、图示与混合媒体

**04 Chunking**（`guides/04-chunking/`）
- `chunking-overview.md` — 按语料形态与失败模式路由策略
- `semantic-chunking.md` / `hierarchical-chunking.md` / `sliding-window-chunking.md` / `contextual-chunk-headers.md` / `choosing-a-chunking-framework.md`

**05 Embedding** — 主页即上方档位表；基准方法论见 `references/embedding_model_benchmark.md`

**06 索引与向量库**（`guides/06-index/`）
- `vector-db-overview.md` — 选库入口
- `choosing-vector-db-by-datatype.md` — 按数据类型（文本/代码/多模态/结构化）选库
- `qdrant-setup-rag.md` / `qdrant-for-production-rag.md` — Qdrant 搭建与生产运维

**07 检索**（`guides/07-retrieval/`）
- `retrieval-strategies-overview.md` — 策略路由入口
- `hybrid-search-bm25-dense.md` — 关键词 + 稠密混合检索
- `query-transformation-strategies.md` / `hyde-hypothetical-document-embeddings.md` / `hype-hypothetical-prompt-embeddings.md` — 查询改写与扩展
- `adaptive-retrieval.md` — 按查询类型动态选策略
- `self-rag.md` / `crag-corrective-rag.md` — 生成中自反思、检索校验兜底
- `graph-rag.md` / `raptor-hierarchical-retrieval.md` — 图结构与层级摘要检索
- `agents-overview.md` / `agentic-rag-routing.md` / `multi-agent-rag-orchestration.md` — agent 化检索与编排
- `latency-overview.md` / `optimize-retrieval-latency.md` — 检索延迟优化

**08 重排**（`guides/08-reranking/`）
- `multi-pass-retrieval-with-reranking.md` — 先广召回，再用更强模型重排

**09 上下文构建**（`guides/09-context-builder/`）
- `context-enrichment-window.md` — 用邻块上下文扩展检索结果

**10 生成** — 组装原则见第 09/11 章指南与检查清单生成节；答案质量指标见第 12 章

**11 引用**（`guides/11-citation/`）
- `verifiable-citations.md` — Citation 数据模型、claim 拆分、三层验证（存在性/蕴含/权限）、发布门禁
- `explainable-retrieval.md` — 溯源与引用提升可解释性

**12 评测**（`guides/12-evaluation/`）
- `evaluation-overview.md` — 评测入口
- `retrieval-evaluation-metrics.md` / `generation-evaluation-metrics.md` — 检索与生成指标
- `rag-evaluation-frameworks.md` — 评测框架选型与 CI 回归门禁

**13 安全**（`guides/13-security/`）
- `rag-security-threat-model.md` — RAG 特有威胁：跨租户、prompt injection、数据投毒、过期权限

**14 可观测**（`guides/14-observability/`）
- `rag-observability.md` — 按 query type/语言/租户分片报告、回归门禁、Shadow/Canary

**15 部署**（`guides/15-deployment/`）
- `deployment-overview.md` — 部署入口
- `production-rag-deployment.md` — 扩展与安全上线
- `index-versioning-and-reindexing.md` — 索引版本管理与不停机重建

## 参考层（references/）

- `references/production_checklist.md` — 15 章生产检查项汇总，上线与重大变更时整表过一遍
- `references/chunking_strategies_comparison.md` — 优化器实现的各策略取舍
- `references/embedding_model_benchmark.md` — 基准*方法论*（带时效警示的快照）
- `references/rag_evaluation_framework.md` — 指标定义（faithfulness、relevance、precision/recall/NDCG）

## 成功标准

- 阶段判断正确：设计期产出带评测基线的架构，生产期产出过检查清单的变更，两者从未混用。
- 选定的 RAG 模式命中用户的真实瓶颈，检索质量提升没有引入多余架构。
- 权限、版本、引用从第一天的数据模型就纳入视野，而不是上线前补丁。
- 真正的实现细节引用外部资料，而不是把大段代码抄进本 skill。
