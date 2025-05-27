"""
EchoLens Configuration Settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-4')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4000))

# App Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

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
