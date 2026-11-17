---
name: rag-for-code-documentation
title: "面向代码文档的 RAG"
description: "通过保留符号、文件结构和 API 上下文来处理代码感知的检索。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "data-type-handling"
tags: ["code", "programming", "syntax", "api", "documentation"]
---

## 概述
由于代码的结构化特性、特定语言的语法模式，以及保留函数签名、导入和上下文关系的重要性，面向代码文档的 RAG 需要专门处理。本 skill 覆盖代码片段的 embedding、API 参考的处理，以及代码感知上下文的检索。

## 问题陈述
通用 RAG 方案在代码相关查询上表现挣扎：
- 标准分块会把函数/类结构从签名中间切断
- 语言模型对代码语法和语义的理解不如自然语言
- 代码需要保留结构关系（导入、依赖、继承）
- API 查询需要精确匹配与语义理解并存
- 代码示例需要上下文才有用（导入、依赖）

## 关键概念
- **代码感知分块（Code-Aware Chunking）**：保留函数/类边界和语法单元
- **代码专用 embedding（Code-Specific Embeddings）**：在代码上训练的模型（CodeBERT、StarCoder）对比通用 embedding
- **语法保留（Syntax Preservation）**：维持格式、缩进和结构
- **上下文追踪（Context Tracking）**：跟踪导入链和依赖关系
- **代码的混合检索（Hybrid Search for Code）**：语义检索与基于 AST 的匹配相结合

## 实施指南

### 第 1 步：代码感知的文档解析
把代码文件解析成保留语法单元的结构化块。

**原因**：基于 AST 的解析能保留通用文本分块会丢失的代码结构。

### 第 2 步：代码专用 embedding
使用为代码设计的 embedding，或在文本 embedding 上补充代码感知特征。

**原因**：代码专用 embedding 能捕捉通用 embedding 会遗漏的代码语义（函数关系、模式）。

### 第 2.5 步：把代码块存入向量数据库
存储带丰富元数据的代码块，以便高效检索。

**原因**：丰富的元数据支持按语言、类型、文件路径等代码专属属性过滤。

### 第 3 步：实现代码感知搜索
带着代码特有的考量进行搜索。

**原因**：代码感知搜索把语义理解与精确过滤结合起来，服务编程专属场景。

### 第 4 步：处理 API 文档
对 API 参考查询做专项处理。

**原因**：API 查询往往需要精确匹配（函数/类名），而非纯语义检索。

实用参考包括 [CodeBERT 论文](https://huggingface.co/papers/2002.08155)、[GraphCodeBERT 论文](https://huggingface.co/papers/2009.08366)、[StarCoder 论文](https://huggingface.co/papers/2305.06161) 和 [GitHub code search](https://github.com/features/code-search)。

## 何时使用本 skill
- 构建代码搜索或文档助手
- 用户查询代码语法、API 或编程概念时
- IDE 集成和代码补全系统
- 构建带代码示例的技术文档
- 排查编程类查询问题

## 何时不要使用本 skill
- 纯自然语言内容（用通用 RAG）
- 代码结构对检索不重要时
- grep 就够用的极简代码库
- 无法部署代码专用 embedding 模型时

## 相关 skill
- [语义分块](../04-chunking/semantic-chunking.md) - 面向文档块
- [按数据类型选择向量数据库](../06-index/choosing-vector-db-by-datatype.md) - 数据库选型
- [层级分块](../04-chunking/hierarchical-chunking.md) - 面向嵌套代码结构

## 指标与成功标准
- **代码检索准确率**：函数/类名的精确匹配 > 90%
- **语义理解**：代码相关查询的 NDCG@10 > 0.7
- **上下文保留**：相关导入的包含率 > 80%
- **语法保留**：代码格式 100% 维持
- **查询延迟**：典型代码查询 < 200ms
