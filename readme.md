# YouTube API Sentiment Analysis & Topic Modeling

## Objective
Retrieve all comments from YouTube videos and perform **topic modeling** and **sentiment analysis** using Python.

## Context 
As a gaming enthusiast, I’m diving into **sentiment analysis** and **topic modeling** for the **Game of the Year (GOTY) 2023 Live event**. Let’s uncover the magic behind the nominees and celebrate gaming excellence!

Please checkout the Game_of_the_Year_2023_Livestream_Analysis_Report.docx for the result.

<img src='Image\GOTY.jpg'>

---

## Requirements

### Microsoft C++ Build Tools:
- [Download Link](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### YouTube Video:
- [Watch Video](https://www.youtube.com/watch?v=Zu2z5M4gmno)

---

## Documentation

1. **YouTube API**  
   [YouTube Data API Documentation](https://developers.google.com/youtube/v3/docs)  
   ⚠️ Projects that enable the YouTube Data API have a default quota allocation of 10,000 units per day.

2. **Google API Client Discovery**  
   [API Client Documentation](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html)

3. **Get API Key**  
   [Get API Key](https://console.cloud.google.com/marketplace/product/google/youtube.googleapis.com?pli=1)

4. **VADER Sentiment Analysis**  
   - [GitHub - VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
   - [YouTube - VADER Overview](https://www.youtube.com/watch?v=uwLWf0rEL18)

5. **BERTopic for Topic Modeling**  
   - [NCBI Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9120935/)
   - [BERTopic Documentation](https://maartengr.github.io/BERTopic/getting_started/embeddings/embeddings.html)
   - [GitHub - BERTopic](https://github.com/MaartenGr/BERTopic)
   - [Sentence-BERT Models](https://sbert.net/docs/sentence_transformer/pretrained_models.html#semantic-search-models)
   - [UMAP Documentation](https://umap-learn.readthedocs.io/en/latest/parameters.html)

---

## Tools
1. Python
2. SQLite
3. Azure SQL Database

---

## Schema

### Comments Table

| Column Name | Data Type    | Description                                           |
|-------------|--------------|-------------------------------------------------------|
| Username    | VARCHAR(256) | Display name of the user who posted the comment.       |
| Comment_ID  | VARCHAR(256) | YouTube's unique identifier for the comment.           |
| Parent_ID   | VARCHAR(256) | Unique ID of the parent comment (for replies).         |
| PublishedAt | DATETIME     | Date and time when the comment was originally published.|
| Like        | INTEGER      | Number of likes the comment has received.              |
| Comments    | TEXT         | The content of the comment.                            |

### Sentiment Comments Table

| Column Name   | Data Type | Description            |
|---------------|-----------|------------------------|
| Comment_ID    | TEXT      | Identifier for the comment. |
| Like          | INTEGER   | Number of likes the comment has received. |
| Comment       | TEXT      | The content of the comment. |
| PublishedAt   | TEXT      | Date of publication. |
| Positive      | REAL      | Positive sentiment score. |
| Negative      | REAL      | Negative sentiment score. |
| Neutral       | REAL      | Neutral sentiment score. |
| Compound      | REAL      | Compound sentiment score (overall sentiment). |
| Sentiment     | TEXT      | Sentiment classification (positive, negative, neutral). |

---

## Methodology

### VADER Sentiment Analysis

#### Key Features:
- **📚 Lexicon and Rule-Based**: Uses a predefined list of words (lexicon) and rules to determine the sentiment of a text.
- **📺 Social Media Focused**: Effective for short, informal texts like tweets, comments, and reviews.
- **💯 Sentiment Scores**: Provides scores for positive, negative, and neutral sentiments, along with a compound score for overall sentiment.

---

### Preprocess the Data: 

#### 1. Convert to Lowercase:
Transformed all text in the 'Comment' column to lowercase to ensure uniformity and prevent case-sensitive discrepancies during analysis.
```python
df['Comment'] = df['Comment'].str.lower()
```
#### 2. Remove HTML Anchor Tags:
Removed HTML anchor tags `<a href="...">...</a>` from the comments. This step is intended to clean the text by eliminating hyperlinks and associated text.
```python
df['Comment'] = df['Comment'].replace(r'<a href=".*?">.*?<\/a>', '', regex=True)
```

#### 3. Remove HTML Line Breaks:
Removed HTML line break tags `<br>` from the comments to clean up the text and ensure it's free from unnecessary formatting.
```python
df['Comment'] = df['Comment'].replace(r'<br>', '', regex=True)
```

#### 4. Define Pronouns and Conjunctions:
Created a set of common pronouns and conjunctions. This set will be used to filter out these words from the text in the next step.
```python
pronouns_conjunctions = { ... }
```
#### 5. Define a Function to Remove Pronouns and Conjunctions:
- Extracts all words from a given text using a regular expression.
- Filters out any words that are in the predefined set of pronouns and conjunctions.
- Joins the remaining words back into a single string.
```python
def remove_pronouns_conjunctions(text):
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in pronouns_conjunctions]
    return ' '.join(filtered_words)
```

#### 6. Apply the Function to Each Comment:
Applied the `remove_pronouns_conjunctions` function to each entry in the 'Comment' column to remove the specified words from all comments.
```python
df['Comment'] = df['Comment'].apply(remove_pronouns_conjunctions)
```
#### 7. Make sure there are english comments only
The script uses a language detection algorithm to ensure that only English comments are retained.
```python
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

df = df[df['Comment'].apply(is_english)]
```

# BERTopic and Sentiment Analysis for YouTube Comments

## BERTopic

### Embedding Models
- **SentenceTransformer `all-mpnet-base-v2`**: Provides the best quality embeddings.
- **SentenceTransformer `all-MiniLM-L6-v2`**: 5 times faster but still maintains good quality.
- **BERTopic's Default Model**: An option when minimal setup is needed.

### Why BERTopic?

#### 1. Handles Short and Noisy Texts
Ideal for short and unstructured texts like YouTube comments. BERTopic effectively processes informal language, slang, and abbreviations.

#### 2. Contextual Understanding
BERTopic leverages transformer-based embeddings to capture the context in which words are used, resulting in better topic extraction and understanding of comments.

#### 3. Dynamic Topic Modeling
Useful for tracking evolving discussions, especially around trending topics. This feature is particularly beneficial for analyzing ongoing conversations, such as those seen in YouTube comment sections.

#### 4. Scalable
BERTopic is efficient for large datasets, making it suitable for channels with vast comment sections. It can scale up easily, maintaining performance even with massive datasets.

#### 5. Probabilistic Topic Assignment
BERTopic assigns probabilities to topics rather than hard clustering. This approach allows for more flexibility and nuanced understanding, as some comments may cover multiple themes.

#### 6. Interactive Visualizations
Rich visualizations, such as **Intertopic Distance Maps**, enable users to explore and interpret the topic structure effectively. These visual aids make it easier to understand relationships between different topics.

---

## Graphs

### Topic Word Scores
- Each **topic** is represented by a list of **keywords** most strongly associated with that topic.
- **Word scores** (term frequencies) indicate the **relevance** or **contribution** of each word.
- Higher-scoring words highlight the **core meaning** of the topic.

### Intertopic Distance Maps

#### Bubble Sizes
- Each **bubble** represents a **topic**.
- Larger bubbles indicate more **dominant topics** in the dataset.

#### Distances Between Bubbles
- The **distance** between bubbles reflects how **distinct** the topics are.
- **Farther apart** indicates more distinct and **separate themes**, while **closer together** suggests **overlapping themes**.

#### Axes (D1 and D2)
- The axes represent **latent topic dimensions** derived from the data.
- They help to **spatially separate topics**, facilitating easier visualization of the relationships between different themes.

---

## Limitations

### 1. VADER's Limitations
- **VADER** struggles with recognizing **negation**, **idioms**, and **sarcasm**.
- This can result in **inaccurate sentiment analysis** in cases where sarcasm or complex language is prevalent.

### 2. English-Only Analysis
- The analysis is **limited to English comments** only. Non-English comments are excluded from the sentiment and topic modeling analysis, which may limit the insights in multilingual or international contexts.
