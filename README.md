# EchoLens 🔍

*"See what echoes through your words"*

EchoLens is an AI-powered tool that analyzes your linguistic patterns to identify ideological and social influences in your speech and writing.

## 🔍 Application Overview

### Application Type
- **Web Application** built with Streamlit
- **AI-powered text analysis tool** for linguistic pattern detection
- **MVP/Proof of Concept** stage with basic similarity matching

### Core Purpose
EchoLens analyzes user writing samples to identify which ideological/social "dialects" influence their language patterns, helping users understand unconscious biases in their communication style.

## 🎯 Current Functionality

### Core Features
- **Text Input** - Users paste writing samples
- **Pattern Analysis** - Compares text against 5 dialect samples using word overlap
- **Similarity Scoring** - Jaccard similarity (intersection/union of words)
- **Visual Results** - Progress bars, metrics, pattern highlighting
- **Detailed Breakdown** - Top matches, shared words, insights

### Analysis Engine (src/analyzer/)
- `simple_similarity_score()` - Basic word overlap calculation
- `analyze_text_patterns()` - Compares user text vs dialect samples
- Stop word filtering - Removes common words for meaningful analysis

### UI Design Philosophy
- **Apple-inspired aesthetic** - Glassmorphism, gradients, clean typography
- **Simon Sinek "Why" approach** - Explains purpose before functionality
- **Progressive disclosure** - Reveals insights gradually

## 📁 Project Structure

```
echolens/
├── main.py                    # Entry point - runs Streamlit app
├── requirements.txt           # Python dependencies
├── .env.example/.env         # Environment variables (API keys)
├── README.md                 # Complete setup guide
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration management
├── src/
│   ├── analyzer/             # Core analysis logic
│   ├── dialects/             # Dialect management
│   ├── ui/
│   │   └── streamlit_app.py  # Main UI component
│   └── utils/                # Utility functions
├── data/
│   └── dialects/
│       └── samples/          # Pre-written dialect text samples
│           ├── la_hippie.txt
│           ├── crossfit_bro.txt
│           ├── startup_techie.txt
│           ├── christian_conservative.txt
│           └── academic_scholar.txt
├── scripts/
│   └── setup_dialects.py    # Initialize dialect samples
└── docs/                     # Documentation
```

## 🛠 Tech Stack

### Primary Technologies
- **Python 3.8+** - Backend language
- **Streamlit** - Web framework for the UI
- **OpenAI API** - For future AI-powered analysis (currently using placeholder)
- **Pandas** - Data manipulation
- **NumPy/SciPy** - Mathematical computations

### Current Dependencies (requirements.txt)
```
streamlit>=1.32.0
openai>=1.30.0
scikit-learn>=1.4.0
numpy>=1.24.0
plotly>=5.15.0
python-dotenv>=1.0.0
pandas>=2.0.0
matplotlib>=3.8.0
scipy>=1.11.0
```

## 🔑 Key Files to Focus On

### 1. Main Entry Point
```python
# main.py
import streamlit as st
from src.ui.streamlit_app import run_app

if __name__ == "__main__":
    run_app()
```

### 2. Core UI Component
```python
# src/ui/streamlit_app.py
# Contains entire Streamlit interface with:
# - Apple-inspired CSS styling
# - Hero section with compelling messaging
# - Analysis logic and results display
# - All user interactions
```

### 3. Configuration
```python
# config/settings.py
# Manages API keys, paths, analysis parameters
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SAMPLES_DIR = 'data/dialects/samples'
MIN_TEXT_LENGTH = 50
```

### 4. Dialect Samples
```
# data/dialects/samples/*.txt
# 5 text files containing representative writing for each dialect:
# - LA Hippie ("holding space", "vibration", "authentic self")
# - CrossFit Bro ("crushing it", "PR", "macros", "grind mindset") 
# - Startup Techie ("disruptive", "MVP", "scale", "iterate")
# - Christian Conservative ("God's timing", "season", "kingdom work")
# - Academic Scholar ("theoretical framework", "discourse analysis")
```

