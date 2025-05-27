# EchoLens 🔍

*"See what echoes through your words"*

EchoLens is an AI-powered tool that analyzes your linguistic patterns to identify ideological and social influences in your speech and writing.

## Quick Start

1. **Setup**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

2. **Initialize Data**
   ```bash
   python scripts/setup_dialects.py
   python scripts/generate_embeddings.py
   ```

3. **Run the App**
   ```bash
   streamlit run main.py
   ```

## Features

- 🎯 Analyze text for ideological patterns
- 🎤 Audio transcription support
- 📊 Visual similarity reports
- 🔄 Extensible dialect database

## Project Structure

- `src/analyzer/` - Core analysis engine
- `src/ui/` - Streamlit interface
- `data/dialects/` - Dialect samples and embeddings
- `scripts/` - Setup and utility scripts

## Adding New Dialects

Simply add a new `.txt` file to `data/dialects/samples/` and run:
```bash
python scripts/generate_embeddings.py
```

## License

MIT License - See LICENSE file for details
