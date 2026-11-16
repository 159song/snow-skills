---
name: sliding-window-chunking
title: "滑动窗口分块（Sliding Window Chunking）"
description: "用重叠窗口在块边界两侧保留上下文，同时控制检索单元大小。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "chunking"
tags: ["overlap", "context-preservation", "window", "boundary"]
---

## 概述
滑动窗口分块创建相互重叠的块，每个块与相邻块共享部分内容。这在块边界处保留了上下文，确保被切分到多个块的信息仍可通过多条检索路径访问到。

## 问题陈述
不重叠的分块会形成硬边界，可能切断重要上下文：
- 关键信息恰好出现在块边界上
- 跨多个块的概念被碎片化
- 检索可能因为内容被切到边界两侧而漏掉相关信息
- 只提供单个碎片时 LLM 丢失上下文

## 关键概念
- **重叠比例（Overlap Percentage）**：相邻块共享内容的占比（通常 10-25%）
- **窗口大小（Window Size）**：每个块含重叠在内的总大小
- **步长（Stride）**：块起点之间的距离（窗口大小 - 重叠）
- **上下文保留（Context Preservation）**：确保边界两侧都存在相关上下文
- **多检索路径（Multiple Retrieval Paths）**：同一内容可从不同块访问

## 实施指南

### 第 1 步：确定重叠参数
根据使用场景和块大小计算合适的重叠。

**原因**：重叠比例决定了保留多少上下文——太少丢上下文，太多产生冗余。

### 第 2 步：实现滑动窗口分块
创建可配置重叠的块。

**原因**：边界调整可防止块在句子中间截断，同时维持滑动窗口模式。

### 第 3 步：添加块元数据
记录重叠信息，供检索时决策使用。

**原因**：元数据让检索系统能识别重叠内容并去重。

### 第 4 步：实现智能检索
妥善处理重叠的检索结果。

**原因**：智能检索在保留重叠块收益的同时避免信息冗余。

### 第 5 步：基于 token 的滑动窗口
按 token 而不是字符实现滑动窗口。

**原因**：基于 token 的分块对 LLM 更准确，并尊重其真实的 token 上限。

可用实现包括 [LangChain RecursiveCharacterTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)、[OpenAI tiktoken cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)、[tiktoken](https://github.com/openai/tiktoken) 和 [Sentence Transformers rerankers](https://www.sbert.net/examples/cross_encoder/training/rerankers/README.html)。

## 何时使用本 skill
- 边界处上下文很重要的文档
- 使用语义检索且可能匹配到边界附近内容时
- 行文连贯性重要的叙述性或顺序性内容
- 能从多条检索路径受益的系统
- 定义/示例可能跨块的技术文档

## 何时不要使用本 skill
- 存储成本敏感时（重叠会增加 20-30% 存储）
- 需要严格去重时（重叠会让去重更难）
- 边界清晰的结构化数据（JSON、CSV）
- 使用重叠无益的精确关键词检索时

## 相关 skill
- [语义分块](../semantic-chunking/SKILL.md) - 感知内容的边界
- [层级分块](../hierarchical-chunking/SKILL.md) - 面向嵌套结构
- [混合检索 BM25 + 稠密向量](../../retrieval-strategies/hybrid-search-bm25-dense/SKILL.md) - 组合检索方法

## 指标与成功标准
- **边界覆盖率**：关键术语至少出现在一个块中（不在边界处丢失）
- **存储开销**：重叠按预期比例增加存储（如 20%）
- **检索召回**：同一内容可通过多个块访问
- **上下文保留**：检索到的块包含足够的周边上下文
- **去重质量**：能有效识别并处理重叠内容
