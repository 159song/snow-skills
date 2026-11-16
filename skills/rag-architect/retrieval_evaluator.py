#!/usr/bin/env python3
"""
检索评估器 - 使用标准信息检索指标评估检索质量。

本脚本使用标准信息检索指标（包括 precision@k、recall@k、MRR 和 NDCG）
评估检索系统性能，并以内置的 TF-IDF 实现作为基线检索系统。

计算的指标：
- Precision@K：检索到的文档中相关文档的占比
- Recall@K：相关文档中被检索到的占比
- 平均倒数排名（MRR）：首个相关结果倒数排名的平均值
- 归一化折损累计增益（NDCG）：带位置折损的排序质量

无外部依赖 - 仅使用 Python 标准库。
"""

import argparse
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any, Optional


class Document:
    """表示语料中的一篇文档。"""

    def __init__(self, doc_id: str, title: str, content: str, path: str = ""):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.path = path
        self.tokens = self._tokenize(content)
        self.token_count = len(self.tokens)

    def _tokenize(self, text: str) -> List[str]:
        """简单的分词 - 按空白符和标点切分。"""
        # 转小写后抽取单词
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def __str__(self):
        return f"Document({self.doc_id}, '{self.title[:50]}...', {self.token_count} tokens)"


class TFIDFRetriever:
    """基于 TF-IDF 的检索系统 - 无外部依赖。"""

    def __init__(self, documents: List[Document]):
        self.documents = {doc.doc_id: doc for doc in documents}
        self.doc_ids = list(self.documents.keys())
        self.vocabulary = set()
        self.tf_scores = {}  # doc_id -> {term: tf_score}
        self.df_scores = {}  # term -> document_frequency
        self.idf_scores = {}  # term -> idf_score
        self._build_index()

    def _build_index(self):
        """基于文档构建 TF-IDF 索引。"""
        print(f"Building TF-IDF index for {len(self.documents)} documents...")

        # 计算词频并构建词表
        for doc_id, doc in self.documents.items():
            term_counts = Counter(doc.tokens)
            doc_length = len(doc.tokens)

            # 计算 TF 得分（term_count / doc_length）
            tf_scores = {}
            for term, count in term_counts.items():
                tf_scores[term] = count / doc_length if doc_length > 0 else 0
                self.vocabulary.add(term)

            self.tf_scores[doc_id] = tf_scores

        # 计算文档频率
        for term in self.vocabulary:
            df = sum(1 for doc in self.documents.values() if term in doc.tokens)
            self.df_scores[term] = df

        # 计算 IDF 得分：log(N / df)
        num_docs = len(self.documents)
        for term, df in self.df_scores.items():
            self.idf_scores[term] = math.log(num_docs / df) if df > 0 else 0

    def search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """使用 TF-IDF 相似度检索与查询匹配的文档。"""
        query_tokens = re.findall(r'\b[a-zA-Z0-9]+\b', query.lower())
        if not query_tokens:
            return []

        # 计算查询的 TF 得分
        query_tf = Counter(query_tokens)
        query_length = len(query_tokens)

        # 为每篇文档计算 TF-IDF 相似度
        scores = {}
        for doc_id in self.doc_ids:
            score = self._calculate_similarity(query_tf, query_length, doc_id)
            if score > 0:
                scores[doc_id] = score

        # 按得分排序并返回前 k 个
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:k]

    def _calculate_similarity(self, query_tf: Counter, query_length: int, doc_id: str) -> float:
        """用 TF-IDF 计算查询与文档之间的余弦相似度。"""
        doc_tf = self.tf_scores[doc_id]

        # 计算 TF-IDF 向量
        query_vector = []
        doc_vector = []

        # 只考虑同时在查询和文档中出现的词
        common_terms = set(query_tf.keys()) & set(doc_tf.keys())

        if not common_terms:
            return 0.0

        for term in common_terms:
            # 查询 TF-IDF
            q_tf = query_tf[term] / query_length
            q_tfidf = q_tf * self.idf_scores.get(term, 0)
            query_vector.append(q_tfidf)

            # 文档 TF-IDF
            d_tfidf = doc_tf[term] * self.idf_scores.get(term, 0)
            doc_vector.append(d_tfidf)

        # 余弦相似度
        dot_product = sum(q * d for q, d in zip(query_vector, doc_vector))
        query_norm = math.sqrt(sum(q * q for q in query_vector))
        doc_norm = math.sqrt(sum(d * d for d in doc_vector))

        if query_norm == 0 or doc_norm == 0:
            return 0.0

        return dot_product / (query_norm * doc_norm)


