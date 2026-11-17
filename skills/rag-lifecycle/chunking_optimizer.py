#!/usr/bin/env python3
"""
分块优化器 - 分析文档语料并推荐最优分块策略。

本脚本分析一批 text/markdown 文档集合，评估不同的分块策略，
以便针对给定语料推荐最合适的方案。

测试的策略：
- 固定大小分块（按字符和按 token），支持重叠
- 基于句子的分块
- 基于段落的分块
- 语义分块（标题感知）

度量的指标：
- 块大小分布（均值、标准差、最小值、最大值）
- 语义连贯性（主题连续性启发式）
- 边界质量（句子断点分析）

无外部依赖 - 仅使用 Python 标准库。
"""

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from math import log, sqrt
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class DocumentCorpus:
    """负责文档语料的加载与预处理。"""

    def __init__(self, directory: str, extensions: List[str] = None):
        self.directory = Path(directory)
        self.extensions = extensions or ['.txt', '.md', '.markdown']
        self.documents = []
        self._load_documents()

    def _load_documents(self):
        """从目录加载全部文本文档。"""
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        for file_path in self.directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if content.strip():  # 仅收录非空文件
                        self.documents.append({
                            'path': str(file_path),
                            'content': content,
                            'size': len(content)
                        })
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")

        if not self.documents:
            raise ValueError(f"No valid documents found in {self.directory}")

        print(f"Loaded {len(self.documents)} documents totaling {sum(d['size'] for d in self.documents):,} characters")


class ChunkingStrategy:
    """分块策略的基类。"""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        """将文本切分为块。返回块字典列表。"""
        raise NotImplementedError


class FixedSizeChunker(ChunkingStrategy):
    """固定大小分块，支持可选重叠。"""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100, unit: str = 'char'):
        config = {'chunk_size': chunk_size, 'overlap': overlap, 'unit': unit}
        super().__init__(f'fixed_size_{unit}', config)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.unit = unit

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        chunks = []
        if self.unit == 'char':
            return self._chunk_by_chars(text)
        else:  # 以词为单位的近似
            words = text.split()
            return self._chunk_by_words(words)

    def _chunk_by_chars(self, text: str) -> List[Dict[str, Any]]:
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]

            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'start': start,
                'end': end,
                'size': len(chunk_text)
            })

            start = max(start + self.chunk_size - self.overlap, start + 1)
            chunk_id += 1

            if start >= len(text):
                break

        return chunks

    def _chunk_by_words(self, words: List[str]) -> List[Dict[str, Any]]:
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)

            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'start': start,
                'end': end,
                'size': len(chunk_text)
            })

            start = max(start + self.chunk_size - self.overlap, start + 1)
            chunk_id += 1

            if start >= len(words):
                break

        return chunks


class SentenceChunker(ChunkingStrategy):
    """基于句子的分块。"""

    def __init__(self, max_size: int = 1000):
        config = {'max_size': max_size}
        super().__init__('sentence_based', config)
        self.max_size = max_size
        # 简单的句子边界检测
        self.sentence_endings = re.compile(r'[.!?]+\s+')

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        # 先切分为句子
        sentences = self._split_sentences(text)
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_id = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            if current_size + sentence_size > self.max_size and current_chunk:
                # 保存当前块
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start': 0,  # 近似值
                    'end': len(chunk_text),
                    'size': len(chunk_text),
                    'sentence_count': len(current_chunk)
                })
                chunk_id += 1
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size

        # 添加最后一个块
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'start': 0,
                'end': len(chunk_text),
                'size': len(chunk_text),
                'sentence_count': len(current_chunk)
            })

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """简单的句子切分。"""
        sentences = []
        parts = self.sentence_endings.split(text)

        for i, part in enumerate(parts[:-1]):
            # 把句尾标点补回去
            ending_match = list(self.sentence_endings.finditer(text))
            if i < len(ending_match):
                sentence = part + ending_match[i].group().strip()
            else:
                sentence = part

            if sentence.strip():
                sentences.append(sentence.strip())

        # 若存在最后一部分则补上
        if parts[-1].strip():
            sentences.append(parts[-1].strip())

        return [s for s in sentences if len(s.strip()) > 0]


