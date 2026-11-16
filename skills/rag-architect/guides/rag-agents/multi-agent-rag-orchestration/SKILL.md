---
name: multi-agent-rag-orchestration
title: "多智能体 RAG 编排（Multi-Agent RAG Orchestration）"
description: "协调 planner 和专职 agent，对复杂 RAG 问题做分解、检索与综合。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "rag-agents"
tags: ["multi-agent", "orchestration", "planner", "decomposition"]
---

## 概述
多智能体编排把一个复杂问题拆分给多个专职 agent，例如一个 planner、一个或多个检索器、以及一个综合器。每个 agent 只负责一件窄职责的事，由协调者对它们排序并把结果合并成一个有依据的答案。

## 问题陈述
有些问题需要多次独立查找、跨来源推理，或多种单一 prompt 难以胜任的技能。把所有东西塞进一个 agent 会产出冗长、失焦的 prompt，以及悄悄丢掉问题一部分的答案。

## 关键概念
- **Planner（规划者）**：把查询分解为有序或并行的子任务。
- **专职 agent**：职责范围很窄的 worker，例如按来源划分的检索器。
- **协调者（Coordinator）**：为 agent 排序、处理故障并强制执行限制。
- **综合器（Synthesizer）**：把部分结果合并成一个有依据、带引用的答案。

## 实施指南

### 第 1 步：分解查询
让 planner 把问题拆成可以独立处理的子任务，在顺序要紧的地方写明显式依赖。

**原因**：清晰的分解避免子任务重叠或丢失原问题的某些部分。

### 第 2 步：分派窄职责的专职 agent
把每个子任务交给只有一个职责、且只带所需工具的 agent。

**原因**：窄职责让 prompt 简短、决策可调试、行为可预测。

### 第 3 步：综合并标注来源
在一个综合步骤中合并部分答案，解决冲突并保留来源引用。

**原因**：专门的综合步骤避免互相矛盾的碎片，并让最终答案可追溯。

完整示例可参见 [Multi-Agent RAG 示例](../../../examples/multi-agent-rag.md)和 [LangGraph 多智能体指南](https://docs.langchain.com/oss/python/langgraph/multi-agent)。

## 何时使用本技能
- 问题需要多次独立查找或跨来源推理
- 子任务需要单一 agent 难以胜任的不同技能或工具
- 需要在检索器之间并行以缩短端到端延迟

## 何时不使用本技能
- 单智能体路由已经能很好回答该查询
- 新增的协调成本和延迟不值得
- 子任务耦合紧密，无法干净拆分

## 相关技能
- [Agentic RAG 路由](../agentic-rag-routing/SKILL.md) - 编排之前先试路由
- [带引用的可解释检索](../../retrieval-strategies/explainable-retrieval/SKILL.md) - 综合阶段的来源标注
- [Graph RAG](../../retrieval-strategies/graph-rag/SKILL.md) - 跨实体推理
- [RAG 评测框架](../../evaluation-metrics/rag-evaluation-frameworks/SKILL.md) - 评测整个系统

## 指标与成功标准
- **分解质量**：子任务完整覆盖原问题
- **答案完整性**：多部分问题被完整回答
- **延迟**：并行 agent 使端到端时间保持可接受
- **可追溯性**：答案的每一段都能映射回某个来源
