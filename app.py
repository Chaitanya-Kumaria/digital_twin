import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import json
from pathlib import Path
from vector_store import SimpleTextSearch
from llm_chain import DigitalTwinChat
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="our journey LLM 💕",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for romantic styling with legible dark text
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #ffeef8 0%, #ffe5f1 50%, #ffd6eb 100%);
        color: #3d2b3a;
    }
    
    /* Force all text to be dark and legible */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp li, .stApp td, .stApp th {
        color: #3d2b3a !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffb3d9 0%, #ff99cc 100%);
    }
    
    [data-testid="stSidebar"], 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #4a1942 !important;
    }
    
    /* Headers */
    h1 {
        color: #d63384 !important;
        font-family: 'Georgia', serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2, h3, h4 {
        color: #c21e56 !important;
        font-family: 'Georgia', serif;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #2d2d2d !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff69b4 0%, #ff1493 100%);
        color: #fff !important;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255,20,147,0.4);
        color: #fff !important;
    }
    
    /* Text input and text areas */
    .stTextInput input, .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #ffb3d9;
        color: #333 !important;
        background-color: #fff !important;
    }
    
    /* Chat input styling */
    .stChatInput {
        background: transparent !important;
    }
    
    .stChatInputContainer {
        background: linear-gradient(135deg, #ffeef8 0%, #ffe5f1 50%, #ffd6eb 100%) !important;
        border-top: 2px solid #ffb3d9 !important;
        border-radius: 20px 20px 0 0 !important;
        padding-top: 15px !important;
        padding-bottom: 20px !important;
    }

    .stChatInput textarea {
        border-radius: 20px !important;
        border: 2px solid #ff69b4 !important;
        background-color: #fff !important;
        color: #333 !important;
    }
    
    /* Add bottom padding so chat messages don't hide behind fixed input */
    .stChatMessageContainer, [data-testid="stChatMessageContainer"] {
        padding-bottom: 80px !important;
    }
    
    /* Selectbox, multiselect, sliders */
    .stSelectbox div[data-baseweb] *,
    .stMultiSelect div[data-baseweb] *,
    [data-testid="stSlider"] * {
        color: #333 !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader, .streamlit-expanderHeader p {
        color: #c21e56 !important;
        font-weight: bold;
    }
    
    /* Info, warning, success, error boxes */
    .stAlert p, .stAlert span {
        color: #333 !important;
    }
    
    /* Radio buttons and labels in sidebar */
    .stRadio label, .stRadio p {
        color: #4a1942 !important;
    }
    
    /* Memory cards */
    .memory-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #ff69b4;
    }
    
    .memory-card h3, .memory-card p {
        color: #3d2b3a !important;
    }
    
    /* Photo gallery */
    .photo-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .photo-container:hover {
        transform: scale(1.05);
    }
    
    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #3d2b3a !important;
    }
    
    /* Italic/subheading text */
    .stMarkdown em {
        color: #6b4d6e !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_engine' not in st.session_state:
    st.session_state.chat_engine = None
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []
if 'memories' not in st.session_state:
    st.session_state.memories = []

# Data directories
DATA_DIR = Path("data")
JOURNAL_FILE = DATA_DIR / "journal.json"
MEMORIES_FILE = DATA_DIR / "memories.json"
PHOTOS_DIR = DATA_DIR / "photos"
KNOWLEDGE_BASE_DIR = "knowledge_base"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(exist_ok=True)
Path(KNOWLEDGE_BASE_DIR).mkdir(exist_ok=True)

# Load journal entries
def load_journal():
    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE, 'r') as f:
            return json.load(f)
    return []

