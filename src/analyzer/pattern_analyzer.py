"""
Pattern Analyzer - Enhanced version using OpenAI embeddings
"""

import os
import logging
from typing import Dict, List, Tuple, Optional
from .embeddings import EmbeddingsManager, simple_word_similarity

logger = logging.getLogger(__name__)

class PatternAnalyzer:
    """
    Advanced pattern analyzer using OpenAI embeddings
    """
    
    def __init__(self, embeddings_manager: Optional[EmbeddingsManager] = None):
        """
        Initialize the pattern analyzer
        
        Args:
            embeddings_manager: EmbeddingsManager instance (optional)
        """
        self.embeddings_manager = embeddings_manager
        self.dialect_embeddings_cache = {}
        
    def load_dialect_samples(self) -> Dict[str, str]:
        """Load dialect samples from files"""
        samples = {}
        samples_dir = os.path.join('data', 'dialects', 'samples')
        
        if os.path.exists(samples_dir):
            for filename in os.listdir(samples_dir):
                if filename.endswith('.txt'):
                    dialect_name = filename.replace('.txt', '').replace('_', ' ').title()
                    try:
                        with open(os.path.join(samples_dir, filename), 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:  # Only add non-empty files
                                samples[dialect_name] = content
                    except Exception as e:
                        logger.warning(f"Failed to load {filename}: {e}")
        
        # Fallback samples if files don't exist
        if not samples:
            samples = {
                "Silicon Valley Optimist": "We're building something truly transformative here. This could fundamentally reshape how people think about this space. We need to move fast and capture this opportunity while maintaining our core values.",
                "Wellness Influencer": "I'm really holding space for this new chapter in my journey. The universe has been conspiring to bring me exactly what I need. I can feel my vibration shifting toward my highest self.",
                "Fitness Enthusiast": "I'm absolutely crushing my goals right now. Hit a new PR yesterday and my nutrition is completely dialed in. The grind mindset is everything - you have to level up every single day.",
                "Academic Researcher": "The theoretical framework employs post-structuralist discourse analysis to examine the underlying assumptions embedded within these linguistic patterns and their sociocultural implications.",
                "Faith Community Leader": "I've been seeking wisdom on this decision and feel called to this new season. It's about walking in purpose and trusting the process, even when the path isn't completely clear."
            }
            
        logger.info(f"Loaded {len(samples)} dialect samples")
        return samples
    
    def _prepare_dialect_embeddings(self, dialects: Dict[str, str]) -> Dict[str, Optional[List[float]]]:
        """
        Generate and cache embeddings for all dialects
        
        Args:
            dialects: Dictionary of dialect names to sample texts
            
        Returns:
            Dictionary of dialect names to embeddings
        """
        if not self.embeddings_manager:
            logger.warning("No embeddings manager available")
            return {}
        
        # Check if we already have cached embeddings
        missing_dialects = []
        for dialect_name in dialects.keys():
            if dialect_name not in self.dialect_embeddings_cache:
                missing_dialects.append(dialect_name)
        
        if missing_dialects:
            logger.info(f"Generating embeddings for {len(missing_dialects)} dialects")
            
            # Get embeddings for missing dialects
            texts_to_embed = [dialects[name] for name in missing_dialects]
            embeddings_result = self.embeddings_manager.get_embeddings_batch(texts_to_embed)
            
            # Cache the results
            for dialect_name in missing_dialects:
                dialect_text = dialects[dialect_name]
                embedding = embeddings_result.get(dialect_text)
                self.dialect_embeddings_cache[dialect_name] = embedding
                
                if embedding:
                    logger.debug(f"Cached embedding for {dialect_name}")
                else:
                    logger.warning(f"Failed to get embedding for {dialect_name}")
        
        return self.dialect_embeddings_cache
    
    def analyze_with_embeddings(self, user_text: str, dialects: Dict[str, str]) -> Dict[str, float]:
        """
        Analyze user text using OpenAI embeddings
        
        Args:
            user_text: Text to analyze
            dialects: Dictionary of dialect samples
            
        Returns:
            Dictionary of dialect names to similarity scores
        """
        if not self.embeddings_manager:
            logger.warning("No embeddings manager - falling back to word similarity")
            return self.analyze_with_word_similarity(user_text, dialects)
        
        # Get user text embedding
        user_embedding = self.embeddings_manager.get_embedding(user_text)
        if not user_embedding:
            logger.warning("Failed to get user text embedding - falling back to word similarity")
            return self.analyze_with_word_similarity(user_text, dialects)
        
        # Prepare dialect embeddings
        dialect_embeddings = self._prepare_dialect_embeddings(dialects)
        
        # Calculate similarities
        similarities = {}
        for dialect_name, dialect_embedding in dialect_embeddings.items():
            if dialect_embedding:
                similarity = self.embeddings_manager.calculate_similarity(
                    user_embedding, dialect_embedding
                )
                similarities[dialect_name] = similarity
                logger.debug(f"{dialect_name}: {similarity:.3f}")
            else:
                # Fallback to word similarity for this dialect
                word_similarity = simple_word_similarity(user_text, dialects[dialect_name])
                similarities[dialect_name] = word_similarity
                logger.debug(f"{dialect_name}: {word_similarity:.3f} (word fallback)")
        
        return similarities
    
    def analyze_with_word_similarity(self, user_text: str, dialects: Dict[str, str]) -> Dict[str, float]:
        """
        Fallback analysis using word similarity
        
        Args:
            user_text: Text to analyze
            dialects: Dictionary of dialect samples
            
        Returns:
            Dictionary of dialect names to similarity scores
        """
        similarities = {}
        for dialect_name, dialect_text in dialects.items():
            similarity = simple_word_similarity(user_text, dialect_text)
            similarities[dialect_name] = similarity
            
        logger.info("Used word similarity analysis (fallback)")
        return similarities
    
    def analyze_text(self, user_text: str, use_embeddings: bool = True) -> Dict[str, float]:
        """
        Main analysis function - tries embeddings first, falls back to word similarity
        
        Args:
            user_text: Text to analyze
            use_embeddings: Whether to try embeddings first
            
        Returns:
            Dictionary of dialect names to similarity scores
        """
        if len(user_text.strip()) < 10:
            logger.warning("Text too short for analysis")
            return {}
        
        # Load dialects
        dialects = self.load_dialect_samples()
        if not dialects:
            logger.error("No dialect samples available")
            return {}
        
        # Choose analysis method
        if use_embeddings and self.embeddings_manager:
            try:
                return self.analyze_with_embeddings(user_text, dialects)
            except Exception as e:
                logger.error(f"Embeddings analysis failed: {e}")
                logger.info("Falling back to word similarity")
                return self.analyze_with_word_similarity(user_text, dialects)
        else:
            return self.analyze_with_word_similarity(user_text, dialects)
    
    def get_detailed_analysis(self, user_text: str, dialect_scores: Dict[str, float]) -> Dict[str, any]:
        """
        Get detailed analysis including word patterns and insights
        
        Args:
            user_text: Original user text
            dialect_scores: Similarity scores from analysis
            
        Returns:
            Dictionary with detailed analysis
        """
        if not dialect_scores:
            return {}
        
        # Sort scores
        sorted_scores = sorted(dialect_scores.items(), key=lambda x: x[1], reverse=True)
        top_dialect, top_score = sorted_scores[0]
        
        # Load dialects for word analysis
        dialects = self.load_dialect_samples()
        
        # Analyze word patterns with top dialect
        user_words = set(user_text.lower().split())
        dialect_words = set(dialects.get(top_dialect, "").lower().split())
        common_words = user_words.intersection(dialect_words)
        
        # Filter out stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
                     'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 
                     'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 
                     'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 
                     'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 
                     'hers', 'its', 'our', 'their'}
        
        meaningful_words = common_words - stop_words
        
        # Calculate metrics
        avg_score = sum(dialect_scores.values()) / len(dialect_scores)
        uniqueness = 100 - (top_score * 100)
        
        return {
            'top_dialect': top_dialect,
            'top_score': top_score,
            'sorted_scores': sorted_scores,
            'avg_score': avg_score,
            'uniqueness': uniqueness,
            'meaningful_words': list(meaningful_words),
            'word_count': len(user_text.split()),
            'analysis_method': 'embeddings' if self.embeddings_manager else 'word_similarity'
        }


# Convenience function for backward compatibility
def analyze_text_patterns(user_text: str, dialects: Dict[str, str] = None, 
                         embeddings_manager: EmbeddingsManager = None) -> Dict[str, float]:
    """
    Analyze text patterns - backward compatible function
    
    Args:
        user_text: Text to analyze
        dialects: Optional dialect samples (will be loaded if not provided)
        embeddings_manager: Optional embeddings manager
        
    Returns:
        Dictionary of dialect names to similarity scores
    """
    analyzer = PatternAnalyzer(embeddings_manager)
    
    if dialects:
        # Use provided dialects with embeddings if available
        if embeddings_manager:
            return analyzer.analyze_with_embeddings(user_text, dialects)
        else:
            return analyzer.analyze_with_word_similarity(user_text, dialects)
    else:
        # Use the full analysis pipeline
        return analyzer.analyze_text(user_text)
