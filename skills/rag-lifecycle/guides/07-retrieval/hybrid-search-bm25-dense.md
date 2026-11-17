---
name: hybrid-search-bm25-dense
title: "Hybrid Search: BM25 + Dense"
description: "结合 BM25 与稠密检索信号，提升关键词查询和语义查询的搜索质量。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["hybrid", "bm25", "dense", "fusion", "keyword"]
---

## 概述
混合检索（hybrid search）把 BM25（关键词搜索）与稠密向量 embedding（语义搜索）结合起来，同时利用精确词匹配和语义理解。这种双路方式能提升多样查询类型下的检索质量——关键词查询获得精确匹配，语义查询捕获概念关联。

## 问题陈述
纯语义搜索或纯关键词搜索各有局限：
- **仅稠密搜索**：难以应对精确词匹配、专有名词和领域术语
- **仅关键词搜索**：无法理解同义词、改述和概念关联
- **查询类型不同**：有些查询偏关键词（"error code 404"），有些偏语义（"如何修复认证问题"）

## 核心概念
- **BM25**：基于 TF-IDF 加权的关键词搜索算法 Okapi BM25
- **稠密搜索**：使用 embedding 的向量语义搜索
- **倒数排名融合（Reciprocal Rank Fusion，RRF）**：合并来自多种排序方法的结果
- **分数归一化**：把不同评分体系拉到统一尺度
- **Alpha 参数**：控制关键词与语义两部分之间的权重

## 实施指南

### 第 1 步：搭建稠密搜索
用你选定的 embedding 模型实现基于向量的语义搜索。

**原因**：稠密搜索能捕获语义，但可能漏掉对许多查询至关重要的精确词匹配。

### 第 2 步：搭建 BM25 搜索
用 BM25 实现基于关键词的搜索。

**原因**：BM25 擅长精确词匹配、领域术语和专有名词搜索，这些正是语义模型可能薄弱的地方。

### 第 3 步：实现分数归一化
把来自不同排序方法的分数归一到可比较的尺度。

**原因**：不同的评分体系（余弦相似度 vs. BM25 分数）无法直接组合——归一化建立统一尺度。

### 第 4 步：实现结果融合
合并来自多种搜索方法的结果。

**原因**：RRF 对不同评分尺度稳健，且不需要显式的分数归一化，非常适合融合。

### 第 5 步：构建混合搜索器
将所有组件组合成单一接口。

**原因**：统一接口简化使用，也便于实验不同的融合策略和权重。

实现模式可对比 [OpenSearch hybrid search 文档](https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/)、[OpenSearch score ranker processor](https://docs.opensearch.org/3.0/search-plugins/search-pipelines/score-ranker-processor/)、[reciprocal rank fusion 论文](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)，以及 [Sentence Transformers retrieve & re-rank](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)。

## 何时使用本 skill
- 构建 precision 和 recall 都重要的生产级 RAG 系统
- 处理多样的查询类型（关键词 + 语义）
- 精确词匹配与概念理解同样重要
- 含特定术语的技术文档
- 用户查询从自然语言到具体术语不等

## 何时不使用本 skill
- 纯语义搜索已经效果极佳
- 非常小的数据集，复杂度不值得
- 查询延迟必须压到最低（混合检索带来额外开销）
- 使用的向量数据库已内置混合检索（如 Weaviate）

## 相关 skill
- [Multi-Pass Retrieval with Reranking](../08-reranking/multi-pass-retrieval-with-reranking.md) - 进一步精炼结果
- [Semantic Chunking](../04-chunking/semantic-chunking.md) - 改善内容质量
- [Optimize Retrieval Latency](../07-retrieval/optimize-retrieval-latency.md) - 性能调优

## 指标与成功标准
- **检索质量**：相比单一方法，NDCG/precision/recall 提升
- **查询类型覆盖**：关键词查询和语义查询都有好结果
- **延迟**：混合检索延迟控制在单一方法的 1.5 倍以内
- **可维护性**：组件分离清晰
- **灵活性**：便于调整 alpha 和融合方法