# Save journal entries
def save_journal(entries):
    with open(JOURNAL_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

# Load memories
def load_memories():
    if MEMORIES_FILE.exists():
        with open(MEMORIES_FILE, 'r') as f:
            return json.load(f)
    return []

# Save memories
def save_memories(memories):
    with open(MEMORIES_FILE, 'w') as f:
        json.dump(memories, f, indent=2)

# Initialize data
st.session_state.journal_entries = load_journal()
st.session_state.memories = load_memories()

# Initialize chat engine
@st.cache_resource
def initialize_chat_engine():
    """Initialize the simple text search + chat engine (no transformers needed)."""
    text_search = SimpleTextSearch(KNOWLEDGE_BASE_DIR)
    chat_engine = DigitalTwinChat(text_search)
    return chat_engine

# Sidebar Navigation
st.sidebar.title("💕 Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["💬 Chat with Her", "📸 Memory Timeline", "📔 Journal"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💝 About")
st.sidebar.info("""
This is your girlfriend's digital twin,
created with love for Valentine's Day 2026.

She knows your memories, understands
your relationship, and responds with
the warmth and love you cherish.
""")

# Main content based on page selection
if page == "💬 Chat with Her":
    # Header photo
    header_photo = DATA_DIR / "chat_header.jpg"
    if header_photo.exists():
        st.image(str(header_photo), use_container_width=True)

    st.title("💕 Chat with Your Digital Twin")
    st.markdown("*She remembers your last 3 messages and speaks from the heart*")
    
    # Initialize chat engine if not already done
    if st.session_state.chat_engine is None:
        with st.spinner("💝 Waking up your digital twin..."):
            st.session_state.chat_engine = initialize_chat_engine()
    
    # Display chat messages (always show history)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - ALWAYS rendered so it never vanishes
    prompt = st.chat_input("Message her... 💕")
    
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from chat engine
        with st.chat_message("assistant"):
            with st.spinner("💭 Thinking..."):
                response = st.session_state.chat_engine.get_response(prompt)
                st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("🔄 Start Fresh Conversation"):
        st.session_state.messages = []
        if st.session_state.chat_engine:
            st.session_state.chat_engine.clear_memory()
        st.rerun()

elif page == "📸 Memory Timeline":
    st.title("📸 Our Memory Timeline")
    st.markdown("*A journey through our beautiful moments together*")
    
    # Add new memory
    with st.expander("➕ Add New Memory", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            memory_title = st.text_input("Memory Title", placeholder="e.g., First Date, Paris Trip")
            memory_date = st.date_input("Date", value=datetime.now())
            memory_description = st.text_area(
                "Description",
                placeholder="Tell the story of this special moment...",
                height=100
            )
        
        with col2:
            memory_category = st.selectbox(
                "Category",
                ["First Times", "Travel", "Celebrations", "Funny Moments", "Romantic", "Other"]
            )
            memory_mood = st.select_slider(
                "Mood",
                options=["😢", "😊", "😄", "🥰", "😍"],
                value="🥰"
            )
        
        uploaded_photo = st.file_uploader(
            "Add Photo (optional)",
            type=['png', 'jpg', 'jpeg'],
            key="memory_photo"
        )
        
        if st.button("💾 Save Memory"):
            if memory_title and memory_description:
                # Save photo if uploaded
                photo_path = None
                if uploaded_photo:
                    photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_photo.name}"
                    photo_path = PHOTOS_DIR / photo_filename
                    with open(photo_path, 'wb') as f:
                        f.write(uploaded_photo.getbuffer())
                    photo_path = str(photo_path)
                
                # Create memory object
                new_memory = {
                    "id": len(st.session_state.memories),
                    "title": memory_title,
                    "date": memory_date.strftime("%Y-%m-%d"),
                    "description": memory_description,
                    "category": memory_category,
                    "mood": memory_mood,
                    "photo": photo_path,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.memories.append(new_memory)
                save_memories(st.session_state.memories)
                st.success(f"✨ Memory '{memory_title}' saved!")
                st.rerun()
            else:
                st.error("Please fill in at least the title and description")
    
    # Display timeline
    if st.session_state.memories:
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            category_filter = st.multiselect(
                "Filter by Category",
                ["First Times", "Travel", "Celebrations", "Funny Moments", "Romantic", "Other"],
                default=[]
            )
        with col2:
            search_term = st.text_input("🔍 Search memories", placeholder="Search titles or descriptions...")
        
        # Filter memories
        filtered_memories = st.session_state.memories.copy()
        if category_filter:
            filtered_memories = [m for m in filtered_memories if m["category"] in category_filter]
        if search_term:
            filtered_memories = [
                m for m in filtered_memories 
                if search_term.lower() in m["title"].lower() or 
                   search_term.lower() in m["description"].lower()
            ]
        
        # Sort by date (newest first)
        filtered_memories.sort(key=lambda x: x["date"], reverse=True)
        
        st.markdown(f"### 💝 {len(filtered_memories)} Memories")
        
        # Create timeline visualization
        if len(filtered_memories) > 0:
            df_timeline = pd.DataFrame([
                {
                    "Date": m["date"],
                    "Title": m["title"],
                    "Category": m["category"],
                    "Mood": m["mood"]
                }
                for m in filtered_memories
            ])
            
            fig = px.scatter(
                df_timeline,
                x="Date",
                y="Category",
                size=[20]*len(df_timeline),
                color="Category",
                hover_data=["Title", "Mood"],
                title="Memory Timeline",
                color_discrete_map={
                    "First Times": "#FF69B4",
                    "Travel": "#FF1493",
                    "Celebrations": "#C71585",
                    "Funny Moments": "#DB7093",
                    "Romantic": "#FF6EC7",
                    "Other": "#FFB6C1"
                }
            )
            fig.update_traces(marker=dict(symbol="heart"))
            fig.update_layout(
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0)',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display memory cards
        for memory in filtered_memories:
            with st.container():
                st.markdown(f"""
                <div class="memory-card">
                    <h3>{memory['mood']} {memory['title']}</h3>
                    <p style="color: #666; font-size: 0.9em;">
                        📅 {memory['date']} | 🏷️ {memory['category']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(memory['description'])
                
                with col2:
                    if memory.get('photo') and Path(memory['photo']).exists():
                        try:
                            img = Image.open(memory['photo'])
                            st.image(img, use_container_width=True, caption=memory['title'])
                        except:
                            st.info("📷 Photo unavailable")
                
                st.markdown("---")
    else:
        st.info("💝 No memories yet! Start adding your special moments above.")

elif page == "📔 Journal":
    st.title("📔 Personal Journal")
    st.markdown("*A space for her thoughts and feelings*")
    
    # Add new journal entry
    with st.expander("✍️ Write New Entry", expanded=True):
        entry_title = st.text_input("Entry Title (optional)", placeholder="Today's thoughts...")
        entry_mood = st.select_slider(
            "How are you feeling?",
            options=["😢 Sad", "😐 Okay", "😊 Good", "😄 Happy", "🥰 Amazing"],
            value="😊 Good"
        )
        entry_content = st.text_area(
            "What's on your mind?",
            placeholder="Write your thoughts here...",
            height=200
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("💾 Save Entry"):
                if entry_content:
                    new_entry = {
                        "id": len(st.session_state.journal_entries),
                        "title": entry_title if entry_title else "Untitled Entry",
                        "content": entry_content,
                        "mood": entry_mood,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.journal_entries.append(new_entry)
                    save_journal(st.session_state.journal_entries)
                    st.success("✨ Journal entry saved!")
                    st.rerun()
                else:
                    st.error("Please write something before saving")
        
        with col2:
            if st.button("🔄 Clear"):
                st.rerun()
    
    # Display journal entries
    if st.session_state.journal_entries:
        st.markdown("---")
        st.markdown(f"### 📖 {len(st.session_state.journal_entries)} Journal Entries")
        
        # Mood statistics
        moods = [entry["mood"] for entry in st.session_state.journal_entries]
        mood_counts = pd.Series(moods).value_counts()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("#### Mood Overview")
            for mood, count in mood_counts.items():
                st.markdown(f"{mood}: {count} entries")
        
        with col2:
            fig = go.Figure(data=[go.Pie(
                labels=mood_counts.index,
                values=mood_counts.values,
                marker=dict(colors=['#FF69B4', '#FF1493', '#C71585', '#DB7093', '#FF6EC7'])
            )])
            fig.update_layout(
                title="Mood Distribution",
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Display entries (newest first)
        sorted_entries = sorted(
            st.session_state.journal_entries,
            key=lambda x: x["created_at"],
            reverse=True
        )
        
        for entry in sorted_entries:
            with st.expander(f"{entry['mood']} {entry['title']} - {entry['date']}"):
                st.markdown(f"*{entry['time']}*")
                st.markdown(entry['content'])
                
                if st.button(f"🗑️ Delete", key=f"delete_{entry['id']}"):
                    st.session_state.journal_entries = [
                        e for e in st.session_state.journal_entries 
                        if e['id'] != entry['id']
                    ]
                    save_journal(st.session_state.journal_entries)
                    st.success("Entry deleted")
                    st.rerun()
    else:
        st.info("📝 No journal entries yet. Start writing your first entry above!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #c21e56; padding: 20px;'>
    <p>💕 Made with love for Valentine's Day 2026 💕</p>
    <p style='font-size: 0.8em;'>Powered by AI, Inspired by Love</p>
</div>
""", unsafe_allow_html=True)