"""
EchoLens Analyzer Module
Core analysis functionality for linguistic pattern detection
"""

from .embeddings import EmbeddingsManager, create_embeddings_manager, simple_word_similarity
from .pattern_analyzer import PatternAnalyzer, analyze_text_patterns

__all__ = [
    'EmbeddingsManager',
    'create_embeddings_manager', 
    'simple_word_similarity',
    'PatternAnalyzer',
    'analyze_text_patterns'
]
