import streamlit as st
import requests

# Define the URL of your backend API
BACKEND_URL = "http://localhost:5000/chat"  # Replace with your actual backend URL

st.title("💰 Personal Finance Chatbot")
st.markdown("Hello! I can help with your questions on savings, taxes, and investments. I can also generate budget summaries and spending insights.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user query to the backend and get the response
    try:
        # Here we'll need to send a user profile as well to support the demographic-aware feature
        # For simplicity, we'll hardcode it for now. You can add a selection box later.
        user_type = "professional"  # Can be "student" or "professional"
        payload = {"query": prompt, "user_type": user_type}
        
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                bot_response = response.json().get("response")
                # Add bot response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                # Display bot response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
            else:
                st.error(f"Error from backend: {response.text}")
    except requests.exceptions.ConnectionError as e:
        st.error(f"Could not connect to the backend server. Please ensure the backend is running. Error: {e}")