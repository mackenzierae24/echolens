"""
EchoLens Embeddings Module
Handles OpenAI embeddings generation and caching for improved analysis
"""

import os
import json
import hashlib
import numpy as np
from typing import List, Dict, Optional, Union
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingsManager:
    """
    Manages OpenAI embeddings with caching and retry logic
    """
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """
        Initialize the embeddings manager
        
        Args:
            api_key: OpenAI API key
            model: Embedding model to use (default: text-embedding-3-small)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.cache_dir = os.path.join('data', 'embeddings_cache')
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the text"""
        return hashlib.md5(text.encode()).hexdigest()
        
    def _get_cache_path(self, cache_key: str) -> str:
        """Get the full path for a cache file"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
        
    def _load_from_cache(self, text: str) -> Optional[List[float]]:
        """Load embedding from cache if it exists"""
        cache_key = self._get_cache_key(text)
        cache_path = self._get_cache_path(cache_key)
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cached_data = json.load(f)
                    if cached_data.get('model') == self.model:
                        logger.debug(f"Cache hit for text: {text[:50]}...")
                        return cached_data['embedding']
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        
        return None
        
    def _save_to_cache(self, text: str, embedding: List[float]):
        """Save embedding to cache"""
        cache_key = self._get_cache_key(text)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cache_data = {
                'text_preview': text[:100],  # Store first 100 chars for debugging
                'model': self.model,
                'embedding': embedding
            }
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
            logger.debug(f"Cached embedding for text: {text[:50]}...")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _get_embedding_from_api(self, text: str) -> List[float]:
        """
        Get embedding from OpenAI API with retry logic
        Uses exponential backoff to handle rate limits gracefully
        """
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"API error getting embedding: {e}")
            raise
    
    def get_embedding(self, text: str, use_cache: bool = True) -> Optional[List[float]]:
        """
        Get embedding for text, using cache if available
        
        Args:
            text: Text to embed
            use_cache: Whether to use caching (default: True)
            
        Returns:
            List of floats representing the embedding, or None if failed
        """
        if not text or len(text.strip()) < 3:
            logger.warning("Text too short for embedding")
            return None
            
        # Check cache first
        if use_cache:
            cached_embedding = self._load_from_cache(text)
            if cached_embedding:
                return cached_embedding
        
        # Get from API
        try:
            embedding = self._get_embedding_from_api(text)
            
            # Save to cache
            if use_cache:
                self._save_to_cache(text, embedding)
                
            logger.info(f"Generated embedding for text: {text[:50]}...")
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to get embedding: {e}")
            return None
    
    def get_embeddings_batch(self, texts: List[str], use_cache: bool = True) -> Dict[str, Optional[List[float]]]:
        """
        Get embeddings for multiple texts efficiently
        
        Args:
            texts: List of texts to embed
            use_cache: Whether to use caching
            
        Returns:
            Dictionary mapping text to embedding
        """
        results = {}
        texts_to_process = []
        
        # Check cache for all texts first
        for text in texts:
            if use_cache:
                cached_embedding = self._load_from_cache(text)
                if cached_embedding:
                    results[text] = cached_embedding
                    continue
            texts_to_process.append(text)
        
        # Process remaining texts
        if texts_to_process:
            logger.info(f"Processing {len(texts_to_process)} texts via API")
            try:
                # For small batches, process individually to handle errors gracefully
                for text in texts_to_process:
                    embedding = self.get_embedding(text, use_cache=use_cache)
                    results[text] = embedding
                    
            except Exception as e:
                logger.error(f"Batch processing failed: {e}")
                # Fill remaining with None
                for text in texts_to_process:
                    if text not in results:
                        results[text] = None
        
        return results
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score between 0 and 1
        """
        if not embedding1 or not embedding2:
            return 0.0
            
        try:
            # Reshape for sklearn
            emb1 = np.array(embedding1).reshape(1, -1)
            emb2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(emb1, emb2)[0][0]
            
            # Convert from [-1, 1] to [0, 1] range
            normalized_similarity = (similarity + 1) / 2
            
            return float(normalized_similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def clear_cache(self):
        """Clear all cached embeddings"""
        try:
            import shutil
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
            self._ensure_cache_dir()
            logger.info("Embedding cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the cache"""
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            return {
                'cached_embeddings': len(cache_files),
                'cache_size_mb': sum(
                    os.path.getsize(os.path.join(self.cache_dir, f)) 
                    for f in cache_files
                ) / (1024 * 1024)
            }
        except Exception:
            return {'cached_embeddings': 0, 'cache_size_mb': 0}


def create_embeddings_manager(api_key: str) -> Optional[EmbeddingsManager]:
    """
    Factory function to create an EmbeddingsManager
    
    Args:
        api_key: OpenAI API key
        
    Returns:
        EmbeddingsManager instance or None if creation fails
    """
    try:
        manager = EmbeddingsManager(api_key)
        logger.info("EmbeddingsManager created successfully")
        return manager
    except Exception as e:
        logger.error(f"Failed to create EmbeddingsManager: {e}")
        return None


# Fallback similarity function (for when embeddings fail)
def simple_word_similarity(text1: str, text2: str) -> float:
    """
    Fallback similarity calculation using word overlap
    Used when embeddings are not available
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0
