import pandas as pd
import vader as v
import matplotlib.pyplot as plt

# Assuming 'df_sentiment' is your DataFrame with a 'Sentiment' column
count_series = v.df_sentiment['Sentiment'].value_counts()

# Assuming 'df' is your DataFrame with 'Sentiment' and 'Like' columns
likes_by_sentiment = v.df.groupby('Sentiment')['Like'].sum()

# Create the data dictionary automatically
data = {
    'Sentiment': count_series.index.tolist(),
    'Count': count_series.values.tolist(),
    'Likes': likes_by_sentiment.reindex(count_series.index).values.tolist()  # Align 'Likes' with 'Sentiment'
}

# Convert the dictionary to a DataFrame if needed
df = pd.DataFrame(data)

# Calculating total counts and likes
total_counts = df['Count'].sum()
total_likes = df['Likes'].sum()

# Calculating percentage distributions for counts and likes
df['Count_Percent'] = df['Count'] / total_counts * 100
df['Likes_Percent'] = df['Likes'] / total_likes * 100

# Calculating engagement (Likes per Count)
df['Engagement'] = df['Likes'] / df['Count']

print(df)

# Plot 1: Sentiment Distribution (Counts and Likes)
fig, ax1 = plt.subplots(figsize=(10, 10))

# Bar plot for counts
ax1.bar(df['Sentiment'], df['Count_Percent'], color='skyblue', width=0.4, align='center', label='Count %')

# Twin axis to plot likes
ax2 = ax1.twinx()
ax2.bar(df['Sentiment'], df['Likes_Percent'], color='lightcoral', width=0.4, align='edge', label='Likes %')

# Labels and titles
ax1.set_xlabel('Sentiment')
ax1.set_ylabel('Percentage of Counts', color='blue')
ax2.set_ylabel('Percentage of Likes', color='red')
plt.title('Sentiment Distribution: Counts vs Likes')

# Adding legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Plot 2: Engagement per Sentiment
plt.figure(figsize=(9, 9))
plt.bar(df['Sentiment'], df['Engagement'], color='purple', alpha=0.7)
plt.title('Engagement (Likes per Count) by Sentiment')
plt.xlabel('Sentiment')
plt.ylabel('Likes per Count')

# Display plots
plt.tight_layout()
plt.show()

