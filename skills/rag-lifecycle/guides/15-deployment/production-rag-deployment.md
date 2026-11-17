---
name: production-rag-deployment
title: "生产环境 RAG 部署（Production RAG Deployment）"
description: "以健康检查、缓存和金丝雀发布来服务、扩展并安全上线 RAG 管道。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "deployment"
tags: ["serving", "scaling", "canary", "observability"]
---

## 概述
本技能覆盖把一个可用的 RAG 管道变成可靠的生产服务：通过 API 对外暴露、独立扩缩检索与生成、缓存热点路径，以及在不影响用户的情况下发布变更。

## 问题陈述
原型 RAG 代码假设只有一个用户、索引是热的、时间无限。在生产环境中，它要面对并发、冷启动、服务商超时和成本上限。没有服务化纪律，延迟会飙升、故障会级联，一次糟糕的发布会同时打击所有用户。

## 关键概念
- **独立扩缩容**：检索和 LLM 生成的资源画像不同，应分别扩缩。
- **缓存（Caching）**：为重复或相似的查询复用 embedding 和答案。
- **优雅降级（Graceful degradation）**：组件故障时退回到更简单的路径。
- **金丝雀发布（Canary rollout）**：在全量发布前先把变更推给一小片流量。

## 实施指南

### 第 1 步：把管道封装成服务
把检索和生成包进一个 API，为每个依赖配上超时、重试和健康检查。

**原因**：显式的超时和健康检查可以避免一个慢的向量库或 LLM 拖住整条请求路径。

### 第 2 步：扩缩并缓存热点路径
独立扩缩检索层和生成层，并缓存 embedding 和高频答案。

**原因**：检索和生成的瓶颈形态不同，而缓存能消除常见查询上重复的成本和延迟。

### 第 3 步：用金丝雀和降级路径发布
先把变更发布到一小片流量，并为组件不可用的情况定义一条降级路径。

**原因**：金丝雀发布和降级路径能控制一次坏发布或依赖故障的影响半径。

基础设施模式可参见 [Qdrant Cloud 文档](https://qdrant.tech/documentation/cloud/)和 [Ray Serve LLM 指南](https://docs.ray.io/en/latest/serve/llm/serving-llms.html)。

## 何时使用本技能
- 把已验证的 RAG 管道带给真实用户和流量
- 服务必须在并发和故障下保持响应
- 需要对管道变更做安全、可回滚的发布

## 何时不使用本技能
- 系统仍是没有真实流量的实验
- 完全托管的 RAG 平台已处理服务化
- 当前问题是离线质量，而不是服务可靠性

## 相关技能
- [索引版本管理与重建索引](../15-deployment/index-versioning-and-reindexing.md) - 安全演进索引
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md) - 存储侧扩缩
- [优化检索延迟](../07-retrieval/optimize-retrieval-latency.md) - 调优热点路径
- [RAG 评测框架](../12-evaluation/rag-evaluation-frameworks.md) - 用质量门槛卡住发布

## 指标与成功标准
- **延迟**：在预期并发下 P95 保持在预算之内
- **可用性**：组件故障时优雅降级而不是级联失败
- **缓存命中率**：重复查询避免冗余计算
- **发布安全**：坏发布在全量之前就被金丝雀捕获
