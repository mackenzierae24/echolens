"""
EchoLens - Simple Streamlit Application (No Plotly)
Analyzes text for ideological and linguistic patterns
"""
import streamlit as st
import os
import sys
import pandas as pd
from typing import Dict, List, Tuple

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def load_dialect_samples() -> Dict[str, str]:
    """Load all dialect samples from the data directory"""
    samples = {}
    samples_dir = os.path.join('data', 'dialects', 'samples')
    
    if os.path.exists(samples_dir):
        for filename in os.listdir(samples_dir):
            if filename.endswith('.txt'):
                dialect_name = filename.replace('.txt', '').replace('_', ' ').title()
                try:
                    with open(os.path.join(samples_dir, filename), 'r', encoding='utf-8') as f:
                        samples[dialect_name] = f.read().strip()
                except Exception as e:
                    st.error(f"Error loading {filename}: {e}")
    
    return samples

def simple_similarity_score(text1: str, text2: str) -> float:
    """Simple similarity calculation using word overlap"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    if union == 0:
        return 0.0
    
    return intersection / union

def analyze_text_patterns(user_text: str, dialects: Dict[str, str]) -> Dict[str, float]:
    """Analyze user text against dialect samples"""
    if len(user_text.strip()) < 10:
        return {}
    
    scores = {}
    for dialect_name, dialect_text in dialects.items():
        score = simple_similarity_score(user_text, dialect_text)
        scores[dialect_name] = score
    
    return scores

def run_app():
    st.set_page_config(
        page_title="EchoLens",
        page_icon="🔍",
        layout="wide"
    )
    
    # Header
    st.title("🔍 EchoLens")
    st.subheader("See what echoes through your words")
    
    # Load dialect samples
    dialects = load_dialect_samples()
    
    if not dialects:
        st.error("❌ No dialect samples found. Make sure to run `python scripts/setup_dialects.py` first.")
        st.stop()
    
    st.success(f"✅ Loaded {len(dialects)} dialect samples: {', '.join(dialects.keys())}")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Enter Your Text")
        user_text = st.text_area(
            "Paste your writing sample here (minimum 50 characters):",
            height=200,
            placeholder="Enter a paragraph or two of your writing, speaking style, or any text you'd like analyzed..."
        )
        
        analyze_button = st.button("🔍 Analyze My Language", type="primary")
    
    with col2:
        st.markdown("### 🎭 Available Dialects")
        for name, sample in dialects.items():
            with st.expander(f"{name}"):
                st.text(sample[:200] + "..." if len(sample) > 200 else sample)
    
    # Analysis Results
    if analyze_button and user_text:
        if len(user_text.strip()) < 50:
            st.warning("⚠️ Please enter at least 50 characters for meaningful analysis.")
        else:
            with st.spinner("🧠 Analyzing your linguistic patterns..."):
                scores = analyze_text_patterns(user_text, dialects)
                
                if scores:
                    # Sort scores to find top matches
                    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                    top_dialect, top_score = sorted_scores[0]
                    
                    st.markdown("## 📊 Analysis Results")
                    
                    # Key insights
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Top Match",
                            top_dialect,
                            f"{top_score:.1%} similarity"
                        )
                    
                    with col2:
                        avg_score = sum(scores.values()) / len(scores)
                        st.metric(
                            "Average Similarity",
                            f"{avg_score:.1%}",
                            "across all dialects"
                        )
                    
                    with col3:
                        unique_score = max(scores.values()) - sorted(scores.values())[-2] if len(scores) > 1 else 0
                        st.metric(
                            "Distinctiveness",
                            f"{unique_score:.1%}",
                            "how unique your top match is"
                        )
                    
                    # Simple bar chart using Streamlit
                    st.markdown("### 📊 Similarity Scores")
                    df = pd.DataFrame(
                        [(dialect, score) for dialect, score in sorted_scores],
                        columns=['Dialect', 'Similarity Score']
                    )
                    st.bar_chart(df.set_index('Dialect'))
                    
                    # Pattern Analysis
                    st.markdown("### 🎯 Pattern Analysis")
                    
                    if top_score > 0.05:
                        user_words = set(user_text.lower().split())
                        dialect_words = set(dialects[top_dialect].lower().split())
                        common_words = user_words.intersection(dialect_words)
                        
                        # Filter out common stop words
                        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
                        meaningful_words = common_words - stop_words
                        
                        if meaningful_words:
                            st.info(f"**Key phrases echoing {top_dialect} patterns:** {', '.join(sorted(meaningful_words))}")
                        else:
                            st.info(f"**Analysis:** Your text shows subtle patterns similar to {top_dialect} communication style.")
                        
                        # Show top 3 matches
                        st.markdown("#### Top 3 Dialect Matches:")
                        for i, (dialect, score) in enumerate(sorted_scores[:3]):
                            st.write(f"{i+1}. **{dialect}**: {score:.1%} similarity")
                    else:
                        st.info("🌟 **Unique Voice Detected!** Your writing style doesn't strongly match any of the current dialect samples.")
                    
                    # Detailed breakdown
                    with st.expander("📈 Detailed Similarity Scores"):
                        for dialect, score in sorted_scores:
                            st.write(f"**{dialect}**: {score:.1%}")
                
                else:
                    st.error("❌ Unable to analyze text. Please try a different sample.")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🚀 About EchoLens")
    st.info("EchoLens analyzes your linguistic patterns to identify what communication styles echo through your words. This MVP uses simple similarity matching.")

if __name__ == "__main__":
    run_app()
