---
name: agentic-rag-routing
title: "Agentic RAG 路由（Agentic RAG Routing）"
description: "用 LLM 驱动的路由器把每个查询送到正确的检索策略、数据源或工具。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "rag-agents"
tags: ["routing", "tool-use", "query-classification", "agentic-rag"]
---

## 概述
Agentic 路由在检索之前加了一个决策步骤：agent 对查询分类，并选择是否检索、命中哪个来源或索引、调用哪个工具。这把一条千篇一律的管道变成了按查询自适应的管道。

## 问题陈述
不同的查询需要不同的处理方式。一个定义型问题、一个多跳（multi-hop）问题和一个实时数据问题，在单一固定检索路径下都会失败。没有路由，管道对简单查询过度检索，对复杂查询又服务不足。

## 关键概念
- **检索决策**：该查询到底需不需要检索。
- **来源路由**：为查询选择正确的索引、collection 或工具。
- **查询分类**：把查询映射到一个处理策略。
- **兜底（Fallback）**：路由器不确定时的安全默认路径。

## 实施指南

### 第 1 步：定义路由空间
枚举所有可用的具体路由，例如：不检索、向量搜索、关键词搜索、web 搜索或结构化数据工具。

**原因**：路由器只能从你定义好的路由中选择；开放式路由器不可预测也难以评测。

### 第 2 步：对查询分类
用 LLM 或轻量分类器把每个查询映射到一条路由，返回结构化决策而不是自由文本。

**原因**：结构化的路由决策可测试，且可以记录日志、重放和评测。

### 第 3 步：加兜底和护栏
为低置信度决策定义默认路由，并限制单个查询可触发的工具数或跳数上限。

**原因**：护栏防止工具调用失控循环，让延迟和成本保持有界。

模式可参见 [LangGraph agentic RAG 指南](https://docs.langchain.com/oss/python/langgraph/agentic-rag)和 [LlamaIndex router query engine](https://docs.llamaindex.ai/en/stable/module_guides/querying/router/)。

## 何时使用本技能
- 查询横跨多个来源、格式或新鲜度要求
- 有些查询不需要检索，另一些需要多跳
- 想在引入完整多智能体编排之前先获得按查询的控制能力

## 何时不使用本技能
- 所有查询用一条检索路径就能回答得很好
- 额外的分类调用会击穿延迟预算
- 只有一个数据源，没有工具可选

## 相关技能
- [自适应检索（Adaptive Retrieval）](../../retrieval-strategies/adaptive-retrieval/SKILL.md) - 按查询类型选择策略
- [Self-RAG](../../retrieval-strategies/self-rag/SKILL.md) - 生成时点的检索决策
- [CRAG - Corrective RAG](../../retrieval-strategies/crag-corrective-rag/SKILL.md) - 弱检索时的兜底搜索
- [多智能体 RAG 编排](../multi-agent-rag-orchestration/SKILL.md) - 当路由不够时

## 指标与成功标准
- **路由准确率**：查询进入正确的处理路径
- **免检索节省**：简单查询跳过不必要的检索
- **有界成本**：工具和跳数保持在限制之内
- **兜底率**：低置信度路由保持少见且安全
