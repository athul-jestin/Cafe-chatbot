import streamlit as st
import matplotlib.pyplot as plt
from gen import load_data, get_visualization_code

# Load data (cache data loading for performance)
@st.cache_data
def cached_load_data():
    return load_data()

# Load the dataset
data = cached_load_data()

# Display dataset overview
st.title("Cafe-Chatbot")
st.subheader("GPT-Driven Data Visualization Chatbot")

# Get user input for visualization request
user_query = st.text_input("Ask a question or request a visualization:")

# Display GPT-generated code and execute visualization
if user_query:
    # Get code from GPT based on user query
    generated_code = get_visualization_code(user_query, data)
    
    # Display the generated code
    st.write("Generated Code:")
    st.code(generated_code, language="python")

    # Execute the generated code for visualization
    try:
        # Execute the generated code
        exec(generated_code)
        
        # Assume the generated code creates a figure named 'fig'
        st.pyplot(plt.gcf())  # Display the current figure
        plt.clf()  # Clear the plot after displaying to prevent overlap
    except Exception as e:
        st.error(f"Error executing code: {e}")
