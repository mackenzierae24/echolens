"""
EchoLens - Functional Streamlit Application
Analyzes text for ideological and linguistic patterns
"""
import streamlit as st
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Tuple

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    """
    Simple similarity calculation using word overlap
    This is a placeholder until we implement OpenAI embeddings
    """
    # Convert to lowercase and split into words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity (intersection over union)
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

def create_similarity_chart(scores: Dict[str, float]):
    """Create a bar chart showing similarity scores"""
    if not scores:
        return None
    
    df = pd.DataFrame(
        list(scores.items()), 
        columns=['Dialect', 'Similarity Score']
    ).sort_values('Similarity Score', ascending=True)
    
    fig = px.bar(
        df, 
        x='Similarity Score', 
        y='Dialect',
        orientation='h',
        title='Linguistic Pattern Analysis',
        color='Similarity Score',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_x=0.5
    )
    
    return fig

def create_radar_chart(scores: Dict[str, float]):
    """Create a radar chart showing similarity scores"""
    if not scores or len(scores) < 3:
        return None
    
    dialects = list(scores.keys())
    values = [scores[d] * 100 for d in dialects]  # Convert to percentage
    
    # Close the radar chart by adding the first value at the end
    dialects_closed = dialects + [dialects[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=dialects_closed,
        fill='toself',
        name='Your Linguistic Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.1 if values else 10]
            )),
        showlegend=True,
        title="Your Linguistic Influence Radar",
        title_x=0.5
    )
    
    return fig

def highlight_key_phrases(user_text: str, top_dialect: str, dialect_text: str) -> str:
    """
    Simple phrase highlighting - finds common words/phrases
    This is a placeholder for more sophisticated pattern detection
    """
    user_words = set(user_text.lower().split())
    dialect_words = set(dialect_text.lower().split())
    
    common_words = user_words.intersection(dialect_words)
    
    # Filter out common stop words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    meaningful_words = common_words - stop_words
    
    if meaningful_words:
        return f"**Key phrases echoing {top_dialect} patterns:** {', '.join(sorted(meaningful_words))}"
    else:
        return f"**Analysis:** Your text shows subtle patterns similar to {top_dialect} communication style."

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
        with st.expander("View dialect samples", expanded=False):
            for name, sample in dialects.items():
                st.markdown(f"**{name}:**")
                st.text(sample[:100] + "..." if len(sample) > 100 else sample)
                st.markdown("---")
    
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
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        bar_chart = create_similarity_chart(scores)
                        if bar_chart:
                            st.plotly_chart(bar_chart, use_container_width=True)
                    
                    with col2:
                        radar_chart = create_radar_chart(scores)
                        if radar_chart:
                            st.plotly_chart(radar_chart, use_container_width=True)
                    
                    # Pattern Analysis
                    st.markdown("### 🎯 Pattern Analysis")
                    
                    if top_score > 0.05:  # If there's meaningful similarity
                        pattern_analysis = highlight_key_phrases(
                            user_text, 
                            top_dialect, 
                            dialects[top_dialect]
                        )
                        st.info(pattern_analysis)
                        
                        # Show top 3 matches
                        st.markdown("#### Top 3 Dialect Matches:")
                        for i, (dialect, score) in enumerate(sorted_scores[:3]):
                            st.write(f"{i+1}. **{dialect}**: {score:.1%} similarity")
                    else:
                        st.info("🌟 **Unique Voice Detected!** Your writing style doesn't strongly match any of the current dialect samples. This suggests you have a distinctive linguistic pattern.")
                    
                    # Detailed breakdown
                    with st.expander("📈 Detailed Similarity Scores"):
                        df = pd.DataFrame(
                            [(dialect, f"{score:.1%}") for dialect, score in sorted_scores],
                            columns=['Dialect', 'Similarity Score']
                        )
                        st.dataframe(df, use_container_width=True)
                
                else:
                    st.error("❌ Unable to analyze text. Please try a different sample.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 🚀 About EchoLens
    
    EchoLens analyzes your linguistic patterns to identify what communication styles and ideological influences 
    echo through your words. This MVP version uses simple similarity matching - future versions will include:
    
    - 🤖 **AI-powered analysis** using OpenAI embeddings and GPT-4
    - 🎤 **Audio transcription** support via Whisper API  
    - 📊 **Advanced pattern detection** for more nuanced insights
    - 🎭 **Custom dialect creation** for personalized analysis
    - 📈 **Historical tracking** of linguistic evolution
    
    **Current Status:** MVP Demo with basic similarity matching
    """)

if __name__ == "__main__":
    run_app()