import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import re
import dateparser
import torch
import os
import warnings

warnings.filterwarnings("ignore")

EMBEDDINGS_FILE = "embeddings.pt" 

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("Using CPU")

class TextMatcher:
    def __init__(self, data_path="Data/news.csv"):
        try:
            self.df = pd.read_csv(data_path, encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: File not found: {data_path}")
            raise

        self.df.columns = self.df.columns.str.strip()

        # NaN values
        self.df[['headline', 'short_description', 'authors']] = self.df[['headline', 'short_description', 'authors']].fillna('')
        
        # date
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'])  # Convert date to datetime objects
        else:
            print("Warning: 'date' column not found in DataFrame.")

        self.df['combined_text'] = self.df['category'] + ' ' + self.df['headline'] + ' ' + self.df['short_description'] + ' ' + self.df['authors']

        # tf-idf
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_vectorizer.fit(self.df['combined_text'])
        self.tfidf_matrix = self.tfidf_vectorizer.transform(self.df['combined_text'])

        # embedder
        MODEL_NAME = 'all-MiniLM-L6-v2'
        MODEL_SAVE_PATH = './models/' + MODEL_NAME

        if not os.path.exists(MODEL_SAVE_PATH):
            os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
            embedder = SentenceTransformer(MODEL_NAME)
            embedder.save(MODEL_SAVE_PATH)
            print(f"Model saved to {MODEL_SAVE_PATH}")
        else:
            embedder = SentenceTransformer(MODEL_SAVE_PATH)
            print(f"Loaded model from {MODEL_SAVE_PATH}")

        self.embedder = embedder.to(device)

        # check if embeddings file exists
        if os.path.exists(EMBEDDINGS_FILE):
            print(f"Loading embeddings from {EMBEDDINGS_FILE}...")
            self.embeddings = torch.load(EMBEDDINGS_FILE, map_location=device, weights_only=True)
            if isinstance(self.embeddings, list):
                self.embeddings = torch.stack(self.embeddings).to(device)
        else:
            print("Embeddings file not found, generating embeddings...")
            batch_size = 256
            embeddings = []
            for i in range(0, len(self.df), batch_size):
                batch = self.df['combined_text'].iloc[i:i + batch_size].tolist()
                batch_embeddings = self.embedder.encode(batch, convert_to_tensor=True, device=device)
                embeddings.extend(batch_embeddings)
                print(f"Processed batch {i // batch_size + 1} of {len(self.df) // batch_size + (1 if len(self.df) % batch_size else 0)}")

            self.embeddings = torch.stack(embeddings).to(device)
            print("Encoding finished.")

            # save embeddings
            print(f"Saving embeddings to {EMBEDDINGS_FILE}...")
            torch.save(embeddings, EMBEDDINGS_FILE)

    def _compute_similarity(self, query, top_n=5, indices=None):
        if indices is None:
            indices = np.arange(len(self.embeddings))

        query_len = len(query.split())
        query_tfidf = self.tfidf_vectorizer.transform([query])
        
        # Calculate lexical similarity on the subset defined by indices
        lexical_sim = cosine_similarity(query_tfidf, self.tfidf_matrix[indices]).flatten()

        query_embedding = self.embedder.encode([query], convert_to_tensor=True)
        query_embedding = query_embedding.cpu().numpy()

        # Calculate semantic similarity on the same subset of embeddings
        semantic_sim = cosine_similarity(query_embedding, self.embeddings[indices].cpu().numpy()).flatten()

        # Weighting based on query length
        if query_len <= 5:
            lexical_weight = 0.8
            semantic_weight = 0.2
        else:
            lexical_weight = 0.5
            semantic_weight = 0.5

        # Combine the similarities
        combined_sim = lexical_weight * lexical_sim + semantic_weight * semantic_sim

        top_indices = np.argsort(combined_sim)[::-1][:top_n]  # Get top indices
        top_docs = self.df.iloc[indices[top_indices]].copy()  # Retrieve the corresponding documents
        return top_docs, combined_sim[top_indices]

    def get_top_n(self, query, top_n=5):
        time_regex = r"\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|[a-zA-Z]+ \d{1,2}(?:st|nd|rd|th)?, \d{4}|[a-zA-Z]+ \d{4})\b"
        time_match = re.search(time_regex, query)
        query_time = dateparser.parse(time_match.group(0)) if time_match else None
        query_text = re.sub(time_regex, "", query).strip()

        # datetime
        self.df['date'] = pd.to_datetime(self.df['date'])

        print(query_time)

        if query_time:
            print('time included')
            relevant_indices = self.df[(self.df['date'].dt.year == query_time.year) & (self.df['date'].dt.month == query_time.month)].index

            if relevant_indices.empty:
                print("No articles found for the specified date.")
                return pd.DataFrame()

            # Compute similarity
            top_docs, scores = self._compute_similarity(query_text, top_n=top_n * 2, indices=relevant_indices) 

            top_docs['time_diff'] = abs(top_docs['date'] - query_time).dt.days
            top_docs = top_docs.sort_values(by=['time_diff', 'combined_text'], ascending=[True, False]).head(top_n)

        else:
            print('no time included')
            top_docs, scores = self._compute_similarity(query_text, top_n=top_n * 2)  # Use full df if no date

        return top_docs[['headline', 'category', 'short_description', 'authors', 'date']]


# Example usage
if __name__ == "__main__":
   matcher = TextMatcher()
   query = "Breaking news in the US in June 2020"
   top_docs = matcher.get_top_n(query, top_n=5)
   print(top_docs)