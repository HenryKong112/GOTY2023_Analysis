import sqlite3
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from langdetect import detect, DetectorFactory

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

# Connect to the SQLite database 'goty2023.db'
conn = sqlite3.connect('goty2023.db')

# Retrieve data from the 'comments' table into a DataFrame
query = "SELECT Comment_ID, Like, Comment, PublishedAt FROM comments"
df = pd.read_sql_query(query, conn)

# Preprocess the 'Comment' column
df['Comment'] = df['Comment'].str.lower()
df['Comment'] = df['Comment'].replace(r'<a href=".*?">.*?<\/a>', '', regex=True)
df['Comment'] = df['Comment'].replace(r'<br>', '', regex=True)

# Function to check if text is in English
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False
# Filter out non-English comments
df = df[df['Comment'].apply(is_english)]

# Create a df for BERTopic, as it doesn't require the removal of stop words
df_for_bertopic = df

# List of pronouns and conjunctions
pronouns_conjunctions = {
'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves',
'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
'theirs', 'themselves', 'this', 'that', 'these', 'those', 'is', 'am', 'are', 'was', 'were', 'be', 
'been', 'being', 'and', 'or', 'but', 'so', 'because', 'although', 'if', 'when', 'while'
}
def remove_pronouns_conjunctions(text):
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in pronouns_conjunctions]
    return ' '.join(filtered_words)

# Apply the function to each comment
df['Comment'] = df['Comment'].apply(remove_pronouns_conjunctions)


# Initialize the VADER sentiment analyzer
sentiments = SentimentIntensityAnalyzer()
# Apply sentiment analysis to the 'Comment' column
df["Positive"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["pos"])
df["Negative"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["neg"])
df["Neutral"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["neu"])
df["Compound"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["compound"])
# Classify the overall sentiment based on the compound score
df["Sentiment"] = df["Compound"].apply(
    lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral')
)
# Save the DataFrame with sentiment analysis results to a new table in the SQLite database
df.to_sql('sentiment_comments', conn, if_exists='replace', index=False)
# Filter the DataFrame by sentiment category
positive_comments = df[df["Sentiment"] == "Positive"].drop(columns=['Positive', 'Negative', 'Neutral', 'Compound'])
negative_comments = df[df["Sentiment"] == "Negative"].drop(columns=['Positive', 'Negative', 'Neutral', 'Compound'])
neutral_comments = df[df["Sentiment"] == "Neutral"].drop(columns=['Positive', 'Negative', 'Neutral', 'Compound'])

# Assign the final DataFrame to 'df_sentiment' for future use
df_sentiment = df
# Close the connection to the database
conn.close()


