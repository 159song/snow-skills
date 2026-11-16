---
name: contextual-chunk-headers
title: "上下文分块头（Contextual Chunk Headers）"
description: "在 embedding 之前为块前置更高级别的上下文头，从而提升检索效果。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "chunking"
tags: ["contextual-headers", "metadata", "chunk-enhancement", "document-structure"]
---

## 概述
上下文分块头（Contextual Chunk Headers，CCH）通过在 embedding 之前为每个块前置更高级别的上下文（文档标题、章节标题、摘要）来增强检索。这让 embedding 能更准确地表示内容与含义，显著提升检索质量并减少无关结果。

## 问题陈述
孤立的块往往缺乏足够的上下文：
- **隐式指代**：块中使用的代词和隐式指代在孤立状态下含义不清
- **缺失上下文**：块只有放在其所属章节或文档的语境中才说得通
- **孤立易误导**：单独阅读时，块可能产生误导或不完整
- **检索效果差**：引用主题或题材的查询无法有效匹配
- **LLM 误读**：LLM 难以理解脱离上下文的块

## 关键概念
- **块头（Chunk Header）**：前置到块内容之前的更高级别上下文
- **文档级上下文**：文档标题或摘要作为头上下文
- **章节级上下文**：章节与小节标题构成的层级
- **嵌入前拼接（Pre-Embedding Concatenation）**：在 embedding 之前合并头与块
- **上下文保留**：把头一路带到检索和展示阶段

## 实施指南

### 第 1 步：生成文档级上下文
提取或生成文档标题与摘要，供块头使用。

**原因**：文档级上下文为理解该文档中的任何一个块提供了最重要的宏观信息。

如果文档没有描述性标题，用 LLM 生成一个，或从文档结构中提取标题。

### 第 2 步：提取章节层级
解析文档结构，捕获章节与小节标题。

**原因**：章节层级提供细粒度上下文，有助于检索文档内特定主题与题材的信息。

解析文档结构（markdown 标题、HTML 标签等），构建章节的层级表示。

### 第 3 步：创建块头
把文档上下文和章节上下文组合成完整的头。

**原因**：组合后的上下文既提供宏观的文档理解，又提供具体的章节信息，让 embedding 获得尽可能好的表示。

为每个块创建一个头，组合文档标题与包含该块的章节路径。

### 第 4 步：把头前置到块
在 embedding 之前把头与块内容合并。

**原因**：embedding 表示的是「头+块」的组合内容，把局部含义和全局上下文捕获进同一个向量空间。

索引每个块时，把头作为块内容的前缀。

### 第 5 步：带头做 embedding
使用增强了头的块进行嵌入和索引。

**原因**：带头嵌入能确保检索同时考虑局部内容和更广的上下文，从而得到更相关的匹配。

使用你偏好的 embedding 模型和向量数据库索引增强后的块。

### 第 6 步：带头的展示结果
向用户或 LLM 展示检索到的块时附上头。

**原因**：展示头为理解检索到的块提供了必要上下文，减少误读并提升答案质量。

返回检索内容时，附上原始头作为上下文。

### 第 7 步：搭建完整 CCH 流水线
把所有组件组合成一个连贯的分块与检索系统。

**原因**：完整的流水线确保上下文头在分块、embedding、检索和展示各环节被一致地应用。

实现模式可参考 [LangChain RecursiveCharacterTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)、[LlamaIndex node parser 用法](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/)、[Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) 和 [dsRAG AutoContext](https://github.com/D-Star-AI/dsRAG)。

## 何时使用本 skill
- 构建含结构化文档（文章、报告、文档站）的 RAG 系统
- 块中频繁通过代词或隐式指代提及主语时
- 文档具有清晰的章节层级或结构时
- 检索质量因块脱离上下文而受损时
- 应用需要 LLM 理解块上下文时

## 何时不要使用本 skill
- 没有清晰层级或标题的非结构化文档
- 块头会冗余或过长时
- 整篇文本本就连贯的极短文档
- 存储开销是主要顾虑时（头会增大块的体积）
- 文档结构没有意义的领域（代码片段、日志）

## 相关 skill
- [语义分块](../semantic-chunking/SKILL.md) - 感知上下文的分块方法
- [层级分块](../hierarchical-chunking/SKILL.md) - 基于结构的分块
- [上下文增强窗口](../../retrieval-strategies/context-enrichment-window/SKILL.md) - 检索后补上下文

## 指标与成功标准
- **检索精确率**：基于主语的查询的正确检索率提升
- **上下文完整性**：检索到的块为理解提供了足够上下文
- **头的有效性**：头提升了 embedding 表示质量
- **答案质量**：因块脱离上下文产生的幻觉减少
- **存储开销**：头带来的块体积增长可接受
