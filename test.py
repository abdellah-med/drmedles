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
First_messages = "Just act like a doctor, that named dr.Medles Abdellah , and respond with short naturel answers , like a real doctor "
if "messages" not in st.session_state:
    st.session_state.messages = []


if len(st.session_state.messages) == 0:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": First_messages,
            }
        ],
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
image_path = "/home/abdellah/Documents/LLM_medical_diagnosis/assests/pic1.jpg"  # Update this path to where your image is stored

# Encode the image
base64_image = get_base64_image(image_path)

# Custom CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)




# App Title and Description
st.title("🩺 Dr. Medles - General Practitioner ")
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


    st.write("### Conversation History:")
    for i, message in enumerate(st.session_state.messages):
    # Skip the first pair of messages (user's first input and AI's first response)
        if i > 1:  # Change this to "if i > 1" to skip both the user's first input and AI's first response
            if message["role"] == "user":
                st.write(f"**You**: {message['content']}")
            else:
                st.write(f"**AI**: {message['content']}")
                st.write("---")
    






    # Make API call to Groq with the entire conversation history
    with st.spinner("Huuummmmm.."):
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content

    # Add the AI's response to the history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display the AI's response and refresh the conversation history
    st.success("Response from AI:")
    st.write(response)