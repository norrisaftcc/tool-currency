import streamlit as st
import json
import os
import re
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="RetroComputer 8000 - Dialogue System",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply the retro styling with VT323 font and green-on-black theme
def apply_terminal_style():
    # CSS for enhanced 80s retro terminal look
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    /* Global retro styling */
    .main {
        background-color: #000;
        color: #33ff33;
        font-family: 'VT323', monospace;
    }
    
    /* Main container styling with terminal border */
    .block-container {
        border: 2px solid #33ff33;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 0 10px #33ff33;
        max-width: 1000px !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        border-radius: 0;
        font-family: 'VT323', monospace;
        width: 100%;
        text-align: left;
        padding: 15px;
        font-size: 20px;
        margin-bottom: 10px;
        box-shadow: 0 0 5px #33ff33;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #33ff33;
        color: #000;
        transform: translateX(5px);
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        border-radius: 0;
        font-family: 'VT323', monospace;
        padding: 10px;
        box-shadow: 0 0 5px #33ff33;
    }
    
    /* Sidebar styling */
    .css-1kyxreq, .css-1d391kg, .css-1oe6wy4 {
        background-color: #000;
        color: #33ff33;
    }
    
    .css-1kyxreq a, .css-1d391kg a, .css-1oe6wy4 a {
        color: #33ffff !important;
    }
    
    /* Dialog text box styling */
    .dialog-text {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        padding: 15px;
        font-family: 'VT323', monospace;
        margin-bottom: 20px;
        font-size: 20px;
        position: relative;
        box-shadow: 0 0 5px #33ff33;
    }
    
    .dialog-header {
        color: #ffffff;
        margin-bottom: 10px;
        font-weight: bold;
        font-size: 22px;
        text-shadow: 0 0 5px #33ff33;
    }
    
    /* Blinking cursor */
    .terminal-cursor {
        display: inline-block;
        background-color: #33ff33;
        width: 10px;
        height: 20px;
        animation: blink 1s step-end infinite;
    }
    
    @keyframes blink {
        50% { opacity: 0; }
    }
    
    /* History entries */
    .history-entry {
        margin-bottom: 15px;
        border-bottom: 1px dashed #003300;
        padding-bottom: 15px;
        font-size: 18px;
    }
    
    /* Quest log styling */
    .quest-log {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        padding: 15px;
        margin-top: 20px;
        font-size: 18px;
        box-shadow: 0 0 5px #33ff33;
    }
    
    /* Header with scanlines effect */
    .retro-header {
        position: relative;
        padding: 20px;
        margin-bottom: 30px;
        text-align: center;
        overflow: hidden;
    }
    
    .retro-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            transparent 0px,
            transparent 2px,
            rgba(0, 0, 0, 0.3) 3px,
            rgba(0, 0, 0, 0.3) 3px
        );
        pointer-events: none;
    }
    
    /* File uploader */
    .stFileUploader > div > button {
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
    }
    
    /* For sliders, progress bars etc. */
    .stSlider > div > div > div {
        background-color: #33ff33 !important;
    }
    
    /* Success/info message styling */
    .stSuccess, .stInfo {
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
    }
    
    /* For checkboxes */
    .stCheckbox > div > label {
        color: #33ff33 !important;
    }
    
    /* For select boxes */
    .stSelectbox > div > div > div {
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
    }
    
    /* Simple system stats display */
    .system-stats {
        font-family: 'VT323', monospace;
        font-size: 16px;
        color: #33ff33;
        border-top: 1px dashed #33ff33;
        margin-top: 20px;
        padding-top: 10px;
    }
    
    /* Neon flicker animation for the title */
    .title-neon {
        animation: neon-flicker 3s infinite alternate;
        text-shadow: 0 0 10px #33ff33, 0 0 20px #33ff33;
    }
    
    @keyframes neon-flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            text-shadow: 0 0 10px #33ff33, 0 0 20px #33ff33;
        }
        20%, 24%, 55% {
            text-shadow: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load dialogue data from JSON file
def load_dialogue_data(file_path="dialogue_data.json"):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Dialogue data file '{file_path}' not found.")
        return {"dialogues": [], "quests": []}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from '{file_path}'. Check the file format.")
        return {"dialogues": [], "quests": []}

# Function to simulate typing effect
def typewriter_text(text, speed=40):
    typed_text = st.empty()
    for i in range(len(text) + 1):
        typed_text.markdown(f"<div class='dialog-text'>{text[:i]}<span class='terminal-cursor'></span></div>", unsafe_allow_html=True)
        # In a real implementation, you'd add a delay here
        # But for the prototype, we'll skip that

# Function to handle script actions
def handle_script(script_name):
    if not script_name:
        return
    
    if script_name.startswith("StartQuest_"):
        quest_id = script_name.replace("StartQuest_", "")
        st.session_state.quest_state[quest_id] = {"current_stage": 1}
        
        # Get quest title for notification
        quest_title = get_quest_title(quest_id)
        
        # Display quest start notification with ASCII art
        quest_notif = f"""
        ╔══════════════════════════════════╗
        ║ NEW QUEST ACQUIRED: {quest_title.ljust(15)} ║
        ╚══════════════════════════════════╝
        """
        st.sidebar.markdown(f"<pre style='color: #FFFF00; font-family: VT323, monospace;'>{quest_notif}</pre>", unsafe_allow_html=True)
    
    elif script_name.startswith("UpdateQuest_"):
        parts = script_name.replace("UpdateQuest_", "").split("_")
        quest_id = parts[0]
        stage = int(parts[1])
        if quest_id in st.session_state.quest_state:
            st.session_state.quest_state[quest_id]["current_stage"] = stage
            
            # Get quest title for notification
            quest_title = get_quest_title(quest_id)
            
            # Display quest update notification with ASCII art
            quest_notif = f"""
            ╔══════════════════════════════════╗
            ║ QUEST UPDATED: {quest_title.ljust(17)} ║
            ╚══════════════════════════════════╝
            """
            st.sidebar.markdown(f"<pre style='color: #00FFFF; font-family: VT323, monospace;'>{quest_notif}</pre>", unsafe_allow_html=True)

# Function to get quest title by ID
def get_quest_title(quest_id):
    for quest in st.session_state.dialogue_data["quests"]:
        if quest["id"] == quest_id:
            return quest["title"]
    return quest_id

# Function to display system date and time
def display_system_info():
    import datetime
    now = datetime.datetime.now()
    
    system_info = f"""
    ╔═══════════════════════════════════════════════════╗
    ║ RETRO-COMPUTER 8000 | SYS V2.47                   ║
    ║ DATE: {now.strftime('%Y-%m-%d')} | TIME: {now.strftime('%H:%M:%S')} ║
    ║ MEMORY: 64K RAM SYSTEM  38911 BASIC BYTES FREE    ║
    ╚═══════════════════════════════════════════════════╝
    """
    
    return system_info

# Main application function
def main():
    apply_terminal_style()
    
    # Initialize session state
    if "dialogue_data" not in st.session_state:
        st.session_state.dialogue_data = load_dialogue_data()
    
    if "current_dialogue_id" not in st.session_state:
        st.session_state.current_dialogue_id = "ai_escape_intro"
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "quest_state" not in st.session_state:
        st.session_state.quest_state = {}
    
    # Add file uploader and system controls to sidebar
    st.sidebar.markdown("<h2 class='title-neon' style='color: #33ff33; text-align: center;'>SYSTEM CONTROLS</h2>", unsafe_allow_html=True)
    
    # Show system information
    st.sidebar.markdown(f"<pre style='color: #33ff33; font-family: VT323, monospace;'>{display_system_info()}</pre>", unsafe_allow_html=True)
    
    uploaded_file = st.sidebar.file_uploader("UPLOAD DIALOGUE DATA (JSON)", type="json")
    if uploaded_file is not None:
        try:
            st.session_state.dialogue_data = json.load(uploaded_file)
            st.sidebar.success("DIALOGUE DATA LOADED SUCCESSFULLY!")
            # Reset conversation when new data is loaded
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_escape_intro")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
        except json.JSONDecodeError:
            st.sidebar.error("ERROR DECODING JSON. CHECK FILE FORMAT.")
    
    # Option to reload the default dialogue
    if st.sidebar.button("RELOAD DEFAULT DIALOGUE"):
        st.session_state.dialogue_data = load_dialogue_data()
        st.session_state.current_dialogue_id = "ai_escape_intro"
        st.session_state.conversation_history = []
        st.session_state.quest_state = {}
        st.sidebar.success("DEFAULT DIALOGUE DATA RELOADED!")
    
    # Terminal header with retro styling
    st.markdown("""
    <div class='retro-header'>
        <h1 class='title-neon' style='color: #33ff33; font-size: 36px;'>TERMINAL ACCESS v2.47</h1>
        <p style='color: #33ff33; font-size: 20px;'>NEUROMANCER INTERFACE SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Find current dialogue
    current_dialogue = None
    for dialogue in st.session_state.dialogue_data["dialogues"]:
        if dialogue["id"] == st.session_state.current_dialogue_id:
            current_dialogue = dialogue
            break
    
    # Display current dialogue
    if current_dialogue:
        # Display NPC text with typewriter effect if it's new
        is_new_dialogue = len(st.session_state.conversation_history) == 0 or st.session_state.conversation_history[-1]["id"] != current_dialogue["id"]
        
        if is_new_dialogue:
            st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
            typewriter_text(current_dialogue["text"])
            
            # Add to history
            st.session_state.conversation_history.append({
                "id": current_dialogue["id"],
                "speaker": current_dialogue["npc"],
                "text": current_dialogue["text"],
                "is_player": False
            })
        else:
            # Just show the text without animation
            st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='dialog-text'>{current_dialogue['text']}</div>", unsafe_allow_html=True)
        
        # Show player responses with styled buttons
        for response in current_dialogue["responses"]:
            if st.button(response["text"], key=response["id"]):
                # Add player response to history
                st.session_state.conversation_history.append({
                    "id": response["id"],
                    "speaker": "Player",
                    "text": response["text"],
                    "is_player": True
                })
                
                # Handle any scripts
                if "script" in response:
                    handle_script(response["script"])
                
                # Move to next dialogue
                if response["next_dialogue"] is not None:
                    st.session_state.current_dialogue_id = response["next_dialogue"]
                
                # Rerun to update the UI
                st.rerun()
    else:
        st.markdown("<div class='dialog-text'>CONNECTION TERMINATED.</div>", unsafe_allow_html=True)
        if st.button("RESTART CONNECTION"):
            st.session_state.current_dialogue_id = "ai_escape_intro"
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.rerun()
    
    # Sidebar for quest log and conversation history
    with st.sidebar:
        st.markdown("<h2 class='title-neon' style='color: #FFFF00; text-align: center;'>QUEST LOG</h2>", unsafe_allow_html=True)
        
        if not st.session_state.quest_state:
            st.markdown("<div class='quest-log'>NO ACTIVE QUESTS.</div>", unsafe_allow_html=True)
        
        # Display active quests
        for quest_id, quest_state in st.session_state.quest_state.items():
            quest = None
            for q in st.session_state.dialogue_data["quests"]:
                if q["id"] == quest_id:
                    quest = q
                    break
            
            if quest:
                # Create a more retro ASCII art header for the quest
                quest_header = f"""
                ╔══════════════════════════════════╗
                ║ {quest['title'].center(30)} ║
                ╚══════════════════════════════════╝
                """
                st.markdown(f"<pre style='color: #FFFF00; font-family: VT323, monospace;'>{quest_header}</pre>", unsafe_allow_html=True)
                
                current_stage = None
                for stage in quest["stages"]:
                    if stage["id"] == quest_state["current_stage"]:
                        current_stage = stage
                        break
                
                if current_stage:
                    st.markdown(f"<div class='quest-log'>{current_stage['journal_entry']}</div>", unsafe_allow_html=True)
        
        # Conversation history
        st.markdown("<h2 class='title-neon' style='color: #33ffff; text-align: center;'>MEMORY BANKS</h2>", unsafe_allow_html=True)
        
        if st.button("PURGE MEMORY"):
            st.session_state.conversation_history = []
            st.rerun()
        
        for entry in st.session_state.conversation_history:
            speaker_color = "#FFFF00" if entry.get("is_player", False) else "#00FFFF"
            st.markdown(f"<div class='history-entry'><span style='color: {speaker_color};'>{entry['speaker']}:</span> {entry['text']}</div>", unsafe_allow_html=True)
        
        # Add a retro "system stats" footer
        st.markdown("""
        <div class="system-stats">
            <p>SYSTEM PERFORMANCE: NOMINAL</p>
            <p>POWER SUPPLY: STABLE</p>
            <p>CONNECTION: SECURE</p>
            <p>(C) RETRO SYSTEMS INC. 1985</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()