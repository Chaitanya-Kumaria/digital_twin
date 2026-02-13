# 📊 Data Structure Reference

This document shows the JSON structure of data files created by the application.

## Memory Data Structure

**File**: `data/memories.json`

```json
[
  {
    "id": 0,
    "title": "First Date",
    "date": "2024-02-14",
    "description": "We met at the coffee shop downtown. It was raining, and we talked for hours about everything under the sun.",
    "category": "First Times",
    "mood": "🥰",
    "photo": "data/photos/20240214_143022_first_date.jpg",
    "created_at": "2026-02-10 14:30:22"
  },
  {
    "id": 1,
    "title": "Paris Trip",
    "date": "2024-07-20",
    "description": "Our first international trip together. We saw the Eiffel Tower at sunset and it was magical.",
    "category": "Travel",
    "mood": "😍",
    "photo": "data/photos/20240720_190500_paris.jpg",
    "created_at": "2026-02-10 15:22:10"
  }
]
```

### Field Descriptions

- **id**: Unique integer identifier (auto-incremented)
- **title**: Short memorable title
- **date**: Date in YYYY-MM-DD format
- **description**: Detailed description of the memory
- **category**: One of: "First Times", "Travel", "Celebrations", "Funny Moments", "Romantic", "Other"
- **mood**: Emoji representing the mood (😢, 😊, 😄, 🥰, 😍)
- **photo**: Path to photo file (optional, can be null)
- **created_at**: Timestamp when memory was added

---

## Journal Data Structure

**File**: `data/journal.json`

```json
[
  {
    "id": 0,
    "title": "Beautiful Day",
    "content": "Today was amazing! We went to the park and had a picnic. The weather was perfect and we talked about our future plans. I'm so grateful for these moments.",
    "mood": "😄 Happy",
    "date": "2026-02-10",
    "time": "20:15:30",
    "created_at": "2026-02-10 20:15:30"
  },
  {
    "id": 1,
    "title": "Reflections",
    "content": "Been thinking a lot about how lucky I am. Every day with him feels like a gift. Even the simple moments are special.",
    "mood": "🥰 Amazing",
    "date": "2026-02-11",
    "time": "22:45:12",
    "created_at": "2026-02-11 22:45:12"
  }
]
```

### Field Descriptions

- **id**: Unique integer identifier (auto-incremented)
- **title**: Entry title (can be "Untitled Entry" if not provided)
- **content**: Full text of the journal entry
- **mood**: One of: "😢 Sad", "😐 Okay", "😊 Good", "😄 Happy", "🥰 Amazing"
- **date**: Date in YYYY-MM-DD format
- **time**: Time in HH:MM:SS format
- **created_at**: Full timestamp when entry was created

---

## Photo Naming Convention

Photos are stored in `data/photos/` with this naming pattern:

```
YYYYMMDD_HHMMSS_original_filename.jpg
```

**Examples**:
- `20240214_143022_first_date.jpg`
- `20240720_190500_paris_eiffel_tower.png`
- `20251225_120000_christmas_morning.jpeg`

**Supported formats**: JPG, JPEG, PNG

---

## Knowledge Base Structure

Files in `knowledge_base/` are plain text (.txt) files. They can be organized however you prefer, but here's a recommended structure:

### personality.txt
```
SECTION TITLE:

Information goes here in natural paragraphs.
Include specific details, examples, and anecdotes.

ANOTHER SECTION:

More information...
```

### memories.txt
```
Memory Name:
Detailed description of the memory including emotions, 
context, and what made it special.

Another Memory:
More details...
```

### preferences.txt
```
CATEGORY:
- List items
- More items

Another paragraph of preferences with natural language descriptions.
```

---

## Chat History (In-Memory)

Chat messages are stored in Streamlit session state (not persisted):

```python
[
  {
    "role": "user",
    "content": "Hey babe, how are you?"
  },
  {
    "role": "assistant", 
    "content": "Hi love! I'm doing great, especially now that I'm talking to you! 💕 How was your day?"
  }
]
```

---

## Vector Store (FAISS)

The vector store is automatically generated from knowledge base files:
- Embeddings are created using `sentence-transformers/all-MiniLM-L6-v2`
- Stored in memory (regenerated on each app start)
- Used for semantic search when chatbot needs context

---

## Backup Your Data

### Important Files to Backup:
1. `data/memories.json` - All your memories
2. `data/journal.json` - All journal entries  
3. `data/photos/` - All uploaded photos
4. `knowledge_base/*.txt` - Your personalized knowledge base
5. `.env` - Your HuggingFace token (keep secure!)

### Backup Command:
```bash
# Create a backup folder
mkdir backup_$(date +%Y%m%d)

# Copy all data
cp -r data/ backup_$(date +%Y%m%d)/
cp -r knowledge_base/ backup_$(date +%Y%m%d)/
cp .env backup_$(date +%Y%m%d)/
```

---

## Restore Data

To restore from backup:
```bash
# Copy files back
cp -r backup_20260210/data/* data/
cp -r backup_20260210/knowledge_base/* knowledge_base/
```

---

## Extending the Data Structure

Want to add new fields? Here's how:

### Adding to Memories
Edit `app.py`, find the memory creation section:
```python
new_memory = {
    "id": len(st.session_state.memories),
    # ... existing fields ...
    "new_field": new_value,  # Add your field here
}
```

### Adding to Journal
Similar process in the journal section of `app.py`

### Adding to Knowledge Base
Just create new `.txt` files in `knowledge_base/` folder!
The vector store will automatically include them.

---

## Data Privacy Note

- All data stored **locally** on your machine
- No external databases
- JSON files are human-readable
- Photos never leave your device
- Only LLM API calls go to HuggingFace (for chat responses)
- You have full control and ownership of your data

---

## Example: Full Data Setup

For a complete working example, your `data` folder might look like:

```
data/
├── memories.json         # 10-20 memories
├── journal.json         # 5-10 entries
└── photos/
    ├── 20240214_143022_first_date.jpg
    ├── 20240720_190500_paris.jpg
    ├── 20241015_120000_birthday.png
    └── 20251225_080000_christmas.jpg
```

Your `knowledge_base` folder:
```
knowledge_base/
├── personality.txt      # 500-1000 words
├── memories.txt        # 800-1200 words
└── preferences.txt     # 600-900 words
```

---

**Keep your data safe and enjoy your digital twin! 💕**
