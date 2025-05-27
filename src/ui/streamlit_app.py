"""
EchoLens - Analyzes text for ideological and linguistic patterns
"""
import streamlit as st
import os
import sys
import pandas as pd
import time
from typing import Dict, List, Tuple

# Configure page with Apple-inspired styling
st.set_page_config(
    page_title="EchoLens",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Apple-inspired design - Using st.markdown with unsafe_allow_html
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.main .block-container {
    background: transparent !important;
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}

.hero-container {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 24px;
    margin: 2rem 0;
    color: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
    background: linear-gradient(45deg, #fff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.4rem;
    font-weight: 400;
    opacity: 0.9;
    margin-bottom: 2rem;
    line-height: 1.5;
}

.why-section {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px;
    padding: 3rem;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
}

.why-title {
    font-size: 2.5rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 1.5rem;
    text-align: center;
}

.why-text {
    font-size: 1.1rem;
    line-height: 1.7;
    color: #424245;
    text-align: center;
    max-width: 800px;
    margin: 0 auto 2rem;
}

.insight-card {
    background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.3);
    transition: all 0.3s ease;
}

.insight-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.12);
}

.insight-number {
    font-size: 3rem;
    font-weight: 700;
    color: #667eea;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.insight-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 0.5rem;
}

.insight-text {
    color: #515154;
    line-height: 1.6;
}

.input-section {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.section-title {
    font-size: 2rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 1rem;
    text-align: center;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
}

.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 2px solid rgba(102, 126, 234, 0.2) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
}

.metric-container {
    background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.3);
    height: 100%;
}

.results-section {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
}

.dialect-preview {
    background: rgba(102, 126, 234, 0.05);
    border-left: 4px solid #667eea;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.fade-in {
    animation: fadeIn 0.8s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.progress-container {
    background: #f0f0f0;
    border-radius: 10px;
    height: 8px;
    margin: 0.5rem 0;
    overflow: hidden;
}

.progress-bar {
    background: linear-gradient(90deg, #667eea, #764ba2);
    height: 100%;
    border-radius: 10px;
    transition: width 1s ease;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Override Streamlit's default styling more aggressively */
div[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
}

div[data-testid="stMarkdownContainer"] {
    background: transparent !important;
}

/* Ensure text areas have proper styling */
.stTextArea label {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: #1d1d1f !important;
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
</style>
""", unsafe_allow_html=True)

def load_dialect_samples() -> Dict[str, str]:
    """Load dialect samples"""
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
                    pass
    
    # Fallback samples if files don't exist
    if not samples:
        samples = {
            "Silicon Valley Optimist": "We're building something truly transformative here. This could fundamentally reshape how people think about this space. We need to move fast and capture this opportunity while maintaining our core values.",
            "Wellness Influencer": "I'm really holding space for this new chapter in my journey. The universe has been conspiring to bring me exactly what I need. I can feel my vibration shifting toward my highest self.",
            "Fitness Enthusiast": "I'm absolutely crushing my goals right now. Hit a new PR yesterday and my nutrition is completely dialed in. The grind mindset is everything - you have to level up every single day.",
            "Academic Researcher": "The theoretical framework employs post-structuralist discourse analysis to examine the underlying assumptions embedded within these linguistic patterns and their sociocultural implications.",
            "Faith Community Leader": "I've been seeking wisdom on this decision and feel called to this new season. It's about walking in purpose and trusting the process, even when the path isn't completely clear."
        }
    
    return samples

def simple_similarity_score(text1: str, text2: str) -> float:
    """
    Simple similarity calculation using word overlap
    This is a placeholder until we implement OpenAI embeddings
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union > 0 else 0.0

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
    # Hero Section
    st.markdown("""
    <div class="hero-container fade-in">
        <div class="hero-title">Your Words<br>Reveal Your World</div>
        <div class="hero-subtitle">
            Discover the hidden influences shaping how you think, speak, and see reality
        </div>
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
            # Loading animation
            with st.spinner("🔍 Analyzing your linguistic DNA..."):
                time.sleep(1)  # Dramatic pause for effect
                scores = analyze_text_patterns(user_text, dialects)
                
                if scores:
                    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                    top_dialect, top_score = sorted_scores[0]
                    
                    st.markdown("""
                    <div class="results-section fade-in">
                        <div class="section-title">Your Linguistic Reflection</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Key Metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h3 style="color: #667eea; margin: 0;">Primary Echo</h3>
                            <h2 style="margin: 0.5rem 0;">{top_dialect}</h2>
                            <p style="color: #666; margin: 0;">{top_score:.1%} similarity</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        avg_score = sum(scores.values()) / len(scores)
                        st.markdown(f"""
                        <div class="metric-container">
                            <h3 style="color: #667eea; margin: 0;">Average Match</h3>
                            <h2 style="margin: 0.5rem 0;">{avg_score:.1%}</h2>
                            <p style="color: #666; margin: 0;">across all patterns</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        uniqueness = 100 - (top_score * 100)
                        st.markdown(f"""
                        <div class="metric-container">
                            <h3 style="color: #667eea; margin: 0;">Uniqueness</h3>
                            <h2 style="margin: 0.5rem 0;">{uniqueness:.0f}%</h2>
                            <p style="color: #666; margin: 0;">distinctly you</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
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
