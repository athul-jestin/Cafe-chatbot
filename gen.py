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
    col_names=', '.join(data.columns)
    sample_data = data.head(3).to_dict()  # Convert first few rows to a dictionary format

    # Create the prompt including column names and a few rows of sample data
    gpt_prompt = (
        f"Analyze the following dataset based on the request below and generate Python code using pandas and matplotlib "
        f"to complete the analysis or create a visualization. First, provide a brief explanation of the approach, "
        f"then generate the code. Sample data is given with only 3 rows, generate the code assuming that there are 2000+ rows, delfine the data frame in the codes as df\n\n"
        f"Column Names: {col_names}\n"
        f"Sample Data (first 3 rows): {sample_data}\n\n"
        f"Task: {prompt}\n"
    )

    response = openai.ChatCompletion.create(  # Use ChatCompletion instead of Chat
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates only code line for data visualization, without any other sentences and remove all commands and other symbols."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    message_content = response['choices'][0]['message']['content'].strip()

    # Separate the explanation and code if possible (using a simple split approach here)
    explanation, generated_code = message_content.split('\n', 1)  # Split the explanation from the code

    return generated_code
