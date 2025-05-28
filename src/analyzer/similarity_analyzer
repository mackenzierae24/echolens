import numpy as np
import pandas as pd
from typing import Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityAnalyzer:
    """
    Simple TF-IDF + cosine-similarity based influence detector.
    """

    def __init__(
        self,
        dialects: Dict[str, str],
        ngram_range: Tuple[int,int] = (1,2),
        max_features: int = 5000
    ):
        self.dialect_names = list(dialects.keys())
        self.dialect_texts = list(dialects.values())

        # Configure a single TF-IDF vectorizer for both dialects + user text
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            stop_words='english',
            max_features=max_features
        )

    def analyze(
        self,
        user_text: str,
        top_n_terms: int = 10
    ) -> Tuple[Dict[str, float], pd.DataFrame]:
        """
        Returns:
          - influence_scores: cosine similarity between user_text and each dialect
          - top_terms_df: top_n_terms from user_text by TF-IDF weight
        """
        # Fit TF-IDF on all dialects + the user text
        corpus = self.dialect_texts + [user_text]
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        feature_names = np.array(self.vectorizer.get_feature_names_out())

        # Split out dialect vectors vs user vector
        dialect_vecs = tfidf_matrix[:-1].toarray()
        user_vec     = tfidf_matrix[-1].toarray().ravel()

        # Cosine similarities
        influence_scores = {
            name: float(cosine_similarity(
                user_vec.reshape(1,-1), 
                vec.reshape(1,-1)
            )[0,0])
            for name, vec in zip(self.dialect_names, dialect_vecs)
        }

        # Top TF-IDF terms in user text
        top_indices = user_vec.argsort()[::-1][:top_n_terms]
        top_terms_df = pd.DataFrame({
            "term":   feature_names[top_indices],
            "weight": user_vec[top_indices]
        })

        return influence_scores, top_terms_df
