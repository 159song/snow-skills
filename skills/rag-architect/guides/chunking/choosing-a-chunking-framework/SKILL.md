---
name: choosing-a-chunking-framework
title: "选择分块框架"
description: "根据文档类型、流水线架构和检索目标选择合适的分块框架。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "chunking"
tags: ["framework-selection", "chonkie", "langchain", "llamaindex", "haystack", "unstructured"]
---

## 概述
分块质量既取决于策略本身，也同样取决于框架。本指南帮助编码 agent 根据数据形态、周围的 RAG 技术栈，以及主要诉求是速度、结构感知、检索质量还是集成简便性，在各个分块框架之间做出选择。

## 问题陈述
团队常常因为错误的理由选择分块框架：
- 默认使用应用里已有的框架，即使它对该数据类型的分块原语较弱
- 为只需要简单确定性切分的文档选择复杂的语义分块器
- 对 PDF、表格或代码仓库这类结构比纯长度更重要的内容使用通用文本切分器
- 只优化分块功能本身，却不考虑元数据传递、摄取（ingestion）工作流或下游检索

## 关键概念
- **框架契合度（Framework Fit）**：分块库与摄取及检索技术栈其余部分的匹配程度
- **结构感知（Structure Awareness）**：框架是否理解章节、标题、表格、页面或代码块
- **语义感知（Semantic Awareness）**：框架能否按含义分块，而不只按大小或分隔符
- **运维简便性（Operational Simplicity）**：在不引入第二套摄取系统的前提下采用该框架有多容易
- **分块深度（Chunking Depth）**：只需要固定大小的块，还是需要层级、句子窗口或代码感知等更丰富的模式

## 实施指南

### 第 1 步：识别主导文档类型
判断语料主要是纯文本、结构化文档、代码，还是杂乱的抽取产物。

**原因**：各分块框架在处理文档结构上的差异最为显著。适合 markdown 文档的选择，对扫描版 PDF 或源代码往往就是错的。

使用以下默认映射：
- 纯文本和通用散文：优先 LangChain 或 Chonkie
- 元数据丰富的 RAG 流水线：优先 LlamaIndex
- 以流水线为中心的搜索应用：优先 Haystack
- 解析后的 PDF、办公文件和版式复杂的文档：优先 Unstructured
- 代码占比高的仓库：优先 Chonkie，如需更简单的集成再考虑 LangChain

### 第 2 步：判断分块是核心需求还是只是工具
确定分块本身是系统的战略性组成部分，还是仅仅一个预处理步骤。

**原因**：如果分块对召回质量、代码结构或高吞吐摄取起决定性作用，就需要分块专业化程度更深的框架。如果只是顺带的，就用已在掌控 RAG 流水线的那个框架。

这样选择：
- 如果分块的精细程度是竞争优势，从 Chonkie 开始
- 如果分块只是更大型编排框架中的一个组件，根据应用技术栈在 LangChain、LlamaIndex 或 Haystack 中选择

### 第 3 步：让框架匹配检索模式
选择其分块模型支持你打算使用的检索模式的框架。

**原因**：有些框架围绕普通块构建，另一些则更适合层级检索、元数据增强的节点或保留章节的文档流。

按检索模式推荐的匹配：
- 对文本做简单向量检索：LangChain 或 Chonkie
- 层级检索和父子上下文：LlamaIndex 或 Haystack
- 面向报告和长文档的章节感知检索：Unstructured 或 Chonkie 递归分块
- 代码搜索和 AST 感知分块：Chonkie
- 需要上下文重建的细粒度句子级检索：LlamaIndex

### 第 4 步：使用框架决策矩阵
选择其优势与工作负载最匹配的框架。

**原因**：框架应按权衡取舍来选，而不是按流行度。

