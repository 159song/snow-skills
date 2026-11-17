#!/usr/bin/env python3
"""
RAG 流水线设计器 - 根据需求设计完整的 RAG 流水线。

本脚本分析需求并生成一份完整的 RAG 流水线设计，
包括架构图、组件推荐、配置模板和成本预估。

设计的组件：
- 分块策略推荐
- Embedding 模型选择
- 向量数据库推荐
- 检索方案（稠密/稀疏/混合）
- 重排序配置
- 评估框架搭建
- 生产部署模式

无外部依赖 - 仅使用 Python 标准库。
"""

import argparse
import json
import math
import os
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Scale(Enum):
    """系统规模分类。"""
    SMALL = "small"      # < 100 万文档，每天 < 1 千次查询
    MEDIUM = "medium"    # 100 万-1 亿文档，每天 1 千-10 万次查询
    LARGE = "large"      # > 1 亿文档，每天 > 10 万次查询


class DocumentType(Enum):
    """文档类型分类。"""
    TEXT = "text"                # 纯文本、文章
    TECHNICAL = "technical"      # 文档、手册
    CODE = "code"               # 源代码文件
    SCIENTIFIC = "scientific"    # 研究论文、期刊
    LEGAL = "legal"             # 法律文书、合同
    MIXED = "mixed"             # 多种文档类型混合


class Latency(Enum):
    """延迟要求。"""
    REAL_TIME = "real_time"      # < 100ms
    INTERACTIVE = "interactive"   # < 500ms
    BATCH = "batch"              # 可接受 > 1s


@dataclass
class Requirements:
    """RAG 系统需求。"""
    document_types: List[str]
    document_count: int
    avg_document_size: int  # 字符数
    queries_per_day: int
    query_patterns: List[str]  # 例如 ["factual", "conversational", "analytical"]
    latency_requirement: str
    budget_monthly: float  # 美元
    accuracy_priority: float  # 0-1 打分
    cost_priority: float     # 0-1 打分
    maintenance_complexity: str  # "low"、"medium"、"high"


@dataclass
class ComponentRecommendation:
    """针对某个流水线组件的推荐。"""
    name: str
    type: str
    config: Dict[str, Any]
    rationale: str
    pros: List[str]
    cons: List[str]
    cost_monthly: float


@dataclass
class PipelineDesign:
    """完整的 RAG 流水线设计。"""
    chunking: ComponentRecommendation
    embedding: ComponentRecommendation
    vector_db: ComponentRecommendation
    retrieval: ComponentRecommendation
    reranking: Optional[ComponentRecommendation]
    evaluation: ComponentRecommendation
    total_cost: float
    architecture_diagram: str
    config_templates: Dict[str, Any]


