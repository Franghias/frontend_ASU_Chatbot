import streamlit as st

def main():
    """Main function to render the About page."""
    st.set_page_config(
        page_title="About - ASU Chatbot",
        page_icon="ℹ️",
        layout="wide"
    )

    # Custom CSS for styling
    st.markdown("""
    <style>
        .about-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0033A0; /* ASU Blue */
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #0033A0; /* ASU Blue */
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .tech-stack {
            background-color: #e9ecef;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="about-header">ℹ️ About the Angelo State University Chatbot</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This intelligent conversational AI is designed to provide comprehensive information about 
    Angelo State University. Built with a modern technology stack, it offers users quick 
    and accurate answers about the university's academic structure, personnel, and programs based on the official undergraduate catalog.
    """)
    
    st.header("🚀 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Intelligent Responses</h3>
            <p>Powered by Google's Gemini large language model to provide accurate, contextual answers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Knowledge Graph Core</h3>
            <p>Built on a Neo4j graph database for efficient information retrieval and understanding relationships between colleges, departments, and faculty.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Natural Conversation</h3>
            <p>Engage in natural language conversations to find the information you need.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📱 User-Friendly Interface</h3>
            <p>A clean and intuitive interface built with Streamlit that works seamlessly on desktop and mobile devices.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("🛠️ Technology Stack")
    
    st.markdown("""
    <div class="tech-stack">
        <h3>Backend</h3>
        <ul>
            <li><strong>FastAPI & Pydantic:</strong> For a high-performance, type-safe API.</li>
            <li><strong>Neo4j:</strong> Graph database for knowledge representation.</li>
            <li><strong>LangChain:</strong> Framework orchestrating the RAG (Retrieval-Augmented Generation) logic.</li>
            <li><strong>Google Gemini:</strong> The advanced language model powering the chatbot.</li>
        </ul>
        <h3>Frontend</h3>
        <ul>
            <li><strong>Streamlit:</strong> For rapid web application development and a real-time chat interface.</li>
        </ul>
        <h3>Data Processing</h3>
        <ul>
            <li><strong>PyMuPDF & LangChain:</strong> For parsing and chunking the source PDF document.</li>
            <li><strong>SpaCy:</strong> For Named Entity Recognition (NER) to identify people in the text.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>© 2025 Angelo State University. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()