| 框架 | 擅长 | 何时选择 | 何时避免 |
|----------|---------|----------------|---------------|
| **[Chonkie](https://docs.chonkie.ai/oss/chunkers/overview)** | 专门的分块策略、高吞吐、语义与代码感知分块 | 分块是一等公民问题、需要语义/代码分块器，或摄取速度很重要 | 想在现有 LangChain 或 Haystack 应用中获得尽可能简单的默认方案 |
| **[LangChain Text Splitters](https://docs.langchain.com/oss/python/integrations/splitters/index)** | 简单可靠、与 LangChain 应用深度集成的通用分块 | 已在使用 LangChain 或 LangGraph，需要以最少额外工具获得实用的默认分块 | 需要超出标准切分器模式的深度代码、版式或语义分块 |
| **[LlamaIndex Node Parsers](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/)** | 元数据丰富的节点、句子窗口、层级解析、面向检索的分块 | 在用 LlamaIndex 摄取/查询流水线，或需要保留节点关系和检索元数据的分块 | 只需要直接的独立分块，不想引入 LlamaIndex 概念 |
| **[Haystack Preprocessors](https://docs.haystack.deepset.ai/docs/documentsplitter)** | 面向生产搜索系统的确定性流水线式切分 | 围绕 Haystack 流水线构建，需要可预测的文档预处理组件 | 需要 Haystack 内置预处理器无法提供的高级语义或代码感知分块 |
| **[Unstructured Chunking](https://docs.unstructured.io/open-source/core-functionality/chunking)** | 面向 PDF、Office 文档、HTML、表格和版式复杂内容的分区优先分块 | 主要挑战是分块之前的文档解析和结构保留 | 语料已经是干净文本，不需要版式感知解析 |

### 第 5 步：前往所选框架的分块文档
矩阵指向某个框架后，直接使用它的分块原语。只在该框架有明确优势时才采用它的分块器，没有理由就不要混用摄取框架。

- **Chonkie**（分块优先的库；token、递归、语义、代码、快速分块器）：[overview](https://docs.chonkie.ai/oss/chunkers/overview)、[RecursiveChunker](https://docs.chonkie.ai/oss/chunkers/recursive-chunker)、[SemanticChunker](https://docs.chonkie.ai/oss/chunkers/semantic-chunker)、[CodeChunker](https://docs.chonkie.ai/oss/chunkers/code-chunker)
- **LangChain**（LangChain/LangGraph 应用内的默认选择）：[splitters overview](https://docs.langchain.com/oss/python/integrations/splitters/index)、[RecursiveCharacterTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)
- **LlamaIndex**（元数据丰富的节点、句子窗口与层级检索）：[node parsers](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/)、[HierarchicalNodeParser](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/hierarchical/)、[SentenceWindowNodeParser](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_window/)
- **Haystack**（确定性流水线预处理）：[DocumentSplitter](https://docs.haystack.deepset.ai/docs/documentsplitter)、[HierarchicalDocumentSplitter](https://docs.haystack.deepset.ai/docs/hierarchicaldocumentsplitter)
- **Unstructured**（面向 PDF、Office、HTML、表格的分区优先方案；`by_title`）：[chunking](https://docs.unstructured.io/open-source/core-functionality/chunking)、[API strategies](https://docs.unstructured.io/platform-api/partition-api/chunking)

## 何时使用本 skill
- 决定编码 agent 应为新的 RAG 流水线采用哪个分块框架时
- 用框架支撑的方案替换临时拼凑的分块逻辑时
- 团队在调整块大小或重叠之前需要框架层面的建议时
- 语料混合了散文、代码和结构化企业文档时

## 何时不要使用本 skill
- 框架已被平台约束固定时
- 问题在于块大小而非框架选择时
- 只需要一个简单的确定性切分器、框架选型无关紧要时

## 相关 skill
- [语义分块](../semantic-chunking/SKILL.md) - 感知含义的块边界
- [层级分块](../hierarchical-chunking/SKILL.md) - 多级块结构
- [滑动窗口分块](../sliding-window-chunking/SKILL.md) - 基于重叠的分块
- [面向代码文档的 RAG](../../data-type-handling/rag-for-code-documentation/SKILL.md) - 代码占比高的语料指南

## 指标与成功标准
- **框架契合度**：所选框架与主导文档和检索模式匹配
- **运维简便性**：框架没有引入不必要的摄取复杂度
- **检索质量**：分块在实际语料上提升了召回率和答案质量
- **可维护性**：分块方案对团队而言可理解、可持续
- **迁移成本**：框架选择没有在没有明确收益的情况下造成可避免的锁定
