from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd
import vader as v
import numpy as np
import random
from umap import UMAP

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Convert the 'Comment' column from the DataFrame to a list of strings
docs = v.df_for_bertopic['Comment'].to_list()

# Initialize the SentenceTransformer for document embeddings
embedding_model = SentenceTransformer("all-mpnet-base-v2")

# Initialize the UMAP model with a fixed random_state for reproducibility
umap_model = UMAP(random_state=42,n_neighbors=15)

# Initialize the BERTopic model with a fixed UMAP and min_topic_size
topic_model = BERTopic(embedding_model=embedding_model, umap_model=umap_model, min_topic_size=30)

# Fit the BERTopic model to the list of documents to extract topics
topics, probs = topic_model.fit_transform(docs)

# Create a DataFrame to associate the extracted topics with the original documents
df = pd.DataFrame({"topic": topics, "document": docs})
print(df.head())  # Display the first few rows of the DataFrame for verification

# Generate a visualization of the topics identified by BERTopic
fig = topic_model.visualize_topics()
barchart = topic_model.visualize_barchart()

# Show the visualizations
barchart.show()
fig.show()