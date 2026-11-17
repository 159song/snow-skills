---
name: qdrant-setup-rag
title: "RAG 的 Qdrant 搭建"
description: "为 RAG 搭建 Qdrant：集合、payload 过滤和批量摄取。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "vector-databases"
tags: ["qdrant", "setup", "ingestion", "filtering"]
---

## 概述
Qdrant 是一个面向高性能 RAG 应用的开源向量相似度检索引擎。本 skill 覆盖 Qdrant 搭建、创建带正确索引的集合、用元数据实现过滤，以及文档摄取管理。

## 问题陈述
为 RAG 搭建向量数据库涉及多项考量：
- 为你的 embedding 模型选择合适的距离度量
- 针对「性能 vs 召回」配置最优索引参数
- 为有效过滤设计元数据结构
- 高效处理批量摄取
- 管理集合 schema 变更

## 关键概念
- **距离度量（Distance Metric）**：用于向量比较的余弦相似度、点积或欧氏距离
- **索引类型（Index Type）**：用于近似最近邻搜索的 HNSW（Hierarchical Navigable Small World）
- **payload 过滤（Payload Filtering）**：基于关联元数据查询向量
- **集合 schema（Collection Schema）**：定义向量维度和 payload 结构
- **批量操作（Batch Operations）**：高效的向量批量插入

## 实施指南

### 第 1 步：安装并初始化 Qdrant
在本地搭建 Qdrant 或连接云实例。

**原因**：Docker 提供带持久化的隔离环境，云选项则提供托管的可扩展性。

### 第 2 步：创建集合
根据你的 embedding 模型和使用场景配置集合参数。

**原因**：创建时的正确配置可避免日后昂贵的重建索引。归一化 embedding 默认用 COSINE。

### 第 3 步：设计元数据 schema
为有效过滤组织你的 payload（元数据）。

**原因**：结构良好的元数据支持强大的过滤查询，并帮助组织检索结果。

### 第 4 步：摄取文档
连同 embedding 和元数据一起上传文档。

**原因**：与逐条上传相比，批量操作能显著提升摄取性能。

### 第 5 步：实现过滤查询
带元数据过滤器的查询，实现定向检索。

**原因**：过滤支持领域限定检索（例如「只搜文档」或「只搜代码示例」）。

### 第 6 步：监控与维护
为集合健康搭建监控。

**原因**：监控帮助在性能问题和扩容需求影响用户之前发现它们。

生产级搭建模式可参考 [Qdrant 文档](https://qdrant.tech/documentation/)、[Qdrant 过滤](https://qdrant.tech/documentation/concepts/filtering/)、[Qdrant Python 客户端](https://github.com/qdrant/qdrant-client) 和 [HNSW 论文](https://arxiv.org/abs/1603.09320)。

## 何时使用本 skill
- 从零构建新的 RAG 应用
- 为开发环境搭建本地向量数据库
- 从其他向量数据库迁移到 Qdrant
- 需要无厂商锁定的开源方案时

## 何时不要使用本 skill
- 需要托管、零运维方案时（考虑 Qdrant Cloud）
- 极小数据集（< 1000 向量），简单列表可能就够
- 需要多向量索引等专门特性时（考虑其他数据库）

## 相关 skill
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md) - 生产扩容
- [按数据类型选择向量数据库](../06-index/choosing-vector-db-by-datatype.md) - 数据库选型指南
- [优化检索延迟](../07-retrieval/optimize-retrieval-latency.md) - 性能调优

## 指标与成功标准
- **搭建时间**：< 10 分钟获得可用集合
- **摄取速度**：普通硬件上 > 10,000 向量/分钟
- **查询延迟**：100 万向量上查询 < 50ms
- **索引**：HNSW 在合理时间内自动完成索引
- **召回率（recall）**：10 近邻召回 > 0.95
