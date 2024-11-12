import openai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Function to load data
def load_data():
    data = pd.read_pickle("cleaned_data.pkl")  # Load the cleaned data from a pickle file
    return data

# Function to get GPT-3.5-generated code for visualization
def get_visualization_code(prompt, data):
    # Create the prompt to instruct GPT to generate code
    gpt_prompt = (
        f"Generate Python code using pandas and matplotlib for the following dataset analysis "
        f"or visualization task:\n\nDataset columns: {', '.join(data.columns)}\nTask: {prompt}\n"
    )
    
    # Request code generation from GPT-3.5 using the Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code for data visualization."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )
    
    # Extract the generated code
    code = response['choices'][0]['message']['content'].strip()
    return code
