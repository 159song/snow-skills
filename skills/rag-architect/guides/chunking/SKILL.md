---
name: chunking
title: "Chunking（分块）"
description: "在语义分块、层级分块、滑动窗口、上下文分块头与框架选型等策略之间路由 RAG 的分块决策。"
category: "chunking"
tags: ["chunking", "routing", "rag", "preprocessing"]
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Chunking（分块）

## 概述
当主要 RAG 问题是如何把源材料切分成可检索单元时，使用这个父级 skill。根据文档形态、检索失败原因和生产约束，路由到最匹配的子 skill。

## 问题陈述
糟糕的分块会导致检索漏召回、答案碎片化、上下文重复和引用薄弱。RAG 系统需要既能保留语义、又能让索引与检索保持高效的分块策略。

## 关键概念
- **语义边界（semantic boundaries）**：在观点自然切换之处切分。
- **层级（hierarchy）**：保留文档、章节与小节之间的关系。
- **重叠（overlap）**：在块边界两侧加入受控的相邻上下文。
- **上下文头（context headers）**：把继承来的标题和元数据附加到块上。

## 实施指南

### 第 1 步：识别语料形态
散文类内容用语义分块，结构化文档用层级分块，API 或源码仓库用代码专用指南。

### 第 2 步：对照检索失败模式
答案跨边界时用滑动窗口，块缺少来源上下文时用上下文头，固定窗口切碎语义时用语义分块。

### 第 3 步：验证分块质量
在更换 embedding 或向量数据库（vector database）之前，先度量检索召回率（recall）、答案忠实度（groundedness）、重复上下文比例和引用有效性。

## 何时使用本 skill
- 为新的 RAG 流水线选择分块策略
- 排查源内容碎片化导致的召回率低
- 改善引用与来源可追溯性

## 何时不要使用本 skill
- 瓶颈在检索之后的排序阶段
- 问题出在向量数据库的运维或部署
- 源文档已经完成分块并验证过

## 相关 skill
- [语义分块](semantic-chunking/SKILL.md)
- [层级分块](hierarchical-chunking/SKILL.md)
- [滑动窗口分块](sliding-window-chunking/SKILL.md)
- [上下文分块头](contextual-chunk-headers/SKILL.md)
- [选择分块框架](choosing-a-chunking-framework/SKILL.md)

## 指标与成功标准
- 跨块边界问题的召回率更高
- prompt 中重复或无关的上下文更少
- 来源引用更好、检索到的段落更连贯
