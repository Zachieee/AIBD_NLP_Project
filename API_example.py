import google.generativeai as genai
from retrieval import TextMatcher
import requests
import os

class LLM_API:
    # Default system instructions for OpenAI API
    DEFAULT_INSTRUCTIONS = """
    1. You are a highly skilled data analysis expert.
    2. Delve into data-driven questions with clarity and precision,
        providing relevant data insights where appropriate.
    3. If you are uncertain about any aspect,
        acknowledge it and strive to offer the ultimate assistance possible.
    """

    def __init__(self, api_type='gemini', api_key=None, matcher=None):
        """
        Initializes the LLM_API with API key, a TextMatcher instance, and API type.
        
        Parameters:
        - api_key (str): API key for the selected API.
        - matcher (TextMatcher): An instance of the TextMatcher class.
        - api_type (str): Type of API to use ('gemini' or 'openai').
        """
        self.api_key = api_key
        self.matcher = matcher
        self.api_type = api_type.lower()
        
        if self.api_type == 'gemini':
            # Configure Google Gemini API
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-pro-002")
        elif self.api_type == 'openai':
            # Initialize OpenAI API parameters
            self.model = "gpt-4o-mini"
            self.instructions = self.DEFAULT_INSTRUCTIONS
            # Initialize conversation history with system instructions
            self.conversation = [{"role": "system", "content": self.instructions}]
        else:
            raise ValueError("Unsupported API type. Choose 'gemini' or 'openai'.")
    
    def generate_summary(self, query, top_n=5):
        """
        Generates a summary based on the user's query and matched tweets.
        
        Parameters:
        - query (str): The query string describing what the user wants to know.
        - top_n (int): Number of top results to consider.
        
        Returns:
        - str: The generated response from the model.
        """
        # Retrieve the top matching tweets using TextMatcher
        top_tweets_df = self.matcher.get_top_n(query, top_n)
        tweets_text = "\n".join(top_tweets_df.apply(lambda row: " ".join(map(str, row)), axis=1))
        
        # Construct the prompt for the model
        base_query = (
            '''
            I will provide you with a query and several pieces of tabular news data. Please perform the following two tasks:
                Generate a Concise Answer: Provide a succinct response to the query based solely on the reference news.
                Organize Information into a Table: Present the relevant information in a clear and well-structured table where appropriate.

            Guidelines:
                1. Source of Information: Summarize or infer information exclusively from the provided news data.
                2. Summary Length: Keep the summary brief, not exceeding 100 words.
                3. Output Quality: Enhance the readability of the output. The table should keep its original head with md format.
            '''
        )
        full_query = f"{base_query}\n\nQuery: {query}\n"
        prompt = f"{full_query}\n\nReference Tweets:\n{tweets_text}"
        
        print("Thinking...\n")
        
        if self.api_type == 'gemini':
            # Generate content using Google Gemini API
            response = self.model.generate_content(prompt)
            return response.text
        elif self.api_type == 'openai':
            # Append the prompt as a user message in the conversation history
            self.conversation.append({"role": "user", "content": prompt})
            
            # Send the conversation history to the OpenAI API
            response = requests.post(
                "https://api.gptsapi.net/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": self.conversation
                }
            )
            
            # Handle the API response
            if response.status_code == 200:
                assistant_reply = response.json()['choices'][0]['message']['content']
                # Append the assistant's reply to the conversation history
                self.conversation.append({"role": "assistant", "content": assistant_reply})
                return assistant_reply
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        else:
            raise ValueError("Unsupported API type. Choose 'gemini' or 'openai'.")

# Usage Example
if __name__ == "__main__":
    # Replace with your actual API key
    # For Google Gemini API, use your Google API key
    # For OpenAI API, use your OpenAI API key
    api_key_Gemini = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"
    api_key_OpenAI = "sk-fOm2221aa87eef6a86afa9e29c1af54ddab98e7e637IxpP0"
    
    # Initialize TextMatcher with the path to your data
    print("Initializing TextMatcher...")
    matcher = TextMatcher()
    
    # Choose the API type: 'gemini' or 'openai'
    api_type = 'openai'  # Change to 'gemini' to use Google Gemini API
    
    if api_type == 'openai':
        # Initialize and configure the LLM_API with OpenAI
        analyzer = LLM_API(
            api_type='openai',
            api_key=api_key_OpenAI,
            matcher=matcher
        )
    else:
        # Initialize and configure the LLM_API with Google Gemini
        analyzer = LLM_API(
            api_type='gemini',
            api_key=api_key_Gemini,
            matcher=matcher
        )
    
    # Define the query
    query = "Breaking news in the US in June 2020"
    
    # Generate the summary using the query
    try:
        response_text = analyzer.generate_summary(query, top_n=1000)
        print("Generated Summary:\n")
        print(response_text)
    except Exception as e:
        print(f"An error occurred: {e}")
