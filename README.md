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

n/a


# 🔍 EchoLens - Complete Setup Guide

*"See what echoes through your words"*

EchoLens is an AI-powered tool that analyzes your writing to reveal the hidden influences shaping how you think, speak, and see reality. This guide will walk you through every step to get EchoLens running on your computer, even if you're not technical.

## 📋 What You'll Need Before Starting

- A Mac computer (this guide is written for Mac)
- Internet connection
- About 30-45 minutes
- An OpenAI API key (we'll show you how to get one)

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

## 📁 Project Structure

```
echolens/
├── main.py                     # Main app file
├── requirements.txt            # Required packages
├── .env                       # Your API keys (keep private!)
├── src/
│   └── ui/
│       └── streamlit_app.py   # Main interface
├── data/
│   └── dialects/
│       └── samples/           # Dialect text samples
├── scripts/
│   └── setup_dialects.py     # Setup script
└── docs/                      # Documentation
```

---

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

---

## 🎯 What's Next?

Now that you have EchoLens running, you can:
- **Analyze your own writing** to see your influences
- **Add new dialect samples** by creating `.txt` files in `data/dialects/samples/`
- **Customize the analysis** by modifying the code
- **Share your app** with others using the Streamlit Cloud URL

---

## 📞 Getting Help

If you run into issues:
1. **Check the troubleshooting section above**
2. **Make sure you followed each step exactly**
3. **Check that your virtual environment is activated** (`(venv)` should show in terminal)
4. **Verify your API key is correct** in the `.env` file

---

## 🏁 Success Checklist

✅ Python installed and working  
✅ VS Code installed with Python extension  
✅ Project downloaded and opened in VS Code  
✅ Virtual environment created and activated  
✅ Required packages installed  
✅ OpenAI API key added to `.env` file  
✅ Dialect samples initialized  
✅ App runs locally at `http://localhost:8501`  
✅ Analysis works when you input text  
✅ (Optional) App deployed to Streamlit Cloud  

**Congratulations! You now have EchoLens running and can start exploring the hidden influences in your language! 🎉**
