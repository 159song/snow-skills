---
name: hype-hypothetical-prompt-embeddings
title: "HyPE - Hypothetical Prompt Embeddings"
description: "在索引阶段预计算假设性问题，消除运行时查询扩展的开销。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["hype", "precomputed-queries", "indexing-time", "query-alignment"]
---

## 概述
HyPE（Hypothetical Prompt Embeddings，假设性提示嵌入）在索引阶段为每个文档块（chunk）生成多个假设性问题，把检索从查询-文档匹配转变为问题-问题匹配。这消除了运行时的 LLM 调用，同时显著提升检索 precision。

## 问题陈述
混合检索与增强检索技术往往依赖运行时查询扩展：
- **延迟开销**：基于 LLM 的查询扩展给每次查询带来明显延迟
- **成本累积**：每次查询都需要额外的 LLM 调用
- **风格错配**：直接的查询-文档匹配受语言差异影响
- **质量不稳定**：运行时生成的结果不一致

## 核心概念
- **预计算问题**：在文档索引期间一次性生成的假设性问题
- **问题-问题匹配**：检索转变为匹配相似的问题模式
- **多向量表示**：每个块用多个不同问题重复索引
- **索引期处理**：所有 LLM 工作离线完成，无运行时开销
- **覆盖扩展**：每块多个问题增加语义覆盖面

## 实施指南

### 第 1 步：为每个块生成假设性问题
为每个文档块生成 3-5 个能检索到它的假设性问题。

**原因**：每块多个问题为检索创造了多样的入口，提高命中各种用户查询表述的概率。

让 LLM 创建这样一组问题：回答了这些问题，就覆盖了该块的主要要点。

### 第 2 步：为假设性问题生成 embedding
为所有假设性问题生成 embedding，并与源块一起存储。

**原因**：问题 embedding 比原始文档 embedding 更贴近用户查询 embedding，同时保留指向原始内容的链接以供答案生成。

用你偏好的 embedding 模型对每个问题做嵌入，并维护到源块的映射。

### 第 3 步：构建多向量索引结构
创建把问题 embedding 映射到源块的索引结构。

**原因**：索引需要在命中问题 embedding 后高效取回原始块内容，这要求维护正确的映射元数据。

构建一个向量索引，其中每个问题 embedding 指向其对应的源块。

### 第 4 步：实现高效检索
直接查询索引，无需运行时生成问题。

**原因**：问题已经预计算，检索和标准向量搜索一样快——查询时零 LLM 延迟、零成本。

用用户查询对预计算的问题 embedding 执行标准向量相似度搜索。

### 第 5 步：优化索引构建
使用并行处理和批处理高效建索引。

**原因**：索引构建是一次性的，但可能耗时。高效处理能缩短部署时间、降低资源占用。

尽可能并行处理多个块，并批量调用 embedding。

### 第 6 步：构建完整的 HyPE 管线
将所有组件组合成一个内聚的系统。

**原因**：带可配置参数的完整管线便于优化，也便于实验不同的窗口策略。

实现模式可参考 [HyPE 论文](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5139335)、[FAISS 文档](https://github.com/facebookresearch/faiss/wiki)，以及多向量索引的向量数据库文档。

## 何时使用本 skill
- 构建运行时延迟至关重要的生产级 RAG 系统
- 查询与文档风格错配是已知问题
- 大型文档集且索引构建时间可接受
- 负担得起一次性 LLM 成本但负担不起每次查询的成本
- 检索 precision 最大化比索引大小更重要

## 何时不使用本 skill
- 文档集频繁变化（重建索引代价高）
- 存储或内存约束紧张（多向量表示会增大索引）
- 非常小的集合，直接搜索已够用
- 查询延迟不是关键问题（HyDE 可能更简单）
- 文档持续到达的实时摄入场景

## 相关 skill
- [HyDE](../hyde-hypothetical-document-embeddings/SKILL.md) - 运行时替代方案
- [Semantic Chunking](../../chunking/semantic-chunking/SKILL.md) - 更好的输入质量
- [Fusion Retrieval](../hybrid-search-bm25-dense/SKILL.md) - 组合多种检索方法

## 指标与成功标准
- **检索 precision**：最高可提升 42 个百分点
- **查询延迟**：相比基线向量搜索零额外延迟
- **论断召回（claim recall）**：最高可提升 45 个百分点
- **索引大小**：增幅可接受（因每块多问题，通常 3-5 倍）
- **索引构建时间**：通过并行化实现高效处理
