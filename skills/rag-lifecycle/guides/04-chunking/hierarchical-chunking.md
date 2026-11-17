---
name: hierarchical-chunking
title: "层级分块（Hierarchical Chunking）"
description: "把嵌套文档切成父子多级结构，让检索能从宽泛章节下钻到细粒度段落。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "chunking"
tags: ["nested", "multi-level", "document-structure", "parent-child"]
---

## 概述
层级分块创建保留文档层级（章、节、小节）的多级块结构。这样既能做宏观概览检索（高层块），也能做细节检索（低层块），并通过父子关系实现上下文传递。

## 问题陈述
扁平的分块策略会丢失文档内部的结构关系：
- 关于宽泛主题的问题检索到的是细节碎片而非摘要
- 无法检索「上下文的上下文」——检索到一条细节时，它所在的章节丢了
- 无法沿文档层级导航
- 检索结果无法按文档结构组织

## 关键概念
- **父子关系（Parent-Child Relationships）**：摘要块与其细节子块之间的链接
- **多级粒度（Multi-Level Granularity）**：不同抽象层级的块（文档 → 章 → 节 → 段落）
- **上下文传递（Context Propagation）**：检索子块时附带父级上下文的能力
- **元数据增强（Metadata Enrichment）**：存储层级信息以供过滤和导航
- **递归分块（Recursive Chunking）**：沿文档结构递归应用分块规则

## 实施指南

### 第 1 步：解析文档结构
提取文档的层级结构。

**原因**：正确的解析是一切的基础——不理解结构就无法创建层级。

### 第 2 步：创建多级块
从解析出的层级生成多个层级的块。

**原因**：多个块层级支持不同的检索策略——宽泛问题用摘要块，具体问题用细节块。

### 第 3 步：存储层级元数据
持久化层级信息，供检索时传递上下文。

**原因**：元数据支持过滤和层级查询（例如「只从第 2 层或更深层检索」）。

### 第 4 步：实现层级检索
检索块时可选地附带父级上下文。

**原因**：层级检索让用户能够从宽泛主题「放大」到具体细节，就像浏览目录一样。

实现细节可参考 [LlamaIndex HierarchicalNodeParser](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/hierarchical/)、[LangChain RecursiveCharacterTextSplitter](https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter)、[Haystack HierarchicalDocumentSplitter](https://docs.haystack.deepset.ai/docs/hierarchicaldocumentsplitter) 和 [LlamaIndex Recursive Retriever + Node References](https://developers.llamaindex.ai/python/framework/integrations/retrievers/recursive_retriever_nodes/)。

## 何时使用本 skill
- 结构清晰的长文档（书籍、技术文档、研究论文）
- 同时需要摘要检索和细节检索时
- 支持「下钻（drill-down）」导航的应用
- 构建文档浏览/搜索界面时
- 能从层级上下文中受益的问答系统

## 何时不要使用本 skill
- 没有结构的扁平内容（博客文章、单页文章）
- 存储复杂度超过检索收益时
- 简单分块就够用的小型文档集合
- 检索延迟极其敏感时（层级检索有额外开销）

## 相关 skill
- [语义分块](../04-chunking/semantic-chunking.md) - 感知内容的分块
- [滑动窗口分块](../04-chunking/sliding-window-chunking.md) - 上下文重叠
- [带重排的多轮检索](../08-reranking/multi-pass-retrieval-with-reranking.md) - 精炼层级结果

## 指标与成功标准
- **覆盖率**：所有文档内容在各层级中完整保留
- **检索灵活性**：可在任意抽象层级检索
- **上下文相关性**：父级上下文提升细节问题的答案质量
- **存储效率**：元数据开销不超过存储量的 30%
- **查询延迟**：层级检索延迟控制在扁平检索的 2 倍以内
