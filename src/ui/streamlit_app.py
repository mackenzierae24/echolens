"""
EchoLens - Analyzes text for ideological and linguistic patterns
"""
import streamlit as st
import os
import sys
import pandas as pd
import time
from typing import Dict, List, Tuple

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.settings import get_config
from src.analyzer import create_embeddings_manager
from src.analyzer.pattern_analyzer import PatternAnalyzer
from src.dialects.loader import load_dialect_samples
#from src.analyzer.similarity_analyzer import SimilarityAnalyzer

# Configure page with Apple-inspired styling
st.set_page_config(
    page_title="EchoLens",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS first with more aggressive targeting
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global overrides */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .main .block-container {
        background: transparent !important;
        padding-top: 2rem !important;
        max-width: 1200px !important;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {visibility: hidden !important;}

    /* Force all markdown containers to be transparent */
    div[data-testid="stMarkdownContainer"] {
        background: transparent !important;
    }

    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }

    div[data-testid="column"] {
        background: transparent !important;
    }

    /* Hero section styling with responsive design */
    .stMarkdown .hero-container,
    div[data-testid="stMarkdownContainer"] .hero-container {
        text-align: center !important;
        padding: clamp(2rem, 5vw, 4rem) clamp(1rem, 3vw, 2rem) !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: clamp(16px, 3vw, 24px) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        color: white !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
    }

    .stMarkdown .hero-title,
    div[data-testid="stMarkdownContainer"] .hero-title {
        font-size: clamp(2rem, 6vw, 3.5rem) !important;
        font-weight: 700 !important;
        margin-bottom: clamp(0.5rem, 2vw, 1rem) !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(45deg, #fff, #e0e7ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.2 !important;
    }

    .stMarkdown .hero-subtitle,
    div[data-testid="stMarkdownContainer"] .hero-subtitle {
        font-size: clamp(1rem, 3vw, 1.4rem) !important;
        font-weight: 400 !important;
        opacity: 0.9 !important;
        margin-bottom: clamp(1rem, 3vw, 2rem) !important;
        line-height: 1.5 !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        max-width: 90% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Why section responsive styling */
    .stMarkdown .why-section,
    div[data-testid="stMarkdownContainer"] .why-section {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(16px, 3vw, 20px) !important;
        padding: clamp(1.5rem, 4vw, 3rem) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    .stMarkdown .why-title,
    div[data-testid="stMarkdownContainer"] .why-title {
        font-size: clamp(1.8rem, 5vw, 2.5rem) !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        margin-bottom: clamp(1rem, 2vw, 1.5rem) !important;
        text-align: center !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stMarkdown .why-text,
    div[data-testid="stMarkdownContainer"] .why-text {
        font-size: clamp(1rem, 2.5vw, 1.1rem) !important;
        line-height: 1.7 !important;
        color: #424245 !important;
        text-align: center !important;
        max-width: min(800px, 90%) !important;
        margin: 0 auto clamp(1rem, 2vw, 2rem) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Responsive insight cards */
    .stMarkdown .insight-card,
    div[data-testid="stMarkdownContainer"] .insight-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(12px, 2vw, 16px) !important;
        padding: clamp(1rem, 3vw, 2rem) !important;
        margin: clamp(0.5rem, 1vw, 1rem) 0 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        transition: all 0.3s ease !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }

    .stMarkdown .insight-card:hover,
    div[data-testid="stMarkdownContainer"] .insight-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(0,0,0,0.12) !important;
    }

    .stMarkdown .insight-number,
    div[data-testid="stMarkdownContainer"] .insight-number {
        font-size: clamp(2rem, 6vw, 3rem) !important;
        font-weight: 700 !important;
        color: #667eea !important;
        line-height: 1 !important;
        margin-bottom: clamp(0.25rem, 1vw, 0.5rem) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stMarkdown .insight-title,
    div[data-testid="stMarkdownContainer"] .insight-title {
        font-size: clamp(1.1rem, 2.5vw, 1.3rem) !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        margin-bottom: clamp(0.25rem, 1vw, 0.5rem) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stMarkdown .insight-text,
    div[data-testid="stMarkdownContainer"] .insight-text {
        color: #515154 !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        flex-grow: 1 !important;
    }

    /* Responsive input section */
    .stMarkdown .input-section,
    div[data-testid="stMarkdownContainer"] .input-section {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(16px, 3vw, 20px) !important;
        padding: clamp(1.5rem, 4vw, 2.5rem) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    }

    .stMarkdown .section-title,
    div[data-testid="stMarkdownContainer"] .section-title {
        font-size: clamp(1.5rem, 4vw, 2rem) !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        margin-bottom: clamp(0.5rem, 1vw, 1rem) !important;
        text-align: center !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Responsive button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: clamp(8px, 2vw, 12px) !important;
        padding: clamp(0.5rem, 2vw, 0.75rem) clamp(1rem, 3vw, 2rem) !important;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }

    /* Responsive text area styling */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: clamp(8px, 2vw, 12px) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        padding: clamp(0.75rem, 2vw, 1rem) !important;
        min-height: clamp(120px, 20vh, 150px) !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }

    .stTextArea label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #1d1d1f !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
    }

    /* Responsive metric containers */
    .stMarkdown .metric-container,
    div[data-testid="stMarkdownContainer"] .metric-container {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(12px, 2vw, 16px) !important;
        padding: clamp(1rem, 2.5vw, 1.5rem) !important;
        text-align: center !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .stMarkdown .metric-container h2,
    div[data-testid="stMarkdownContainer"] .metric-container h2 {
        font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
        margin: clamp(0.25rem, 1vw, 0.5rem) 0 !important;
    }

    .stMarkdown .metric-container h3,
    div[data-testid="stMarkdownContainer"] .metric-container h3 {
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
    }

    .stMarkdown .metric-container p,
    div[data-testid="stMarkdownContainer"] .metric-container p {
        font-size: clamp(0.8rem, 1.8vw, 0.9rem) !important;
    }

    /* Responsive results section */
    .stMarkdown .results-section,
    div[data-testid="stMarkdownContainer"] .results-section {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(16px, 3vw, 20px) !important;
        padding: clamp(1.5rem, 4vw, 2.5rem) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    /* Responsive typography */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1d1d1f !important;
    }

    .stMarkdown h4 {
        font-size: clamp(1.1rem, 3vw, 1.3rem) !important;
    }

    .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        line-height: 1.6 !important;
    }

    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .stMarkdown .hero-container,
        div[data-testid="stMarkdownContainer"] .hero-container {
            margin: 1rem 0 !important;
        }
        
        .stMarkdown .why-section,
        div[data-testid="stMarkdownContainer"] .why-section,
        .stMarkdown .input-section,
        div[data-testid="stMarkdownContainer"] .input-section,
        .stMarkdown .results-section,
        div[data-testid="stMarkdownContainer"] .results-section {
            margin: 1rem 0 !important;
        }
        
        .stMarkdown .insight-card,
        div[data-testid="stMarkdownContainer"] .insight-card {
            margin: 0.5rem 0 !important;
        }
    }

    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            max-width: 90% !important;
        }
    }

    /* Large screen adjustments */
    @media (min-width: 1400px) {
        .main .block-container {
            max-width: 1200px !important;
        }
    }

    /* Progress bars */
    .progress-container {
        background: #f0f0f0 !important;
        border-radius: 10px !important;
        height: 8px !important;
        margin: 0.5rem 0 !important;
        overflow: hidden !important;
    }

    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        height: 100% !important;
        border-radius: 10px !important;
        transition: width 1s ease !important;
    }

    /* Dialect preview */
    .dialect-preview {
        background: rgba(102, 126, 234, 0.05) !important;
        border-left: 4px solid #667eea !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }

    /* Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-in !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Typography overrides */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1d1d1f !important;
    }

    .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.3);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.5);
    }

    /* Force font loading */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS immediately
