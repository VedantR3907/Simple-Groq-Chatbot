import json
import os
from typing import List, Dict
import streamlit as st

DATABASE_FILE = os.path.join(os.path.dirname(__file__), '..', 'database.json')

async def read_chat_history(limit: int = 999999) -> List[Dict[str, str]]:
    try:
        with open(DATABASE_FILE, 'r') as file:
            data = json.load(file)
            # Return the last `limit` entries
            return data[-limit:]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

async def format_chat_history(chat_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    formatted_history = []
    
    for entry in chat_history:
        # Convert each entry to the new format
        if "user" in entry:
            formatted_history.append({
                "role": "user",
                "content": entry["user"]
            })
        if "assistant" in entry:
            formatted_history.append({
                "role": "assistant",
                "content": entry["assistant"]
            })
    
    return formatted_history

def load_chat_history() -> List[Dict[str, str]]:
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return []

def display_chat_history(chat_history: List[Dict[str, str]]):
    for entry in chat_history:
        if "user" in entry:
            with st.chat_message("HUMAN", avatar='./assets/user.png'):
                st.markdown(entry["user"])
        if "assistant" in entry:
            with st.chat_message("AI", avatar='./assets/meta.png'):
                st.markdown(entry["assistant"])