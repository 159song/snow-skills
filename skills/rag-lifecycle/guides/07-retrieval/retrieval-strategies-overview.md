---
name: retrieval-strategies
title: "Retrieval Strategies"
description: "在 RAG 检索质量工作中路由到混合检索（hybrid search）、重排序（reranking）、查询变换、HyDE、Self-RAG、RAPTOR、CRAG 与 Graph RAG。"
category: "retrieval-strategies"
tags: ["retrieval", "ranking", "hybrid-search", "rag"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 检索策略

## 概述
当主要 RAG 问题是搜索质量、排序、召回（recall）、上下文选择或证据可追溯性时，使用这个父级 skill。根据检索失败的具体情况路由到最匹配的子 skill。

## 问题陈述
仅靠 embedding 搜索常常漏掉精确词、把弱证据排得过高，或检索到不完整的上下文。RAG 系统需要能适应查询类型和证据需求的检索策略。

## 核心概念
- **混合检索（hybrid search）**：结合稀疏与稠密两类信号。
- **重排序（reranking）**：用更强的相关性模型对宽泛的候选集重新排序。
- **查询变换（query transformation）**：改写、扩展或分解用户问题。
- **纠正式检索（corrective retrieval）**：在生成前校验并修复弱证据。

## 实施指南

### 第 1 步：诊断失败原因
确认问题出在召回、排序、查询不匹配、上下文缺失，还是引用质量差。

### 第 2 步：选择检索模式
精确词漏检选混合检索；top-k 结果噪声多选重排序；问题模糊选查询变换；证据不可靠选纠正式模式。

### 第 3 步：用扎实的指标评估
度量 recall@k、MRR 或 nDCG、引用准确率、答案忠实度（faithfulness），以及延迟影响。

## 何时使用本 skill
- 改进现有 RAG 管线的检索质量
- 为新的 RAG 系统选择搜索模式
- 排查引用薄弱或上下文不相关的问题

## 何时不使用本 skill
- 源内容尚未解析或切分（chunking）
- 主要问题是向量数据库部署
- 任务是纯生成、不涉及检索

## 相关 skill
- [Hybrid Search BM25 Dense](../07-retrieval/hybrid-search-bm25-dense.md)
- [Multi-Pass Retrieval with Reranking](../08-reranking/multi-pass-retrieval-with-reranking.md)
- [Query Transformation Strategies](../07-retrieval/query-transformation-strategies.md)
- [Adaptive Retrieval](../07-retrieval/adaptive-retrieval.md)
- [Graph RAG](../07-retrieval/graph-rag.md)

## 指标与成功标准
- 评估查询上的召回与排序质量得到提升
- 答案忠实度和引用准确率更好
- 延迟仍在产品工作流可接受的范围内