## 🎨 Current Design System

### Color Palette
- **Primary Gradient**: `#667eea` to `#764ba2`
- **Background**: `#f5f7fa` to `#c3cfe2`
- **Glassmorphism**: `rgba(255, 255, 255, 0.8)` with blur effects
- **Text**: `#1d1d1f` (dark), `#424245` (medium), `#515154` (light)

### Typography
- **Font**: Inter (Google Fonts)
- **Hero Title**: 3.5rem, gradient text effect
- **Sections**: 2rem-2.5rem headings
- **Body**: 1.1rem with 1.7 line height

## 🔄 Current Analysis Workflow

1. **User inputs text** (minimum 50 characters)
2. **`load_dialect_samples()`** - Loads 5 dialect text files
3. **`analyze_text_patterns()`** - Calculates similarity scores
4. **`simple_similarity_score()`** - Word overlap using Jaccard similarity
5. **Results display** - Metrics, progress bars, pattern analysis
6. **Meaningful words extraction** - Filters stop words, shows common phrases

## 🚀 Deployment Status

### Current Hosting
- **Streamlit Cloud** - Live web application
- **GitHub Integration** - Auto-deploys from main branch
- **Environment Variables** - API keys stored as Streamlit secrets in TOML format

### Known Issues
- **CSS Loading Problems** - Apple-inspired styling sometimes doesn't apply on Streamlit Cloud
- **Placeholder Analysis** - Currently using basic word matching instead of AI embeddings

## 🎯 Future Enhancement Opportunities

### Immediate Improvements
1. **Implement OpenAI embeddings** - Replace simple word matching
2. **Add audio transcription** - Whisper API integration
3. **Pattern detection** - Use GPT-4 for linguistic analysis
4. **Fix CSS persistence** - Ensure styling works reliably

### Advanced Features
1. **Custom dialect creation** - User-defined communication patterns
2. **Historical tracking** - Language evolution over time
3. **Batch analysis** - Multiple text samples
4. **Export functionality** - PDF reports, data export

## 💡 Key Concepts to Understand

### "Dialects" = Communication Patterns
Not linguistic dialects, but ideological/social speech patterns that reveal influences from specific communities or thought leaders.

### "Echo" Metaphor
The idea that your words "echo" the voices/content you consume, revealing unconscious influence on your thinking.

### MVP Philosophy
Simple, functional proof-of-concept that demonstrates value before building complex features.

## 🚀 Quick Start

1. **Setup**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

2. **Initialize Data**
   ```bash
   python scripts/setup_dialects.py
   ```

3. **Run the App**
   ```bash
   streamlit run main.py
   ```

## ✨ Features

- 🎯 Analyze text for ideological patterns
- 📊 Visual similarity reports
- 🔄 Extensible dialect database
- 🎨 Apple-inspired user interface

## 🔧 Adding New Dialects

Simply add a new `.txt` file to `data/dialects/samples/` and restart the application.

---

# 📖 Complete Setup Guide

*For detailed, step-by-step instructions (especially for non-technical users), see below.*

## 📋 What You'll Need Before Starting

