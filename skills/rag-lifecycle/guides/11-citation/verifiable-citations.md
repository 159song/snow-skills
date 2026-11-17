---
name: verifiable-citations
title: "可验证引用（Verifiable Citations）"
description: "把答案拆成原子 claim，对每条引用做存在性/蕴含/权限三层验证，引用解析器在查询时重新授权，未过引用门禁的答案不发布。"
allowed-tools:
  - Read
  - Grep
  - Glob
category: "citation"
tags: ["citation", "verification", "entailment", "grounding", "gating"]
---

## 概述
"模型给了引用"不等于"引用成立"。生产级引用是一条可验证的链：答案拆成原子 claim → 每个 claim 挂具体 chunk 引用 → 引用过三层验证（存在性、蕴含、权限）→ 查询时由 Citation Resolver 重新授权 → 引用覆盖率过门禁才发布。lineage（见第 2 章）是这条链的数据基础。

## 问题陈述
弱引用系统的典型失败：
- 引用指向的文档里根本没有那句话（幻觉引用）
- 引用存在但**不支持**答案的断言（断章取义）
- 引用今天有权限、明天权限被收回，缓存答案继续泄露（过期权限）
- 用户无法在 30 秒内从答案跳到原文核对

## 关键概念
- **Claim 拆分**：把答案分解为原子断言，每条断言独立可验证
- **三层验证**：
  1. **存在性（existence）**：被引文本确实出现在被引 chunk 中
  2. **蕴含（entailment）**：chunk 内容逻辑上支持该 claim
  3. **权限（permission）**：当前 principal 对被引 chunk 有读权限
- **Citation Resolver**：查询时按 principal 重新解析每条引用，失效引用触发降级（重检索或拒答）
- **引用覆盖率门禁**：claim 中带有效引用的比例达到阈值（如 ≥ 95%）才允许发布答案

## 参考数据模型（Pydantic）

```python
from pydantic import BaseModel

class Citation(BaseModel):
    claim_id: str
    chunk_id: str
    version_id: str          # 引用钉死版本，防止源文档更新后引用漂移
    quote: str               # 被引原文片段（存在性验证的对象）
    span: tuple[int, int]    # chunk 内定位

class Claim(BaseModel):
    claim_id: str
    text: str                # 原子断言
    citations: list[Citation]
```

## 实施指南

### 第 1 步：生成时拆 claim 并挂引用
提示词要求：每条陈述句独立成段、句末挂 `[n]` 标记；后处理把标记解析为 Citation 记录，quote 由 chunk 内精确匹配回填。

**原因**：整段挂一个引用时，验证只能整段通过或整段失败，无法定位断章取义。

### 第 2 步：离线验证三层
存在性用字符串匹配（quote ∈ chunk.text）；蕴含用 NLI 模型或 LLM judge（claim 是否被 chunk 蕴含）；权限用事实层 ACL（见 [RAG 数据模型](../02-data-model/rag-data-model.md)）。

**原因**：三层各自独立失败——存在性抓幻觉，蕴含抓断章取义，权限抓越权。

### 第 3 步：查询时重新授权
Citation Resolver 在每次回答前对引用集按当前 principal 重查 ACL：失效引用若承载关键 claim，触发重检索或拒答，而非静默删除。

**原因**：权限是时变属性；缓存的答案与引用不能继承旧权限。

### 第 4 步：发布门禁
引用覆盖率 = 有效引用 claim 数 / 总 claim 数。低于阈值（按用例商定，精确性要求越高阈值越高）时降级为"无法验证"话术或人工审核队列。

**原因**：没有门禁的引用系统会在质量下滑时静默产出半真半假的答案。

## 何时使用本指南
- 需求八问中精确性要求为"引用级"（合规、法务、医疗）
- 用户投诉"答案看起来对但点开引用对不上"

## 相关
- [可解释检索](explainable-retrieval.md) - 引用的检索侧基础
- [RAG 数据模型](../02-data-model/rag-data-model.md) - lineage 与版本钉死
- [RAG 安全威胁模型](../13-security/rag-security-threat-model.md) - 过期权限威胁的完整面
- [生成评测指标](../12-evaluation/generation-evaluation-metrics.md) - faithfulness 指标

## 指标与成功标准
- 引用覆盖率、三层验证通过率进入可观测面板（见第 14 章），并设告警阈值
- 抽样 20 条答案，每条 claim 都能在 30 秒内人工核对到原文
- 权限收回的回归测试：撤权后同一查询不再返回该引用
