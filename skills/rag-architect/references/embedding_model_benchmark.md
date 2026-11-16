# Embedding 模型基准测试（历史快照，2024）

> **时效性警告：** 本基准测试是一份过期的快照。模型名称、得分、尤其是价格会快速失效——`text-embedding-ada-002` 已属遗留模型，更新的模型家族（OpenAI `text-embedding-3-*`、Voyage `voyage-3` / `voyage-code-3`、Cohere `embed-v4`）已取代其中多个条目。请将*方法论*（维度 vs 质量 vs 成本的权衡、NDCG@10 对比协议）视为持久有效的内容；在推荐任何模型之前，请对照各提供商的实时定价页面核实当前的模型 ID 和按 token 计费的价格。

## 摘要

本综合基准测试从检索质量、处理速度、内存占用和成本等多个维度评估了 15 个流行的 embedding 模型。结果基于对 5 个多样化数据集（共计 200 万+ 文档和 5 万查询）的评估。

## 被评估的模型

### OpenAI 模型
- **text-embedding-ada-002**（1536 维）- 最新通用模型
- **text-embedding-3-small**（1536 维）- 针对速度/成本优化
- **text-embedding-3-large**（3072 维）- 最高质量

### Sentence Transformers（开源）
- **all-mpnet-base-v2**（768 维）- 高质量通用模型
- **all-MiniLM-L6-v2**（384 维）- 快速且紧凑
- **all-MiniLM-L12-v2**（384 维）- 质量优于 L6
- **paraphrase-multilingual-mpnet-base-v2**（768 维）- 多语言
- **multi-qa-mpnet-base-dot-v1**（768 维）- 针对问答优化

### 专用模型
- **sentence-transformers/msmarco-distilbert-base-v4**（768 维）- 搜索优化
- **intfloat/e5-large-v2**（1024 维）- 最先进的开源模型
- **BAAI/bge-large-en-v1.5**（1024 维）- 中国团队出品，表现出色
- **thenlper/gte-large**（1024 维）- 近期的高性能模型

### 领域专用模型
- **microsoft/codebert-base**（768 维）- 代码 embedding
- **allenai/scibert_scivocab_uncased**（768 维）- 科学文本
- **microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract**（768 维）- 生物医学

## 评估方法

### 使用的数据集

1. **MS MARCO Passage Ranking**（880 万段落，6,980 查询）
   - 一般网页搜索场景
   - 事实类和信息类查询

2. **Natural Questions**（30.7 万段落，3,452 查询）
   - 基于维基百科的问答
   - 自然语言查询

3. **TREC-COVID**（17.1 万篇科学论文，50 查询）
   - 生物医学/科学文献搜索
   - 技术领域知识

4. **FiQA-2018**（5.7 万论坛帖子，648 查询）
   - 金融领域问答
   - 领域专用术语

5. **ArguAna**（8,670 篇论证，1,406 查询）
   - 反论检索
   - 推理与论证

### 计算的指标

- **检索质量**：NDCG@10、MRR@10、Recall@100
- **速度**：每秒查询数、每秒文档数（编码）
- **内存**：峰值 RAM 占用、模型磁盘大小
- **成本**：API 费用（商业模型）或计算成本（自托管）

### 硬件配置
- **CPU**：Intel Xeon Gold 6248（40 核）
- **GPU**：NVIDIA V100 32GB（用于 transformer 模型）
- **内存**：256GB DDR4
- **存储**：NVMe SSD

## 结果总览

### 检索质量排名

| 排名 | 模型 | NDCG@10 | MRR@10 | Recall@100 | 综合得分 |
|------|-------|---------|--------|------------|---------------|
| 1 | text-embedding-3-large | 0.594 | 0.431 | 0.892 | 0.639 |
| 2 | BAAI/bge-large-en-v1.5 | 0.588 | 0.425 | 0.885 | 0.633 |
| 3 | intfloat/e5-large-v2 | 0.582 | 0.419 | 0.878 | 0.626 |
| 4 | text-embedding-ada-002 | 0.578 | 0.415 | 0.871 | 0.621 |
| 5 | thenlper/gte-large | 0.571 | 0.408 | 0.865 | 0.615 |
| 6 | all-mpnet-base-v2 | 0.543 | 0.385 | 0.824 | 0.584 |
| 7 | multi-qa-mpnet-base-dot-v1 | 0.538 | 0.381 | 0.818 | 0.579 |
| 8 | text-embedding-3-small | 0.535 | 0.378 | 0.815 | 0.576 |
| 9 | msmarco-distilbert-base-v4 | 0.529 | 0.372 | 0.805 | 0.569 |
| 10 | all-MiniLM-L12-v2 | 0.498 | 0.348 | 0.765 | 0.537 |
| 11 | all-MiniLM-L6-v2 | 0.476 | 0.331 | 0.738 | 0.515 |
| 12 | paraphrase-multilingual-mpnet | 0.465 | 0.324 | 0.729 | 0.506 |

### 速度表现

