---
name: multi-pass-retrieval-with-reranking
title: "Multi-Pass Retrieval with Reranking"
description: "使用带重排序的两阶段检索管线，在召回、precision 和延迟之间取得平衡。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["reranking", "cross-encoder", "two-stage", "relevance"]
---

## 概述
带重排序（reranking）的多趟检索是一种两阶段方法：先用快速的双编码器（bi-encoder）搜索检索出宽泛的候选集，再用更准确但更慢的交叉编码器（cross-encoder）重排器进行精炼。在保持可接受延迟的同时平衡召回与相关性。

## 问题陈述
单阶段检索存在固有权衡：
- **仅双编码器**：快但相关性有限——难以处理复杂的查询-文档关系
- **仅交叉编码器**：准确但对大型文档集来说太慢
- **固定 top-k**：无法适应查询难度——有些查询需要更多/更少的候选
- **静态检索**：检索过程中无法纳入用户反馈或上下文

## 核心概念
- **双编码器（bi-encoder）**：为文档和查询生成固定向量的快速编码模型
- **交叉编码器（cross-encoder）**：联合编码查询-文档对以精确打分（但更慢）
- **两阶段检索**：宽泛检索后接精炼
- **自适应 top-k**：根据查询特征动态调整检索深度
- **重排管线**：检索后对候选打分并重新排序

## 实施指南

### 第 1 步：搭建双编码器检索
用你的向量数据库实现第一阶段检索。

**原因**：双编码器检索快速且可扩展，但产生的是近似分数——适合作为收窄候选集的第一趟。

### 第 2 步：搭建交叉编码器重排
实现第二阶段重排以获得准确打分。

**原因**：交叉编码器通过联合编码查询-文档对产生更准确的相关性分数，但对全量检索来说太慢。

### 第 3 步：实现自适应检索
根据查询特征动态调整检索参数。

**原因**：自适应检索确保复杂查询获得更多重排候选，简单查询保持快速。

### 第 4 步：构建多趟管线
将所有组件组合成完整的检索管线。

**原因**：带计时和解释的统一管线便于优化和调试检索系统。

### 第 5 步：实现缓存与优化
为生产使用添加缓存和优化。

**原因**：缓存能减少重复查询的计算，这在生产系统中很常见。

可运行的示例可参考 [Sentence Transformers CrossEncoder 文档](https://www.sbert.net/docs/package_reference/cross_encoder/cross_encoder.html)、[Sentence Transformers rerankers](https://www.sbert.net/examples/cross_encoder/training/rerankers/README.html)、[Sentence Transformers retrieve & re-rank](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)，以及 [MonoT5 论文](https://arxiv.org/abs/2207.14235)。

## 何时使用本 skill
- 相关性至关重要的生产级 RAG 系统
- 文档集太大，无法全量跑交叉编码器搜索
- 双编码器的 precision 不够用的复杂查询
- 能为更好结果容忍略高的延迟
- 有明确性能指标的应用（NDCG、precision@k）

## 何时不使用本 skill
- 延迟必须压到最低（单双编码器更快）
- 非常小的集合，全量交叉编码器可行
- 双编码器已经提供出色的相关性
- 简单关键词搜索（BM25 可能就够）

## 相关 skill
- [Hybrid Search BM25 Dense](../07-retrieval/hybrid-search-bm25-dense.md) - 第一阶段增强
- [Semantic Chunking](../04-chunking/semantic-chunking.md) - 更好的检索输入
- [Optimize Retrieval Latency](../07-retrieval/optimize-retrieval-latency.md) - 性能调优

## 指标与成功标准
- **相关性**：NDCG@10 相比仅用双编码器提升 > 10%
- **延迟**：典型查询总检索耗时 < 500ms
- **召回**：保持第一阶段 95% 以上的召回
- **重排质量**：重排后的 top-10 应显著优于第一阶段 top-10
- **成本效率**：计算开销与相关性收益相称
