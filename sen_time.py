import vader as v
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assuming 'v.df_sentiment' is the DataFrame with a 'PublishedAt' datetime column and 'sentiment_score'
# Convert 'PublishedAt' to datetime if not done already
v.df_sentiment['PublishedAt'] = pd.to_datetime(v.df_sentiment['PublishedAt'], utc=True)

# Sort the DataFrame by 'PublishedAt' in ascending order
v.df_sentiment.sort_values("PublishedAt", ascending=True, inplace=True)

# Resample by day and calculate the average sentiment per day


# Plot the trend of sentiment over time
plt.figure(figsize=(20, 5))
plt.plot(v.df_sentiment['PublishedAt'], v.df_sentiment['Compound'], marker='o', linestyle='-', color='b')

# Format x-axis to show one tick per week
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Sets major ticks to every week
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Formats the tick labels

# Rotate date labels for better readability
plt.gcf().autofmt_xdate()

# Add labels and title
plt.title('Trend of Sentiment Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Average Sentiment Score', fontsize=12)

# Show the plot
plt.grid(True)
plt.show()
