---
name: retrieval-evaluation-metrics
title: "检索评测指标（Retrieval Evaluation Metrics）"
description: "用 recall、precision、MRR、nDCG 以及 context precision 与 context recall 度量检索质量。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "evaluation-metrics"
tags: ["retrieval", "recall", "ndcg", "mrr", "context-precision"]
---

## 概述
检索评测度量的是在 LLM 看到数据之前，管道是否取回了正确的 chunk。由于生成质量的上限由检索质量决定，这些指标隔离出了 RAG 坏答案中最常见、也最可修复的来源。

## 问题陈述
团队只凭最终答案质量评判 RAG，这会掩盖故障出在哪一层。当正确的 chunk 从未被检索到时，任何 prompt 或模型变更都无法挽回，但管道却常常被归咎于生成而不是检索。

## 关键概念
- **Recall@k**：相关 chunk 出现在前 k 条结果中的比例。
- **Precision@k**：前 k 条结果中真正相关的比例。
- **MRR（Mean Reciprocal Rank，平均倒数排名）**：奖励把第一条相关 chunk 放在靠前的位置。
- **nDCG**：感知排名的得分，相关结果排得越靠前权重越高。
- **Context precision 与 context recall**：RAGAS 风格的指标，评判检索到的上下文对于回答该问题是否相关且完整。

## 实施指南

### 第 1 步：构建带标注的查询集
收集有代表性的问题，并标注每个问题相关的是哪些文档 chunk。这个金标集就是所有指标对照的 ground truth。

**原因**：没有已知的相关目标可对照，基于排名的指标毫无意义。

### 第 2 步：先测 Recall 再测 Precision
先在多个候选 k 值上看 recall@k，确认相关 chunk 到底有没有被检索到，然后用 MRR 和 nDCG 检查精确率和排序质量。

**原因**：一个从未被检索到的相关 chunk 不可能靠 rerank 救回来，所以 recall 是下游一切的上限。

### 第 3 步：加入免参考的上下文指标
当人工相关性标注稀缺时，使用由 LLM 评判的 context precision 和 context recall，评估检索到的上下文是否足以支撑参考答案。

**原因**：人工标注相关性很贵；免参考指标让评测可以扩展到更大的查询集。

定义与实现可参见 [RAGAS context 指标](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)、[RAGAS 论文](https://arxiv.org/abs/2309.15217)和 [scikit-learn 排名指标](https://scikit-learn.org/stable/modules/model_evaluation.html#ranking-metrics)。

## 何时使用本技能
- 诊断坏答案究竟来自检索还是生成
- 客观比较 chunking 策略、embedding 模型或 rerankers
- 在调优下游生成之前先确立 recall 基线

## 何时不使用本技能
- 已知检索到的上下文是好的，但答案仍然错误
- 语料库没有相关性标注，也无法生产或近似得到
- 系统不做检索（纯生成或闭卷设置）

## 相关技能
- [生成评测指标](../generation-evaluation-metrics/SKILL.md) - 给答案打分，而不是上下文
- [RAG 评测框架](../rag-evaluation-frameworks/SKILL.md) - 计算这些指标的工具
- [带 Reranking 的多轮检索](../../retrieval-strategies/multi-pass-retrieval-with-reranking/SKILL.md) - 改善基于排名的得分
- [混合检索 BM25 + 稠密向量](../../retrieval-strategies/hybrid-search-bm25-dense/SKILL.md) - 改善 recall

## 指标与成功标准
- **Recall@k**：足够高，相关上下文几乎总是出现在前 k 条中
- **MRR / nDCG**：相关 chunk 排在前列，而不是被埋没
- **Context Precision**：最终上下文中不相关 chunk 占比低
- **稳定性**：指标在固定的金标集上计算，便于跨运行比较
