import streamlit as st
import matplotlib.pyplot as plt
from gen import load_data, get_visualization_code

# Page configuration
st.set_page_config(layout="centered")  # Center layout without sidebar

# Title and subheader
st.title("Cafe-Chatbot")
st.subheader("GPT-Driven Data Visualization Chatbot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to add message to chat history
def add_to_chat(role, message):
    st.session_state.chat_history.append({"role": role, "message": message})

# Display chat history in a scrollable container
with st.container():
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['message']}")
        elif chat["role"] == "assistant":
            st.markdown(f"**Cafe-Chatbot:** {chat['message']}")

# Input for user query
user_query = st.text_input("Ask a question or request a visualization:", key="user_input")

# Button to submit query
if st.button("Send"):
    if user_query:
        # Add user's question to chat history
        add_to_chat("user", user_query)

        # Load data and get GPT response
        data = load_data()
        explanation, generated_code = get_visualization_code(user_query, data)
        
        # Add explanation to chat history
        add_to_chat("assistant", explanation)
        
        # Add generated code to chat history
        add_to_chat("assistant", "Generated Code:\n" + generated_code)
        
        # Display explanation and code
        st.markdown("## Explanation")
        st.markdown(explanation)
        
        st.markdown("## Generated Code")
        st.code(generated_code, language="python")

        # Attempt to execute generated code and display visualization
        try:
            exec(generated_code)
            st.pyplot(plt.gcf())
            plt.clf()  # Clear the plot after displaying to prevent overlap
        except Exception as e:
            error_message = f"Error executing code: {e}"
            add_to_chat("assistant", error_message)
            st.error(error_message)
        
        # Clear the user input
        st.session_state.user_input = ""
