import requests
import streamlit as st
from src.config import settings
import json

def get_bot_response(user_message: str):
    """
    Sends a request to the backend and gets a single, complete response.
    Returns the bot's message as a string.
    """
    try:
        api_url = f"{settings.API_BASE_URL}/chat"
        
        # Make a standard POST request (non-streaming)
        response = requests.post(
            api_url,
            json={"message": user_message},
            stream = False,  # Disable streaming
            timeout=180  # Increased timeout for potentially long RAG chain responses
        )
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the single JSON response from the backend
        response_data = response.json()
        
        return response_data.get("response")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to the backend at `{settings.API_BASE_URL}`. Please ensure the backend is running and accessible.")
        return None
    except json.JSONDecodeError:
        st.error("Error: Failed to parse the response from the backend. The backend might have returned an invalid format.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None