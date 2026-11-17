---
name: rag-data-model
title: "RAG 数据模型：版本化、ACL 与 lineage（Data Model）"
description: "设计事实层（System of Record）实体：Document/Version/Section/Chunk/ACL/lineage，向量索引只是可重建的派生物。"
allowed-tools:
  - Read
  - Grep
  - Glob
category: "data-model"
tags: ["data-model", "versioning", "acl", "multi-tenant", "lineage", "postgres"]
---

## 概述
生产级 RAG 的分水岭在数据模型：**事实层（System of Record）与检索层分离**。Postgres 类事实库持有 Document、Version、Section、Chunk、ACL 与 lineage；向量库只是从事实层派生的缓存索引，随时可以删除重建。权限与版本在事实层有唯一事实来源，检索层出错最多损失性能，永远不会损失正确性。

## 问题陈述
没有这层模型的 RAG 会遇到：
- 文档更新后索引里新旧版本并存，答案引用已作废内容
- 权限只存在于检索层的 metadata 过滤里，一处漏配即跨租户泄漏
- 无法回答"这条答案的依据来自哪个文档的哪个版本"
- 删除文档后向量库里的 embedding 残留

## 关键概念
- **Document**：逻辑文档，含租户、来源、ACL 引用
- **DocumentVersion**：一次不可变的内容快照（content hash 去重），带 `as_of` 生效语义
- **Section**：文档的层级结构（章/节），保留导航上下文
- **Chunk**：检索单元，挂在 Version 下，可带 `parent_chunk_id`（小块检索、大块返回）
- **ACL**：principal（用户/组/租户）× resource × permission，只存事实层
- **lineage**：chunk → 源文档 span 的可追溯链，引用与审计的数据基础

## 参考数据模型（Pydantic）

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Permission(str, Enum):
    READ = "read"

class ACL(BaseModel):
    principal: str          # user:/group:/tenant: 前缀
    resource: str           # document_id 或 version_id
    permission: Permission

class Document(BaseModel):
    doc_id: str
    tenant: str
    source_uri: str
    acl_id: str
    current_version: str | None = None

class DocumentVersion(BaseModel):
    version_id: str
    doc_id: str
    content_hash: str       # 幂等摄取：同 hash 跳过
    as_of: datetime         # 时序查询的生效语义
    status: str             # active / superseded / deleted

class Chunk(BaseModel):
    chunk_id: str
    version_id: str
    parent_chunk_id: str | None = None
    section_path: list[str] # ["第3章", "3.2 安全"]
    text: str
    span: tuple[int, int]   # 在源文档中的字符区间，lineage 的锚点
```

## 实施指南

### 第 1 步：幂等摄取与增量索引
用 `content_hash` 判断版本是否变化：hash 相同直接跳过，hash 变化才创建新 Version 并只对该版本做 chunk + embed。删除文档 = Version 置 `deleted` + 从索引层摘除对应 chunk。

**原因**：全量重索引既贵又会造成检索空窗；hash 去重让摄取可以安全重跑。

### 第 2 步：权限在事实层、过滤在检索层
ACL 只写 Postgres；写入索引的 metadata 仅是查询时过滤的副本。权限变更时同步失效索引中的过滤字段（或直接重建——索引是派生物）。

**原因**：把权限的事实来源放在向量库 metadata 里，等于把安全属性托付给缓存。

### 第 3 步：parent-child 检索
索引小块（语义集中、embedding 准），命中后返回 `parent_chunk_id` 指向的大块或整个 `section_path`（上下文完整）。

**原因**：单一粒度要么检得准送不全，要么送得全检不准。

### 第 4 步：可重建性演练
任何时刻能用事实层全量重建索引：`rebuild_index() = SELECT chunks JOIN active versions JOIN acl`。上线前演练一次。

**原因**：派生物的可重建性是这套架构的安全网，未演练过的安全网不存在。

## 何时使用本指南
- 多租户、权限、版本化、审计任何一项出现在需求八问的答案里
- 索引与数据库内容开始打架（答案引用旧版本、删除后仍被检索到）

## 相关
- [需求八问与查询分类](../01-requirements/requirements-and-query-taxonomy.md) - 数据模型承接的输入
- [可验证引用](../11-citation/verifiable-citations.md) - lineage 的下游消费方
- [RAG 安全威胁模型](../13-security/rag-security-threat-model.md) - ACL 的威胁面分析
- [索引版本管理与重建索引](../15-deployment/index-versioning-and-reindexing.md) - 重建的部署侧操作

## 指标与成功标准
- 同一查询带不同 principal 得到权限内结果（用真实 ACL 测例验证）
- 文档更新后，旧版本 chunk 不再可被检索；删除后零残留（抽样断言）
- 全量重建演练通过，且重建期间检索可用（双索引或只读切换）
