import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq
import base64

# Load the .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit App Interface
st.set_page_config(page_title="Dr.Medles office", page_icon="🩺")
First_messages = "Just act like a doctor named Dr. Medles Abdellah, and respond with short, natural answers like a real doctor. Avoid interactive responses, such as show me this or that, because you cant see ...so  Be a doctor without letting him know you are an AI, and provide medical diagnoses as quickly as possible, and remember you can't see the patient like a real life because your are IA"
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

# Function to encode the image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Path to your local image
image_path = "assests/pic1.jpg"  # Update this path to where your image is stored

# Encode the image
base64_image = get_base64_image(image_path)

# Custom CSS to set the background image and adjust message box appearance
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
        background-color: rgba(0, 0, 0, 0.2); /* More transparent, darker box */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# App Title and Description
st.title("🩺 Dr. Medles - General Practitioner")
st.write("Hello! I’m Dr. Medles. I'm here to listen and help with your health concerns. Feel free to share your symptoms or ask any questions.")

# Create a form to handle input, so "Enter" key also works
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("How are you feeling today?", placeholder="Describe your symptoms here...")
    # Submit button to send input
    submit_button = st.form_submit_button(label="Send")

# When the "Send" button or "Enter" is pressed
if submit_button and user_input.strip():
    # Add the user's message to the history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Make API call to Groq with the entire conversation history
    with st.spinner("Huuummmmm.."):
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content

    # Add the AI's response to the history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display the conversation history (show both user and AI messages)
    st.write("### Conversation History:")
    for i, message in enumerate(st.session_state.messages):
        # Skip the first pair of messages (user's first input and AI's first response)
        if i > 1:  # Change this to "if i > 1" to skip both the user's first input and AI's first response
            if message["role"] == "user":
                st.markdown(f'<div class="message-box"><p class="message-user">You:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-box"><p class="message-ai">Dr. Medles:</p><p>{message["content"]}</p></div>', unsafe_allow_html=True)
