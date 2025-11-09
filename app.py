import streamlit as st
from src.api_client import get_bot_response
from src.ui_components import setup_page, render_sidebar, render_chat_messages, render_example_questions

def handle_prompt(prompt: str):
    """
    Core logic to handle user input. This function updates the session state
    with the user's message and the bot's response, then triggers a rerun.
    It does NOT directly render any chat messages.
    """
    # 1. Add user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Get bot response and add it to the session state
    with st.spinner("ASU Bot is thinking..."):
        response_text = get_bot_response(prompt)
        if response_text:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        # Note: The api_client handles displaying critical connection errors to the user.

    # 3. Trigger a rerun. This is key to making the UI update correctly.
    # The entire script will run from top to bottom again.
    st.rerun()

# --- 1. Initial Page Setup ---
# This runs once at the start of each script run.
setup_page()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. Render UI elements from top to bottom ---
render_sidebar()
st.markdown('<h1 class="main-header">🎓 Angelo State University Chatbot</h1>', unsafe_allow_html=True)

# The chat messages are rendered here, based on the current session state.
# On the first run, this does nothing. After a prompt, it draws the full conversation.
render_chat_messages()

# The example questions and the chat input are rendered at the bottom.
render_example_questions(handle_prompt)

# --- 3. Handle New User Input ---
# The chat_input widget is sticky at the bottom.
if prompt := st.chat_input("Ask me anything about Angelo State University..."):
    # When the user enters a prompt, call the handler function.
    handle_prompt(prompt)