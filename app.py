import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from gen import load_data, get_visualization_code
from recommendation import get_visualization_recommendations

# Load data
data = load_data()

# Page configuration
st.set_page_config(layout="centered")

# Title and subheader
st.header("Cafe-Chatbot")
st.subheader("GPT-Driven Data Visualization Chatbot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    if chat["role"] == "user" and chat["content_type"] == "text":
        st.markdown(f"**You:** {chat['content']}")
    elif chat["role"] == "assistant" and chat["content_type"] == "image":
        #st.markdown("**Cafe-Chatbot:**")
        st.image(chat["content"])
    elif chat["role"] == "assistant" and chat["content_type"] == "text":
         st.markdown(f"**Cafe-Chatbot:** {chat['content']}")

# Function to add message to chat history
def add_to_chat(role, content_type, content):
    st.session_state.chat_history.append({
        "role": role,
        "content_type": content_type,
        "content": content
    })
    if role == "user" and content_type == "text":
        st.markdown(f"**You:** {content}")
    elif role == "assistant" and content_type == "image":
        #st.markdown("**Cafe-Chatbot:**")
        st.image(content)
    elif role == "assistant" and content_type == "text":
        st.markdown(f"**Cafe-Chatbot:** {content}")

# Input for user query (fixed at the bottom, centered)
with st.sidebar:
    user_input = st.text_input("Ask a question or request a visualization:", key="user_input", max_chars=500)
    button=st.button("Send")

if button:
    if user_input:
        add_to_chat("user", "text", user_input)
        recom=get_visualization_recommendations(user_input, data)
        text=(f"I recommend to plot a {recom}")
        add_to_chat("assistant", "text", text)
        generated_code = get_visualization_code(recom, user_input, data).replace('```', '').replace('python', '')
        exec(generated_code, {"data": data, "plt": plt, "pd": pd})
        output_path="generated_plot.png"
        plt.savefig(output_path, format="png")
        img=Image.open("generated_plot.png")
        add_to_chat("assistant", "image", img)
        plt.clf()
