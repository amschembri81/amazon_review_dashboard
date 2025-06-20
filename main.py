import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import re
import os

# 1. Load the dataset
df = pd.read_csv("Reviews.csv")

# 2. Optional: Reduce dataset for testing speed
df = df.head(10000)

# 3. Preview the data
print("Preview of data:")
print(df.head())

# 4. Reduce columns
df = df[['Id', 'ProductId', 'UserId', 'Score', 'Time', 'Summary', 'Text']]

# 5. Clean the review text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["CleanedText"] = df["Text"].apply(clean_text)

# 6. Run sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

df["SentimentScore"] = df["CleanedText"].apply(get_sentiment)
df["SentimentLabel"] = df["SentimentScore"].apply(
    lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
)

# 7. Save to SQLite
db_path = os.path.join(os.getcwd(), "amazon_reviews.db")
print(f"Saving database to: {db_path}")
conn = sqlite3.connect(db_path)
df.to_sql("reviews", conn, if_exists="replace", index=False)
print("Data successfully written to amazon_reviews.db")

# 8. Basic SQL queries
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM reviews")
print("Total reviews:", cursor.fetchone()[0])

cursor.execute("""
    SELECT ProductId, COUNT(*) as review_count
    FROM reviews
    GROUP BY ProductId
    ORDER BY review_count DESC
    LIMIT 5
""")
print("Most reviewed products:")
for row in cursor.fetchall():
    print(row)

# 9. Score distribution plot
query = "SELECT Score, COUNT(*) as count FROM reviews GROUP BY Score"
score_distribution = pd.read_sql_query(query, conn)

sns.barplot(x="Score", y="count", data=score_distribution)
plt.title("Distribution of Review Scores")
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()

# 10. Close connection
conn.close()
