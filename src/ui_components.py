import streamlit as st
from typing import Callable

# More robust and modern CSS for a cleaner, ChatGPT-like feel
CUSTOM_CSS = """
<style>
    /* Center the main content for a more focused view */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Main header style */
    .main-header {
        text-align: center;
        color: #1E1E1E;
        padding-bottom: 1rem;
    }
    /* Style for all chat messages for a consistent look */
    [data-testid="chat-message-container"] {
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    /* User message specific style */
    [data-testid="chat-message-container"]:has([data-testid="stChatMessageContent-user"]) {
        background-color: #f0f2f6; /* Light gray for user messages */
    }
    /* Assistant message specific style */
    [data-testid="chat-message-container"]:has([data-testid="stChatMessageContent-assistant"]) {
        background-color: #ffffff; /* White for assistant messages */
    }
    /* Style for the example question buttons */
    .stButton>button {
        border-radius: 0.5rem;
        background-color: #ffffff;
        color: #31333f;
        border: 1px solid #dcdfe6;
        transition: background-color 0.3s, color 0.3s, border-color 0.3s;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .stButton>button:hover {
        background-color: #f0f2f6;
        color: #000;
        border-color: #c0c4cc;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
"""

def setup_page():
    """Configures the Streamlit page and applies custom CSS."""
    st.set_page_config(
        page_title="ASU Chatbot",
        page_icon="🎓",
        layout="centered",  # Use 'centered' for a more focused chat experience
        initial_sidebar_state="expanded"
    )
    # Inject custom CSS for better styling
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar():
    """Renders the sidebar content."""
    with st.sidebar:
        st.header("About")
        st.markdown(
            "This chatbot provides information about Angelo State University "
            "using an AI-powered knowledge graph built with Neo4j."
        )
        st.header("Controls")
        if st.button("Clear Chat History", use_container_width=True, type="primary"):
            # A full clear is better to reset the 'show_examples' state
            st.session_state.clear()
            st.rerun()

def render_chat_messages():
    """
    Displays the chat message history from the session state, now with avatars.
    """
    if "messages" not in st.session_state:
        return

    for message in st.session_state.messages:
        # Use avatars for a more personal feel
        avatar = "🧑‍💻" if message["role"] == "user" else "🎓"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

def render_example_questions(prompt_handler: Callable[[str], None]):
    """
    Renders a set of clickable example questions ONLY if the chat is empty.
    """
    # ✅ UX IMPROVEMENT: Only show examples for a new chat session.
    if not st.session_state.get("messages", []):
        st.subheader("💡 Or try one of these questions:")
        example_questions = [
            "What undergraduate programs are in the College of Science and Engineering?",
            "Who is the dean of the Archer College of Health and Human Services?",
            "What are the admission requirements for new students?",
        ]
        
        cols = st.columns(len(example_questions))
        for i, question in enumerate(example_questions):
            with cols[i]:
                if st.button(question, key=f"example_{i}", use_container_width=True):
                    prompt_handler(question)