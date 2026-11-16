---
name: rag-evaluation-frameworks
title: "RAG 评测框架（RAG Evaluation Frameworks）"
description: "选择并接入一个 RAG 评测框架，把它变成 CI 回归门槛。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "evaluation-metrics"
tags: ["ragas", "deepeval", "trulens", "ci", "regression"]
---

## 概述
本技能覆盖 RAG 评测的工具层：选哪个框架、如何组织金标集、以及如何在每次变更时自动运行评测，从而在质量回退上线之前把它拦下。

## 问题陈述
指标只有持续运行才有用。团队在笔记本里算一次分数，从不自动化，然后丢掉基线。临时性的评测无法捕捉由数据漂移、prompt 修改或模型替换带来的缓慢回退。

## 关键概念
- **评测框架**：一个从「问题、上下文、答案」数据集计算检索和生成指标的库。
- **金标集（Golden set）**：纳入版本控制的、带参考答案和相关上下文的问题集。
- **免参考（reference-free） vs 依赖参考（reference-based）**：指标是否需要 ground-truth 答案，还是直接评判质量。
- **回归门槛（Regression gate）**：当指标跌破基线时失败的 CI 任务。

## 实施指南

### 第 1 步：按契合度选择框架
选择与你的技术栈匹配的框架，而不是最流行的那个。

**原因**：每个工具的数据模型和集成方式都不同，后期切换成本很高。

默认映射：
- 指标优先、希望最少配置的 RAG 打分：倾向 [RAGAS](https://docs.ragas.io/)
- 单元测试风格的断言和 CI 集成：倾向 [DeepEval](https://docs.confident-ai.com/)
- 面向运行中应用的实时埋线和仪表盘：倾向 [TruLens](https://www.trulens.org/)
- prompt 与服务商对比矩阵：倾向 [promptfoo](https://www.promptfoo.dev/)

### 第 2 步：构建带版本管理的金标集
整理有代表性的问题，配上参考答案和相关上下文，并提交进代码仓库。

**原因**：固定的、纳入版本管理的数据集让得分在不同运行和贡献者之间可比较。

### 第 3 步：把评测接入 CI
在 CI 中对金标集运行框架，当得分回退超过阈值时让构建失败。

**原因**：自动化门槛把评测从一次性报告变成常设护栏。

## 何时使用本技能
- 首次搭建可重复的评测管道
- 为 RAG 项目增加自动化质量门槛
- 在确定一套评测技术栈之前比较各工具

## 何时不使用本技能
- 只需要单个指标的定义，而不是工具
- 项目是一次性原型，没有回退风险
- 没有金标集，且暂时无法创建

## 相关技能
- [检索评测指标](../retrieval-evaluation-metrics/SKILL.md) - 这些工具计算的指标
- [生成评测指标](../generation-evaluation-metrics/SKILL.md) - 答案质量指标
- [生产环境 RAG 部署](../../deployment/production-rag-deployment/SKILL.md) - 用得分卡住部署
- [优化检索延迟](../../performance-optimization/optimize-retrieval-latency/SKILL.md) - 在质量与速度之间权衡

## 指标与成功标准
- **可复现性**：同一金标集在不同运行间产出可比较的得分
- **覆盖面**：金标集覆盖真实的查询分布
- **自动化**：每个相关变更都会在 CI 中运行评测
- **可行动性**：门槛失败时能指出回退发生在哪一层