class RAGPipelineDesigner:
    """流水线设计器主类。"""

    def __init__(self):
        self.embedding_models = self._load_embedding_models()
        self.vector_databases = self._load_vector_databases()
        self.chunking_strategies = self._load_chunking_strategies()

    def design_pipeline(self, requirements: Requirements) -> PipelineDesign:
        """根据需求设计完整的 RAG 流水线。"""
        print(f"Designing RAG pipeline for {requirements.document_count:,} documents...")

        # 确定系统规模
        scale = self._determine_scale(requirements)
        print(f"System scale: {scale.value}")

        # 逐个设计各组件
        chunking = self._recommend_chunking(requirements, scale)
        embedding = self._recommend_embedding(requirements, scale)
        vector_db = self._recommend_vector_db(requirements, scale)
        retrieval = self._recommend_retrieval(requirements, scale)
        reranking = self._recommend_reranking(requirements, scale)
        evaluation = self._recommend_evaluation(requirements, scale)

        # 计算总成本
        total_cost = (chunking.cost_monthly + embedding.cost_monthly +
                     vector_db.cost_monthly + retrieval.cost_monthly +
                     evaluation.cost_monthly)
        if reranking:
            total_cost += reranking.cost_monthly

        # 生成架构图
        architecture = self._generate_architecture_diagram(
            chunking, embedding, vector_db, retrieval, reranking, evaluation
        )

        # 生成配置模板
        configs = self._generate_config_templates(
            chunking, embedding, vector_db, retrieval, reranking, evaluation
        )

        return PipelineDesign(
            chunking=chunking,
            embedding=embedding,
            vector_db=vector_db,
            retrieval=retrieval,
            reranking=reranking,
            evaluation=evaluation,
            total_cost=total_cost,
            architecture_diagram=architecture,
            config_templates=configs
        )

    def _determine_scale(self, req: Requirements) -> Scale:
        """根据需求确定系统规模。"""
        if req.document_count < 1_000_000 and req.queries_per_day < 1_000:
            return Scale.SMALL
        elif req.document_count < 100_000_000 and req.queries_per_day < 100_000:
            return Scale.MEDIUM
        else:
            return Scale.LARGE

    def _recommend_chunking(self, req: Requirements, scale: Scale) -> ComponentRecommendation:
        """推荐分块策略。"""
        doc_types = set(req.document_types)

        if "code" in doc_types:
            strategy = "semantic_code_aware"
            config = {"max_size": 1000, "preserve_functions": True, "overlap": 50}
            rationale = "Code documents benefit from function/class boundary awareness"
        elif "technical" in doc_types or "scientific" in doc_types:
            strategy = "semantic_heading_aware"
            config = {"max_size": 1500, "heading_weight": 2.0, "overlap": 100}
            rationale = "Technical documents have clear hierarchical structure"
        elif len(doc_types) > 2 or "mixed" in doc_types:
            strategy = "adaptive_chunking"
            config = {"strategies": ["paragraph", "sentence", "fixed"], "auto_select": True}
            rationale = "Mixed document types require adaptive strategy selection"
        else:
            if req.avg_document_size > 5000:
                strategy = "paragraph_based"
                config = {"max_size": 2000, "min_paragraph_size": 100}
                rationale = "Large documents benefit from paragraph-based chunking"
            else:
                strategy = "sentence_based"
                config = {"max_size": 1000, "sentence_overlap": 1}
                rationale = "Small to medium documents work well with sentence chunking"

        return ComponentRecommendation(
            name=strategy,
            type="chunking",
            config=config,
            rationale=rationale,
            pros=self._get_chunking_pros(strategy),
            cons=self._get_chunking_cons(strategy),
            cost_monthly=0.0  # 仅处理成本
        )

    def _recommend_embedding(self, req: Requirements, scale: Scale) -> ComponentRecommendation:
        """推荐 embedding 模型。"""
        doc_types = set(req.document_types)

        # 权衡准确率与成本优先级
        high_accuracy = req.accuracy_priority > 0.7
        cost_sensitive = req.cost_priority > 0.6

        if "code" in doc_types:
            if high_accuracy and not cost_sensitive:
                model = "voyage-code-3"
                cost_per_1k_tokens = 0.00018  # 做预算前请核实当前定价
                dimensions = 1024
            else:
                model = "sentence-transformers/code-bert-base"
                cost_per_1k_tokens = 0.0  # 自托管
                dimensions = 768
        elif "scientific" in doc_types:
            if high_accuracy:
                model = "openai-text-embedding-3-large"
                cost_per_1k_tokens = 0.00013  # 做预算前请核实当前定价
                dimensions = 3072
            else:
                model = "sentence-transformers/scibert-nli"
                cost_per_1k_tokens = 0.0
                dimensions = 768
        else:
            if cost_sensitive or scale == Scale.SMALL:
                model = "sentence-transformers/all-MiniLM-L6-v2"
                cost_per_1k_tokens = 0.0
                dimensions = 384
            elif high_accuracy:
                model = "openai-text-embedding-3-large"
                cost_per_1k_tokens = 0.00013  # 做预算前请核实当前定价
                dimensions = 3072
            else:
                model = "sentence-transformers/all-mpnet-base-v2"
                cost_per_1k_tokens = 0.0
                dimensions = 768

        # 计算每月 embedding 成本
        total_tokens = req.document_count * (req.avg_document_size / 4)  # 约 4 字符折 1 个 token
        query_tokens = req.queries_per_day * 30 * 20  # 每月每查询约 20 个 token
        monthly_cost = (total_tokens + query_tokens) * cost_per_1k_tokens / 1000

        return ComponentRecommendation(
            name=model,
            type="embedding",
            config={
                "model": model,
                "dimensions": dimensions,
                "batch_size": 100 if scale == Scale.SMALL else 1000,
                "cache_embeddings": True
            },
            rationale=f"Selected for {doc_types} with accuracy priority {req.accuracy_priority}",
            pros=self._get_embedding_pros(model),
            cons=self._get_embedding_cons(model),
            cost_monthly=monthly_cost
        )

    def _recommend_vector_db(self, req: Requirements, scale: Scale) -> ComponentRecommendation:
        """推荐向量数据库。"""
        if scale == Scale.SMALL and req.cost_priority > 0.7:
            db = "chroma"
            cost = 0.0
            rationale = "Local/embedded database suitable for small scale and cost optimization"
        elif scale == Scale.SMALL and req.maintenance_complexity == "low":
            db = "pgvector"
            cost = 50.0  # PostgreSQL 托管费用
            rationale = "Leverage existing PostgreSQL infrastructure"
        elif scale == Scale.LARGE or req.latency_requirement == "real_time":
            db = "pinecone"
            vectors = req.document_count * 2  # 计入分块带来的向量数增加
            cost = max(70, vectors * 0.00005)  # $70 起步 + 每向量 $0.00005
            rationale = "Managed service with excellent performance for large scale"
        elif req.maintenance_complexity == "low":
            db = "weaviate_cloud"
            vectors = req.document_count * 2
            cost = max(25, vectors * 0.00003)
            rationale = "Managed Weaviate with good balance of features and cost"
        else:
            db = "qdrant"
            cost = 100.0  # 自托管基础设施的预估
            rationale = "High performance self-hosted option with good scaling"

        return ComponentRecommendation(
            name=db,
            type="vector_database",
            config=self._get_vector_db_config(db, req, scale),
            rationale=rationale,
            pros=self._get_vector_db_pros(db),
            cons=self._get_vector_db_cons(db),
            cost_monthly=cost
        )

    def _recommend_retrieval(self, req: Requirements, scale: Scale) -> ComponentRecommendation:
        """推荐检索策略。"""
        if req.accuracy_priority > 0.8:
            strategy = "hybrid"
            rationale = "Hybrid retrieval for maximum accuracy combining dense and sparse methods"
        elif "technical" in req.document_types or "code" in req.document_types:
            strategy = "hybrid"
            rationale = "Technical content benefits from both semantic and keyword matching"
        elif req.latency_requirement == "real_time":
            strategy = "dense"
            rationale = "Dense retrieval faster for real-time requirements"
        else:
            strategy = "dense"
            rationale = "Dense retrieval suitable for general text search"

        return ComponentRecommendation(
            name=strategy,
            type="retrieval",
            config={
                "strategy": strategy,
                "dense_weight": 0.7 if strategy == "hybrid" else 1.0,
                "sparse_weight": 0.3 if strategy == "hybrid" else 0.0,
                "top_k": 20 if req.accuracy_priority > 0.7 else 10,
                "similarity_threshold": 0.7
            },
            rationale=rationale,
            pros=self._get_retrieval_pros(strategy),
            cons=self._get_retrieval_cons(strategy),
            cost_monthly=0.0
        )

    def _recommend_reranking(self, req: Requirements, scale: Scale) -> Optional[ComponentRecommendation]:
        """在有收益时推荐重排序。"""
        if req.accuracy_priority < 0.6 or req.latency_requirement == "real_time":
            return None

        if req.cost_priority > 0.8:
            return None

        # 估算每月需重排序的查询量
        monthly_queries = req.queries_per_day * 30
        cost_per_query = 0.002  # 交叉编码器重排序的估算成本
        monthly_cost = monthly_queries * cost_per_query

        if monthly_cost > req.budget_monthly * 0.3:  # 不超过预算的 30%
            return None

        return ComponentRecommendation(
            name="cross_encoder_reranking",
            type="reranking",
            config={
                "model": "cross-encoder/ms-marco-MiniLM-L-12-v2",
                "rerank_top_k": 20,
                "return_top_k": 5,
                "batch_size": 16
            },
            rationale="Reranking improves precision for high-accuracy requirements",
            pros=["Higher precision", "Better ranking quality", "Handles complex queries"],
            cons=["Additional latency", "Higher cost", "More complexity"],
            cost_monthly=monthly_cost
        )

    def _recommend_evaluation(self, req: Requirements, scale: Scale) -> ComponentRecommendation:
        """推荐评估框架。"""
        return ComponentRecommendation(
            name="comprehensive_evaluation",
            type="evaluation",
            config={
                "metrics": ["precision@k", "recall@k", "mrr", "ndcg"],
                "k_values": [1, 3, 5, 10],
                "faithfulness_check": True,
                "relevance_scoring": True,
                "evaluation_frequency": "weekly" if scale == Scale.LARGE else "monthly",
                "sample_size": min(1000, req.queries_per_day * 7)
            },
            rationale="Comprehensive evaluation essential for production RAG systems",
            pros=["Quality monitoring", "Performance tracking", "Issue detection"],
            cons=["Additional overhead", "Requires ground truth data"],
            cost_monthly=20.0  # 评估工具与计算开销
        )

    def _generate_architecture_diagram(self, chunking: ComponentRecommendation,
                                     embedding: ComponentRecommendation,
                                     vector_db: ComponentRecommendation,
                                     retrieval: ComponentRecommendation,
                                     reranking: Optional[ComponentRecommendation],
                                     evaluation: ComponentRecommendation) -> str:
        """生成 Mermaid 架构图。"""

        diagram = """```mermaid
graph TB
    %% Document Processing Pipeline
    A[Document Corpus] --> B[Document Chunking]
    B --> C[Embedding Generation]
    C --> D[Vector Database Storage]

    %% Query Processing Pipeline
    E[User Query] --> F[Query Processing]
    F --> G[Vector Search]
    D --> G
    G --> H[Retrieved Chunks]
"""

        if reranking:
            diagram += "    H --> I[Reranking]\n    I --> J[Final Results]\n"
        else:
            diagram += "    H --> J[Final Results]\n"

        diagram += """    
    %% Evaluation Pipeline
    J --> K[Response Generation]
    K --> L[Evaluation Metrics]

    %% Component Details
    B -.-> B1[Strategy: """ + chunking.name + """]
    C -.-> C1[Model: """ + embedding.name + """]
    D -.-> D1[Database: """ + vector_db.name + """]
    G -.-> G1[Method: """ + retrieval.name + """]
"""

        if reranking:
            diagram += "    I -.-> I1[Model: " + reranking.name + "]\n"

        diagram += "    L -.-> L1[Framework: " + evaluation.name + "]\n```"

        return diagram

    def _generate_config_templates(self, *components) -> Dict[str, Any]:
        """为所有组件生成配置模板。"""
        configs = {}

        for component in components:
            if component:
                configs[component.type] = {
                    "component": component.name,
                    "config": component.config,
                    "rationale": component.rationale
                }

        # 追加部署配置
        configs["deployment"] = {
            "infrastructure": "cloud" if any("pinecone" in str(c.name) for c in components if c) else "hybrid",
            "scaling": {
                "auto_scaling": True,
                "min_replicas": 1,
                "max_replicas": 10
            },
            "monitoring": {
                "metrics": ["latency", "throughput", "accuracy"],
                "alerts": ["high_latency", "low_accuracy", "service_down"]
            }
        }

        return configs

    def _load_embedding_models(self) -> Dict[str, Dict[str, Any]]:
        """加载 embedding 模型规格。"""
        return {
            "openai-text-embedding-3-large": {
                "dimensions": 3072,
                "cost_per_1k_tokens": 0.00013,  # 请核实当前定价
                "quality": "high",
                "speed": "medium"
            },
            "voyage-3-large": {
                "dimensions": 1024,
                "cost_per_1k_tokens": 0.00018,  # 请核实当前定价
                "quality": "high",
                "speed": "medium"
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "dimensions": 768,
                "cost_per_1k_tokens": 0.0,
                "quality": "high",
                "speed": "medium"
            },
            "sentence-transformers/all-MiniLM-L6-v2": {
                "dimensions": 384,
                "cost_per_1k_tokens": 0.0,
                "quality": "medium",
                "speed": "fast"
            }
        }

    def _load_vector_databases(self) -> Dict[str, Dict[str, Any]]:
        """加载向量数据库规格。"""
        return {
            "pinecone": {"managed": True, "scaling": "excellent", "cost": "high"},
            "weaviate": {"managed": False, "scaling": "good", "cost": "medium"},
            "qdrant": {"managed": False, "scaling": "excellent", "cost": "low"},
            "chroma": {"managed": False, "scaling": "poor", "cost": "free"},
            "pgvector": {"managed": False, "scaling": "good", "cost": "medium"}
        }

    def _load_chunking_strategies(self) -> Dict[str, Dict[str, Any]]:
        """加载分块策略规格。"""
        return {
            "fixed_size": {"complexity": "low", "quality": "medium"},
            "sentence_based": {"complexity": "medium", "quality": "good"},
            "paragraph_based": {"complexity": "medium", "quality": "good"},
            "semantic_heading_aware": {"complexity": "high", "quality": "excellent"}
        }

    def _get_vector_db_config(self, db: str, req: Requirements, scale: Scale) -> Dict[str, Any]:
        """获取向量数据库配置。"""
        base_config = {
            "collection_name": "rag_documents",
            "distance_metric": "cosine",
            "index_type": "hnsw"
        }

        if db == "pinecone":
            base_config.update({
                "environment": "us-east1-gcp",
                "replicas": 1 if scale == Scale.SMALL else 2,
                "shards": 1 if scale != Scale.LARGE else 3
            })
        elif db == "qdrant":
            base_config.update({
                "memory_mapping": True,
                "quantization": scale == Scale.LARGE,
                "replication_factor": 1 if scale == Scale.SMALL else 2
            })

        return base_config

    def _get_chunking_pros(self, strategy: str) -> List[str]:
        """获取分块策略的优点。"""
        pros_map = {
            "semantic_heading_aware": ["Preserves document structure", "High semantic coherence", "Good for technical docs"],
            "paragraph_based": ["Respects natural boundaries", "Good balance", "Readable chunks"],
            "sentence_based": ["Natural language boundaries", "Consistent quality", "Good for general text"],
            "fixed_size": ["Predictable sizes", "Simple implementation", "Consistent processing"],
            "adaptive_chunking": ["Handles mixed content", "Optimizes per document", "Best quality"]
        }
        return pros_map.get(strategy, ["Good general purpose strategy"])

    def _get_chunking_cons(self, strategy: str) -> List[str]:
        """获取分块策略的缺点。"""
        cons_map = {
            "semantic_heading_aware": ["Complex implementation", "May create large chunks", "Document-dependent"],
            "paragraph_based": ["Variable sizes", "May break context", "Document-dependent"],
            "sentence_based": ["May create small chunks", "Sentence detection issues", "Variable sizes"],
            "fixed_size": ["Breaks semantic boundaries", "May split sentences", "Context loss"],
            "adaptive_chunking": ["High complexity", "Slower processing", "Harder to debug"]
        }
        return cons_map.get(strategy, ["May not fit all use cases"])

    def _get_embedding_pros(self, model: str) -> List[str]:
        """获取 embedding 模型的优点。"""
        if "openai" in model:
            return ["High quality", "Regular updates", "Good performance"]
        elif "all-mpnet" in model:
            return ["High quality", "Free to use", "Good balance"]
        elif "MiniLM" in model:
            return ["Fast processing", "Small size", "Good for real-time"]
        else:
            return ["Specialized for domain", "Good performance"]

    def _get_embedding_cons(self, model: str) -> List[str]:
        """获取 embedding 模型的缺点。"""
        if "openai" in model:
            return ["API costs", "Vendor lock-in", "Rate limits"]
        elif "sentence-transformers" in model:
            return ["Self-hosting required", "Model updates needed", "GPU beneficial"]
        else:
            return ["May require fine-tuning", "Domain-specific"]

    def _get_vector_db_pros(self, db: str) -> List[str]:
        """获取向量数据库的优点。"""
        pros_map = {
            "pinecone": ["Fully managed", "Excellent performance", "Auto-scaling"],
            "weaviate": ["Rich features", "GraphQL API", "Multi-modal"],
            "qdrant": ["High performance", "Rust-based", "Good scaling"],
            "chroma": ["Simple setup", "Free", "Good for development"],
            "pgvector": ["SQL integration", "ACID compliance", "Familiar"]
        }
        return pros_map.get(db, ["Good performance"])

    def _get_vector_db_cons(self, db: str) -> List[str]:
        """获取向量数据库的缺点。"""
        cons_map = {
            "pinecone": ["Expensive", "Vendor lock-in", "Limited customization"],
            "weaviate": ["Complex setup", "Learning curve", "Resource intensive"],
            "qdrant": ["Self-managed", "Smaller community", "Setup complexity"],
            "chroma": ["Limited scaling", "Not production-ready", "Basic features"],
            "pgvector": ["PostgreSQL knowledge needed", "Less specialized", "Manual optimization"]
        }
        return cons_map.get(db, ["Requires maintenance"])

    def _get_retrieval_pros(self, strategy: str) -> List[str]:
        """获取检索策略的优点。"""
        pros_map = {
            "dense": ["Semantic understanding", "Good for paraphrases", "Fast"],
            "sparse": ["Exact matching", "Interpretable", "Good for keywords"],
            "hybrid": ["Best of both", "High accuracy", "Robust"]
        }
        return pros_map.get(strategy, ["Good performance"])

    def _get_retrieval_cons(self, strategy: str) -> List[str]:
        """获取检索策略的缺点。"""
        cons_map = {
            "dense": ["May miss exact matches", "Embedding dependent", "Less interpretable"],
            "sparse": ["Vocabulary mismatch", "No semantic understanding", "Synonym issues"],
            "hybrid": ["More complex", "Tuning required", "Higher latency"]
        }
        return cons_map.get(strategy, ["May require tuning"])


