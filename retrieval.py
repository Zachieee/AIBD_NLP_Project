import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

# load data
df = pd.read_csv("Data/processed_data.csv")

# TF-IDF and SentenceTransformer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# TF-IDF for lemmatized text and sentence embeddings
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Lemmatized_text'])
tweet_embeddings = embedder.encode(df['Lemmatized_text'], convert_to_tensor=True)

tweet_embeddings = tweet_embeddings.cpu().numpy()

def compute_similarity(query, query_len, top_n=5):
    # preprocess the query
    
    # TF-IDF similarity
    query_tfidf = tfidf_vectorizer.transform([query])
    lexical_sim = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
    
    # embedding similarity
    query_embedding = embedder.encode([query], convert_to_tensor=True)
    query_embedding = query_embedding.cpu().numpy()  # Move to CPU and convert to NumPy
    
    semantic_sim = cosine_similarity(query_embedding, tweet_embeddings).flatten()

    # dynamic weighting
    if query_len <= 5:
        lexical_weight = 0.8
        semantic_weight = 0.2
    else:
        lexical_weight = 0.5
        semantic_weight = 0.5
    
    # score
    combined_sim = lexical_weight * lexical_sim + semantic_weight * semantic_sim
    
    # top N tweets
    top_indices = np.argsort(combined_sim)[::-1][:top_n]
    top_tweets = df.iloc[top_indices]

    # Write only the original sentences to file
    top_tweets[['Original Sentence']].to_csv("top_tweets.csv", index=False)
    
    return top_tweets[['Original Sentence', 'Lemmatized_text']], combined_sim[top_indices]

# test
query = "what do people think of apple"
query_len = len(query.split())
top_tweets, scores = compute_similarity(query, query_len, top_n=100)

print(top_tweets)