---
name: rag-for-multimodal-content
title: "面向多模态内容的 RAG"
description: "以共享的文档上下文索引并检索文本、图片、表格等多种模态。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "data-type-handling"
tags: ["multimodal", "images", "text", "vision", "clip"]
---

## 概述
多模态 RAG 把检索扩展到文本之外的图片、视频、音频和混合媒体内容。本 skill 覆盖多模态的处理、多模态 embedding 模型（如 CLIP）的使用，以及跨模态检索的实现——文本查询可以找到图片内容，反之亦然。

## 问题陈述
标准 RAG 系统只处理文本，会错过其他媒体中的有价值信息：
- 图片、图表和示意图包含文本未覆盖的信息
- 视频在转录文本之外还有视觉上下文
- 跨模态查询（如「给我看架构图」）需要同时理解两种模态
- 不同模态需要不同的 embedding 模型和处理流水线
- 多种向量类型让存储和检索更复杂

## 关键概念
- **多模态 embedding（Multimodal Embeddings）**：把不同模态映射到共享嵌入空间的模型（CLIP、ALIGN）
- **命名向量（Named Vectors）**：在向量数据库中为每个文档存储多条 embedding 向量
- **跨模态检索（Cross-Modal Retrieval）**：文搜图、图搜文以及组合检索
- **按模态处理（Modality-Specific Processing）**：图片、音频、视频各自不同的预处理
- **统一索引（Unified Index）**：单一索引结构处理多种模态

## 实施指南

### 第 1 步：选择多模态 embedding 模型
选择支持你所需模态的模型。

**原因**：CLIP 及类似模型创建了文本与图片可以直接比较的共享嵌入空间。

### 第 2 步：处理多模态文档
解析包含混合媒体内容的文档。

**原因**：正确的解析能分离不同模态，同时保留它们在文档内的关系。

### 第 3 步：存储多模态块
用命名向量（named vectors）按不同模态存储。

**原因**：命名向量允许同一文档针对不同模态和搜索策略拥有多条 embedding。

### 第 4 步：实现跨模态搜索
用混合查询跨文本和图片搜索。

**原因**：跨模态搜索让「给我看架构图」这类自然查询能检索到相关图片。

### 第 5 步：处理视频和音频
把支持扩展到视频和音频模态。

**原因**：视频和音频增加了复杂度，但能支撑丰富的多媒体 RAG 应用。

可用实现包括 [OpenAI CLIP](https://openai.com/index/clip/)、[MM-Embed 论文](https://huggingface.co/papers/2411.02571)、[LlamaIndex 多模态文档](https://docs.llamaindex.ai/en/stable/) 和 [Sentence Transformers 文档](https://www.sbert.net/)。

## 何时使用本 skill
- 构建含示意图和图表的文档
- 创建视觉搜索应用
- 处理带插图的科学论文
- 构建带商品图片的电商
- 查询涉及视觉概念时

## 何时不要使用本 skill
- 纯文本内容（用标准 RAG）
- 存储/带宽成本敏感时
- 应用不需要视觉信息时
- GPU 资源有限时（多模态模型需要更多算力）

## 相关 skill
- [RAG 的 Qdrant 搭建](../../vector-databases/qdrant-setup-rag/SKILL.md) - 命名向量配置
- [按数据类型选择向量数据库](../../vector-databases/choosing-vector-db-by-datatype/SKILL.md) - 数据库选型
- [语义分块](../../chunking/semantic-chunking/SKILL.md) - 面向文本块

## 指标与成功标准
- **跨模态准确率**：文搜图和图搜文的检索 mAP > 0.6
- **纯文本基线**：在纯文本查询上没有显著退化
- **存储开销**：典型混合内容的存储 < 纯文本的 2 倍
- **查询延迟**：跨模态查询 < 500ms
- **相关性**：图片查询的相关视觉内容命中率 > 80%
