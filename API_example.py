import google.generativeai as genai
from retrieval import TextMatcher

# Google Gemini API
class LLM_API:
    def __init__(self, api_key, matcher):
        """
        Initializes the LLM_API with API key and a TextMatcher instance.

        Parameters:
        - api_key (str): API key for Google Generative AI.
        - matcher (TextMatcher): An instance of the TextMatcher class.
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.matcher = matcher
        self.model = genai.GenerativeModel("gemini-1.5-pro-002")

    def generate_summary(self, query, top_n=5):
        """
        Generates a summary based on the user's query and matched tweets.

        Parameters:
        - query (str): The query string describing what the user wants to know.
        - top_n (int): Number of top results to consider.

        Returns:
        - str: The generated response from the model.
        """
        # Get the top tweets matching the query from TextMatcher
        top_tweets_df = self.matcher.get_top_n(query, top_n)
        tweets_text = "\n".join(top_tweets_df.apply(lambda row: " ".join(map(str, row)), axis=1))
        
        # Construct the prompt for the model
        base_query = (
            "I will give you a query and several reference tweetes. \
             I need you to do two tasks: \
                Task 1: Generate a concise answer for the query based on the reference tweets. \
                Task 2: Organize the information into a clear table where appropriate. \
             Please always adher to the following guidelines: \
                1. Summarize or infer information directly from the provided tweets only \
                2. Keep the summary brief, with a maximum length of 150 words. \
                3. Use bullet points to enhance readability."
        )
        full_query = base_query + f"\nQuery: {query}\n"
        prompt = f"{full_query}\n\nReference Tweets:\n{tweets_text}"

        print("Thinking...\n")
        response = self.model.generate_content(prompt)
        return response.text


# Usage Example
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = "AIzaSyCLFFxeTtwHObbN2HlaCLZo-MxppsszChg"
    
    # Initialize TextMatcher with the path to your data
    print ("Sentences Embedding...")
    matcher = TextMatcher()
    
    # Initialize and configure the LLM_API
    analyzer = LLM_API(api_key, matcher)
    
    # Define the query
    query = "Breaking news in the US in June 2020"
    
    # Generate the summary using the query
    response_text = analyzer.generate_summary(query, top_n=1000)
    print(response_text)
