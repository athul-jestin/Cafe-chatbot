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
    col=', '.join(data.columns)
    gpt_prompt = (
        f"Generate Python code using pandas and matplotlib for the following dataset analysis "
        f"or visualization task. First, provide a brief explanation of the approach, "
        f"then provide the code.\n\nDataset columns: {col}\nTask: {prompt}\n"
    )

    response = openai.ChatCompletion.create(  # Use ChatCompletion instead of Chat
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code and explanations for data visualization."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=300,
        temperature=0.5
    )

    message_content = response['choices'][0]['message']['content'].strip()

    # Separate the explanation and code if possible (using a simple split approach here)
    explanation, generated_code = message_content.split('\n', 1)  # Split the explanation from the code

    return explanation, generated_code
