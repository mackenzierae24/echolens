"""
EchoLens - Analyzes text for ideological and linguistic patterns
Located at: echolens/src/ui/streamlit_app.py
"""
import streamlit as st
import os
import sys
import time # Keep time for the spinner's dramatic pause
from typing import Dict, Tuple # Ensure Tuple is imported

# --- Path Adjustments ---
# Current file: echolens/src/ui/streamlit_app.py
# __file__ is .../echolens/src/ui/streamlit_app.py
# ui_dir is .../echolens/src/ui/
# src_dir is .../echolens/src/
# project_root_dir is .../echolens/
ui_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(ui_dir)
project_root_dir = os.path.dirname(src_dir)

# Add project_root_dir to sys.path to allow imports like `from config...` and `from src...`
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)
# --- End Path Adjustments ---

from config.settings import get_config
from src.analyzer import create_embeddings_manager, PatternAnalyzer # Corrected import path

# Configure page with Apple-inspired styling
st.set_page_config(
    page_title="EchoLens",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS (ensure this function is defined as in your original file)
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
        max-width: 1200px !important; /* Main content width */
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

    div[data-testid="stVerticalBlock"] { /* Handles columns and other vertical blocks */
        background: transparent !important;
    }

    div[data-testid="column"] { /* Specifically for columns */
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
        max-width: 90% !important; /* Ensure subtitle doesn't get too wide */
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Why section responsive styling */
    .stMarkdown .why-section,
    div[data-testid="stMarkdownContainer"] .why-section {
        background: rgba(255, 255, 255, 0.9) !important; /* Slightly more opaque */
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(16px, 3vw, 20px) !important;
        padding: clamp(1.5rem, 4vw, 3rem) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important; /* Subtle border */
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
        max-width: min(800px, 90%) !important; /* Responsive max width */
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
        margin: clamp(0.5rem, 1vw, 1rem) 0 !important; /* Vertical margin, no horizontal */
        box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        transition: all 0.3s ease !important;
        height: 100% !important; /* Ensure cards in a row have same height */
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
        flex-grow: 1 !important; /* Allows text to fill space if card heights vary */
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

    .stMarkdown .section-title, /* General section title */
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
        width: 100% !important; /* Make button full width of its container */
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }


    /* Responsive text area styling */
    .stTextArea > div > div > textarea { /* Target the actual textarea element */
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: clamp(8px, 2vw, 12px) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        padding: clamp(0.75rem, 2vw, 1rem) !important;
        min-height: clamp(120px, 20vh, 150px) !important; /* Responsive min height */
        color: #1d1d1f !important; /* Text color inside textarea */
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important; /* Focus ring */
    }

    .stTextArea label { /* Style for the label of the text area if visible */
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #1d1d1f !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        margin-bottom: 0.5rem !important; /* Space between label and textarea */
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
        height: 100% !important; /* Ensure cards in a row have same height */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .stMarkdown .metric-container h2, /* Metric value */
    div[data-testid="stMarkdownContainer"] .metric-container h2 {
        font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
        margin: clamp(0.25rem, 1vw, 0.5rem) 0 !important;
        color: #1d1d1f !important; /* Ensure metric value is clearly visible */
    }

    .stMarkdown .metric-container h3, /* Metric title (e.g., "Primary Echo") */
    div[data-testid="stMarkdownContainer"] .metric-container h3 {
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
        color: #667eea !important; /* Use accent color for metric title */
        margin-bottom: 0.25rem !important;
    }

    .stMarkdown .metric-container p, /* Metric description */
    div[data-testid="stMarkdownContainer"] .metric-container p {
        font-size: clamp(0.8rem, 1.8vw, 0.9rem) !important;
        color: #515154 !important;
    }

    /* Responsive results section */
    .stMarkdown .results-section,
    div[data-testid="stMarkdownContainer"] .results-section {
        background: rgba(255, 255, 255, 0.95) !important; /* Slightly more opaque for results */
        backdrop-filter: blur(20px) !important;
        border-radius: clamp(16px, 3vw, 20px) !important;
        padding: clamp(1.5rem, 4vw, 2.5rem) !important;
        margin: clamp(1rem, 2vw, 2rem) 0 !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* Status Indicator styling */
    .status-indicator {
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid transparent;
        display: inline-block; /* Allows centering if parent is text-align: center */
    }
    .status-embeddings { /* AI analysis active */
        background-color: #dcfce7; /* Light green */
        color: #166534; /* Dark green */
        border-color: #4ade80; /* Green */
    }
    .status-fallback { /* Basic analysis */
        background-color: #ffedd5; /* Light orange */
        color: #9a3412; /* Dark orange */
        border-color: #fb923c; /* Orange */
    }
    .status-info { /* General info status */
        background-color: #e0e7ff; /* Light Indigo */
        color: #3730a3; /* Dark Indigo */
        border-color: #818cf8; /* Indigo */
    }


    /* Responsive typography for general markdown elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1d1d1f !important;
    }

    .stMarkdown h4 { /* Used for sub-section titles in results */
        font-size: clamp(1.1rem, 3vw, 1.3rem) !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        line-height: 1.6 !important;
        color: #424245; /* Default paragraph color */
    }

    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .stMarkdown .hero-container,
        div[data-testid="stMarkdownContainer"] .hero-container,
        .stMarkdown .why-section,
        div[data-testid="stMarkdownContainer"] .why-section,
        .stMarkdown .input-section,
        div[data-testid="stMarkdownContainer"] .input-section,
        .stMarkdown .results-section,
        div[data-testid="stMarkdownContainer"] .results-section {
            margin: 1rem 0 !important; /* Reduce vertical margins on mobile */
            padding-left: 1rem !important; /* Reduce horizontal padding on mobile */
            padding-right: 1rem !important;
        }
        
        .stMarkdown .insight-card,
        div[data-testid="stMarkdownContainer"] .insight-card {
            margin: 0.5rem 0 !important; /* Stack cards vertically with less margin */
        }
        
        /* Adjust columns to stack on mobile if st.columns is used for layout */
        /* Streamlit handles column stacking by default, but this can be for custom HTML columns */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
             flex-basis: 100% !important; /* Make columns take full width to stack */
             margin-bottom: 1rem; /* Add space between stacked columns */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
             margin-bottom: 0;
        }
    }

    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            max-width: 90% !important; /* Slightly wider for tablets */
        }
    }

    /* Large screen adjustments (already have max-width: 1200px) */
    /* @media (min-width: 1400px) { ... } */

    /* Progress bars */
    .progress-container {
        background: #e9ecef !important; /* Lighter gray for progress track */
        border-radius: 10px !important;
        height: 10px !important; /* Slightly thicker progress bar */
        margin: 0.5rem 0 !important;
        overflow: hidden !important;
    }

    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        height: 100% !important;
        border-radius: 10px !important; /* Match container radius */
        transition: width 1.2s ease-in-out !important; /* Smoother transition */
    }

    /* Dialect preview in expander */
    .dialect-preview {
        background: rgba(102, 126, 234, 0.05) !important; /* Very subtle background */
        border-left: 3px solid #667eea !important; /* Thinner accent border */
        border-radius: 6px !important; /* Slightly smaller radius */
        padding: 0.75rem 1rem !important; /* Adjust padding */
        margin: 0.5rem 0 1rem 0 !important; /* Add bottom margin */
        font-size: 0.9rem; /* Slightly smaller font for preview */
        line-height: 1.5;
        color: #333;
    }

    /* Animations */
    .fade-in {
        animation: fadeIn 0.7s ease-out !important; /* Slightly faster, ease-out */
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); } /* Less dramatic transform */
        to { opacity: 1; transform: translateY(0); }
    }

    /* Custom scrollbar for webkit browsers */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(245, 247, 250, 0.1); /* Match light background gradient */
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.4); /* Semi-transparent accent */
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.6); /* Darker on hover */
    }

    /* Ensure all text uses Inter, overriding Streamlit defaults where necessary */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

