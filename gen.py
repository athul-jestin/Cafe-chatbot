import openai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Function to load data
def load_data():
    data = pd.read_pickle("cleaned_data.pkl")
    return data

# Function to get GPT-3.5-generated code for visualization
def get_visualization_code(user_input, recom, data): 
    col_names = ', '.join(data.columns)
    sample_data = data.head(3).to_dict()
    gpt_prompt = (
        f"Based on the following dataset and user request, generate Python code using pandas and matplotlib "
        f"to create a {recom} visualization. Do not include any explanation, symbols, or extra text. "
        f"Use 'data' as the DataFrame name, assuming it has 2000+ rows.\n\n"
        f"Column Names: {col_names}\n"
        f"Sample Data (first 3 rows): {sample_data}\n\n"
        f"User Request: {user_input}\n"
        f"Task: Generate only the code for a {recom} visualization based on the dataset.\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates only Python code for data visualization based on the user's request and dataset structure. Provide no explanations or additional text, only the code."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    generated_code = response['choices'][0]['message']['content'].strip()
    return generated_code
