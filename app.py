import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Amazon Reviews Dashboard", layout="wide")
st.title("📊 Explore Selected Product Reviews")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Reviews.csv")
    df['Time'] = pd.to_datetime(df['Time'], unit='s')  # Convert UNIX timestamp
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Reviews")

# Sentiment Filter
sentiments = ["All"] + sorted(df['SentimentLabel'].dropna().unique().tolist()) if 'SentimentLabel' in df.columns else ["All"]
selected_sentiment = st.sidebar.selectbox("Sentiment:", sentiments)

# Score Filter
scores = ["All"] + sorted(df['Score'].dropna().unique().tolist())
selected_score = st.sidebar.selectbox("Score:", scores)

# ProductId Search (partial OK)
search_product_id = st.sidebar.text_input("Search ProductId (partial OK):")

# --- Apply Filters ---
filtered_df = df.copy()

if selected_sentiment != "All" and 'SentimentLabel' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['SentimentLabel'] == selected_sentiment]

if selected_score != "All":
    filtered_df = filtered_df[filtered_df['Score'] == selected_score]

if search_product_id:
    filtered_df = filtered_df[filtered_df['ProductId'].str.contains(search_product_id, case=False, na=False)]

# --- Filtered Review Table ---
st.markdown(f"### 💬 Showing {len(filtered_df)} Filtered Reviews")
display_cols = ['Summary', 'CleanedText', 'SentimentLabel', 'Score']
available_cols = [col for col in display_cols if col in filtered_df.columns]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[available_cols].sort_values('Score', ascending=False).head(10),
        use_container_width=True
    )
else:
    st.warning("No results match the current filter selections.")

# --- Visualizations Section (2 rows of 2 equal-sized charts) ---
if not filtered_df.empty:
    st.markdown("### 📊 Score & Sentiment Breakdown")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if 'Score' in filtered_df.columns:
            st.subheader("Score Distribution")
            score_counts = filtered_df['Score'].value_counts().sort_index()
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            score_counts.plot(kind='bar', ax=ax1, color='teal')
            ax1.set_title("Review Score Distribution")
            ax1.set_xlabel("Score")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

    with col2:
        if 'SentimentLabel' in filtered_df.columns:
            st.subheader("Sentiment Breakdown")
            sentiment_counts = filtered_df['SentimentLabel'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sentiment_counts.plot(kind='bar', ax=ax2, color='orchid')
            ax2.set_title("Sentiment Label Breakdown")
            ax2.set_xlabel("Sentiment")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)

    st.markdown("### 📈 Monthly Trends")
    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.subheader("Monthly Review Count")
        monthly_reviews = filtered_df.set_index('Time').resample('M').size()
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        monthly_reviews.plot(ax=ax3, color='skyblue')
        ax3.set_title("Monthly Review Count")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Review Count")
        st.pyplot(fig3)

    with col4:
        if 'Score' in filtered_df.columns:
            st.subheader("Monthly Average Score")
            monthly_avg_score = filtered_df.set_index('Time').resample('M')['Score'].mean()
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            monthly_avg_score.plot(ax=ax4, color='orange')
            ax4.set_title("Monthly Average Review Score")
            ax4.set_xlabel("Date")
            ax4.set_ylabel("Average Score")
            st.pyplot(fig4)

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
