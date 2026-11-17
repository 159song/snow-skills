---
name: choosing-vector-db-by-datatype
title: "按数据类型选择向量数据库"
description: "根据内容类型、元数据需求和查询模式选择向量数据库。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "vector-databases"
tags: ["selection", "text", "multimodal", "code", "comparison"]
---

## 概述
选择合适的向量数据库在很大程度上取决于数据类型（文本、图片、代码、多模态）和用例需求。本 skill 提供一个基于数据特征和运维约束、在主流向量数据库之间做选择的决策框架。

## 问题陈述
不同向量数据库各有所长：
- 文本密集型负载需要高效的语义检索
- 代码仓库需要专门的 embedding 处理
- 多模态数据需要多向量支持
- 生产约束（成本、扩容、延迟）差异巨大
- 选错数据库会导致性能差或成本高

## 关键概念
- **数据类型**：文本、代码、图片、音频或多模态组合
- **embedding 模型兼容性**：对不同嵌入维度和模型的支持
- **多向量支持（Multi-Vector Support）**：为每个文档存储并搜索多条 embedding 的能力
- **扩容模型**：垂直扩容与水平扩容能力
- **部署模型**：自托管、托管云或混合

## 数据库对比矩阵

### 文本密集型负载

| 数据库 | 优势 | 劣势 | 最适合 |
|----------|-----------|------------|----------|
| **[Qdrant](https://qdrant.tech/documentation/)** | 开源、过滤出色、混合检索（hybrid search） | 社区比 Pinecone 小 | 生产 RAG、成本敏感场景 |
| **[Pinecone](https://docs.pinecone.io/)** | 托管、扩容能力出色、上手简单 | 昂贵、厂商锁定 | 企业、零运维要求 |
| **[Weaviate](https://docs.weaviate.io/weaviate/introduction)** | GraphQL API、模块化、schema 优先 | 学习曲线、可能复杂 | 需要灵活 schema 的团队 |
| **[ChromaDB](https://docs.trychroma.com/)** | API 简单、易嵌入、开源 | 生产扩容性较弱 | 原型、中小规模 |
| **[Milvus](https://milvus.io/docs)** | 扩容性强、功能丰富 | 部署复杂、体量重 | 有数据团队的企业 |

### 代码与文档

| 数据库 | 优势 | 劣势 | 最适合 |
|----------|-----------|------------|----------|
| **[Qdrant](https://qdrant.tech/documentation/)** | 元数据过滤出色、payload 索引 | 无代码专属功能 | 带元数据的代码搜索 |
| **[Weaviate](https://docs.weaviate.io/weaviate/introduction)** | 图遍历、关系处理 | 部署复杂 | 代码图/上下文搜索 |
| **[ChromaDB](https://docs.trychroma.com/)** | 与代码工具集成简单 | 扩容有限 | IDE 集成、代码助手 |
| **[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)** | 文本检索 + 向量、生态成熟 | 非向量优先 | 代码 + 关键词混合检索 |

### 多模态（文本 + 图片）

| 数据库 | 优势 | 劣势 | 最适合 |
|----------|-----------|------------|----------|
| **[Weaviate](https://docs.weaviate.io/weaviate/introduction)** | 多向量、内置 CLIP 支持 | 性能开销 | 图片 + 文本搜索 |
| **[Qdrant](https://qdrant.tech/documentation/)** | 通过命名向量支持多向量 | 需手动配置 | 定制多模态流水线 |
| **[Pinecone](https://docs.pinecone.io/)** | 多命名空间、稀疏向量 | 多向量支持有限 | 有限的多模态需求 |
| **[Milvus](https://milvus.io/docs)** | 多向量、混合检索 | 部署复杂 | 大规模多模态系统 |

## 实施指南

### 第 1 步：分析你的数据类型
识别主要的数据特征。

**原因**：数据画像确保选择基于实际需求，而不是炒作或流行度。

### 第 2 步：评估候选数据库
根据需求给各数据库打分。

**原因**：评分框架提供客观标准，而非主观意见。

### 第 3 步：实现类型专属策略
针对每种数据类型定制方案。

**原因**：不同数据类型需要根本不同的方案才能获得最优性能。

### 第 4 步：概念验证
创建 PoC 验证选择。

**原因**：没有什么比用真实数据和查询测试更有说服力——PoC 能揭示真实世界的性能特征。

### 第 5 步：迁移路径
为未来可能的数据库更换做规划。

**原因**：导出策略能防止锁定，并在需求变化时支持迁移。

对比与厂商文档可参考 [ANN Benchmarks](https://ann-benchmarks.com/)、[Qdrant 文档](https://qdrant.tech/documentation/)、[Pinecone 文档](https://docs.pinecone.io/)、[Weaviate 文档](https://docs.weaviate.io/weaviate/introduction)、[ChromaDB 文档](https://docs.trychroma.com/)、[Milvus 文档](https://milvus.io/docs) 和 [Elasticsearch 文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)。

## 何时使用本 skill
- 启动新的 RAG 项目，需要数据库选型指导
- 评估是否更换向量数据库
- 构建多模态 RAG 系统
- 成本是重要约束时
- 扩容需求尚不明确时

## 何时不要使用本 skill
- 已有满足需求的可用方案
- 任何数据库都能应付的简单原型（< 1 万文档）
- 使用的是由托管服务代管数据库选择的方案

## 相关 skill
- [RAG 的 Qdrant 搭建](../06-index/qdrant-setup-rag.md) - 搭建 Qdrant
- [面向代码文档的 RAG](../03-ingestion/rag-for-code-documentation.md) - 代码专属 RAG
- [面向多模态内容的 RAG](../03-ingestion/rag-for-multimodal-content.md) - 多模态 RAG

## 指标与成功标准
- **选型准确性**：所选数据库满足功能需求
- **性能**：达到或超过延迟/吞吐目标
- **成本**：在预算约束之内
- **可扩展性**：能随预期数据量增长
- **运维开销**：与团队能力匹配
