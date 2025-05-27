"""
Pattern Analyzer - Enhanced version using OpenAI embeddings
"""

import os
import logging
from typing import Dict, List, Tuple, Optional, Any # Updated Tuple and Any
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
        self.dialect_embeddings_cache: Dict[str, Optional[List[float]]] = {} # Type hint for clarity
        
    def load_dialect_samples(self) -> Dict[str, str]:
        """Load dialect samples from files"""
        samples: Dict[str, str] = {}
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
        
        if not samples: # Fallback samples if files don't exist or directory is empty
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
            logger.warning("No embeddings manager available for preparing dialect embeddings.")
            return {name: None for name in dialects.keys()} # Return None for all if no manager
        
        missing_dialects = [name for name in dialects.keys() if name not in self.dialect_embeddings_cache]
        
        if missing_dialects:
            logger.info(f"Generating embeddings for {len(missing_dialects)} dialects")
            
            texts_to_embed = [dialects[name] for name in missing_dialects]
            # Assuming get_embeddings_batch returns a Dict[str_text, Optional[List[float]]]
            embeddings_result_map = self.embeddings_manager.get_embeddings_batch(texts_to_embed)
            
            for dialect_name in missing_dialects:
                dialect_text_content = dialects[dialect_name]
                embedding = embeddings_result_map.get(dialect_text_content)
                self.dialect_embeddings_cache[dialect_name] = embedding
                
                if embedding:
                    logger.debug(f"Cached embedding for {dialect_name}")
                else:
                    logger.warning(f"Failed to get embedding for {dialect_name}")
        
        return self.dialect_embeddings_cache
    
    def analyze_with_embeddings(self, user_text: str, dialects: Dict[str, str]) -> Tuple[Dict[str, float], str]:
        """
        Analyze user text using OpenAI embeddings.
        Returns scores and the analysis method string ("embeddings" or "word_similarity" if fallback).
        """
        if not self.embeddings_manager:
            logger.warning("No embeddings manager - falling back to word similarity")
            return self.analyze_with_word_similarity(user_text, dialects)
        
        user_embedding = self.embeddings_manager.get_embedding(user_text)
        if not user_embedding:
            logger.warning("Failed to get user text embedding - falling back to word similarity")
            return self.analyze_with_word_similarity(user_text, dialects)
        
        dialect_embeddings = self._prepare_dialect_embeddings(dialects)
        
        similarities: Dict[str, float] = {}
        for dialect_name, dialect_embedding in dialect_embeddings.items():
            if dialect_embedding:
                similarity_score = self.embeddings_manager.calculate_similarity(
                    user_embedding, dialect_embedding
                )
                similarities[dialect_name] = similarity_score
                logger.debug(f"{dialect_name} (embeddings): {similarity_score:.3f}")
            else:
                # Fallback to word similarity for this specific dialect if its embedding failed
                word_similarity_score = simple_word_similarity(user_text, dialects[dialect_name])
                similarities[dialect_name] = word_similarity_score
                logger.debug(f"{dialect_name} (word fallback for dialect): {word_similarity_score:.3f}")
        
        return similarities, "embeddings"
    
    def analyze_with_word_similarity(self, user_text: str, dialects: Dict[str, str]) -> Tuple[Dict[str, float], str]:
        """
        Fallback analysis using word similarity.
        Returns scores and the analysis method string ("word_similarity").
        """
        similarities: Dict[str, float] = {}
        for dialect_name, dialect_text in dialects.items():
            similarity = simple_word_similarity(user_text, dialect_text)
            similarities[dialect_name] = similarity
            
        logger.info("Used word similarity analysis (full fallback or direct call)")
        return similarities, "word_similarity"
    
    def analyze_text(self, user_text: str, use_embeddings: bool = True) -> Tuple[Dict[str, float], str]:
        """
        Main analysis function - tries embeddings first, falls back to word similarity.
        Returns scores and the actual analysis method string used.
        """
        scores: Dict[str, float] = {}
        actual_method_used: str = "unknown"

        if len(user_text.strip()) < 10: # Minimum length for meaningful analysis
            logger.warning("Text too short for analysis")
            return scores, "not_analyzed_too_short"
        
        dialects = self.load_dialect_samples()
        if not dialects:
            logger.error("No dialect samples available for analysis")
            return scores, "not_analyzed_no_dialects"
        
        if use_embeddings and self.embeddings_manager:
            try:
                scores, actual_method_used = self.analyze_with_embeddings(user_text, dialects)
            except Exception as e:
                logger.error(f"Embeddings analysis failed: {e}. Falling back to word similarity.")
                scores, actual_method_used = self.analyze_with_word_similarity(user_text, dialects)
        else:
            if not self.embeddings_manager and use_embeddings:
                logger.info("Embeddings analysis requested but manager not available. Using word similarity.")
            scores, actual_method_used = self.analyze_with_word_similarity(user_text, dialects)
        
        return scores, actual_method_used
    
    def get_detailed_analysis(self, user_text: str, dialect_scores: Dict[str, float], actual_method_used: str) -> Dict[str, Any]:
        """
        Get detailed analysis including word patterns and insights.
        Now takes actual_method_used as an argument.
        """
        if not dialect_scores: # No scores to analyze
            return {
                'top_dialect': None,
                'top_score': 0.0,
                'sorted_scores': [],
                'avg_score': 0.0,
                'uniqueness': 100.0, # Max uniqueness if no scores
                'meaningful_words': [],
                'word_count': len(user_text.split()),
                'analysis_method': actual_method_used # Still report the method attempted/used
            }
        
        sorted_scores_list = sorted(dialect_scores.items(), key=lambda x: x[1], reverse=True)
        top_dialect, top_score = sorted_scores_list[0]
        
        dialects = self.load_dialect_samples() # For word analysis consistency
        
        user_words = set(user_text.lower().split())
        dialect_words = set(dialects.get(top_dialect, "").lower().split()) # Safe get
        common_words = user_words.intersection(dialect_words)
        
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
                     'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 
                     'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 
                     'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 
                     'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 
                     'hers', 'its', 'our', 'their'}
        
        meaningful_words = common_words - stop_words
        
        # Calculate metrics (already correct)
        avg_score_val = sum(dialect_scores.values()) / len(dialect_scores)
        uniqueness_val = 100.0 - (top_score * 100.0) # Ensure float arithmetic
        
        return {
            'top_dialect': top_dialect,
            'top_score': top_score,
            'sorted_scores': sorted_scores_list,
            'avg_score': avg_score_val,
            'uniqueness': uniqueness_val,
            'meaningful_words': sorted(list(meaningful_words)), # Sort for consistent output
            'word_count': len(user_text.split()),
            'analysis_method': actual_method_used # Use the passed-in method
        }

# Convenience function for backward compatibility or other uses
# Note: The main Streamlit app will likely call methods on an analyzer instance.
def analyze_text_patterns(user_text: str, dialects: Dict[str, str] = None, 
                         embeddings_manager: Optional[EmbeddingsManager] = None) -> Tuple[Dict[str, float], str]:
    """
    Analyze text patterns - backward compatible function.
    Returns scores and the analysis method string.
    """
    analyzer = PatternAnalyzer(embeddings_manager)
    
    # This convenience function needs to decide how to get dialects if not provided.
    # The PatternAnalyzer class instance methods handle this internally.
    # For simplicity, if dialects are provided, we assume a more direct analysis.
    # If not, it uses the full `analyze_text` pipeline.
    
    if dialects:
        # If dialects are provided, decide method based on embeddings_manager
        if embeddings_manager:
            return analyzer.analyze_with_embeddings(user_text, dialects)
        else:
            return analyzer.analyze_with_word_similarity(user_text, dialects)
    else:
        # Use the full analysis pipeline which loads its own dialects
        return analyzer.analyze_text(user_text, use_embeddings=bool(embeddings_manager))
