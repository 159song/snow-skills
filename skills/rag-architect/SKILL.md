---
name: rag-architect
description: 设计、搭建、调试、评测、优化 RAG（检索增强生成）管线：chunking 策略、embedding 选型、向量数据库选型、混合检索、重排、多模态 RAG、代码文档 RAG、检索延迟、评测指标与生产部署。用户要构建文档搜索、选向量库、或检索答案总缺上下文时使用。内含 3 个确定性 Python 工具与 38 篇专题指南。
---

# RAG Architect

设计、调优并评测生产级 RAG 管线。核心原则：**工具先行、指南兜底**——先用本 skill 自带的
3 个确定性工具在真实语料上跑出数字，再按专题指南深入。不凭直觉选 chunk 大小或数据库。

## 硬规则

1. **绝不把模型名或厂商价格当作现行事实。** Embedding 模型和向量库报价几个月就过期。
   推荐*档位*（见下表），点名一个当前世代候选，并要求用户去供应商页面核实。
2. **每个设计以一次评测收尾。** 没跑过 `retrieval_evaluator.py` 的 RAG 设计只是假设，
   不是交付物。
3. **Chunking 由语料决定。** 选策略前先在真实文档上跑 `chunking_optimizer.py`。

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

## 工具工作流

所有路径相对本 skill 目录。产出链：语料分析 → 设计 → 评测。

### 1. 分析语料并选 chunking

```bash
python3 chunking_optimizer.py /path/to/docs --extensions .md .txt -o chunking.json
```

输出 `chunking.json`：`corpus_info`、各策略 `strategy_results`、`recommendation` 和
`sample_chunks`。采用 `recommendation.strategy` 及其配置；给用户看 2-3 个 `sample_chunks`
以人工核对边界。

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

### 3. 评测检索质量

准备 `queries.json`（`{id, text}` 列表或 `{"queries": [...]}`）和
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

## 参考层

### 设计参考（references/）

- `references/chunking_strategies_comparison.md` — 优化器实现的各策略取舍
- `references/embedding_model_benchmark.md` — 基准*方法论*（带时效警示的快照）
- `references/rag_evaluation_framework.md` — 指标定义（faithfulness、relevance、precision/recall/NDCG）

### 专题指南（guides/）

实现或排查具体环节时，按主题打开对应指南：

**Chunking**
- `guides/chunking/semantic-chunking/SKILL.md` — 按语义边界切分，替代固定 token 窗口
- `guides/chunking/hierarchical-chunking/SKILL.md` — 跨章节/标题/嵌套结构保留文档层级
- `guides/chunking/sliding-window-chunking/SKILL.md` — 加重叠保住块边界上下文
- `guides/chunking/contextual-chunk-headers/SKILL.md` — 给块附加继承的章节上下文
- `guides/chunking/choosing-a-chunking-framework/SKILL.md` — chunking 库与框架选型

**向量数据库**
- `guides/vector-databases/qdrant-setup-rag/SKILL.md` — Qdrant 搭建：元数据与过滤
- `guides/vector-databases/qdrant-for-production-rag/SKILL.md` — 生产环境 Qdrant 运维
- `guides/vector-databases/choosing-vector-db-by-datatype/SKILL.md` — 按数据类型（文本/代码/多模态/结构化）选库

**检索策略**
- `guides/retrieval-strategies/hybrid-search-bm25-dense/SKILL.md` — 关键词 + 稠密向量混合检索
- `guides/retrieval-strategies/multi-pass-retrieval-with-reranking/SKILL.md` — 先广召回，再用更强模型重排
- `guides/retrieval-strategies/query-transformation-strategies/SKILL.md` — 检索前改写/分解/扩展查询
- `guides/retrieval-strategies/hyde-hypothetical-document-embeddings/SKILL.md` — 用假设答案文档改进查询向量
- `guides/retrieval-strategies/hype-hypothetical-prompt-embeddings/SKILL.md` — 索引时附带可能的提问
- `guides/retrieval-strategies/self-rag/SKILL.md` — 生成流程中加入自反思与检索校验
- `guides/retrieval-strategies/raptor-hierarchical-retrieval/SKILL.md` — 在层级摘要 + 原始块上检索
- `guides/retrieval-strategies/context-enrichment-window/SKILL.md` — 用邻块上下文扩展检索结果
- `guides/retrieval-strategies/adaptive-retrieval/SKILL.md` — 按查询类型动态选检索策略
- `guides/retrieval-strategies/explainable-retrieval/SKILL.md` — 溯源与引用提升可解释性
- `guides/retrieval-strategies/crag-corrective-rag/SKILL.md` — 校验 + 兜底搜索修正弱检索
- `guides/retrieval-strategies/graph-rag/SKILL.md` — 用图结构与实体关系检索

**数据类型处理**
- `guides/data-type-handling/rag-for-code-documentation/SKILL.md` — 代码、API、示例与技术文档
- `guides/data-type-handling/rag-for-multimodal-content/SKILL.md` — 图片、表格、图示与混合媒体

**性能优化**
- `guides/performance-optimization/optimize-retrieval-latency/SKILL.md` — 索引、缓存与查询优化降延迟

**评测指标**
- `guides/evaluation-metrics/retrieval-evaluation-metrics/SKILL.md` — recall、precision、MRR、nDCG、上下文 precision/recall
- `guides/evaluation-metrics/generation-evaluation-metrics/SKILL.md` — faithfulness、答案相关性、LLM-as-judge
- `guides/evaluation-metrics/rag-evaluation-frameworks/SKILL.md` — 选评测框架并接入 CI 回归门禁

**RAG Agents**
- `guides/rag-agents/agentic-rag-routing/SKILL.md` — 每条查询路由到合适的检索策略/来源/工具
- `guides/rag-agents/multi-agent-rag-orchestration/SKILL.md` — planner + 专家 agent 分解并综合复杂答案

**部署**
- `guides/deployment/production-rag-deployment/SKILL.md` — 服务的扩展与安全上线
- `guides/deployment/index-versioning-and-reindexing/SKILL.md` — 索引版本管理与不停机重建

## 成功标准

- 选定的 RAG 模式命中用户的真实瓶颈。
- 检索质量提升没有引入多余架构。
- 实现从一开始就把元数据、评测与生产约束纳入视野。
- 真正的实现细节引用外部资料，而不是把大段代码抄进本 skill。
