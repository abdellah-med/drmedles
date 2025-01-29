import os
import base64
import streamlit as st
import requests

# Streamlit App Interface
st.set_page_config(page_title="Dr. Medles Office", page_icon="🩺")

# Path to your local image for background
image_path = "assets/pic1.jpg"  # Update to the correct path for your image

# Function to encode the image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# Encode the image for custom background
base64_image = get_base64_image(image_path)

# Custom CSS for styling
if base64_image:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .message-user {{
            color: #1e90ff;
            font-weight: bold;
            padding: 5px 0;
        }}
        .message-ai {{
            color: #32cd32;
            font-weight: bold;
            padding: 5px 0;
        }}
        .message-box {{
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            max-width: 80%;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# App Title and Description
st.title("🩺 Dr. Medles - General Practitioner")
st.write("Hello! I’m Dr. Medles. I'm here to listen and help with your health concerns. Feel free to share your symptoms or ask any questions.")

# Initialize the conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome! How can I help you today?"}]

# Display the conversation history
st.write("### Conversation History:")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="message-box"><p class="message-user">You:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-box"><p class="message-ai">Dr. Medles:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)

# User input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("How are you feeling today?", placeholder="Describe your symptoms here...")
    submit_button = st.form_submit_button(label="Send")

# API Endpoint for your FastAPI backend
api_url = "http://127.0.0.1:8000/predict/"  # Update to your API's actual URL

# When the user sends a message
if submit_button and user_input.strip():
    # Add user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send the conversation history to the API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(api_url, json={"question": user_input})
            response.raise_for_status()  # Raise an error for bad responses
            assistant_response = response.json().get("response")
        except requests.exceptions.RequestException as e:
            assistant_response = f"Error: {str(e)}"

    # Add the assistant's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Dynamically update the conversation display
    st.write("### Conversation History:")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-box"><p class="message-user">You:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-box"><p class="message-ai">Dr. Medles:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
