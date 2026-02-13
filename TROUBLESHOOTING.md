# 🔧 Troubleshooting Guide

## Installation Issues

### Problem: "pip: command not found"
**Solution**: 
- Install Python from python.org
- Make sure Python is added to PATH
- Try `python -m pip install -r requirements.txt`

### Problem: "Module not found" errors
**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements again
pip install -r requirements.txt

# If still failing, install packages individually:
pip install streamlit
pip install langchain
pip install langchain-community
pip install langchain-huggingface
pip install huggingface_hub
pip install faiss-cpu
pip install sentence-transformers
pip install python-dotenv
pip install Pillow
pip install pandas
pip install plotly
```

### Problem: FAISS installation fails on Windows
**Solution**:
```bash
# Try CPU version explicitly
pip install faiss-cpu

# Or use conda
conda install -c conda-forge faiss-cpu
```

---

## Configuration Issues

### Problem: "HF_TOKEN not found" or "Invalid token"
**Solutions**:

1. **Check .env file exists**:
```bash
# Windows
dir .env

# Mac/Linux
ls -la .env
```

2. **Verify .env format** (no quotes, no spaces):
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxx
```

3. **Get new token**:
- Go to https://huggingface.co/settings/tokens
- Create new token with READ access
- Copy entire token including `hf_` prefix

4. **Check file encoding**:
- Save .env as UTF-8 (not UTF-8 BOM)

### Problem: ".env file not loading"
**Solution**:
```bash
# Make sure .env is in the same directory as app.py
# Check current directory
pwd  # Mac/Linux
cd   # Windows

# List files
ls -la  # Mac/Linux
dir    # Windows
```

---

## App Launch Issues

### Problem: "streamlit: command not found"
**Solution**:
```bash
# Use python -m
python -m streamlit run app.py

# Or add to PATH (Mac/Linux)
export PATH="$HOME/.local/bin:$PATH"

# Or add to PATH (Windows)
# Add Python Scripts folder to System PATH
```

### Problem: "Port 8501 already in use"
**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8501 | xargs kill -9
```

### Problem: "Browser doesn't open automatically"
**Solution**:
- Manually open: http://localhost:8501
- Check firewall settings
- Try: `streamlit run app.py --server.headless false`

---

## Chatbot Issues

### Problem: "Chatbot gives generic/irrelevant responses"
**Root Causes**:
1. Empty or minimal knowledge base
2. Poor quality information in knowledge base
3. Vector store not initialized

**Solutions**:

1. **Enhance knowledge base**:
```
knowledge_base/
├── personality.txt     (min 500 words)
├── memories.txt        (min 800 words)
└── preferences.txt     (min 600 words)
```

2. **Add specific details**:
❌ Bad: "She likes movies"
✅ Good: "She loves romantic comedies, especially 'The Notebook'. She cries every time at the ending when Noah reads to Allie. We watch it together every Valentine's Day."

3. **Restart app** to reload vector store:
```bash
# Stop app (Ctrl+C)
# Start again
streamlit run app.py
```

### Problem: "Chatbot takes too long to respond"
**Solutions**:
1. **Internet connection**: Check your connection
2. **HuggingFace API**: May be rate-limited or down
3. **Try smaller model** (edit `llm_chain.py`):
```python
repo_id="meta-llama/Meta-Llama-3-8B-Instruct"  # Current
# Change to:
repo_id="mistralai/Mistral-7B-Instruct-v0.2"  # Faster
```

### Problem: "Chatbot doesn't remember conversation"
**Check**:
1. Memory is set to last 3 exchanges (6 messages)
2. After 3 exchanges, older messages are forgotten (this is normal)
3. To increase memory, edit `llm_chain.py`:
```python
self.memory = ConversationBufferWindowMemory(
    k=5,  # Change from 3 to 5 (or more)
    ...
)
```

### Problem: "API rate limit errors"
**Solutions**:
1. Wait a few minutes (HuggingFace free tier has limits)
2. Upgrade to HuggingFace Pro
3. Use different model
4. Space out your messages

---

## Memory Timeline Issues

### Problem: "Photos not displaying"
**Solutions**:

1. **Check file format**:
- Supported: JPG, JPEG, PNG
- Not supported: HEIC, WebP (convert first)

2. **Check file size**:
- Large files (>10MB) may be slow
- Resize images before uploading

3. **Check file path**:
```python
# In app.py, verify photos directory exists
import os
print(os.path.exists("data/photos"))  # Should be True
```

4. **Fix permissions** (Mac/Linux):
```bash
chmod -R 755 data/photos/
```

### Problem: "Timeline not showing all memories"
**Solutions**:
1. Check filters are not active
2. Clear search box
3. Check `data/memories.json` file:
```bash
cat data/memories.json  # Mac/Linux
type data\memories.json  # Windows
```

4. Restart app

### Problem: "Can't delete memories"
**Solution**:
- Check file permissions on `data/memories.json`
- Close other programs that might have the file open
- Restart app

---

## Journal Issues

### Problem: "Journal entries not saving"
**Solutions**:

1. **Check write permissions**:
```bash
# Mac/Linux
chmod 755 data/
chmod 644 data/journal.json