def load_requirements(file_path: str) -> Requirements:
    """从 JSON 文件加载需求。"""
    with open(file_path, 'r') as f:
        data = json.load(f)

    return Requirements(**data)


def save_design(design: PipelineDesign, output_path: str):
    """将流水线设计保存为 JSON 文件。"""
    # 转为可 JSON 序列化的字典
    design_dict = {}

    for field_name in design.__dataclass_fields__:
        value = getattr(design, field_name)
        if isinstance(value, ComponentRecommendation):
            design_dict[field_name] = asdict(value)
        elif value is None:
            design_dict[field_name] = None
        else:
            design_dict[field_name] = value

    with open(output_path, 'w') as f:
        json.dump(design_dict, f, indent=2)


def print_design_summary(design: PipelineDesign):
    """打印人类可读的设计摘要。"""
    print("\n" + "="*60)
    print("RAG PIPELINE DESIGN SUMMARY")
    print("="*60)

    print(f"\n💰 Total Monthly Cost: ${design.total_cost:.2f}")

    print(f"\n🔧 Component Recommendations:")
    components = [design.chunking, design.embedding, design.vector_db,
                 design.retrieval, design.reranking, design.evaluation]

    for component in components:
        if component:
            print(f"\n  {component.type.upper()}: {component.name}")
            print(f"    Rationale: {component.rationale}")
            if component.cost_monthly > 0:
                print(f"    Monthly Cost: ${component.cost_monthly:.2f}")

    print(f"\n📊 Architecture Diagram:")
    print(design.architecture_diagram)


def main():
    """主函数，提供命令行界面。"""
    parser = argparse.ArgumentParser(description='根据需求设计 RAG 流水线')
    parser.add_argument('requirements', help='包含系统需求的 JSON 文件')
    parser.add_argument('--output', '-o', help='流水线设计的输出文件（JSON）')
    parser.add_argument('--verbose', '-v', action='store_true', help='输出详细信息')

    args = parser.parse_args()

    try:
        # 加载需求
        print("Loading requirements...")
        requirements = load_requirements(args.requirements)

        # 设计流水线
        designer = RAGPipelineDesigner()
        design = designer.design_pipeline(requirements)

        # 保存设计
        if args.output:
            save_design(design, args.output)
            print(f"Pipeline design saved to {args.output}")

        # 打印摘要
        print_design_summary(design)

        if args.verbose:
            print(f"\n📋 Configuration Templates:")
            for component_type, config in design.config_templates.items():
                print(f"\n  {component_type.upper()}:")
                print(f"    {json.dumps(config, indent=4)}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
