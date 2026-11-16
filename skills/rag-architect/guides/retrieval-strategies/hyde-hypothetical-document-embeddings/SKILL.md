---
name: hyde-hypothetical-document-embeddings
title: "HyDE - Hypothetical Document Embeddings"
description: "利用 LLM 生成的假设性文档弥合查询与文档之间的鸿沟，提升检索相关性。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["hyde", "query-expansion", "llm-generation", "semantic-gap"]
---

## 概述
HyDE（Hypothetical Document Embeddings，假设性文档嵌入）是一种查询扩展技术：先生成一份回答用户查询的假设性文档，再把这份合成文档作为向量搜索的查询。以此弥合短查询与更长、更详细的文档表示之间的语义鸿沟。

## 问题陈述
传统 RAG 系统面临一个根本性错配：
- **查询风格**：用户查询简短、随意、以提问为主
- **文档风格**：被索引的文档冗长、正式、以作答为主
- **embedding 空间鸿沟**：这两种风格在 embedding 空间中占据不同区域
- **直接匹配失败**：查询-文档直接算相似度往往产生糟糕的匹配

## 核心概念
- **假设性文档**：由 LLM 生成的、回答该查询的合成文档
- **查询-文档风格鸿沟**：查询与文档写作风格之间的差异
- **embedding 相似度**：把生成的答案与语料库中的真实答案做匹配
- **答案-答案匹配**：把问题从查询-文档匹配转换为答案-答案匹配
- **文档感知生成**：假设性文档的长度与典型块（chunk）长度对齐

## 实施指南

### 第 1 步：实现假设性文档生成
用 LLM 生成一份回答用户查询的详细文档。

**原因**：生成的假设性文档与语料库中的真实文档具有相似特征（长度、风格、内容结构），能在 embedding 空间中获得更好的相似度匹配。

让 LLM 生成一份全面的回答，长度和风格与文档集中的典型文档对齐。

### 第 2 步：配置文档感知生成
让假设性文档的大小匹配平均块大小。

**原因**：长度相近的文档的 embedding 表示更具可比性。长度不匹配会引入与语义无关的距离偏差。

以匹配你的切分（chunking）策略为目标设定字符数或 token 数（通常 400-1000 字符）。

### 第 3 步：用假设性文档执行向量搜索
用生成的文档而非原始查询作为相似度搜索的查询。

**原因**：假设性文档与被索引文档处于相同的风格和语义空间，向量数据库能更有效地找到语义相似的内容。

执行向量相似度搜索时，用生成的假设性文档替换原始查询。

### 第 4 步：实现结果过滤
按与原始查询的实际相关性过滤检索到的文档。

**原因**：HyDE 虽能改善检索，但有些结果可能语义相似却与事实无关。相关性过滤保证质量。

用原始查询（而非假设性文档）评估检索到的文档，过滤掉无关匹配。

### 第 5 步：构建完整的 HyDE 管线
将生成、检索和过滤组合成一个内聚的系统。

**原因**：带计时和解释的完整管线便于优化、调试和生产部署。

实现模式可参考 [HyDE 论文](https://arxiv.org/abs/2212.10596)、[LlamaIndex HyDE Query Transform](https://docs.llamaindex.ai/en/stable/examples/query_transformations/HyDEQueryTransformDemo/)，以及 [LangChain HyDE 参考](https://reference.langchain.com/python/langchain-classic/chains/hyde)。

## 何时使用本 skill
- 构建查询短、文档长的 RAG 系统
- 查询与文档风格错配导致检索效果差
- 问题与答案具有不同语言模式的领域
- 使用向量 embedding 的语义搜索
- 传统的同义词查询扩展不够用

## 何时不使用本 skill
- 查询与文档风格已经相近（如 FAQ 系统）
- 延迟极度敏感的应用（每次查询多一次 LLM 调用）
- 使用无法从风格对齐中受益的关键词检索（BM25）
- LLM 生成成本超过相关性收益
- 非常小的文档集，直接匹配已经够好

## 相关 skill
- [HyPE](../hype-hypothetical-prompt-embeddings/SKILL.md) - 预计算的替代方案
- [Query Transformation Strategies](../query-transformation-strategies/SKILL.md) - 其他扩展方法
- [Multi-Pass Retrieval with Reranking](../multi-pass-retrieval-with-reranking/SKILL.md) - 检索后精炼

## 指标与成功标准
- **检索相关性**：NDCG@10 相比基线提升 > 15%
- **风格对齐**：假设性文档与语料库风格特征匹配
- **延迟**：典型查询端到端延迟 < 1s
- **成本**：LLM 生成成本与相关性收益相称
- **答案质量**：最终答案的事实准确率提升