- A Mac computer (this guide is written for Mac)
- Internet connection
- About 30-45 minutes
- An OpenAI API key (we'll show you how to get one)

## 🚀 Step-by-Step Setup Guide

### Step 1: Get Your OpenAI API Key

Before we start coding, you'll need an API key from OpenAI:

1. **Go to [platform.openai.com](https://platform.openai.com)**
2. **Sign up or log in** to your OpenAI account
3. **Click your profile picture** in the top right → "View API keys"
4. **Click "Create new secret key"**
5. **Copy the key** that starts with `sk-` (it's long!)
6. **Save it somewhere safe** - you'll need it later

💡 **Important:** Keep this key private and never share it publicly!

### Step 2: Download and Install Required Software

#### Install Python (if you don't have it)
1. **Go to [python.org](https://python.org)**
2. **Click "Downloads"** → Download the latest version for Mac
3. **Run the installer** and follow the prompts
4. **When done, open Terminal** (press `Cmd + Space`, type "Terminal", press Enter)
5. **Type:** `python3 --version` and press Enter
6. **You should see something like:** `Python 3.11.x`

#### Install VS Code
1. **Go to [code.visualstudio.com](https://code.visualstudio.com)**
2. **Click "Download for Mac"**
3. **Drag VS Code to your Applications folder**
4. **Open VS Code** from Applications

#### Install Git (if you don't have it)
1. **In Terminal, type:** `git --version` and press Enter
2. **If you see a version number, skip to Step 3**
3. **If not, go to [git-scm.com](https://git-scm.com)**
4. **Download and install Git for Mac**

### Step 3: Create the EchoLens Project

#### Download the Project Files
1. **Open Terminal**
2. **Navigate to your Desktop:**
   ```bash
   cd ~/Desktop
   ```
3. **Download the project:**
   ```bash
   git clone https://github.com/yourusername/echolens.git
   ```
   *(Replace `yourusername` with the actual GitHub username)*

4. **Go into the project folder:**
   ```bash
   cd echolens
   ```

#### Verify You're in the Right Place
1. **Type:** `pwd` and press Enter
2. **You should see:** `/Users/yourusername/Desktop/echolens`
3. **Type:** `ls` and press Enter
4. **You should see files like:** `main.py`, `requirements.txt`, `src/`, etc.

### Step 4: Open Project in VS Code

1. **In VS Code, click:** File → Open Folder
2. **Navigate to:** Desktop → echolens
3. **Click "Open"**
4. **You should see the project files** in the left sidebar

#### Install Python Extension
1. **Click the Extensions icon** (4 squares) in the left sidebar
2. **Search for "Python"**
3. **Install the "Python" extension** by Microsoft
4. **Wait for it to install**

### Step 5: Set Up Your Python Environment

#### Open Terminal in VS Code
1. **In VS Code, click:** Terminal → New Terminal
2. **A terminal should open at the bottom** of VS Code
3. **Verify you're in the right directory:** type `pwd`
4. **You should see:** `/Users/yourusername/Desktop/echolens`

#### Create a Virtual Environment
1. **In the VS Code terminal, type:**
   ```bash
   python3 -m venv venv
   ```
2. **Wait for it to finish** (might take a minute)

#### Activate the Virtual Environment
1. **Type:**
   ```bash
   source venv/bin/activate
   ```
2. **You should see `(venv)` appear** at the beginning of your terminal prompt
3. **This means it's working!**

💡 **Important:** You'll need to do the `source venv/bin/activate` command every time you open a new terminal to work on this project.

#### Install Required Packages
1. **Make sure you see `(venv)` in your terminal**
2. **Type:**
   ```bash
   pip install --upgrade pip
   ```
3. **Then type:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Wait for all packages to install** (this might take a few minutes)

#### Verify Installation
1. **Type:**
   ```bash
   pip list
   ```
2. **You should see a list** of installed packages including `streamlit`, `openai`, etc.

### Step 6: Add Your OpenAI API Key

#### Create Your Environment File
1. **In VS Code, look at the file list** on the left
2. **You should see a file called** `.env.example`
3. **Right-click on `.env.example`** → Copy
4. **Right-click in the file area** → Paste
5. **Rename the copy to** `.env` (just remove `.example`)

#### Add Your API Key
1. **Open the `.env` file** by clicking on it
2. **Find the line that says:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
3. **Replace `your_openai_api_key_here` with your actual API key** (the one that starts with `sk-`)
4. **It should look like:**
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
5. **Save the file** (Cmd + S)

💡 **Important:** Make sure there are no spaces around the `=` sign!

### Step 7: Test Your Setup

#### Initialize the Dialect Samples
1. **In the VS Code terminal** (make sure you see `(venv)`), type:
   ```bash
   python scripts/setup_dialects.py
   ```
2. **You should see:**
   ```
   🎭 Setting up dialect samples...
   Found 5 dialect samples:
     - Academic Scholar
     - Christian Conservative
     - Crossfit Bro
     - La Hippie
     - Startup Techie
   ✅ Dialect setup complete!
   ```

#### Run the Application
1. **Type:**
   ```bash
   streamlit run main.py
   ```
2. **You should see:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
3. **Your browser should automatically open** showing the EchoLens app
4. **If it doesn't open automatically,** copy the URL and paste it in your browser

#### Test the App
1. **You should see the beautiful EchoLens interface**
2. **Try pasting some text** in the input area
3. **Click "🧠 Reveal My Influences"**
4. **You should see analysis results!**

### Step 8: Deploy to the Internet (Optional)

#### Push to GitHub
1. **Go to [github.com](https://github.com) and sign in**
2. **Click the "+" icon** → "New repository"
3. **Name it "echolens"**
4. **Click "Create repository"**
5. **In VS Code terminal, type:**
   ```bash
   git add .
   git commit -m "Initial EchoLens setup"
   git remote add origin https://github.com/yourusername/echolens.git
   git push -u origin main
   ```
   *(Replace `yourusername` with your GitHub username)*

#### Deploy to Streamlit Cloud
1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Select your `echolens` repository**
5. **Set Main file path to:** `main.py`
6. **Click "Deploy"**
7. **Go to App settings → Secrets**
8. **Add your API key in TOML format:**
   ```toml
   OPENAI_API_KEY = "sk-proj-your-actual-key-here"
   ```
9. **Click "Save"**
10. **Your app will be live at:** `https://your-app-name.streamlit.app`

## 🆘 Troubleshooting

### "Command not found" errors
- **Make sure you've activated your virtual environment:** `source venv/bin/activate`
- **You should see `(venv)` in your terminal prompt**

### "Module not found" errors
- **Activate your virtual environment:** `source venv/bin/activate`
- **Reinstall packages:** `pip install -r requirements.txt`

### API key errors
- **Check your `.env` file** - make sure the API key starts with `sk-`
- **Make sure there are no extra spaces** around the `=` sign
- **Verify your OpenAI account has credits**

### App won't start
- **Make sure you're in the right directory:** `pwd` should show `.../echolens`
- **Try:** `python -m streamlit run main.py`

### "Permission denied" errors
- **Make sure you're in the echolens folder:** `cd ~/Desktop/echolens`

## 🔄 Daily Usage

Every time you want to work on EchoLens:

1. **Open VS Code**
2. **Open your echolens folder**
3. **Open Terminal in VS Code**
4. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```
5. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## 🎯 What's Next?

Now that you have EchoLens running, you can:
- **Analyze your own writing** to see your influences
- **Add new dialect samples** by creating `.txt` files in `data/dialects/samples/`
- **Customize the analysis** by modifying the code
- **Share your app** with others using the Streamlit Cloud URL

## 📞 Getting Help

If you run into issues:
1. **Check the troubleshooting section above**
2. **Make sure you followed each step exactly**
3. **Check that your virtual environment is activated** (`(venv)` should show in terminal)
4. **Verify your API key is correct** in the `.env` file

## 🏁 Success Checklist

- ✅ Python installed and working  
- ✅ VS Code installed with Python extension  
- ✅ Project downloaded and opened in VS Code  
- ✅ Virtual environment created and activated  
- ✅ Required packages installed  
- ✅ OpenAI API key added to `.env` file  
- ✅ Dialect samples initialized  
- ✅ App runs locally at `http://localhost:8501`  
- ✅ Analysis works when you input text  
- ✅ (Optional) App deployed to Streamlit Cloud  

**Congratulations! You now have EchoLens running and can start exploring the hidden influences in your language! 🎉**

## 📄 License

This project is open source. Feel free to contribute and improve EchoLens!
