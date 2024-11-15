import streamlit as st
import openai
import os
import pandas as pd
from gen import load_data
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
openai.api_key=api_key

data = load_data()

def analyze_data(data):
    analysis = {
        "columns": data.columns.tolist(),
        "types": data.dtypes.apply(lambda x: x.name).to_dict(),
        "n_unique_values": data.nunique().to_dict(),
        "summary": data.describe(include='all').to_dict()
    }
    return analysis

def get_visualization_recommendations(user_request, data):

    analysis = analyze_data(data)
    messages = [
    {"role": "system", "content": "You are an assistant that recommends a single, best data visualization type based on data characteristics and user requests. Answer in one word only."},
    {"role": "user", "content": f"I have a dataset with the following structure and summary:\n\n{analysis}\n\nThe user has asked: {user_request}\n\nBased on the data characteristics, recommend the single best type of visualization to use for this dataset. Respond with only one word."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )
    recommendations = response.choices[0].message['content'].strip()
    return recommendations

