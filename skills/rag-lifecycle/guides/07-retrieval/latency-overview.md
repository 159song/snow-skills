---
name: performance-optimization
title: "性能优化（Performance Optimization）"
description: "将 RAG 性能工作路由到延迟、缓存、索引、过滤、批处理和查询优化等方向。"
category: "performance-optimization"
tags: ["latency", "performance", "caching", "rag"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 性能优化（Performance Optimization）

## 概述
当 RAG 系统功能上已经可用、但在预期流量下太慢、太贵或不稳定时，使用这个父技能。路由到针对性的延迟与检索优化指南。

## 问题陈述
RAG 的延迟可能来自 embedding 调用、向量搜索、元数据过滤、rerank、prompt 拼装或重复计算。优化需要在改动架构之前先对完整检索路径做性能剖析（profiling）。

## 关键概念
- **延迟预算（Latency budget）**：在 embedding、检索、rerank 和生成之间分配时间。
- **缓存（Caching）**：对常见查询和稳定文档避免重复计算。
- **索引调优（Index tuning）**：让搜索参数和索引匹配工作负载。
- **查询规划（Query planning）**：减少不必要的检索和 rerank 工作。

## 实施指南

### 第 1 步：剖析检索路径
分别测量 embedding、搜索、过滤、rerank、prompt 拼装和模型推理的延迟。

### 第 2 步：应用针对性优化
在剖析显示有瓶颈的地方使用缓存、批处理、payload 索引、top-k 调优和 reranker 门控。

### 第 3 步：复查质量与成本
确认优化没有降低 recall、忠实度、引用质量或运维可靠性。

## 何时使用本技能
- 检索对于产品体验来说太慢
- rerank 或查询扩展带来过多延迟
- 元数据过滤器或向量索引需要调优

## 何时不使用本技能
- 检索质量差但延迟可以接受
- 语料库尚未分块或建索引
- 系统缺少基线测量数据

## 相关技能
- [优化检索延迟](../07-retrieval/optimize-retrieval-latency.md)
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md)
- [带 Reranking 的多轮检索](../08-reranking/multi-pass-retrieval-with-reranking.md)

## 指标与成功标准
- 更低的 p50 和 p95 检索延迟
- 优化后答案质量保持稳定
- 单查询成本降低，且不以掩盖故障为代价