load_css()

@st.cache_resource
def initialize_analyzer():
    """Initialize embeddings manager with caching"""
    try:
        api_key = get_config('OPENAI_API_KEY')
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please check your configuration.")
            return None
        
        embeddings_manager = create_embeddings_manager(api_key)
        if embeddings_manager:
            st.success("🤖 AI-powered analysis enabled!")
            return embeddings_manager
        else:
            st.warning("⚠️ Failed to initialize AI analysis. Using basic word matching.")
            return None
    except Exception as e:
        st.error(f"❌ Error initializing AI: {str(e)}")
        return None



# In your run_app, pass embeddings_manager to analyze_text_patterns where needed
def run_app():
    load_css() # Reload CSS to ensure it's applied
    embeddings_manager = initialize_analyzer() # Initialize embeddings manager
    analyzer = PatternAnalyzer(embeddings_manager) # Create analyzer
    
    # Hero Section
    st.markdown("""
    <div class="hero-container fade-in">
        <div class="hero-title">Your Words<br>Reveal Your World</div>
        <div class="hero-subtitle">
            Discover the hidden influences shaping how you think, speak, and see reality
        </div>
    </div>
    """, unsafe_allow_html=True)

    # System Status Indicator
    if embeddings_manager:
        status_html = '<span class="status-indicator status-embeddings">🤖 AI Analysis Active</span>'
    else:
        status_html = '<span class="status-indicator status-fallback">📝 Basic Analysis</span>'
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        Analysis Mode: {status_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Why Section - Simon Sinek Style
    st.markdown("""
    <div class="why-section fade-in">
        <div class="why-title">Why does this matter?</div>
        <div class="why-text">
            Every day, you absorb thousands of words from podcasts, social media, books, and conversations. 
            These aren't just information—they're quietly reshaping how you think, what you believe, and 
            how you express yourself.
        </div>
        <div class="why-text">
            <strong>You might be thinking with someone else's brain without even knowing it.</strong>
        </div>
        <div class="why-text">
            What if you could see exactly whose ideas are echoing through your words? 
            What if you could understand which voices have unconsciously become your voice?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Three Key Insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-card fade-in">
            <div class="insight-number">01</div>
            <div class="insight-title">Hidden Influence</div>
            <div class="insight-text">
                Your language patterns reveal which thought leaders, communities, and 
                ideologies have shaped your worldview—often without you realizing it.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-card fade-in">
            <div class="insight-number">02</div>
            <div class="insight-title">Blind Spots</div>
            <div class="insight-text">
                When you only echo certain voices, you develop blind spots. 
                Understanding your linguistic biases helps you see where your perspective might be limited.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-card fade-in">
            <div class="insight-number">03</div>
            <div class="insight-title">Conscious Choice</div>
            <div class="insight-text">
                Awareness creates freedom. Once you see whose voices echo in yours, 
                you can choose more intentionally what influences to embrace.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown("""
    <div class="input-section">
        <div class="section-title">See Your Reflection</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load dialects
    dialects = load_dialect_samples()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Paste a sample of your writing")
        st.markdown("*Any text that represents how you naturally express yourself—emails, social posts, journal entries, or thoughts*")
        
        user_text = st.text_area(
            "Text Input",
            height=150,
            placeholder="Paste your writing here... The more authentic to your voice, the more revealing the analysis will be.",
            label_visibility="hidden"
        )
        
        analyze_button = st.button("🧠 Reveal My Influences", type="primary")
    
    with col2:
        st.markdown("#### What we analyze against")
        st.markdown("*Your writing will be compared to these distinct communication patterns:*")
        
        for name in dialects.keys():
            st.markdown(f"• **{name}**")
    
   # Analysis Results
    if analyze_button and user_text:
        if len(user_text.strip()) < 50:
            st.warning("⚠️ Please enter at least 50 characters for meaningful analysis.")
        else:
            analysis_method = "AI-powered semantic analysis" if embeddings_manager else "pattern matching analysis"
            with st.spinner(f"🔍 Running {analysis_method}..."):
                time.sleep(1)

                # 1) Unpack the tuple: scores dict and the actual method used
                scores, method_used = analyzer.analyze_text(user_text)
                
                # 2) Pass BOTH scores and method_used into get_detailed_analysis
                detailed_analysis = analyzer.get_detailed_analysis(user_text, scores, method_used)

                # Now use detailed_analysis['sorted_scores'], detailed_analysis['top_dialect'], etc.
                if scores:
                    # Pull out what you need
                    sorted_scores = detailed_analysis['sorted_scores']
                    top_dialect   = detailed_analysis['top_dialect']
                    top_score     = detailed_analysis['top_score']
                    avg_score     = detailed_analysis['avg_score']
                    uniqueness    = detailed_analysis['uniqueness']

                    # Choose display text/colors based on the actual method used
                    method_display = "🤖 AI Semantic Analysis" if method_used == 'embeddings' else "📝 Word Pattern Analysis"
                    method_color   = "#10b981" if method_used == 'embeddings' else "#f59e0b"
                
                    st.markdown("""
                    <div class="results-section fade-in">
                        <div class="section-title">Your Linguistic Reflection</div>
                     </div>
                    """, unsafe_allow_html=True)
                    
                    # Analysis method indicator
                    method_text = detailed_analysis.get('analysis_method', 'unknown')
                    if method_text == 'embeddings':
                        method_display = "🤖 AI Semantic Analysis"
                        method_color = "#10b981"
                    else:
                        method_display = "📝 Word Pattern Analysis"  
                        method_color = "#f59e0b"
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <span style="color: {method_color}; font-weight: 600; font-size: 0.9rem;">
                            {method_display}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Use existing metrics and analysis display code but replace:
                    # detailed_analysis.get('avg_score', 0) instead of sum(scores.values()) / len(scores)
                    # detailed_analysis.get('uniqueness', 0) instead of 100 - (top_score * 100)
                    
                    # Detailed Analysis
                    st.markdown('<h4 style="color: #1d1d1f; font-weight: 600; margin: 2rem 0 1rem 0;">Your Influence Breakdown</h4>', unsafe_allow_html=True)
                    
                    for dialect, score in sorted_scores:
                        percentage = score * 100
                        st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <span style="font-weight: 600; color: #1d1d1f; font-size: 1.1rem;">{dialect}</span>
                                <span style="color: #667eea; font-weight: bold; font-size: 1.1rem;">{percentage:.1f}%</span>
                            </div>
                            <div class="progress-container" style="height: 12px; background: #e8e8e8; border-radius: 6px; overflow: hidden;">
                                <div class="progress-bar" style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 6px; transition: width 1.5s ease;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Pattern Analysis
                    st.markdown('<h4 style="color: #1d1d1f; font-weight: 600; margin: 2rem 0 1rem 0;">🎯 Pattern Analysis</h4>', unsafe_allow_html=True)
                    
                    # Get meaningful words
                    user_words = set(user_text.lower().split())
                    dialect_words = set(dialects[top_dialect].lower().split())
                    common_words = user_words.intersection(dialect_words)
                    
                    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'hers', 'its', 'our', 'their'}
                    meaningful_words = common_words - stop_words
                    
                    if meaningful_words:
                        pattern_text = f"**Key phrases echoing {top_dialect} patterns:** {', '.join(sorted(meaningful_words))}"
                    else:
                        pattern_text = f"**Analysis:** Your text shows subtle patterns similar to {top_dialect} communication style."
                    
                    # Custom styled info box
                    st.markdown(f"""
                    <div style="background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; font-size: 1.1rem; color: #1d1d1f;">
                        {pattern_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    
                    # ─── Quick TF-IDF Influence Demo ─────────────────────────────────
                    # this sits right after your Pattern Analysis box  
                    #sim_analyzer = SimilarityAnalyzer(dialects)
                    #influence_scores, df_top_terms = sim_analyzer.analyze(
                    #    user_text,
                    #    top_n_terms=10
                    #)
    
                    #st.subheader("🔍 TF-IDF Influence Scores")
                    #st.bar_chart(influence_scores)
    
                    #st.subheader("📝 Top Terms by TF-IDF Weight")
                    #st.dataframe(df_top_terms)
                    # ──   
                    
                    # Show top 3 matches with better styling
                    st.markdown("""
                    <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                        <h5 style="color: #1d1d1f; font-weight: 600; margin: 0 0 1rem 0;">Top 3 Dialect Matches:</h5>
                    """, unsafe_allow_html=True)
                    
                    for i, (dialect, score) in enumerate(sorted_scores[:3]):
                        st.markdown(f"""
                        <div style="margin: 0.75rem 0; padding: 0.5rem 0;">
                            <span style="color: #667eea; font-weight: bold; font-size: 1.1rem;">{i+1}.</span>
                            <span style="font-weight: 600; color: #1d1d1f; margin-left: 0.5rem;">{dialect}:</span>
                            <span style="color: #515154; margin-left: 0.5rem;">{score:.1%} similarity</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Insights
                    if top_score > 0.1:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea20, #764ba220); 
                                   border-radius: 12px; padding: 1.5rem; margin: 2rem 0; 
                                   border-left: 4px solid #667eea;">
                            <h4 style="color: #667eea; margin-top: 0;">💡 What This Reveals</h4>
                            <p>Your writing strongly echoes <strong>{top_dialect}</strong> communication patterns. 
                            This suggests you've been influenced by content, communities, or thought leaders 
                            who share this linguistic style.</p>
                            <p><strong>Consider:</strong> What podcasts, books, or communities do you engage with? 
                            How might this influence be shaping your perspective on the world?</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #10b98120, #059fe220); 
                                   border-radius: 12px; padding: 1.5rem; margin: 2rem 0; 
                                   border-left: 4px solid #10b981;">
                            <h4 style="color: #10b981; margin-top: 0;">🌟 Unique Voice Detected</h4>
                            <p>Your writing doesn't strongly match any single pattern—this suggests you have 
                            a distinctive voice that draws from diverse influences or represents an original 
                            perspective.</p>
                            <p><strong>This is rare and valuable.</strong> Your unique linguistic fingerprint 
                            suggests independent thinking.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Sample comparisons in expander
                    with st.expander("🔍 See detailed pattern comparison", expanded=False):
                        st.markdown(f"**Sample from {top_dialect} pattern:**")
                        st.markdown(f'<div class="dialect-preview">{dialects[top_dialect][:200]}...</div>', 
                                  unsafe_allow_html=True)
                        
                        st.markdown("**Detailed word analysis:**")
                        if meaningful_words:
                            st.markdown(f"Shared meaningful words: {', '.join(sorted(meaningful_words))}")
                        else:
                            st.markdown("Your text shows stylistic similarity without obvious shared vocabulary.")

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #666;">
        <h3 style="color: #1d1d1f;">Ready to expand your perspective?</h3>
        <p>Understanding your influences is the first step toward conscious growth.</p>
        <p style="font-size: 0.9rem; margin-top: 2rem;">
            EchoLens uses AI to reveal the invisible patterns in your language, 
            helping you become more aware of how your worldview is shaped.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_app()
