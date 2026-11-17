---
name: optimize-retrieval-latency
title: "优化检索延迟（Optimize Retrieval Latency）"
description: "通过缓存、批处理和索引层优化来降低检索延迟。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "performance-optimization"
tags: ["latency", "performance", "caching", "indexing", "optimization"]
---

## 概述
优化 RAG 检索延迟对于用户体验依赖快速响应的生产应用至关重要。本技能覆盖在每一个阶段降低查询延迟的技术：索引、embedding 生成、搜索执行和结果处理。

## 问题陈述
RAG 系统常见延迟问题：
- 向量搜索操作耗时数百毫秒
- embedding 生成给每个查询带来显著开销
- 服务之间的网络往返使延迟叠加
- 冷启动导致不可预测的延迟尖峰
- 准确率与速度之间的取舍不明确

## 关键概念
- **查询路径（Query Path）**：从用户请求到检索结果的完整旅程
- **热路径优化（Hot Path Optimization）**：聚焦高频执行的操作
- **冷路径（Cold Path）**：低频操作，准确率比速度更重要
- **缓存策略（Caching Strategies）**：面向重复查询和 embedding 的多级缓存
- **索引调优（Index Tuning）**：在 recall、构建时间和搜索速度之间权衡

## 实施指南

### 第 1 步：测量当前性能
在优化之前先建立基线测量。

**原因**：无法测量就无法优化。性能剖析揭示的是真实瓶颈，而不是猜测。

### 第 2 步：优化 embedding 生成
降低生成查询 embedding 的开销。

**原因**：embedding 生成常常是瓶颈——缓存可以减少重复查询带来的这项开销。

### 第 3 步：优化向量数据库操作
针对延迟调优索引和搜索参数。

**原因**：索引参数直接影响搜索延迟，更低的 `ef` 值会以牺牲 recall 为代价换取更短的搜索时间。

### 第 4 步：实现多级缓存
在多个层级缓存以减少冗余计算。

**原因**：多级缓存能减少重复查询的计算，同时不牺牲独特查询的新鲜度。

### 第 5 步：优化结果处理
流式返回结果，并最小化后处理开销。

**原因**：流式降低内存占用，让用户更早看到结果，改善体感延迟。

### 第 6 步：实现查询优先级
对查询做优先级排序和批处理，以更好地利用资源。

**原因**：查询优先级确保重要查询优先获得资源，并减少争用。

有用的参考包括 [Qdrant 生产指南](https://qdrant.tech/documentation/guides/production/)、[Qdrant 快照概念](https://qdrant.tech/documentation/concepts/snapshots/)、[ANN Benchmarks](https://ann-benchmarks.com/)和 [AWS 缓存最佳实践](https://aws.amazon.com/caching/best-practices/)。

## 何时使用本技能
- 有延迟 SLA 要求的生产 RAG 系统
- 高流量应用（> 100 QPS）
- 用户体验至关重要的场景
- 存在重复查询的系统
- 资源受限的环境

## 何时不使用本技能
- 早期原型阶段（过早优化）
- 流量极低（< 1 QPS）
- 准确率比速度更重要的场景
- 一次性的批处理操作

## 相关技能
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md) - 生产环境配置
- [带 Reranking 的多轮检索](../08-reranking/multi-pass-retrieval-with-reranking.md) - 两阶段优化
- [混合检索 BM25 + 稠密向量](../07-retrieval/hybrid-search-bm25-dense.md) - 查询优化

## 指标与成功标准
- **端到端延迟**：典型查询 P50 < 100ms，P99 < 500ms
- **缓存命中率**：常见查询 > 60%
- **吞吐量**：单实例 > 100 QPS
- **Recall 衰减**：相对未优化基线 < 5%
- **资源效率**：CPU < 80%，内存占用稳定
