# -*- coding: utf-8 -*-

import pandas as pd
import google.generativeai as genai

# Load the CSV file
file_path = '../Data/processed_data.csv'
df = pd.read_csv(file_path)

# Sample 1000 random tweets
sampled_tweets = df['Original Sentence'].sample(n=1000, random_state=42).tolist()

# Convert the list of tweets to a formatted string
tweets_text = "\n".join(sampled_tweets)

# Configure the API
# You should generate your api key from https://aistudio.google.com/
genai.configure(api_key="AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg")
model = genai.GenerativeModel("gemini-1.5-pro-002")

# Define the query
user_query = "Query: How many kinds of product it discussed?\n"
base_query = "Please generate answers for the query based on the reference tweets below. You should summary rather than simply list."
query = user_query + base_query

# Combine query and tweets in the prompt
prompt = f"{query}\n\nReference Tweets:\n{tweets_text}"

# Generate the response
print("thinknig...")
try:
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")

