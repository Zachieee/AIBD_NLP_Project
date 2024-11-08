# -*- coding: utf-8 -*-

import pandas as pd
import google.generativeai as genai

# # Load the CSV file
# file_path = '../Data/processed_data.csv'
# df = pd.read_csv(file_path)

# # Sample 1000 random tweets for
# tweets = df['Original Sentence'].sample(n=1000, random_state=42).tolist()

# Load the CSV file with top tweets
file_path = 'top_tweets.csv'
df = pd.read_csv(file_path)

# Extract the "Original Sentence" column and convert it to a list
tweets = df['Original Sentence'].tolist()

# Convert the list of tweets to a formatted string
tweets_text = "\n".join(tweets)

# Configure the API
# You should generate your api key from https://aistudio.google.com/
genai.configure(api_key="AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg")
model = genai.GenerativeModel("gemini-1.5-pro-002")

# Define the query
user_query = "Query: what do people think of apple?\n"
base_query = "Please generate answers for the query based on the reference tweets below. \
              You should extract useful information from given tweets and make a summary. \
              Use bullet points to butify the output. \
              CAUTION: make it concise."
            #   Before that, I need you to polish the prompts by using this doc (https://platform.openai.com/docs/guides/prompt-engineering). \
            #   Use the polished prompt to generate the final anwser."
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

