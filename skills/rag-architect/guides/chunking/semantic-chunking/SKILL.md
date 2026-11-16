---
name: semantic-chunking
title: "语义分块（Semantic Chunking）"
description: "利用语义边界和 embedding 相似度切分文本，获得更高相关性的检索。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "chunking"
tags: ["semantic", "nlp", "sentence-boundary", "context-preservation"]
---

## 概述
语义分块基于自然语言边界和语义含义（而非固定字符数）把文档切分成段。这种方式保留上下文完整性，并把相关观点聚在一起，从而提升检索相关性。

## 问题陈述
固定大小的分块（如 1000 token）经常把句子、段落或概念从中间切断，导致：
- 碎片丢失语义
- 上下文在不相关的块之间串味
- 语义检索的相关性差
- LLM 难以理解孤立碎片

## 关键概念
- **语义边界（Semantic Boundaries）**：文本中的自然断点（段落、章节、句子）
- **上下文保留（Context Preservation）**：把相关观点和论证聚在一起
- **句子边界检测（Sentence Boundary Detection）**：用 NLP 工具识别真正的句子结尾
- **段落凝聚（Paragraph Cohesion）**：判断新观点或新论证从何处开始
- **重叠窗口（Overlapping Windows）**：用少量重叠保留相邻块之间的上下文

## 实施指南

### 第 1 步：检测句子边界
使用句子边界检测，而不是简单的句号切分。这样才能处理缩写、小数和其他边界情况。

**原因**：简单的句号/正则切分在 "Dr. Smith"、"3.14"、"U.S.A." 等情况下会出错。

### 第 2 步：把句子分组成语义单元
按语义凝聚度而不是固定数量把句子分组成块。

**原因**：基于相似度的分块能适应文档密度——密集的技术章节得到较小的块，叙述性章节得到较大的块。

### 第 3 步：应用基于结构的分块
利用文档结构（标题、markdown、HTML 标签）识别自然章节。

**原因**：文档结构往往就编码了语义边界（章、节、小节）。

### 第 4 步：实现自适应大小
根据内容特征（代码块、列表、表格）调整块大小。

**原因**：不同内容类型需要不同的分块策略才能获得最优检索效果。

实践实现可对比 [Sentence-BERT](https://arxiv.org/abs/1908.10084)、[LlamaIndex Semantic Chunker](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/)、[LangChain RecursiveCharacterTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter) 和 [spaCy 句子切分](https://spacy.io/usage/linguistic-features#sentence-segmentation)。

## 何时使用本 skill
- 具有清晰语义结构的文档（文章、报告、文档站）
- 检索质量比固定大小保证更重要时
- 上下文很重要的叙述性或解释性内容
- 使用语义检索（向量 embedding）时
- 需要连贯上下文来生成答案的问答系统

## 何时不要使用本 skill
- 行级精度很重要的代码仓库
- 固定格式的日志文件或结构化数据
- 需要严格保证 token 数量时（如受 API 限制）
- 块边界无法延迟确定的流式数据
- 使用精确关键词匹配（BM25）且块大小影响不大时

## 相关 skill
- [层级分块](../hierarchical-chunking/SKILL.md) - 面向嵌套文档结构
- [滑动窗口分块](../sliding-window-chunking/SKILL.md) - 保留重叠上下文
- [混合检索 BM25 + 稠密向量](../../retrieval-strategies/hybrid-search-bm25-dense/SKILL.md) - 组合检索方法

## 指标与成功标准
- **检索相关性**：检索到的块应包含完整、自含的信息
- **上下文保留**：相关概念留在同一个块内
- **覆盖率**：块边界处没有丢失重要信息
- **Token 效率**：块的大小在过小（有损）和过大（噪声多）之间取得平衡
- **语义连贯**：块代表连贯的观点或章节
