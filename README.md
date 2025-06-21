# 🛍️ Amazon Review Sentiment Dashboard

This project analyzes Amazon product reviews and visualizes customer sentiment using an interactive Streamlit dashboard. It helps identify how customers feel about products based on review text and star ratings.

---

## 📦 Dataset

- **Source:** Amazon Reviews (CSV format)
- **Columns:**  
  - `ProductId`, `UserId`, `Score`  
  - `Summary`, `Text`  
  - `Time` (converted to readable datetime)  

---

## 🧠 Features

- 🔍 **Text Preprocessing:** Clean review text, lowercase, remove stopwords/punctuation  
- 📈 **Sentiment Analysis:** Using VADER or TextBlob to determine polarity  
- 🎨 **Dashboard Features:**
  - Filter by sentiment (Positive / Neutral / Negative)
  - Filter by score
  - Search by keyword or product ID
  - View total reviews and sentiment distribution
  - Optional: download filtered data

---

## 🛠 Tech Stack

- **Python 3.9+**
- **pandas**
- **nltk / textblob / vaderSentiment** (for sentiment analysis)
- **Streamlit** (for dashboard)
- **matplotlib / seaborn / plotly** (for visuals)

---

## 📁 Project Structure

amazon_review_dashboard/
├── reviews.csv # Amazon product reviews dataset
├── sentiment_utils.py # Functions for sentiment labeling
├── amazon_dashboard.py # Main Streamlit app
├── cleaned_reviews.csv # Preprocessed version (optional)
├── README.md


---

## 🚀 How to Run

1. **Install dependencies** (preferably in a virtual environment):

```bash
pip install streamlit pandas textblob matplotlib seaborn
```

2. **Start the dashboard:**

```bash
streamlit run amazon_dashboard.py
```

3. **Open your browser:**
   
    Visit http://localhost:8501 to use the dashboard


## 🖥 Example Use Cases
Track customer sentiment over time

Analyze reviews for a specific product ID

Export filtered reviews for further analysis


## 📌 To Do
 Add product image previews (via API)

 Deploy to Streamlit Cloud

 Add word cloud or keyword frequency chart
