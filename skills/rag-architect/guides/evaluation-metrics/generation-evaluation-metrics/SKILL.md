---
name: generation-evaluation-metrics
title: "生成评测指标（Generation Evaluation Metrics）"
description: "使用 LLM-as-judge（LLM 充当裁判）方法，对 RAG 答案的忠实度、答案相关性和正确性打分。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "evaluation-metrics"
tags: ["generation", "faithfulness", "llm-as-judge", "hallucination"]
---

## 概述
生成评测度量的是答案本身：它是否有检索到的上下文作为依据、是否回答了所问的问题、以及是否事实正确。这些指标能捕捉到检索指标看不到的幻觉（hallucination）和漂移。

## 问题陈述
一个管道可能检索到完美的上下文，却仍然产出错误、无依据或跑题的答案。精确匹配和 BLEU 类得分在开放式答案上会失效，因此团队需要语义层面的、感知依据（grounding-aware）的评测。

## 关键概念
- **忠实度（Faithfulness）**：答案中的每个论断是否都被检索到的上下文支持。
- **答案相关性（Answer relevancy）**：答案是否真正回答了所问的问题。
- **正确性（Correctness）**：答案是否与参考答案（ground truth）一致。
- **LLM-as-judge**：用一个强模型配合评分细则（rubric）大规模地给答案打分。
- **幻觉率（Hallucination rate）**：包含无上下文依据论断的答案占比。

## 实施指南

### 第 1 步：把依据性与正确性分开
对照检索到的上下文给忠实度打分，对照参考答案给正确性打分，作为两个不同的数字。

**原因**：一个答案可能忠实于糟糕的上下文却是错的，也可能正确却无依据；把它们混为一谈会同时掩盖这两种失败模式。

### 第 2 步：使用带固定评分细则的 LLM-as-Judge
定义一份显式的 rubric，用强裁判模型打分，并要求每个分数附带一段简短理由。

**原因**：固定的 rubric 和留档的理由让 LLM 的判断可重复、可审计，而不是随意的。

### 第 3 步：用人类标注校准裁判
对裁判打分抽样与人类标注比对，并调整 rubric 直到二者一致。

**原因**：未校准的裁判会产出自信但误导性的数字；校准让自动化得分值得信赖。

评分细则与实现可参见 [RAGAS 生成指标](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)、[DeepEval 指标](https://docs.confident-ai.com/docs/metrics-introduction)和 [G-Eval 论文](https://arxiv.org/abs/2303.16634)。

## 何时使用本技能
- 检测答案中的幻觉和无依据论断
- 在答案质量上比较 prompt、模型或生成参数
- 在检索指标之上增加一道答案质量门槛

## 何时不使用本技能
- 瓶颈在检索，且已知上下文质量差
- 答案是简短的精确事实，确定性匹配已经足够
- 不存在可用于评判的参考答案或依据上下文

## 相关技能
- [检索评测指标](../retrieval-evaluation-metrics/SKILL.md) - 给上下文打分，而不是答案
- [RAG 评测框架](../rag-evaluation-frameworks/SKILL.md) - 计算这些指标的工具
- [Self-RAG](../../retrieval-strategies/self-rag/SKILL.md) - 运行时自我评估依据性
- [带引用的可解释检索](../../retrieval-strategies/explainable-retrieval/SKILL.md) - 可追溯的依据

## 指标与成功标准
- **忠实度**：答案论断中可追溯到检索上下文的比例高
- **答案相关性**：答案始终切中所问的问题
- **正确性**：在金标集上与参考答案高度一致
- **裁判校准**：LLM-as-judge 得分与抽样的人类标注对齐
