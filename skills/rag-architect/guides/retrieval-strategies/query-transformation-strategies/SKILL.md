---
name: query-transformation-strategies
title: "Query Transformation Strategies"
description: "利用查询改写、回退提示（step-back prompting）和子查询分解，提升检索质量与全面性。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["query-expansion", "step-back", "sub-query", "query-rewriting"]
---

## 概述
查询变换（query transformation）策略在检索前修改或扩展用户查询，弥合自然语言查询与文档表示之间的鸿沟。这些技术通过生成多个查询变体（每个针对信息需求的不同侧面）来提升检索相关性。

## 问题陈述
查询到文档的直接匹配存在固有局限：
- **歧义**：自然语言查询常含模糊用词或多种解读
- **风格错配**：用户查询在结构和词汇上与被索引文档不同
- **信息不完整**：单一查询可能覆盖不了复杂信息需求的所有相关侧面
- **上下文不敏感**：直接查询不考虑更广的上下文或领域知识

## 核心概念
- **查询改写（query rewriting）**：把查询重述得更具体、更详细
- **回退提示（step-back prompting）**：生成更宽泛、更一般的查询以检索背景上下文
- **子查询分解（sub-query decomposition）**：把复杂查询拆成更简单的组成问题
- **查询扩展（query expansion）**：向原始查询添加相关术语和概念
- **多查询检索（multi-query retrieval）**：执行多个查询变体并合并结果

## 实施指南

### 第 1 步：实现查询改写
用 LLM 把原始查询重述为更详细、更具体的版本。

**原因**：增强后的查询包含原始查询可能遗漏的相关术语、恰当上下文和具体侧面。这能改善与技术文档和领域内容的匹配。

指示 LLM 用相关领域术语扩展查询、澄清模糊用词，并补充目标文档中会出现的上下文。

### 第 2 步：实现回退提示
生成一个更宽泛、更一般的查询版本，用于检索基础性上下文。

**原因**：回退查询提供背景信息和基础概念，帮助更具体的答案扎根。这对理解基础至关重要的技术主题尤其有价值。

生成能捕获与具体查询相关的高层概念、一般原理或背景知识的回退查询。

### 第 3 步：实现子查询分解
把复杂查询拆成 2-4 个覆盖不同侧面的更简单的子问题。

**原因**：子查询分解确保对多侧面问题的全面覆盖。每个子查询针对一个侧面，让检索到的多样信息合起来构成完整回答。

让 LLM 找出组成问题——这些问题合在一起回答，就全面覆盖了原始查询。

### 第 4 步：构建多查询检索管线
执行多个查询变体并合并其检索结果。

**原因**：多查询检索通过命中不同查询表述的文档来提升召回。合并结果保证更广的覆盖，也更有可能找到相关信息。

为每个查询变体检索文档，再去重并按与原始查询的相关性重排。

### 第 5 步：实现结果融合策略
用打分和去重合并来自不同查询变换的结果。

**原因**：结果融合避免信息冗余，并在所有查询变体中优先最相关的文档。加权打分方法在具体性与全面性之间取得平衡。

用倒数排名融合（RRF）或加权打分合并不同查询变体的结果。

实现模式可参考 [LangChain routing workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents)、[LlamaIndex Query Transform Cookbook](https://docs.llamaindex.ai/en/stable/examples/query_transformations/query_transform_cookbook/)，以及 [Step-back prompting 论文](https://arxiv.org/abs/2310.06117)。

## 何时使用本 skill
- 构建查询歧义常见的 RAG 系统
- 处理复杂、多侧面的用户问题
- 文档使用的术语与用户不同
- 既需要具体细节又需要宽泛上下文的领域
- 单查询检索产出不完整或不相关的结果

## 何时不使用本 skill
- 非常简单直接的查询（单步检索更快）
- 延迟必须压到最低（查询变换增加 LLM 调用）
- 查询与文档的对齐已经很好
- 有严格延迟预算的实时系统
- 查询本身已经表述良好的数据集

## 相关 skill
- [HyDE](../hyde-hypothetical-document-embeddings/SKILL.md) - 另一种查询扩展思路
- [Fusion Retrieval](../hybrid-search-bm25-dense/SKILL.md) - 组合多种检索信号
- [Adaptive Retrieval](../adaptive-retrieval/SKILL.md) - 动态查询处理

## 指标与成功标准
- **检索召回**：复杂查询的召回提升 15-25%
- **查询覆盖**：多个查询变体覆盖信息需求的不同侧面
- **结果质量**：文档集更全面、更相关
- **延迟**：典型查询的端到端延迟增加 < 500ms
- **成本效率**：LLM 调用与相关性收益相称
