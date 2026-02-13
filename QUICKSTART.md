# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Python Packages (2 minutes)
```bash
pip install -r requirements.txt
```

### 2. Get HuggingFace Token (1 minute)
- Visit: https://huggingface.co/settings/tokens
- Click "New token"
- Copy the token

### 3. Set Up Environment (30 seconds)
Create `.env` file:
```bash
HF_TOKEN=paste_your_token_here
```

### 4. Personalize Knowledge Base (1 minute)
Edit files in `knowledge_base/` folder:
- `personality.txt` - Her traits and quirks
- `memories.txt` - Your special moments
- `preferences.txt` - What she loves

### 5. Launch! (30 seconds)
```bash
streamlit run app.py
```

Browser opens automatically at http://localhost:8501

---

## First Time Using the App

### Start with Chat
1. Go to "💬 Chat with Her"
2. Say hi: "Hey babe, how are you?"
3. Ask about memories: "Remember our first date?"

### Add a Memory
1. Go to "📸 Memory Timeline"
2. Click "➕ Add New Memory"
3. Add your first date or a special moment
4. Upload a photo if you have one

### Try the Journal
1. Go to "📔 Journal"
2. Write a quick entry about your day
3. Select your mood
4. Save it

---

## Customization Checklist

Before gifting, make sure to:

- [ ] Replace sample knowledge base with real information
- [ ] Add at least 5 meaningful memories with photos
- [ ] Test the chatbot with different questions
- [ ] Customize the greeting message
- [ ] Add your relationship's inside jokes
- [ ] Include her favorite things and preferences
- [ ] Write about your special traditions
- [ ] Add photos to the photos folder

---

## Common First-Time Issues

**"Module not found" error**
→ Run: `pip install -r requirements.txt`

**"HF_TOKEN not set" error**
→ Create `.env` file with your token

**Chatbot gives generic responses**
→ Add more details to knowledge base files

**App won't start**
→ Make sure you're in the project directory
→ Run: `streamlit run app.py`

---

## Tips for Best Experience

1. **Be Specific**: Instead of "she likes movies", write "she loves watching romantic comedies, especially 'The Notebook', and always cries at the ending"

2. **Add Context**: Include WHY things are special, not just WHAT happened

3. **Use Her Voice**: Write memories as she would tell them

4. **Update Often**: Add new memories as they happen

5. **Quality over Quantity**: 5 detailed memories > 20 generic ones

---

## Example Questions to Ask the Chatbot

- "What's my favorite food?"
- "Tell me about our first date"
- "What should we do this weekend?"
- "Remember that funny thing that happened?"
- "What do you love about me?"
- "What's your dream vacation?"

---

## Next Steps

Once you're comfortable:
1. Add more memories regularly
2. Explore the timeline visualizations
3. Encourage her to use the journal
4. Share cute moments from your chats
5. Keep the knowledge base updated

---

**Ready to impress? Run the app and enjoy! 💕**
