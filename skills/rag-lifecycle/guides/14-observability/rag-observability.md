---
name: rag-observability
title: "RAG 可观测性（Observability）"
description: "按 query type/语言/租户分片报告质量指标，用回归门禁、Shadow 与 Canary 发布把检索质量变成可管理的线上属性。"
allowed-tools:
  - Read
  - Grep
  - Glob
category: "observability"
tags: ["observability", "regression-gating", "shadow", "canary", "monitoring"]
---

## 概述
整体平均分是烟雾弹：语义型查询 95 分 + 精确型查询 40 分，平均 68 分会把一半用户的灾难藏起来。RAG 可观测的核心是**分片（segmentation）**——按 query type、语言、租户分别报告——再加上把评测变成部署门禁（回归门禁、Shadow、Canary）。

## 问题陈述
- 某类查询悄悄劣化，整体指标不动
- 换 embedding / 改 chunking 上线后无人知道质量变化
- 权限、引用、投毒等安全信号没有面板
- 线上只有延迟监控，质量全靠用户投诉

## 关键概念
- **分片报告（segmented reporting）**：指标按 query type / language / tenant / 来源切片，各自有基线
- **回归门禁（regression gate）**：CI 中跑评测集，任何分片跌破阈值即阻断发布
- **Shadow 部署**：新管线与旧管线同时服务真实流量，仅新管线不返回用户，对比指标
- **Canary 发布**：小比例真实流量切新管线，盯分片指标再逐步放量

## 指标面板（最小集）

| 层 | 指标 |
|---|---|
| 检索 | recall@k、precision@k、命中率、空结果率（按分片） |
| 生成 | 引用覆盖率、三层验证通过率、拒答率 |
| 安全 | 越权拦截数、Citation Resolver 失效引用数、来源命中率突增（投毒信号） |
| 成本/性能 | 每查询成本、P50/P95/P99 延迟、token 用量 |

**注意**：检索层指标离线算（评测集），引用与安全指标在线算（真实流量日志）。

## 实施指南

### 第 1 步：评测集分片并定阈值
把第 12 章的评测集按 query type / 语言 / 租户分片，每个分片定独立阈值（如精确型 recall@10 ≥ 0.9，语义型 ≥ 0.8），写入 CI 门禁配置。

**原因**：单一全局阈值的门禁要么放走局部劣化，要么卡死正常发布。

### 第 2 步：变更走 Shadow → Canary
embedding/chunking/重排任何变更先 Shadow 跑真实流量对比，分片指标不回退才 Canary 放量。

**原因**：离线评测集无法完全代表线上分布；Shadow 用真实流量补上这一块。

### 第 3 步：安全信号进面板
越权拦截、引用解析失效、来源命中率突增设独立告警阈值（见第 13 章）。

**原因**：质量劣化损失体验，安全信号劣化损失的是信任，告警优先级不同。

### 第 4 步：每个分片有主人
面板上每个分片标注责任团队/人，劣化时知道找谁。

**原因**：无主的分片指标会沦为装饰。

## 何时使用本指南
- 上线前搭建最小面板与门禁
- 线上质量投诉定位（先看分片，再查整体）
- 任何检索层变更的发布流程

## 相关
- [RAG 评测框架](../12-evaluation/rag-evaluation-frameworks.md) - 门禁用的评测集与工具
- [RAG 安全威胁模型](../13-security/rag-security-threat-model.md) - 安全信号的来源
- [生产环境 RAG 部署](../15-deployment/production-rag-deployment.md) - 发布流程载体
- [索引版本管理与重建索引](../15-deployment/index-versioning-and-reindexing.md) - Shadow 双索引的底层

## 指标与成功标准
- 每个分片有基线、阈值、责任人，三者可在面板上一眼确认
- 最近一次检索层变更有 Shadow/Canary 记录与分片对比结论
- 安全告警在演练注入时真的响了
