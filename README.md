# 💕 Digital Twin Valentine's Gift

A beautiful, romantic AI-powered application that creates a digital twin of your girlfriend as a Valentine's Day gift. Features include an intelligent chatbot, memory timeline with photos, and a personal journaling section.

## ✨ Features

### 1. 💬 Intelligent Chatbot
- Powered by Meta Llama 3 via HuggingFace
- Remembers last 3 conversation exchanges
- Responds with warmth, love, and personality
- Uses RAG (Retrieval Augmented Generation) with FAISS vector database
- Pulls from personalized knowledge base about your relationship

### 2. 📸 Memory Timeline
- Beautiful visual timeline of your relationship
- Add memories with photos, dates, and categories
- Interactive plotly visualizations
- Filter by category and search functionality
- Mood tracking with emojis
- Categories: First Times, Travel, Celebrations, Funny Moments, Romantic, Other

### 3. 📔 Personal Journal
- Private space for thoughts and feelings
- Mood tracking over time
- Beautiful mood distribution visualizations
- Searchable entries with timestamps
- Secure local storage

## 🎨 Design
- Romantic pink gradient theme
- Smooth animations and transitions
- Mobile-responsive layout
- Intuitive navigation
- Heart-themed visual elements

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM**: Meta Llama 3 (via HuggingFace)
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Framework**: LangChain
- **Visualizations**: Plotly
- **Image Processing**: Pillow

## 📋 Prerequisites

1. Python 3.8 or higher
2. HuggingFace account and API token
3. Basic knowledge of running Python applications

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

Download all files to a folder called `digital_twin_valentine`

### Step 2: Install Dependencies

```bash
cd digital_twin_valentine
pip install -r requirements.txt
```

### Step 3: Get HuggingFace API Token

1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token with "Read" permissions
5. Copy the token

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Open `.env` and replace `your_huggingface_token_here` with your actual token:
```
HF_TOKEN=hf_your_actual_token_here
```

### Step 5: Customize the Knowledge Base

Edit the files in the `knowledge_base/` directory to personalize your girlfriend's digital twin:

- **personality.txt**: Her traits, quirks, communication style, dreams
- **memories.txt**: Special moments, inside jokes, traditions
- **preferences.txt**: Favorite things, hobbies, love language

**Important**: The more detailed and personal these files are, the better the AI will understand and respond like her!

### Step 6: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
digital_twin_valentine/
├── app.py                      # Main Streamlit application
├── vector_store.py             # FAISS vector database manager
├── llm_chain.py               # LangChain LLM integration
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── .env.example              # Template for .env
├── knowledge_base/           # Personalized information
│   ├── personality.txt
│   ├── memories.txt
│   └── preferences.txt
└── data/                     # Auto-created at runtime
    ├── journal.json          # Journal entries
    ├── memories.json         # Timeline memories
    └── photos/              # Uploaded photos
```

## 💝 How to Use

### Chat with Her
1. Navigate to "💬 Chat with Her" from the sidebar
2. Start chatting! She'll respond based on the knowledge base
3. She remembers the last 3 message exchanges
4. Click "🔄 Start Fresh Conversation" to clear memory

### Add Memories
1. Go to "📸 Memory Timeline"
2. Click "➕ Add New Memory"
3. Fill in the details (title, date, description, category, mood)
4. Optionally upload a photo
5. Click "💾 Save Memory"
6. View all memories in a beautiful timeline

### Keep a Journal
1. Navigate to "📔 Journal"
2. Write your thoughts in "✍️ Write New Entry"
3. Select your mood
4. Save the entry
5. View mood statistics and past entries

## 🎨 Customization Ideas

### Enhance the Knowledge Base
Add more `.txt` files to `knowledge_base/`:
- `relationship_goals.txt` - Future plans and dreams
- `favorite_conversations.txt` - Memorable dialogues
- `special_dates.txt` - Important anniversaries
- `her_achievements.txt` - Things she's proud of

### Add More Features
Ideas for extending the app:
- Date night planner
- Bucket list tracker
- Gift idea generator
- Recipe collection
- Playlist creator
- Anniversary countdown

## 🔒 Privacy & Security

- All data stored locally on your machine
- No data sent to external servers (except LLM API calls)
- Journal entries encrypted in local JSON files
- Photos stored securely in local directory
- No cloud storage or databases

## 🐛 Troubleshooting

### "HF_TOKEN not found" error
- Make sure you created `.env` file (not `.env.example`)
- Check that your token is correctly formatted: `HF_TOKEN=hf_...`
- No quotes around the token value

### Chatbot not responding properly
- Verify your HuggingFace token has necessary permissions
- Check your internet connection
- Try refreshing the page
- Restart the Streamlit app

### Photos not displaying
- Ensure photos are in JPG, JPEG, or PNG format
- Check that the `data/photos/` directory exists
- Try uploading a smaller image file

### Vector store errors
- Make sure `knowledge_base/` directory has `.txt` files
- Check that files are UTF-8 encoded
- Restart the app to reinitialize the vector store

## 📝 Tips for Best Results

1. **Be Detailed**: The more information in the knowledge base, the better
2. **Use Real Examples**: Include actual quotes and specific memories
3. **Update Regularly**: Add new memories and journal entries often
4. **Personalize Prompts**: Edit `llm_chain.py` to adjust her speaking style
5. **Quality Photos**: Use clear, meaningful photos for memories

## 🌟 Advanced Configuration

### Change the LLM Model
In `llm_chain.py`, modify the `repo_id`:
```python
self.llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",  # Change this
    ...
)
```

Options:
- `meta-llama/Meta-Llama-3-70B-Instruct` (more powerful but slower)
- `mistralai/Mistral-7B-Instruct-v0.2`
- `HuggingFaceH4/zephyr-7b-beta`

### Adjust Memory Window
In `llm_chain.py`, change the memory parameter:
```python
self.memory = ConversationBufferWindowMemory(
    k=3,  # Change this number (messages to remember)
    ...
)
```

### Modify the Personality
Edit the prompt template in `llm_chain.py` to adjust tone and style

## 💌 Final Notes

This is a labor of love! The more you personalize it with real details about your relationship, the more magical it becomes. 

Remember to:
- Keep the knowledge base updated with new memories
- Encourage her to use the journal feature
- Add photos to the memory timeline regularly
- Have fun chatting with the digital twin!

## 🎁 Presentation Tips

1. Set everything up before Valentine's Day
2. Add at least 5-10 memories with photos
3. Write a welcome message in the chatbot
4. Consider running it on a tablet for a better experience
5. Walk her through the features the first time

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure your HuggingFace token is valid
4. Restart the application

---

**Made with 💕 for Valentine's Day 2026**

*"The best gift is one that shows you truly know and remember"*