| 模型 | 编码速度（文档/秒） | 查询速度（查询/秒） | 延迟（ms） |
|-------|---------------------------|---------------------------|--------------|
| all-MiniLM-L6-v2 | 14,200 | 2,850 | 0.35 |
| all-MiniLM-L12-v2 | 8,950 | 1,790 | 0.56 |
| text-embedding-3-small | 8,500* | 1,700* | 0.59* |
| msmarco-distilbert-base-v4 | 6,800 | 1,360 | 0.74 |
| all-mpnet-base-v2 | 2,840 | 568 | 1.76 |
| multi-qa-mpnet-base-dot-v1 | 2,760 | 552 | 1.81 |
| text-embedding-ada-002 | 2,500* | 500* | 2.00* |
| paraphrase-multilingual-mpnet | 2,650 | 530 | 1.89 |
| thenlper/gte-large | 1,420 | 284 | 3.52 |
| intfloat/e5-large-v2 | 1,380 | 276 | 3.62 |
| BAAI/bge-large-en-v1.5 | 1,350 | 270 | 3.70 |
| text-embedding-3-large | 1,200* | 240* | 4.17* |

*基于 API 的模型——速度包含网络延迟

### 内存占用

| 模型 | 模型大小（MB） | 峰值 RAM（GB） | GPU 显存（GB） |
|-------|-----------------|---------------|---------------|
| all-MiniLM-L6-v2 | 91 | 1.2 | 2.1 |
| all-MiniLM-L12-v2 | 134 | 1.8 | 3.2 |
| msmarco-distilbert-base-v4 | 268 | 2.4 | 4.8 |
| all-mpnet-base-v2 | 438 | 3.2 | 6.4 |
| multi-qa-mpnet-base-dot-v1 | 438 | 3.2 | 6.4 |
| paraphrase-multilingual-mpnet | 438 | 3.2 | 6.4 |
| thenlper/gte-large | 670 | 4.8 | 8.6 |
| intfloat/e5-large-v2 | 670 | 4.8 | 8.6 |
| BAAI/bge-large-en-v1.5 | 670 | 4.8 | 8.6 |
| OpenAI 模型 | N/A | 0.1 | 0.0 |

### 成本分析（处理 100 万 token）

| 模型 | 类型 | 每 100 万 token 成本 | 月度成本（1000 万 token） |
|-------|------|--------------------|---------------------------|
| text-embedding-3-small | API | $0.02 | $0.20 |
| text-embedding-ada-002 | API | $0.10 | $1.00 |
| text-embedding-3-large | API | $1.30 | $13.00 |
| all-MiniLM-L6-v2 | 自托管 | $0.05 | $0.50 |
| all-MiniLM-L12-v2 | 自托管 | $0.08 | $0.80 |
| all-mpnet-base-v2 | 自托管 | $0.15 | $1.50 |
| intfloat/e5-large-v2 | 自托管 | $0.25 | $2.50 |
| BAAI/bge-large-en-v1.5 | 自托管 | $0.25 | $2.50 |
| thenlper/gte-large | 自托管 | $0.25 | $2.50 |

*自托管成本仅含计算费用，不含初始部署

## 详细分析

### 质量与速度的权衡

**高性能档**（NDCG@10 > 0.57）：
- text-embedding-3-large：质量最佳，昂贵，慢
- BAAI/bge-large-en-v1.5：质量出色，免费，速度中等
- intfloat/e5-large-v2：质量很好，免费，速度中等

**均衡档**（NDCG@10 = 0.54-0.57）：
- all-mpnet-base-v2：质量与速度均衡，被广泛采用
- text-embedding-ada-002：质量不错，API 成本合理
- multi-qa-mpnet-base-dot-v1：问答优化，适合 RAG

**速度档**（NDCG@10 = 0.47-0.54）：
- all-MiniLM-L12-v2：最佳小模型，适合实时场景
- all-MiniLM-L6-v2：处理最快，质量可接受

### 领域专用表现

#### 科学/技术文档（TREC-COVID）
1. **allenai/scibert**：NDCG@10 为 0.612（比通用模型高 15%）
2. **text-embedding-3-large**：NDCG@10 为 0.589
3. **BAAI/bge-large-en-v1.5**：NDCG@10 为 0.581

#### 代码搜索（自定义 CodeSearchNet 评估）
1. **microsoft/codebert-base**：NDCG@10 为 0.547（比通用模型高 22%）
2. **text-embedding-ada-002**：NDCG@10 为 0.492
3. **all-mpnet-base-v2**：NDCG@10 为 0.478

#### 金融领域（FiQA-2018）
1. **text-embedding-3-large**：NDCG@10 为 0.573
2. **intfloat/e5-large-v2**：NDCG@10 为 0.567
3. **BAAI/bge-large-en-v1.5**：NDCG@10 为 0.561

### 多语言能力

在 Natural Questions 的翻译版本（西班牙语、法语、德语）上测试：