@st.cache_resource # Caches the manager instance
def initialize_embeddings_manager_cached():
    """Initialize embeddings manager with caching for the instance itself."""
    try:
        api_key = get_config('OPENAI_API_KEY')
        if not api_key:
            # This message will appear in the UI if API key is missing
            # st.error("⚠️ OpenAI API key not found. Please check your .env file or environment variables.")
            return None 
        
        manager = create_embeddings_manager(api_key)
        if manager:
            # Optional: Log success, avoid st.success here as it's persistent on reruns
            # print("EmbeddingsManager initialized successfully via cache_resource.")
            pass
        else:
            # st.warning("⚠️ Failed to initialize AI analysis capabilities. Using basic word matching.")
            pass
        return manager
    except Exception as e:
        # st.error(f"❌ Critical Error initializing AI services: {str(e)}")
        print(f"❌ Critical Error initializing AI services: {str(e)}") # Log to console
        return None

@st.cache_data # Caches the loaded dialect samples
def load_dialect_samples_for_ui() -> Dict[str, str]:
    """Load dialect samples for UI display.
       PatternAnalyzer loads its own samples for analysis.
    """
    samples: Dict[str, str] = {}
    # Path relative to this script (echolens/src/ui/streamlit_app.py)
    # to echolens/data/dialects/samples/
    samples_data_dir = os.path.join(project_root_dir, 'data', 'dialects', 'samples')
    
    if os.path.exists(samples_data_dir):
        for filename in os.listdir(samples_data_dir):
            if filename.endswith('.txt'):
                # Create a more readable name, e.g., "La Hippie" from "la_hippie.txt"
                dialect_name = filename.replace('.txt', '').replace('_', ' ').title()
                try:
                    with open(os.path.join(samples_data_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content: # Ensure sample is not empty
                             samples[dialect_name] = content
                except Exception as e:
                    print(f"Warning: Failed to load UI dialect sample {filename}: {e}")
    
    if not samples: # Fallback if no samples found or directory is empty
        print("Warning: No dialect samples found in data directory for UI. Using fallback samples.")
        samples = {
            "Silicon Valley Optimist": "We're building something truly transformative here. This could fundamentally reshape how people think about this space. We need to move fast and capture this opportunity while maintaining our core values.",
            "Wellness Influencer": "I'm really holding space for this new chapter in my journey. The universe has been conspiring to bring me exactly what I need. I can feel my vibration shifting toward my highest self.",
            "Fitness Enthusiast": "I'm absolutely crushing my goals right now. Hit a new PR yesterday and my nutrition is completely dialed in. The grind mindset is everything - you have to level up every single day.",
            "Academic Researcher": "The theoretical framework employs post-structuralist discourse analysis to examine the underlying assumptions embedded within these linguistic patterns and their sociocultural implications.",
            "Faith Community Leader": "I've been seeking wisdom on this decision and feel called to this new season. It's about walking in purpose and trusting the process, even when the path isn't completely clear."
            # Add other fallbacks if necessary
         }
    return samples


def run_app():
    # Initialize embeddings manager (cached)
    embeddings_manager = initialize_embeddings_manager_cached()
    
    # Create analyzer instance
    analyzer = PatternAnalyzer(embeddings_manager)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container fade-in">
        <div class="hero-title">Your Words<br>Reveal Your World</div>
        <div class="hero-subtitle">
            Discover the hidden influences shaping how you think, speak, and see reality.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # System Status Indicator (Displayed once per session)
    if 'status_indicator_shown' not in st.session_state:
        if embeddings_manager:
            status_html = '<span class="status-indicator status-embeddings">🤖 AI Analysis Capability Active</span>'
        else:
            status_html = '<span class="status-indicator status-fallback">📝 Basic Analysis Capability Only</span>'
        
        st.markdown(f"""
        <div style="text-align: center; margin: -1rem 0 1.5rem 0; font-size: 0.9em;">
            <i>{status_html}</i>
        </div>
        """, unsafe_allow_html=True)
        st.session_state['status_indicator_shown'] = True
        
    # Why Section
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
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    with col_insight1:
        st.markdown("""
        <div class.stMarkdown .insight-card fade-in">
            <div class="insight-number">01</div>
            <div class="insight-title">Hidden Influence</div>
            <div class="insight-text">
                Your language patterns reveal which thought leaders, communities, and 
                ideologies have shaped your worldview—often without you realizing it.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_insight2:
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
    with col_insight3:
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
    
    ui_dialects = load_dialect_samples_for_ui() # For displaying available dialects
    
    col_input_text, col_input_dialects = st.columns([2, 1])
    with col_input_text:
        st.markdown("#### Paste a sample of your writing")
        st.markdown("*Any text that represents how you naturally express yourself—emails, social posts, journal entries, or thoughts.*")
        user_text = st.text_area(
            "Text Input Area", # Unique key for the text_area
            height=180, # Slightly taller
            placeholder="Paste your writing here... The more authentic to your voice, the more revealing the analysis will be (min. 10 characters for analysis, 50+ for best results).",
            label_visibility="hidden"
        )
        analyze_button = st.button("🧠 Reveal My Influences", type="primary", key="analyze_btn")
    
    with col_input_dialects:
        st.markdown("#### What we analyze against")
        st.markdown("*Your writing will be compared to these distinct communication patterns:*")
        if ui_dialects:
            for name in ui_dialects.keys():
                st.markdown(f"• **{name}**")
        else:
            st.markdown("<p style='color: #888;'><em>(Dialect samples not loaded for display)</em></p>", unsafe_allow_html=True)

    # Analysis Results
    if analyze_button and user_text:
        if len(user_text.strip()) < 10: # Frontend check, backend also checks
            st.warning("⚠️ Please enter at least 10 characters for analysis. More text (50+ characters) provides better insights.")
        else:
            spinner_msg_verb = "AI-powered semantic" if embeddings_manager else "pattern matching"
            with st.spinner(f"🔍 Running {spinner_msg_verb} analysis... This may take a moment."):
                # time.sleep(1) # Optional dramatic pause

                scores, actual_method_used = analyzer.analyze_text(user_text)
                detailed_analysis = analyzer.get_detailed_analysis(user_text, scores, actual_method_used)

            if detailed_analysis and detailed_analysis.get('top_dialect'): # Check if analysis yielded results
                st.markdown("""
                <div class="results-section fade-in">
                    <div class="section-title">Your Linguistic Reflection</div>
                </div>
                """, unsafe_allow_html=True)

                # Display the actual analysis method used
                method_key = detailed_analysis.get('analysis_method', 'unknown')
                method_display_text = "Analysis Status" # Default
                status_class = "status-info" # Default class

                if method_key == 'embeddings':
                    method_display_text = "🤖 AI Semantic Analysis"
                    status_class = "status-embeddings"
                elif method_key == 'word_similarity':
                    method_display_text = "📝 Word Pattern Analysis"
                    status_class = "status-fallback"
                elif method_key == 'not_analyzed_too_short':
                    method_display_text = "ℹ️ Input Too Short for Analysis"
                elif method_key == 'not_analyzed_no_dialects':
                     method_display_text = "ℹ️ Dialect Data Missing"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 2rem;">
                    <span class="status-indicator {status_class}">
                        {method_display_text}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                # Key Metrics section
                top_dialect = detailed_analysis['top_dialect']
                top_score = detailed_analysis.get('top_score', 0.0)
                avg_score_val = detailed_analysis.get('avg_score', 0.0)
                uniqueness_val = detailed_analysis.get('uniqueness', 100.0)

                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3>Primary Echo</h3>
                        <h2>{top_dialect}</h2>
                        <p>{top_score:.1%} similarity</p>
                    </div>
                    """, unsafe_allow_html=True)
                with metric_col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3>Average Match</h3>
                        <h2>{avg_score_val:.1%}</h2>
                        <p>across all patterns</p>
                    </div>
                    """, unsafe_allow_html=True)
                with metric_col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3>Uniqueness</h3>
                        <h2>{uniqueness_val:.0f}%</h2>
                        <p>distinctly you</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer

                # Detailed Analysis - Influence Breakdown
                st.markdown('<h4>Your Influence Breakdown</h4>', unsafe_allow_html=True)
                sorted_scores_list = detailed_analysis.get('sorted_scores', [])
                for dialect_item, score_item_value in sorted_scores_list:
                    percentage = score_item_value * 100
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); border-radius: 12px; padding: 1.25rem; margin: 0.75rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.07);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <span style="font-weight: 600; color: #1d1d1f; font-size: 1.05rem;">{dialect_item}</span>
                            <span style="color: #667eea; font-weight: bold; font-size: 1.05rem;">{percentage:.1f}%</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {max(0, min(100, percentage))}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Pattern Analysis
                st.markdown('<h4>🎯 Pattern Analysis</h4>', unsafe_allow_html=True)
                meaningful_words_list = detailed_analysis.get('meaningful_words', [])
                pattern_analysis_text = f"**Analysis:** Your text shows subtle patterns similar to {top_dialect} communication style, or no significant common keywords were found after filtering."
                if meaningful_words_list:
                    pattern_analysis_text = f"**Key phrases echoing {top_dialect} patterns:** {', '.join(meaningful_words_list)}"
                
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.08); border-left: 3px solid #667eea; border-radius: 8px; padding: 1.25rem; margin: 1rem 0; font-size: 1rem; color: #1d1d1f;">
                    {pattern_analysis_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Top 3 Matches
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.07);">
                    <h5 style="color: #1d1d1f; font-weight: 600; margin: 0 0 1rem 0; font-size:1.1rem;">Top 3 Dialect Matches:</h5>
                """, unsafe_allow_html=True) # Start of Top 3 div
                for i, (dialect_item_top, score_item_top) in enumerate(sorted_scores_list[:3]):
                    st.markdown(f"""
                    <div style="margin: 0.6rem 0; padding: 0.4rem 0;">
                        <span style="color: #667eea; font-weight: bold; font-size: 1rem;">{i+1}.</span>
                        <span style="font-weight: 600; color: #1d1d1f; margin-left: 0.5rem;">{dialect_item_top}:</span>
                        <span style="color: #515154; margin-left: 0.5rem;">{score_item_top:.1%} similarity</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True) # End of Top 3 div
                
                # Insights
                # Using a threshold for "strong echo" vs "unique voice"
                strong_echo_threshold = 0.10 # 10% similarity
                if top_score > strong_echo_threshold:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea1A, #764ba21A); 
                                 border-radius: 12px; padding: 1.5rem; margin: 2rem 0; 
                                 border-left: 4px solid #667eea;">
                        <h4 style="color: #667eea; margin-top: 0;">💡 What This Reveals</h4>
                        <p>Your writing echoes <strong>{top_dialect}</strong> communication patterns. 
                        This suggests you may have been influenced by content, communities, or thought leaders 
                        who share this linguistic style.</p>
                        <p><strong>Consider:</strong> What podcasts, books, or communities do you engage with? 
                        How might this influence be shaping your perspective on the world?</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #10b9811A, #059fe21A); 
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
                top_dialect_sample_text = ui_dialects.get(top_dialect, "Sample text for this dialect is not available.")
                with st.expander("🔍 See detailed pattern comparison", expanded=False):
                    st.markdown(f"**Sample from '{top_dialect}' pattern:**")
                    st.markdown(f'<div class="dialect-preview">{top_dialect_sample_text[:350]}...</div>', 
                                unsafe_allow_html=True)
                    
                    st.markdown("**Shared Keywords Analysis (if any):**")
                    if meaningful_words_list:
                        st.markdown(f"Common meaningful words with '{top_dialect}': {', '.join(meaningful_words_list)}")
                    else:
                        st.markdown(f"Your text shows stylistic similarity with '{top_dialect}' without obvious shared keywords, or no significant common keywords were found after filtering.")
            
            elif detailed_analysis and detailed_analysis.get('analysis_method') in ["not_analyzed_too_short", "not_analyzed_no_dialects"]:
                 # The status message is already shown above.
                 st.info(f"Analysis could not be performed as indicated. Please adjust your input or check dialect data.")
            else: # Fallback if analysis didn't produce a displayable result
                st.error("❌ Analysis seems to have completed, but results could not be displayed. Please try again or check the input text.")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem 2rem 1rem; color: #515154; font-size: 0.9rem;">
        <h3 style="color: #1d1d1f; font-weight:600; margin-bottom:0.75rem;">Ready to expand your perspective?</h3>
        <p style="margin-bottom:1.5rem; font-size: 1rem; color: #424245;">Understanding your influences is the first step toward conscious growth.</p>
        <p>
            EchoLens uses AI to reveal the invisible patterns in your language, 
            helping you become more aware of how your worldview is shaped.
        </p>
        <p style="margin-top:2rem; font-size:0.8rem; color: #777;">
            &copy; EchoLens Concept. For demonstration purposes.
        </p>
    </div>
    """, unsafe_allow_html=True)

# This is typically in main.py, but if streamlit_app.py is run directly:
if __name__ == "__main__":
    run_app()
