---
name: context-enrichment-window
title: "Context Enrichment Window"
description: "为检索结果补充相邻块（chunk），提供更连贯、更完整的上下文。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["context-enrichment", "surrounding-context", "window", "coherence"]
---

## 概述
上下文富集窗口（context enrichment window）通过纳入原文档中的相邻文本来扩展被检索到的块（chunk）。这样能提供更连贯、上下文更丰富的结果，缓解向量搜索倾向于返回孤立文本片段的问题。

## 问题陈述
基于向量的检索常返回孤立片段：
- **句子中间截断**：块可能在语义未完处开始或结束
- **上下文缺失**：相关信息可能在相邻块中
- **不连贯**：孤立片段缺乏叙事流畅性
- **信息不完整**：理解所需的关键上下文可能缺失
- **答案碎片化**：LLM 难以从零散片段生成连贯的回答

## 核心概念
- **相邻上下文**：被检索块前后紧邻的文本
- **窗口大小**：每侧纳入的块数量
- **块索引**：维护原文档的顺序和位置
- **上下文扩展**：把相邻块追加到检索结果中
- **重叠处理**：管理相邻块之间的重叠区域

## 实施指南

### 第 1 步：实现块索引
在索引阶段存储块索引和文档位置。

**原因**：要检索相邻块，必须知道每个块在原文档中的位置。索引维护的就是这类位置信息。

在切分（chunking）过程中为每个块分配顺序索引，并将索引存为元数据。

### 第 2 步：存储带位置元数据的块
把块索引和位置信息存入向量数据库。

**原因**：向量数据库需要把位置元数据和内容一起存储，才能在检索后进行上下文富集。

为向量数据库中的每个块添加索引、起始位置和结束位置作为元数据字段。

### 第 3 步：实现上下文窗口检索
对每个被检索到的块，按索引获取相邻块。

**原因**：补充相邻上下文能提供叙事流畅性，以及正确理解被检索片段所需的信息。

对每个被检索块，取索引 ±N 范围内的块，N 为窗口大小。

### 第 4 步：实现重叠处理
正确合并重叠的块，避免内容重复。

**原因**：块重叠意味着相邻块与目标块共享文本。正确合并可避免重复并保持连贯。

拼接块时考虑重叠，确保每个字符只出现一次。

### 第 5 步：实现自适应窗口大小
根据块的特征调整窗口大小。

**原因**：并非所有块都需要相同的上下文量。自适应大小在完整性与效率之间取得平衡。

对较短的块使用较大窗口，对较长的块使用较小窗口。

### 第 6 步：构建完整的上下文富集管线
将所有组件组合成一个内聚的检索系统。

**原因**：带可配置参数的完整管线便于优化，也便于实验不同的窗口策略。

实现模式可参考 [LlamaIndex SentenceWindowNodeParser](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_window/)、[LangChain ContextualCompressionRetriever](https://reference.langchain.com/python/langchain-classic/retrievers/contextual_compression/ContextualCompressionRetriever)，以及用于切分策略的 [RecursiveCharacterTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)。

### 第 7 步：设定上下文预算与裁剪优先级
富集后的上下文先去重（同一文档多块命中时合并相邻区间），再按预算裁剪：预算内装不下时，按「重排分数 → 引用需要（claim 对应块优先）→ 文档新鲜度（as_of 新者优先）」的顺序保留。

**原因**：没有预算的拼装会把低相关富集内容挤进 prompt，挤掉高相关主证据；没有固定优先级，超预算时裁剪结果不可复现。

## 何时使用本 skill
- 构建叙事连贯性重要的 RAG 系统
- 文档具有自然行文或故事结构
- 问答系统需要完整上下文才能作答
- 检索到的块经常截断在句子或语义中间
- 理解依赖周围信息的领域

## 何时不使用本 skill
- 块本身已自包含的集合（FAQ 条目）
- 使用过大的窗口以至于抵消了切分的好处
- 检索必须尽可能快的系统（富集带来额外开销）
- 块重叠已经很大（50% 以上）
- 位置无关紧要的纯关键词检索

## 相关 skill
- [Semantic Chunking](../04-chunking/semantic-chunking.md) - 更好的初始切分
- [Hierarchical Chunking](../04-chunking/hierarchical-chunking.md) - 基于结构的方法
- [Sliding Window Chunking](../04-chunking/sliding-window-chunking.md) - 基于重叠的切分

## 指标与成功标准
- **上下文连贯性**：检索内容代表完整、自包含的信息
- **答案质量**：生成回答的连贯性提升
- **覆盖度**：块边界处没有明显信息丢失
- **Token 效率**：富集后的块在过小和过大之间取得平衡
- **延迟**：富集的开销可接受（通常 < 100ms）
