import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class TextMatcher:
    def __init__(self, data_path="Data/processed_data.csv"):
        # Load data and compute embeddings
        self.df = pd.read_csv(data_path)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Compute TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['Lemmatized_text'])
        
        # Compute sentence embeddings
        tweet_embeddings = self.embedder.encode(self.df['Lemmatized_text'], convert_to_tensor=True)
        self.tweet_embeddings = tweet_embeddings.cpu().numpy()
    
    def _compute_similarity(self, query, top_n=5):
        # Preprocess the query
        query_len = len(query.split())
        
        # Compute TF-IDF similarity
        query_tfidf = self.tfidf_vectorizer.transform([query])
        lexical_sim = cosine_similarity(query_tfidf, self.tfidf_matrix).flatten()
        
        # Compute embedding similarity
        query_embedding = self.embedder.encode([query], convert_to_tensor=True)
        query_embedding = query_embedding.cpu().numpy()
        semantic_sim = cosine_similarity(query_embedding, self.tweet_embeddings).flatten()
    
        # Dynamic weighting based on query length
        if query_len <= 5:
            lexical_weight = 0.8
            semantic_weight = 0.2
        else:
            lexical_weight = 0.5
            semantic_weight = 0.5
    
        # Combine similarities
        combined_sim = lexical_weight * lexical_sim + semantic_weight * semantic_sim
    
        # Get top N tweets
        top_indices = np.argsort(combined_sim)[::-1][:top_n]
        top_tweets = self.df.iloc[top_indices]
    
        # Write only the original sentences to file
        top_tweets[['Original Sentence']].to_csv("top_tweets.csv", index=False)
        
        return top_tweets[['Original Sentence', 'Lemmatized_text']], combined_sim[top_indices]
    
    def get_top_n(self, query, top_n=5):
        """
        Get the top N tweets similar to the query.

        Parameters:
        - query (str): The search query.
        - top_n (int): Number of top results to return.

        Returns:
        - pd.DataFrame: DataFrame containing the top tweets and their lemmatized text.
        """
        top_n, scores = self._compute_similarity(query, top_n)
        return top_n

# Example usage
if __name__ == "__main__":
    # Instantiate the class
    matcher = TextMatcher()
    
    # Define your query
    query = "what do people think of apple"
    
    # Get top tweets using only query and top_n
    top_tweets = matcher.get_top_n(query, top_n=100)
    
    # Print the top tweets
    print(top_tweets)