class ParagraphChunker(ChunkingStrategy):
    """基于段落的分块。"""

    def __init__(self, max_size: int = 2000, min_paragraph_size: int = 50):
        config = {'max_size': max_size, 'min_paragraph_size': min_paragraph_size}
        super().__init__('paragraph_based', config)
        self.max_size = max_size
        self.min_paragraph_size = min_paragraph_size

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        # 按双换行符（段落边界）切分
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_id = 0

        for paragraph in paragraphs:
            paragraph_size = len(paragraph)

            # 跳过过短的段落，除非它是唯一内容
            if paragraph_size < self.min_paragraph_size and len(paragraphs) > 1:
                continue

            if current_size + paragraph_size > self.max_size and current_chunk:
                # 保存当前块
                chunk_text = '\n\n'.join(current_chunk)
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start': 0,
                    'end': len(chunk_text),
                    'size': len(chunk_text),
                    'paragraph_count': len(current_chunk)
                })
                chunk_id += 1
                current_chunk = [paragraph]
                current_size = paragraph_size
            else:
                current_chunk.append(paragraph)
                current_size += paragraph_size + 2  # 计入换行符

        # 添加最后一个块
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'start': 0,
                'end': len(chunk_text),
                'size': len(chunk_text),
                'paragraph_count': len(current_chunk)
            })

        return chunks


class SemanticChunker(ChunkingStrategy):
    """标题感知的语义分块。"""

    def __init__(self, max_size: int = 1500, heading_weight: float = 2.0):
        config = {'max_size': max_size, 'heading_weight': heading_weight}
        super().__init__('semantic_heading', config)
        self.max_size = max_size
        self.heading_weight = heading_weight

        # Markdown 与纯文本的标题匹配模式
        self.heading_patterns = [
            re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE),  # Markdown 标题
            re.compile(r'^(.+)\n[=-]+\s*$', re.MULTILINE),  # 下划线式标题
            re.compile(r'^\d+\.\s*(.+)$', re.MULTILINE),   # 编号章节
        ]

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        sections = self._identify_sections(text)
        chunks = []
        chunk_id = 0

        for section in sections:
            section_chunks = self._chunk_section(section, chunk_id)
            chunks.extend(section_chunks)
            chunk_id += len(section_chunks)

        return chunks

    def _identify_sections(self, text: str) -> List[Dict[str, Any]]:
        """依据标题识别章节。"""
        sections = []
        lines = text.split('\n')
        current_section = {'heading': 'Introduction', 'content': '', 'level': 0}

        for line in lines:
            is_heading = False
            heading_level = 0
            heading_text = line.strip()

            # 检查 Markdown 标题
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:
                    heading_text = line.strip('#').strip()
                    heading_level = level
                    is_heading = True

            # 检查下划线式标题
            elif len(sections) > 0 and line.strip() and all(c in '=-' for c in line.strip()):
                # 上一行可能是标题
                if current_section['content']:
                    content_lines = current_section['content'].strip().split('\n')
                    if content_lines:
                        potential_heading = content_lines[-1].strip()
                        if len(potential_heading) > 0 and len(potential_heading) < 100:
                            # 视为标题
                            current_section['content'] = '\n'.join(content_lines[:-1])
                            sections.append(current_section)
                            current_section = {
                                'heading': potential_heading,
                                'content': '',
                                'level': 1 if '=' in line else 2
                            }
                            continue

            if is_heading:
                if current_section['content'].strip():
                    sections.append(current_section)
                current_section = {
                    'heading': heading_text,
                    'content': '',
                    'level': heading_level
                }
            else:
                current_section['content'] += line + '\n'

        # 添加最后一个章节
        if current_section['content'].strip():
            sections.append(current_section)

        return sections

    def _chunk_section(self, section: Dict[str, Any], start_id: int) -> List[Dict[str, Any]]:
        """对单个章节进行分块。"""
        content = section['content'].strip()
        if not content:
            return []

        heading = section['heading']
        chunks = []

        # 章节足够小则整体作为一个块返回
        if len(content) <= self.max_size:
            chunks.append({
                'id': start_id,
                'text': f"{heading}\n\n{content}" if heading else content,
                'start': 0,
                'end': len(content),
                'size': len(content),
                'heading': heading,
                'level': section['level']
            })
            return chunks

        # 大章节按段落拆分
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        current_chunk = []
        current_size = len(heading) + 2 if heading else 0  # 计入标题长度
        chunk_id = start_id

        for paragraph in paragraphs:
            paragraph_size = len(paragraph)

            if current_size + paragraph_size > self.max_size and current_chunk:
                # 保存当前块
                chunk_text = '\n\n'.join(current_chunk)
                if heading and chunk_id == start_id:
                    chunk_text = f"{heading}\n\n{chunk_text}"

                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start': 0,
                    'end': len(chunk_text),
                    'size': len(chunk_text),
                    'heading': heading if chunk_id == start_id else f"{heading} (continued)",
                    'level': section['level']
                })
                chunk_id += 1
                current_chunk = [paragraph]
                current_size = paragraph_size
            else:
                current_chunk.append(paragraph)
                current_size += paragraph_size + 2  # 计入换行符

        # 添加最后一个块
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            if heading and chunk_id == start_id:
                chunk_text = f"{heading}\n\n{chunk_text}"
            elif heading:
                chunk_text = f"{heading} (continued)\n\n{chunk_text}"

            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'start': 0,
                'end': len(chunk_text),
                'size': len(chunk_text),
                'heading': heading if chunk_id == start_id else f"{heading} (continued)",
                'level': section['level']
            })

        return chunks


