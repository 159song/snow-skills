---
name: vector-databases
title: "向量数据库（Vector Databases）"
description: "在 Qdrant 搭建、生产运维和按数据类型选择存储方案之间路由 RAG 的向量数据库决策。"
category: "vector-databases"
tags: ["vector-database", "qdrant", "metadata", "rag"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 向量数据库（Vector Databases）

## 概述
当主要 RAG 问题是选择、配置或运行向量存储层时，使用这个父级 skill。按搭建、生产或存储选型的需要路由到对应子 skill。

## 问题陈述
向量数据库的失误常表现为查询慢、过滤弱、元数据建模差或生产运维昂贵。RAG 系统需要一个与数据类型、规模和查询模式相匹配的存储层。

## 关键概念
- **集合与索引（collections & indexes）**：存储向量并调优搜索行为。
- **payload 元数据**：用结构化字段过滤和路由检索。
- **混合需求**：在需要时把向量与关键词或结构化检索结合。
- **生产运维**：规划备份、监控、扩容和迁移。

## 实施指南

### 第 1 步：识别数据类型
区分文本、代码、多模态和元数据密集的检索需求。

### 第 2 步：设计存储与过滤
选择集合布局、向量字段、payload 索引和元数据约定。

### 第 3 步：规划生产行为
验证延迟、备份策略、迁移路径、监控和故障恢复。

## 何时使用本 skill
- 为 RAG 系统选择向量数据库
- 为带过滤的语义检索搭建 Qdrant
- 让 Qdrant 或其他向量存储进入生产就绪状态

## 何时不要使用本 skill
- 主要问题是分块或文档解析
- 主要问题是 prompt 构造
- 向量数据库已选定，问题在重排（rerank）质量

## 相关 skill
- [RAG 的 Qdrant 搭建](../06-index/qdrant-setup-rag.md)
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md)
- [按数据类型选择向量数据库](../06-index/choosing-vector-db-by-datatype.md)

## 指标与成功标准
- 目标查询的元数据过滤正确
- 在预期语料规模下延迟稳定
- 备份、迁移和监控方案清晰
