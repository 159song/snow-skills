---
name: index-versioning-and-reindexing
title: "索引版本管理与重建索引（Index Versioning and Reindexing）"
description: "为向量索引做版本管理，并做到不停机、无质量回退地重建索引或迁移 embedding。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
category: "deployment"
tags: ["reindexing", "versioning", "embedding-migration", "blue-green"]
---

## 概述
本技能覆盖线上 RAG 系统背后的索引演进：在模型或 chunking 策略变更后重建 embedding、在不同 embedding 模型之间迁移，以及为索引做版本管理，使变更是可逆的、查询永不中断。

## 问题陈述
索引不是静态的。embedding 模型在进步，chunking 策略会变化，文档也在更新。原地重建索引会让搜索下线，而且如果新构建更差，就没有回头路了。混用两个 embedding 模型的向量会悄然污染相似度得分。

## 关键概念
- **不可变的索引版本**：每次构建都是一个命名制品，绝不原地修改。
- **别名或指针切换**：通过翻转一个指针把流量在版本之间移动。
- **embedding 迁移**：切换模型需要对全部向量重新 embedding，而不是混用。
- **蓝绿重建（Blue-green reindex）**：在旧索引旁边构建新索引，然后切换。

## 实施指南

### 第 1 步：在旧索引旁边构建新索引
把新版本创建为一个独立的 collection 或索引，同时当前版本继续承接流量。

**原因**：在现役索引旁边构建，意味着查询永远不会打到一半构建或空的 collection 上。

### 第 2 步：切换前先验证
在切换之前，用评测金标集（golden set）跑新索引，并与当前基线比较得分。

**原因**：与基线比较可以在回退到达用户之前而不是之后发现它。

### 第 3 步：用别名切换，并随时保持可回滚
通过把别名重新指向新版本来完成切换，并在新版本被验证之前保留旧版本。

**原因**：别名切换让切换和回滚都近乎瞬时且低风险。

绝不要混合两个 embedding 模型来服务查询：模型变更时对整个语料库重新 embedding。参见 [Qdrant 别名指南](https://qdrant.tech/documentation/concepts/collections/#collection-aliases)和 [Qdrant 快照](https://qdrant.tech/documentation/concepts/snapshots/)。

## 何时使用本技能
- 在生产环境中变更 embedding 模型、chunking 策略或索引 schema
- 文档频繁更新，索引必须保持新鲜
- 需要可逆的、零停机的索引变更

## 何时不使用本技能
- 语料库是静态的，从不需要重新 embedding
- 托管服务已经替你处理重建索引和版本管理
- 系统是可以接受停机的原型

## 相关技能
- [生产环境 RAG 部署](../15-deployment/production-rag-deployment.md) - 对版本化索引提供服务
- [面向生产 RAG 的 Qdrant](../06-index/qdrant-for-production-rag.md) - collection 与别名操作
- [检索评测指标](../12-evaluation/retrieval-evaluation-metrics.md) - 切换前验证
- [按数据类型选择向量数据库](../06-index/choosing-vector-db-by-datatype.md) - 存储选型

## 指标与成功标准
- **零停机**：重建索引期间查询持续服务
- **可逆性**：回滚到先前版本快速且经过测试
- **不混用模型**：所有现役向量来自同一个 embedding 模型
- **经验证的切换**：新索引在切换前达到或超过基线