class ChunkAnalyzer:
    """分析分块结果并提供质量指标。"""

    def __init__(self):
        self.vocabulary = set()
        self.word_freq = Counter()

    def analyze_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """对块做全面分析。"""
        if not chunks:
            return {'error': 'No chunks to analyze'}

        sizes = [chunk['size'] for chunk in chunks]

        # 基础大小统计
        size_stats = {
            'count': len(chunks),
            'mean': statistics.mean(sizes),
            'median': statistics.median(sizes),
            'std': statistics.stdev(sizes) if len(sizes) > 1 else 0,
            'min': min(sizes),
            'max': max(sizes),
            'total': sum(sizes)
        }

        # 边界质量分析
        boundary_quality = self._analyze_boundary_quality(chunks)

        # 语义连贯性（简单启发式）
        coherence_score = self._calculate_semantic_coherence(chunks)

        # 词汇分布
        vocab_stats = self._analyze_vocabulary(chunks)

        return {
            'size_statistics': size_stats,
            'boundary_quality': boundary_quality,
            'semantic_coherence': coherence_score,
            'vocabulary_statistics': vocab_stats
        }

    def _analyze_boundary_quality(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析块对自然边界的尊重程度。"""
        sentence_breaks = 0
        word_breaks = 0
        total_chunks = len(chunks)

        sentence_endings = re.compile(r'[.!?]\s*$')

        for chunk in chunks:
            text = chunk['text'].strip()
            if not text:
                continue

            # 检查块是否以句子边界结尾
            if sentence_endings.search(text):
                sentence_breaks += 1

            # 检查块是否以词边界结尾
            if text[-1].isalnum() or text[-1] in '.!?':
                word_breaks += 1

        return {
            'sentence_boundary_ratio': sentence_breaks / total_chunks if total_chunks > 0 else 0,
            'word_boundary_ratio': word_breaks / total_chunks if total_chunks > 0 else 0,
            'clean_breaks': sentence_breaks,
            'total_chunks': total_chunks
        }

    def _calculate_semantic_coherence(self, chunks: List[Dict[str, Any]]) -> float:
        """基于词汇重合度的简单语义连贯性启发式。"""
        if len(chunks) < 2:
            return 1.0

        coherence_scores = []

        for i in range(len(chunks) - 1):
            chunk1_words = set(re.findall(r'\b\w+\b', chunks[i]['text'].lower()))
            chunk2_words = set(re.findall(r'\b\w+\b', chunks[i+1]['text'].lower()))

            if not chunk1_words or not chunk2_words:
                continue

            # 用 Jaccard 相似度作为连贯性度量
            intersection = len(chunk1_words & chunk2_words)
            union = len(chunk1_words | chunk2_words)

            if union > 0:
                coherence_scores.append(intersection / union)

        return statistics.mean(coherence_scores) if coherence_scores else 0.0

    def _analyze_vocabulary(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析各块之间的词汇分布。"""
        all_words = []
        chunk_vocab_sizes = []

        for chunk in chunks:
            words = re.findall(r'\b\w+\b', chunk['text'].lower())
            all_words.extend(words)
            chunk_vocab_sizes.append(len(set(words)))

        total_vocab = len(set(all_words))
        word_freq = Counter(all_words)

        return {
            'total_vocabulary': total_vocab,
            'avg_chunk_vocabulary': statistics.mean(chunk_vocab_sizes) if chunk_vocab_sizes else 0,
            'vocabulary_diversity': total_vocab / len(all_words) if all_words else 0,
            'most_common_words': word_freq.most_common(10)
        }


class ChunkingOptimizer:
    """测试不同分块策略并给出建议的主优化器。"""

    def __init__(self):
        self.analyzer = ChunkAnalyzer()

    def optimize(self, corpus: DocumentCorpus, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """测试全部分块策略并推荐最佳策略。"""
        config = config or {}

        strategies = self._create_strategies(config)
        results = {}

        print(f"Testing {len(strategies)} chunking strategies...")

        for strategy in strategies:
            print(f"  Testing {strategy.name}...")
            strategy_results = self._test_strategy(corpus, strategy)
            results[strategy.name] = strategy_results

        # 推荐最佳策略
        recommendation = self._recommend_strategy(results)

        return {
            'corpus_info': {
                'document_count': len(corpus.documents),
                'total_size': sum(d['size'] for d in corpus.documents),
                'avg_document_size': statistics.mean([d['size'] for d in corpus.documents])
            },
            'strategy_results': results,
            'recommendation': recommendation,
            'sample_chunks': self._generate_sample_chunks(corpus, recommendation['best_strategy'])
        }

    def _create_strategies(self, config: Dict[str, Any]) -> List[ChunkingStrategy]:
        """创建所有待测试的分块策略。"""
        strategies = []

        # 固定大小策略
        for size in config.get('fixed_sizes', [512, 1000, 1500]):
            for overlap in config.get('overlaps', [50, 100]):
                strategies.append(FixedSizeChunker(size, overlap, 'char'))

        # 基于句子的策略
        for max_size in config.get('sentence_max_sizes', [800, 1200]):
            strategies.append(SentenceChunker(max_size))

        # 基于段落的策略
        for max_size in config.get('paragraph_max_sizes', [1500, 2000]):
            strategies.append(ParagraphChunker(max_size))

        # 语义策略
        for max_size in config.get('semantic_max_sizes', [1200, 1800]):
            strategies.append(SemanticChunker(max_size))

        return strategies

    def _test_strategy(self, corpus: DocumentCorpus, strategy: ChunkingStrategy) -> Dict[str, Any]:
        """测试单个分块策略。"""
        all_chunks = []
        document_results = []

        for doc in corpus.documents:
            try:
                chunks = strategy.chunk(doc['content'])
                all_chunks.extend(chunks)

                doc_analysis = self.analyzer.analyze_chunks(chunks)
                document_results.append({
                    'path': doc['path'],
                    'chunk_count': len(chunks),
                    'analysis': doc_analysis
                })
            except Exception as e:
                print(f"    Error processing {doc['path']}: {e}")
                continue

        # 整体分析
        overall_analysis = self.analyzer.analyze_chunks(all_chunks)

        return {
            'strategy_config': strategy.config,
            'total_chunks': len(all_chunks),
            'overall_analysis': overall_analysis,
            'document_results': document_results,
            'performance_score': self._calculate_performance_score(overall_analysis)
        }

    def _calculate_performance_score(self, analysis: Dict[str, Any]) -> float:
        """计算某个策略的综合性能得分。"""
        if 'error' in analysis:
            return 0.0

        size_stats = analysis['size_statistics']
        boundary_quality = analysis['boundary_quality']
        coherence = analysis['semantic_coherence']

        # 将各指标归一化到 0-1 区间后合并
        size_consistency = 1.0 - min(size_stats['std'] / size_stats['mean'], 1.0) if size_stats['mean'] > 0 else 0
        boundary_score = (boundary_quality['sentence_boundary_ratio'] + boundary_quality['word_boundary_ratio']) / 2
        coherence_score = coherence

        # 加权合并
        return (size_consistency * 0.3 + boundary_score * 0.4 + coherence_score * 0.3)

    def _recommend_strategy(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """基于分析结果推荐最佳分块策略。"""
        best_strategy = None
        best_score = 0

        strategy_scores = {}

        for strategy_name, result in results.items():
            score = result['performance_score']
            strategy_scores[strategy_name] = score

            if score > best_score:
                best_score = score
                best_strategy = strategy_name

        return {
            'best_strategy': best_strategy,
            'best_score': best_score,
            'all_scores': strategy_scores,
            'reasoning': self._generate_reasoning(best_strategy, results[best_strategy] if best_strategy else None)
        }

    def _generate_reasoning(self, strategy_name: str, result: Dict[str, Any]) -> str:
        """为推荐结果生成人类可读的理由说明。"""
        if not result:
            return "No valid strategy found."

        analysis = result['overall_analysis']
        size_stats = analysis['size_statistics']
        boundary = analysis['boundary_quality']

        reasoning = f"Recommended '{strategy_name}' because:\n"
        reasoning += f"- Average chunk size: {size_stats['mean']:.0f} characters\n"
        reasoning += f"- Size consistency: {size_stats['std']:.0f} std deviation\n"
        reasoning += f"- Boundary quality: {boundary['sentence_boundary_ratio']:.2%} clean sentence breaks\n"
        reasoning += f"- Semantic coherence: {analysis['semantic_coherence']:.3f}\n"

        return reasoning

    def _generate_sample_chunks(self, corpus: DocumentCorpus, strategy_name: str) -> List[Dict[str, Any]]:
        """用被推荐的策略生成示例块。"""
        if not strategy_name or not corpus.documents:
            return []

        # 创建策略实例
        strategy = None
        if 'fixed_size' in strategy_name:
            strategy = FixedSizeChunker()
        elif 'sentence' in strategy_name:
            strategy = SentenceChunker()
        elif 'paragraph' in strategy_name:
            strategy = ParagraphChunker()
        elif 'semantic' in strategy_name:
            strategy = SemanticChunker()

        if not strategy:
            return []

        # 取第一个文档生成分块
        sample_doc = corpus.documents[0]
        chunks = strategy.chunk(sample_doc['content'])

        # 返回前 3 个块作为示例
        return chunks[:3]


def main():
    """主函数，提供命令行界面。"""
    parser = argparse.ArgumentParser(description='分析文档并推荐最优分块策略')
    parser.add_argument('directory', help='包含 text/markdown 文档的目录')
    parser.add_argument('--output', '-o', help='结果输出文件（JSON 格式）')
    parser.add_argument('--config', '-c', help='配置文件（JSON 格式）')
    parser.add_argument('--extensions', nargs='+', default=['.txt', '.md', '.markdown'],
                       help='要处理的文件扩展名')
    parser.add_argument('--verbose', '-v', action='store_true', help='输出详细信息')

    args = parser.parse_args()

    # 加载配置
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)

    try:
        # 加载语料
        print(f"Loading documents from {args.directory}...")
        corpus = DocumentCorpus(args.directory, args.extensions)

        # 运行优化
        optimizer = ChunkingOptimizer()
        results = optimizer.optimize(corpus, config)

        # 保存结果
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")

        # 打印摘要
        print("\n" + "="*60)
        print("CHUNKING OPTIMIZATION RESULTS")
        print("="*60)

        corpus_info = results['corpus_info']
        print(f"Corpus: {corpus_info['document_count']} documents, {corpus_info['total_size']:,} characters")

        recommendation = results['recommendation']
        print(f"\nRecommended Strategy: {recommendation['best_strategy']}")
        print(f"Performance Score: {recommendation['best_score']:.3f}")
        print(f"\nReasoning:\n{recommendation['reasoning']}")

        if args.verbose:
            print("\nAll Strategy Scores:")
            for strategy, score in recommendation['all_scores'].items():
                print(f"  {strategy}: {score:.3f}")

        print("\nSample Chunks:")
        for i, chunk in enumerate(results['sample_chunks'][:2]):
            print(f"\nChunk {i+1} ({chunk['size']} chars):")
            print("-" * 40)
            print(chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'])

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