class RetrievalEvaluator:
    """使用标准信息检索指标评估检索系统性能。"""

    def __init__(self):
        self.metrics = {}

    def evaluate(self, queries: List[Dict[str, Any]], ground_truth: Dict[str, List[str]],
                 retriever: TFIDFRetriever, k_values: List[int] = None) -> Dict[str, Any]:
        """评估检索性能。"""
        k_values = k_values or [1, 3, 5, 10]

        print(f"Evaluating retrieval performance for {len(queries)} queries...")

        query_results = []
        all_precision_at_k = {k: [] for k in k_values}
        all_recall_at_k = {k: [] for k in k_values}
        all_ndcg_at_k = {k: [] for k in k_values}
        reciprocal_ranks = []

        for query_data in queries:
            query_id = query_data['id']
            query_text = query_data['query']

            # 获取该查询的参考答案
            relevant_docs = set(ground_truth.get(query_id, []))

            if not relevant_docs:
                print(f"Warning: No ground truth found for query {query_id}")
                continue

            # 检索文档
            max_k = max(k_values)
            results = retriever.search(query_text, max_k)
            retrieved_doc_ids = [doc_id for doc_id, _ in results]

            # 计算该查询的各项指标
            query_metrics = {}

            # Precision@K 与 Recall@K
            for k in k_values:
                retrieved_at_k = set(retrieved_doc_ids[:k])
                relevant_retrieved = retrieved_at_k & relevant_docs

                precision = len(relevant_retrieved) / len(retrieved_at_k) if retrieved_at_k else 0
                recall = len(relevant_retrieved) / len(relevant_docs) if relevant_docs else 0

                query_metrics[f'precision@{k}'] = precision
                query_metrics[f'recall@{k}'] = recall

                all_precision_at_k[k].append(precision)
                all_recall_at_k[k].append(recall)

            # 平均倒数排名（MRR）
            reciprocal_rank = self._calculate_reciprocal_rank(retrieved_doc_ids, relevant_docs)
            query_metrics['reciprocal_rank'] = reciprocal_rank
            reciprocal_ranks.append(reciprocal_rank)

            # NDCG@K
            for k in k_values:
                ndcg = self._calculate_ndcg(retrieved_doc_ids[:k], relevant_docs)
                query_metrics[f'ndcg@{k}'] = ndcg
                all_ndcg_at_k[k].append(ndcg)

            # 保存查询级结果
            query_results.append({
                'query_id': query_id,
                'query': query_text,
                'relevant_count': len(relevant_docs),
                'retrieved_count': len(retrieved_doc_ids),
                'metrics': query_metrics,
                'retrieved_docs': results[:5],  # 取前 5 个用于分析
                'relevant_docs': list(relevant_docs)
            })

        # 计算汇总指标
        aggregate_metrics = {}

        for k in k_values:
            aggregate_metrics[f'mean_precision@{k}'] = self._safe_mean(all_precision_at_k[k])
            aggregate_metrics[f'mean_recall@{k}'] = self._safe_mean(all_recall_at_k[k])
            aggregate_metrics[f'mean_ndcg@{k}'] = self._safe_mean(all_ndcg_at_k[k])

        aggregate_metrics['mean_reciprocal_rank'] = self._safe_mean(reciprocal_ranks)

        # 失败分析
        failure_analysis = self._analyze_failures(query_results)

        return {
            'aggregate_metrics': aggregate_metrics,
            'query_results': query_results,
            'failure_analysis': failure_analysis,
            'evaluation_summary': self._generate_summary(aggregate_metrics, len(queries))
        }

    def _calculate_reciprocal_rank(self, retrieved_docs: List[str], relevant_docs: Set[str]) -> float:
        """计算倒数排名 - 首个相关文档排名的倒数。"""
        for i, doc_id in enumerate(retrieved_docs):
            if doc_id in relevant_docs:
                return 1.0 / (i + 1)
        return 0.0

    def _calculate_ndcg(self, retrieved_docs: List[str], relevant_docs: Set[str]) -> float:
        """计算归一化折损累计增益（NDCG）。"""
        if not retrieved_docs:
            return 0.0

        # DCG 计算
        dcg = 0.0
        for i, doc_id in enumerate(retrieved_docs):
            relevance = 1 if doc_id in relevant_docs else 0
            dcg += relevance / math.log2(i + 2)  # +2 是因为 log2(1) = 0

        # IDCG 计算（理想 DCG）
        ideal_relevances = [1] * min(len(relevant_docs), len(retrieved_docs))
        idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_relevances))

        return dcg / idcg if idcg > 0 else 0.0

    def _safe_mean(self, values: List[float]) -> float:
        """计算均值，并处理空列表。"""
        return sum(values) / len(values) if values else 0.0

    def _analyze_failures(self, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析常见的失败模式。"""
        total_queries = len(query_results)

        # 找出表现不佳的查询
        poor_precision_queries = []
        poor_recall_queries = []
        zero_results_queries = []

        for result in query_results:
            metrics = result['metrics']

            if metrics.get('precision@5', 0) < 0.2:
                poor_precision_queries.append(result)

            if metrics.get('recall@5', 0) < 0.3:
                poor_recall_queries.append(result)

            if result['retrieved_count'] == 0:
                zero_results_queries.append(result)

        # 分析查询特征
        query_length_analysis = self._analyze_query_lengths(query_results)

        return {
            'poor_precision_count': len(poor_precision_queries),
            'poor_recall_count': len(poor_recall_queries),
            'zero_results_count': len(zero_results_queries),
            'poor_precision_examples': poor_precision_queries[:3],
            'poor_recall_examples': poor_recall_queries[:3],
            'query_length_analysis': query_length_analysis,
            'common_failure_patterns': self._identify_failure_patterns(query_results)
        }

    def _analyze_query_lengths(self, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析查询长度与性能之间的关系。"""
        short_queries = []  # <= 3 个词
        medium_queries = []  # 4-7 个词
        long_queries = []  # >= 8 个词

        for result in query_results:
            query_length = len(result['query'].split())
            precision = result['metrics'].get('precision@5', 0)

            if query_length <= 3:
                short_queries.append(precision)
            elif query_length <= 7:
                medium_queries.append(precision)
            else:
                long_queries.append(precision)

        return {
            'short_queries': {
                'count': len(short_queries),
                'avg_precision@5': self._safe_mean(short_queries)
            },
            'medium_queries': {
                'count': len(medium_queries),
                'avg_precision@5': self._safe_mean(medium_queries)
            },
            'long_queries': {
                'count': len(long_queries),
                'avg_precision@5': self._safe_mean(long_queries)
            }
        }

    def _identify_failure_patterns(self, query_results: List[Dict[str, Any]]) -> List[str]:
        """识别失败查询中的共性模式。"""
        patterns = []

        # 检查词汇失配
        vocab_mismatch_count = 0
        for result in query_results:
            if result['metrics'].get('precision@1', 0) == 0 and result['retrieved_count'] > 0:
                vocab_mismatch_count += 1

        if vocab_mismatch_count > len(query_results) * 0.2:
            patterns.append(f"Vocabulary mismatch: {vocab_mismatch_count} queries may have vocabulary mismatch issues")

        # 检查查询过于具体的问题
        zero_results = sum(1 for r in query_results if r['retrieved_count'] == 0)
        if zero_results > len(query_results) * 0.1:
            patterns.append(f"Query specificity: {zero_results} queries returned no results (may be too specific)")

        # 检查召回问题
        low_recall = sum(1 for r in query_results if r['metrics'].get('recall@10', 0) < 0.5)
        if low_recall > len(query_results) * 0.3:
            patterns.append(f"Low recall: {low_recall} queries have recall@10 < 0.5 (missing relevant documents)")

        return patterns

    def _generate_summary(self, metrics: Dict[str, float], num_queries: int) -> str:
        """生成人类可读的评估摘要。"""
        summary = f"Evaluation Summary ({num_queries} queries):\n"
        summary += f"{'='*50}\n"

        # 关键指标
        p1 = metrics.get('mean_precision@1', 0)
        p5 = metrics.get('mean_precision@5', 0)
        r5 = metrics.get('mean_recall@5', 0)
        mrr = metrics.get('mean_reciprocal_rank', 0)
        ndcg5 = metrics.get('mean_ndcg@5', 0)

        summary += f"Precision@1:  {p1:.3f} ({p1*100:.1f}%)\n"
        summary += f"Precision@5:  {p5:.3f} ({p5*100:.1f}%)\n"
        summary += f"Recall@5:     {r5:.3f} ({r5*100:.1f}%)\n"
        summary += f"MRR:          {mrr:.3f}\n"
        summary += f"NDCG@5:       {ndcg5:.3f}\n"

        # 性能评定
        summary += f"\nPerformance Assessment:\n"
        if p1 >= 0.7:
            summary += "✓ Excellent precision - most queries return relevant results first\n"
        elif p1 >= 0.5:
            summary += "○ Good precision - many queries return relevant results first\n"
        else:
            summary += "✗ Poor precision - few queries return relevant results first\n"

        if r5 >= 0.8:
            summary += "✓ Excellent recall - finding most relevant documents\n"
        elif r5 >= 0.6:
            summary += "○ Good recall - finding many relevant documents\n"
        else:
            summary += "✗ Poor recall - missing many relevant documents\n"

        return summary


def load_queries(file_path: str) -> List[Dict[str, Any]]:
    """从 JSON 文件加载查询。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 兼容不同的 JSON 格式
    if isinstance(data, list):
        return data
    elif 'queries' in data:
        return data['queries']
    else:
        raise ValueError("Invalid query file format. Expected list of queries or {'queries': [...]}.")


def load_ground_truth(file_path: str) -> Dict[str, List[str]]:
    """加载参考答案的相关性判定。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 兼容不同的 JSON 格式
    if isinstance(data, dict):
        # 将所有不是列表的值转为列表
        return {k: v if isinstance(v, list) else [v] for k, v in data.items()}
    else:
        raise ValueError("Invalid ground truth format. Expected dict mapping query_id -> relevant_doc_ids.")


def load_corpus(directory: str, extensions: List[str] = None) -> List[Document]:
    """从目录加载文档语料。"""
    extensions = extensions or ['.txt', '.md', '.markdown']
    documents = []

    corpus_path = Path(directory)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus directory not found: {directory}")

    for file_path in corpus_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if content.strip():
                    # 用文件名（不含扩展名）作为 doc_id
                    doc_id = file_path.stem
                    title = file_path.name

                    doc = Document(doc_id, title, content, str(file_path))
                    documents.append(doc)

            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

    if not documents:
        raise ValueError(f"No valid documents found in {directory}")

    print(f"Loaded {len(documents)} documents from corpus")
    return documents


def generate_recommendations(evaluation_results: Dict[str, Any]) -> List[str]:
    """根据评估结果生成改进建议。"""
    recommendations = []

    metrics = evaluation_results['aggregate_metrics']
    failure_analysis = evaluation_results['failure_analysis']

    # 基于精确率的建议
    p1 = metrics.get('mean_precision@1', 0)
    p5 = metrics.get('mean_precision@5', 0)

    if p1 < 0.3:
        recommendations.append("LOW PRECISION: Consider implementing query expansion or reranking to improve result quality.")

    if p5 < 0.4:
        recommendations.append("RANKING ISSUES: Current ranking may not prioritize relevant documents. Consider BM25 or learning-to-rank models.")

    # 基于召回的建议
    r5 = metrics.get('mean_recall@5', 0)
    r10 = metrics.get('mean_recall@10', 0)

    if r5 < 0.5:
        recommendations.append("LOW RECALL: Consider query expansion techniques (synonyms, related terms) to find more relevant documents.")

    if r10 - r5 > 0.2:
        recommendations.append("RANKING DEPTH: Many relevant documents found in positions 6-10. Consider increasing default result count.")

    # 基于 MRR 的建议
    mrr = metrics.get('mean_reciprocal_rank', 0)
    if mrr < 0.4:
        recommendations.append("POOR RANKING: First relevant result appears late in rankings. Implement result reranking.")

    # 基于失败模式的建议
    zero_results = failure_analysis.get('zero_results_count', 0)
    total_queries = len(evaluation_results['query_results'])

    if zero_results > total_queries * 0.1:
        recommendations.append("COVERAGE ISSUES: Many queries return no results. Check for vocabulary mismatch or missing content.")

    # 查询长度分析
    query_analysis = failure_analysis.get('query_length_analysis', {})
    short_perf = query_analysis.get('short_queries', {}).get('avg_precision@5', 0)
    long_perf = query_analysis.get('long_queries', {}).get('avg_precision@5', 0)

    if short_perf < 0.3:
        recommendations.append("SHORT QUERY ISSUES: Brief queries perform poorly. Consider query completion or suggestion features.")

    if long_perf > short_perf + 0.2:
        recommendations.append("QUERY PROCESSING: Longer queries perform better. Consider query parsing to extract key terms.")

    # 一般性建议
    if not recommendations:
        recommendations.append("GOOD PERFORMANCE: System performs well overall. Consider A/B testing incremental improvements.")

    return recommendations


def main():
    """主函数，提供命令行界面。"""
    parser = argparse.ArgumentParser(description='评估检索系统性能')
    parser.add_argument('queries', help='包含查询的 JSON 文件')
    parser.add_argument('corpus', help='包含文档语料的目录')
    parser.add_argument('ground_truth', help='包含参考答案相关性判定的 JSON 文件')
    parser.add_argument('--output', '-o', help='结果输出文件（JSON 格式）')
    parser.add_argument('--k-values', nargs='+', type=int, default=[1, 3, 5, 10],
                       help='用于 precision@k、recall@k、NDCG@k 评估的 K 值')
    parser.add_argument('--extensions', nargs='+', default=['.txt', '.md', '.markdown'],
                       help='从语料中纳入的文件扩展名')
    parser.add_argument('--verbose', '-v', action='store_true', help='输出详细信息')

    args = parser.parse_args()

    try:
        # 加载数据
        print("Loading evaluation data...")
        queries = load_queries(args.queries)
        ground_truth = load_ground_truth(args.ground_truth)
        documents = load_corpus(args.corpus, args.extensions)

        print(f"Loaded {len(queries)} queries, {len(documents)} documents, ground truth for {len(ground_truth)} queries")

        # 构建检索系统
        retriever = TFIDFRetriever(documents)

        # 运行评估
        evaluator = RetrievalEvaluator()
        results = evaluator.evaluate(queries, ground_truth, retriever, args.k_values)

        # 生成改进建议
        recommendations = generate_recommendations(results)
        results['recommendations'] = recommendations

        # 保存结果
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")

        # 打印摘要
        print("\n" + results['evaluation_summary'])

        print("\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

        if args.verbose:
            print(f"\nDetailed Metrics:")
            for metric, value in results['aggregate_metrics'].items():
                print(f"  {metric}: {value:.4f}")

            print(f"\nFailure Analysis:")
            fa = results['failure_analysis']
            print(f"  Poor precision queries: {fa['poor_precision_count']}")
            print(f"  Poor recall queries: {fa['poor_recall_count']}")
            print(f"  Zero result queries: {fa['zero_results_count']}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
