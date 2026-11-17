---
name: evaluation-metrics
title: "评测指标（Evaluation Metrics）"
description: "将 RAG 评测工作路由到检索指标、生成质量与端到端评测框架等子技能。"
category: "evaluation-metrics"
tags: ["evaluation", "metrics", "ragas", "routing"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 评测指标（Evaluation Metrics）

## 概述
当 RAG 的主要问题是度量质量、检测回退（regression）、或证明某个变更确实有效时，使用这个父技能。根据故障出在检索、生成、还是评测装置（harness）本身，路由到对应的子技能。

## 问题陈述
团队在没有基线的情况下发布 RAG 变更，凭感觉调参，无法判断一个新的分块器（chunker）、embedding 模型或 prompt 到底是变好还是变坏。没有指标，检索和生成的回退会悄然上线，只能靠用户来发现。

## 关键概念
- **检索指标**：是否取回了正确的 chunk（recall@k、precision@k、MRR、nDCG、context precision/recall）。
- **生成指标**：答案是否有依据且有用（忠实度 faithfulness、答案相关性、正确性）。
- **金标集（Golden set）**：一个带标注的问答集合，用作比较的固定基线。
- **回归测试装置（Regression harness）**：对每次变更自动运行的评测，接入 CI。

## 实施指南

### 第 1 步：隔离出故障的层
分别度量检索和生成。上下文很好但答案很差是生成问题；上下文很差则不可能有好的答案。

### 第 2 步：为该层选择指标
当正确的 chunk 缺失或排序不当时用检索指标；当上下文很好但答案错误、无依据或跑题时用生成指标。

### 第 3 步：自动化为回归门槛
建立金标集，对每次变更跑指标，让回退基线的合并被拦截，而不是靠人工评估。

## 何时使用本技能
- 为新的或现有的 RAG 管道选择要跟踪的指标
- 证明某次 chunking、embedding 或 prompt 变更是否有效
- 在部署前搭建自动化评测门槛

## 何时不使用本技能
- 管道还没建好，没有可度量的东西
- 瓶颈是已知的实现 bug，而不是质量度量
- 已经有一套指标体系，问题在于检索或生成的设计

## 相关技能
- [检索评测指标](../12-evaluation/retrieval-evaluation-metrics.md)
- [生成评测指标](../12-evaluation/generation-evaluation-metrics.md)
- [RAG 评测框架](../12-evaluation/rag-evaluation-frameworks.md)
- [Self-RAG](../07-retrieval/self-rag.md)

## 指标与成功标准
- 每个 RAG 变更都与固定的金标集基线比较
- 检索质量和生成质量作为两个独立的数字分别跟踪
- 回退在 CI 中被捕获，而不是由用户发现
