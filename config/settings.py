"""
EchoLens Configuration Settings
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Function to get config values from either environment or Streamlit secrets
def get_config(key, default=None):
    try:
        # Try Streamlit secrets first (for deployed app)
        return st.secrets[key]
    except:
        # Fall back to environment variables (for local development)
        return os.getenv(key, default)

# OpenAI Configuration
OPENAI_API_KEY = get_config('OPENAI_API_KEY')
EMBEDDING_MODEL = get_config('EMBEDDING_MODEL', 'text-embedding-3-small')
GPT_MODEL = get_config('GPT_MODEL', 'gpt-4')
MAX_TOKENS = int(get_config('MAX_TOKENS', 4000))

# App Configuration
DEBUG = get_config('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = get_config('LOG_LEVEL', 'INFO')

# Paths
DATA_DIR = 'data'
DIALECTS_DIR = os.path.join(DATA_DIR, 'dialects')
SAMPLES_DIR = os.path.join(DIALECTS_DIR, 'samples')
EMBEDDINGS_DIR = os.path.join(DIALECTS_DIR, 'embeddings')
USER_INPUTS_DIR = os.path.join(DATA_DIR, 'user_inputs')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')

# Analysis Settings
MIN_TEXT_LENGTH = 50
MAX_TEXT_LENGTH = 10000
SIMILARITY_THRESHOLD = 0.7