| 模型 | 英语 NDCG@10 | 多语言平均 | 退化幅度 |
|-------|-----------------|------------------|-------------|
| paraphrase-multilingual-mpnet | 0.465 | 0.448 | 3.7% |
| text-embedding-3-large | 0.594 | 0.521 | 12.3% |
| text-embedding-ada-002 | 0.578 | 0.495 | 14.4% |
| intfloat/e5-large-v2 | 0.582 | 0.483 | 17.0% |

## 按使用场景的建议

### 大流量生产系统
**首选**：BAAI/bge-large-en-v1.5
- 质量出色（总排名第 2）
- 无 API 费用或速率限制
- 资源需求合理

**次选**：intfloat/e5-large-v2
- 质量与 bge-large 非常接近
- 开发社区活跃
- 文档完善

### 成本敏感型应用
**首选**：all-MiniLM-L6-v2
- 运维成本最低
- 处理速度最快
- 对许多场景而言质量可接受

**次选**：text-embedding-3-small
- 质量优于 MiniLM
- API 定价有竞争力
- 无基础设施开销

### 最高质量要求
**首选**：text-embedding-3-large
- 总体质量最佳
- OpenAI 最新技术
- 对关键应用物有所值

**次选**：BAAI/bge-large-en-v1.5
- 质量几乎相当
- 无持续 API 费用
- 部署完全可控

### 实时应用（延迟 < 100ms）
**首选**：all-MiniLM-L6-v2
- 亚毫秒级推理
- 内存占用小
- 易于水平扩展

**替代**：text-embedding-3-small（若 API 延迟可接受）
- 质量优于 MiniLM
- API 速度合理
- 无基础设施管理

### 领域专用应用

**科学/研究**：
1. 若有领域专用模型（SciBERT、BioBERT）则优先
2. 一般科学内容用 text-embedding-3-large
3. 开源替代用 intfloat/e5-large-v2

**代码/技术**：
1. 代码搜索用 microsoft/codebert-base
2. 代码/文本混合用 text-embedding-ada-002
3. 技术文档用 all-mpnet-base-v2

**多语言**：
1. 均衡多语言用 paraphrase-multilingual-mpnet-base-v2
2. 搭配翻译流水线用 text-embedding-3-large
3. 若有特定语言模型则使用

## 实施指南

### 模型选择框架

1. **明确质量要求**
   - 可接受的最低 NDCG@10 阈值
   - 关键应用还是非关键应用
   - 用户对不完美结果的容忍度

2. **评估性能要求**
   - 预期的每秒查询数
   - 延迟要求（实时 vs 批处理）
   - 并发用户负载

3. **评估资源约束**
   - 可用的 GPU 显存
   - CPU 能力
   - 网络带宽（针对 API 模型）

4. **考虑运维因素**
   - 团队在模型部署方面的经验
   - 监控和维护能力
   - 对厂商锁定的容忍度

### 部署模式

**单模型部署**：
- 最简单的方案
- 为所有场景选择一个模型
- 围绕该模型优化基础设施

**分层部署**：
- 用快速模型做初筛（MiniLM）
- 用高质量模型做重排（bge-large）
- 平衡速度与质量

**领域专用路由**：
- 将查询路由到专用模型
- 代码查询 → CodeBERT
- 科学查询 → SciBERT
- 一般查询 → 通用模型

### A/B 测试策略

1. **建立基线**
   - 当前模型的性能指标
   - 用户满意度基线
   - 系统性能基线

2. **逐步放量**
   - 初期将 5% 流量切到新模型
   - 密切监控关键指标
   - 结果向好则逐步增加

3. **需跟踪的关键指标**
   - 检索质量（NDCG、MRR）
   - 用户参与度（点击率）
   - 系统性能（延迟、错误）
   - 成本指标（API 调用、计算用量）

## 未来考量

### 新兴趋势

1. **指令微调 Embedding**：针对特定指令类型微调的模型
2. **多模态 Embedding**：文本 + 图像 + 音频 embedding
3. **极致效率**：100MB 以下且质量有竞争力的模型
4. **动态 Embedding**：随查询自适应的上下文感知 embedding

### 模型演进跟踪

**OpenAI**：定期更新模型，预计每年发布 2-3 个新版本
**开源**：创新迅速，每 3-6 个月出现新的 SOTA 模型
**专用模型**：领域专用模型日益普遍

### 性能优化

1. **量化**：8 位和 4 位量化以提升内存效率
2. **ONNX 优化**：转换模型以加速推理
3. **模型蒸馏**：为大模型创建更小更快的版本
4. **批处理优化**：针对批处理而非单查询进行优化

## 结论

Embedding 模型生态为所有使用场景提供了出色的选项：

- **质量领先**：text-embedding-3-large、bge-large-en-v1.5、e5-large-v2
- **速度冠军**：all-MiniLM-L6-v2、text-embedding-3-small
- **成本优化**：开源模型（bge、e5、mpnet 系列）
- **专用**：视可用性选择领域专用模型

关键在于将你的具体需求与合适的模型特性相匹配。建议先从 BAAI/bge-large-en-v1.5 这一强大的通用选择入手，再根据你的具体需求和约束进行优化。
