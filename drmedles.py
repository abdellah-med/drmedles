import os
import base64
import streamlit as st
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit App Interface
st.set_page_config(page_title="Dr.Medles office", page_icon="🩺")
First_messages = "i will give you lora question just make it correct dont add to much information just correct it "
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the conversation history with the first message if it's empty
if len(st.session_state.messages) == 0:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": First_messages}],
        model="llama3-70b-8192",
    )
    response = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "user", "content": First_messages})
    st.session_state.messages.append({"role": "assistant", "content": response})


# Path to your local image for background
image_path = "assests/pic1.jpg"  # Update to the correct path for your image

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

base64_image = get_base64_image(image_path)

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

st.title("🩺 Dr. Medles - General Practitioner")
st.write("Hello! I’m Dr. Medles. I'm here to listen and help with your health concerns. Feel free to share your symptoms or ask any questions.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# API Endpoint for LoRA model
lora_api_url = "http://127.0.0.1:8000/predict/"  # Update with the actual API URL

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("How are you feeling today?", placeholder="Describe your symptoms here...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from LoRA model
    with st.spinner("Getting initial response..."):
        try:
            response = requests.post(lora_api_url, json={"question": user_input})
            response.raise_for_status()
            lora_response = response.json().get("response", "I couldn't understand that. Please try again.")
        except requests.exceptions.RequestException as e:
            lora_response = f"Error: {str(e)}"

    # Use LLaMA to refine the LoRA response
    prompt = f"""here is Lora answer, just correct directly without adding anythings  , like i'ts your response  ,  and without adding to much information  , lora :  "{lora_response}    """
    
    with st.spinner("Refining response..."):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
        )
        refined_response = chat_completion.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": refined_response})

    # Display conversation history (hiding the first response)
    st.write("### Conversation History:")
    for i, message in enumerate(st.session_state.messages):
        if i > 1:  # Hide the first response
            if message["role"] == "user":
                st.markdown(f'<div class="message-box"><p class="message-user">You:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-box"><p class="message-ai">Dr. Medles:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