# Windows
# Right-click data folder → Properties → Security
# Ensure full control for your user
```

2. **Check disk space**:
```bash
# Mac/Linux
df -h

# Windows
# Check in File Explorer
```

3. **Verify JSON format**:
```bash
# Check if file is valid JSON
python -m json.tool data/journal.json
```

### Problem: "Mood chart not displaying"
**Solutions**:
1. Add at least 1 journal entry
2. Check browser console (F12) for errors
3. Clear browser cache
4. Update Plotly: `pip install --upgrade plotly`

---

## Performance Issues

### Problem: "App is slow/laggy"
**Solutions**:

1. **Clear cache**:
```bash
# Stop app
# Delete Streamlit cache
rm -rf ~/.streamlit/cache  # Mac/Linux
rmdir /s %USERPROFILE%\.streamlit\cache  # Windows
```

2. **Reduce image sizes**:
```bash
# Use image compression tools
# Or resize before upload
```

3. **Limit memories displayed**:
- Filter by category
- Use search to narrow results

4. **Restart app regularly**

### Problem: "High memory usage"
**Solutions**:
1. Close other browser tabs
2. Reduce memory window size in `llm_chain.py`
3. Use smaller embedding model
4. Clear old photos from `data/photos/`

---

## Data Issues

### Problem: "Lost all my data!"
**Prevention**:
```bash
# Create daily backup
mkdir -p backups
cp -r data/ backups/backup_$(date +%Y%m%d)/
cp -r knowledge_base/ backups/backup_$(date +%Y%m%d)/
```

**Recovery**:
```bash
# Restore from backup
cp -r backups/backup_YYYYMMDD/data/* data/
```

### Problem: "JSON file corrupted"
**Solutions**:

1. **Validate JSON**:
```bash
python -m json.tool data/memories.json
```

2. **Fix manually**:
- Open in text editor
- Look for syntax errors (missing commas, quotes)
- Use JSONLint online validator

3. **Start fresh**:
```bash
# Backup first!
cp data/memories.json data/memories.json.backup
# Replace with empty array
echo "[]" > data/memories.json
```

---

## Browser-Specific Issues

### Chrome/Edge
- Clear cache: Ctrl+Shift+Delete
- Disable extensions that might interfere
- Try incognito mode

### Firefox
- Clear cache: Ctrl+Shift+Delete
- Check if Enhanced Tracking Protection is interfering
- Try private window

### Safari
- Clear cache: Cmd+Option+E
- Check cookie settings
- Try private window

---

## Common Error Messages

### "FileNotFoundError: knowledge_base/"
**Solution**:
```bash
mkdir knowledge_base
# Add .txt files
```

### "PermissionError: data/memories.json"
**Solution**:
- Close Excel/text editors viewing the file
- Check file permissions
- Restart app

### "Connection timeout" when chatting
**Solution**:
- Check internet connection
- Verify HuggingFace API status: https://status.huggingface.co
- Try again in a few minutes

### "Out of memory" errors
**Solution**:
- Close other applications
- Reduce batch size
- Use smaller model
- Restart computer

---

## Getting Help

### Before asking for help:

1. **Check logs**:
```bash
# Terminal output when running app shows errors
# Save output: streamlit run app.py > debug.log 2>&1
```

2. **Try fresh install**:
```bash
# Create new virtual environment
python -m venv venv_fresh
source venv_fresh/bin/activate  # Mac/Linux
venv_fresh\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Verify system requirements**:
- Python 3.8+
- 4GB+ RAM
- Stable internet connection
- Modern browser (Chrome, Firefox, Edge, Safari)

### Useful commands for debugging:

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Streamlit version
streamlit version

# Test imports
python -c "import streamlit; import langchain; print('OK')"

# Verify HuggingFace token
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', os.getenv('HF_TOKEN')[:10])"
```

---

## Still Having Issues?

1. **Read the full README.md**
2. **Check QUICKSTART.md** for setup steps
3. **Review DATA_STRUCTURE.md** for file formats
4. **Try a fresh installation** in a new folder
5. **Check your internet connection** and firewall

---

**Most issues are solved by:**
1. Restarting the app
2. Checking the .env file
3. Adding more content to knowledge base
4. Clearing browser cache
5. Verifying file permissions

**Happy debugging! 💕**
