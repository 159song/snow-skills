---
name: rag-agents
title: "RAG Agents"
description: "将 agentic RAG（智能体化 RAG）工作路由到查询路由、工具化检索与多智能体编排等子技能。"
category: "rag-agents"
tags: ["agents", "agentic-rag", "orchestration", "routing"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# RAG Agents

## 概述
当单次「先检索后生成」已经不够、系统必须决定检索什么、调用哪些工具、或如何在多个 agent 之间拆分工作时，使用这个父技能。根据问题属于路由决策还是多智能体编排，路由到对应的子技能。

## 问题陈述
静态 RAG 管道对每个查询都以同样方式回答：一次检索、一次生成。复杂问题需要条件化检索、多个来源、工具调用或分解为子任务。把这些硬塞进线性管道会产生脆弱、难以调试的系统。

## 关键概念
- **路由（Routing）**：在回答之前决定是否检索以及去哪里检索。
- **工具使用（Tool use）**：把检索器、搜索和计算器当作可调用的工具。
- **分解（Decomposition）**：把复杂查询拆成有序的子任务。
- **编排（Orchestration）**：协调多个专职 agent 并合并它们的输出。

## 实施指南

### 第 1 步：先决定是否真的需要 Agent
只有当查询在所需步骤或来源上确实差异明显时才引入智能体化控制。固定管道更便宜也更容易评测。

### 第 2 步：从路由开始，而不是多智能体
在引入多个协同 agent 之前，先加一个按查询选择检索策略或工具的路由器。

### 第 3 步：仅在确有必要时引入编排
当子任务确实相互独立或需要专门处理时，再转向 planner + worker agent 的结构，并保持每个 agent 的职责足够窄。

## 何时使用本技能
- 查询需要条件化检索、多个来源或工具调用
- 单次检索产出的答案不完整或肤浅
- 工作天然可以分解为专职子任务

## 何时不使用本技能
- 固定的「先检索后生成」管道已经回答得很好
- 延迟和成本预算无法承受额外的 LLM 调用
- 真正的瓶颈是检索质量，而不是控制流

## 相关技能
- [Agentic RAG 路由](../07-retrieval/agentic-rag-routing.md)
- [多智能体 RAG 编排](../07-retrieval/multi-agent-rag-orchestration.md)
- [自适应检索（Adaptive Retrieval）](../07-retrieval/adaptive-retrieval.md)
- [Self-RAG](../07-retrieval/self-rag.md)

## 指标与成功标准
- 智能体化控制相对固定管道有可度量的答案提升
- 每次新增的 LLM 调用都配得上它的延迟和成本
- 路由和 agent 决策可追溯、可调试
