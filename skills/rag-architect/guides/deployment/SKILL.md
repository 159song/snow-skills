---
name: deployment
title: "部署（Deployment）"
description: "将生产环境 RAG 上线工作路由到服务化、扩缩容、索引版本管理与安全重建索引等子技能。"
category: "deployment"
tags: ["deployment", "production", "reindexing", "routing"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 部署（Deployment）

## 概述
当 RAG 系统在开发环境已经可用、但需要在生产环境中做到可靠时，使用这个父技能。根据问题属于「管道的服务化与扩缩容」还是「不停机演进索引」，路由到对应的子技能。

## 问题陈述
即使在本地测试中通过的 RAG 系统，上线后仍会因为冷索引、高负载下延迟无上限、以及需要让检索层下线的全量重建索引而失败。原型代码很少处理版本管理、灰度发布或漂移问题，因此上线后质量会悄然衰减。

## 关键概念
- **服务化（Serving）**：将检索与生成封装在一个可扩展、可观测的服务之后。
- **索引版本管理（Index versioning）**：把向量索引当作一个带版本、可替换的制品。
- **零停机重建索引（Zero-downtime reindex）**：在不中断查询的情况下重建 embedding。
- **漂移（Drift）**：随着数据和用法偏离基线，质量缓慢衰减。

## 实施指南

### 第 1 步：把管道做成服务
在扩容之前，先给检索和生成套上一层 API，带上健康检查、超时和可观测性。

### 第 2 步：为索引做版本管理
把每次索引构建当作一个命名的、不可变的制品，这样只需切换一个指针就可以向前或向后回滚。

### 第 3 步：提前规划重建索引与回滚
把 embedding 模型迁移和重建索引设计成别名切换加快速回滚，而不是原地重刷。

## 何时使用本技能
- 将一个可用的 RAG 原型推向生产环境
- 系统需要可扩展、可观测，并能安全回滚
- embedding 模型或 schema 变更需要重建线上数据的索引

## 何时不使用本技能
- 系统仍是处于积极设计阶段的本地原型
- 瓶颈在检索或生成质量，而非运维
- 托管平台已经覆盖了服务化、扩缩容和重建索引

## 相关技能
- [生产环境 RAG 部署](production-rag-deployment/SKILL.md)
- [索引版本管理与重建索引](index-versioning-and-reindexing/SKILL.md)
- [面向生产 RAG 的 Qdrant](../vector-databases/qdrant-for-production-rag/SKILL.md)
- [优化检索延迟](../performance-optimization/optimize-retrieval-latency/SKILL.md)

## 指标与成功标准
- 管道以健康检查、超时和监控的方式对外提供服务
- 索引有版本管理，可不停机替换
- 重建索引与回滚是事先演练过的，而不是临时救火
