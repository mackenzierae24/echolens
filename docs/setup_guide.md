# EchoLens Setup Guide

## Prerequisites
- Python 3.8+
- OpenAI API key

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd echolens
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Initialize data**
   ```bash
   python scripts/setup_dialects.py
   python scripts/generate_embeddings.py
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## Troubleshooting

### Common Issues
- **API Key Error**: Make sure your OpenAI API key is set in `.env`
- **Module Import Error**: Ensure you're running from the project root directory
- **Streamlit Error**: Try `pip install --upgrade streamlit`

### Getting Help
- Check the logs for detailed error messages
- Verify all dependencies are installed correctly
- Ensure Python version is 3.8 or higher
