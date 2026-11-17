---
name: raptor-hierarchical-retrieval
title: "RAPTOR - Hierarchical Abstractive Retrieval"
description: "利用层次聚类和摘要构建多层文档树，改进检索效果。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "retrieval-strategies"
tags: ["raptor", "hierarchical", "clustering", "summarization", "tree-structure"]
---

## 概述
RAPTOR（Recursive Abstractive Processing and Tree-Organized Retrieval）构建文档摘要的层次树，支持在多个抽象层级上检索。这种方法在宏观概览与具体细节之间取得平衡，能从大型文档集中进行更细腻的信息检索。

## 问题陈述
大型文档集给检索带来挑战：
- **粒度错配**：查询可能需要宽泛上下文或具体细节，但单层检索无法自适应
- **信息过载**：从所有文档检索返回的内容太多
- **连贯性丢失**：检索到的片段缺乏与更广主题的关联
- **扩展性问题**：随着集合增长，线性搜索变得低效
- **上下文断层**：跨文档的相关概念之间缺少联系

## 核心概念
- **树构建**：通过聚类和抽象创建层次化摘要
- **逐层抽象**：每层代表信息浓缩程度递增
- **簇摘要**：把相似文档分组并生成摘要
- **多层检索**：跨多个抽象层级查询
- **父子链接**：维护摘要与源文档之间的联系

## 实施指南

### 第 1 步：文档 embedding 与聚类
为所有文档生成 embedding，并按语义相似度聚类。

**原因**：聚类把相关文档聚在一起，使摘要能捕获跨多个文档的主题，而不是零散单篇。

用你偏好的 embedding 模型生成向量表示，再应用聚类算法（如高斯混合模型、k-means）。

### 第 2 步：簇摘要
为每个文档簇生成摘要。

**原因**：摘要捕获多个文档的关键信息，形成保留重要主题又缩减体量的更高层抽象。

对每个簇，拼接其中的文档并用 LLM 生成简明摘要。

### 第 3 步：层次化构建树
递归地应用 embedding、聚类和摘要，构建多个层级。

**原因**：多个抽象层级让系统能按合适粒度检索——高层取宽泛上下文，低层取具体细节。

对上一层生成的摘要重复同样的过程，逐层向上建树，直到产生单个根摘要或达到最大层数。

### 第 4 步：构建多层向量索引
把所有层级的文档和摘要都建立索引。

**原因**：统一的向量索引允许跨所有抽象层级高效做相似度搜索，使检索器能为每个查询选择最合适的层级。

对树中所有层级的内容做 embedding 并索引，附带标明层级和来源的元数据。

### 第 5 步：实现多层检索
跨所有层级查询并智能合并结果。

**原因**：多层检索确保宽泛上下文和具体细节都被考虑。合并不同层级的结果能提供全面的信息。

从多个层级检索并平衡结果，确保检索信息兼具广度和深度。

### 第 6 步：实现上下文压缩
只提取检索内容中相关的部分。

**原因**：高层摘要包含的信息可能超出特定查询所需。上下文压缩聚焦最相关的部分。

用 LLM 或压缩技术，针对具体查询提取检索内容中最相关的部分。

### 第 7 步：构建完整的 RAPTOR 管线
将所有组件组合成一个内聚的系统。

**原因**：带计时和解释的完整管线便于优化、调试和生产部署。

实现模式可参考 [RAPTOR 论文](https://arxiv.org/abs/2401.18059)、[LlamaIndex RAPTOR pack](https://docs.llamaindex.ai/en/stable/api_reference/packs/raptor/)，以及 [scikit-learn clustering 文档](https://scikit-learn.org/stable/modules/clustering.html)。

## 何时使用本 skill
- 构建大型文档集（100+ 文档）的 RAG 系统
- 查询从宏观概览到具体细节不等
- 主题组织重要的领域（学术论文、研究）
- 需要在检索中同时保持具体性与广度
- 需要从摘要追溯到源文档的应用

## 何时不使用本 skill
- 小型文档集，单层搜索已足够
- 文档更新频繁（重建树代价高）
- 只需要具体事实性答案的应用
- 延迟必须压到最低（多层检索带来额外开销）
- 实时文档摄入场景

## 相关 skill
- [Hierarchical Chunking](../04-chunking/hierarchical-chunking.md) - 文档层面的层次结构
- [Multi-Pass Retrieval with Reranking](../08-reranking/multi-pass-retrieval-with-reranking.md) - 结果精炼
- [Graph RAG](../07-retrieval/graph-rag.md) - 基于关系的检索

## 指标与成功标准
- **可扩展性**：高效应对不断增长的文档集
- **检索质量**：通过平衡的层级选择提升 NDCG
- **查询覆盖**：宽泛查询和具体查询都得到更好结果
- **索引构建时间**：建树时间可接受
- **可追溯性**：父子链接可靠，便于核验来源
