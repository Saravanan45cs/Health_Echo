import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sentiment_analysis import analyze_sentiment
def clean_text(text):
    """Cleans text by removing unwanted symbols and digits."""
    # Remove special characters and digits
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_data(df):
    """Preprocesses text data."""
    # Drop rows with missing values
    df.dropna(subset=['Review'], inplace=True)

    # Clean review text
    df["Review"] = df["Review"].apply(clean_text)

    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    # Tokenize, process, and store each review
    for i, row in df.iterrows():
        review = row["Review"]

        # Tokenize the review
        tokens = word_tokenize(review)

        # Remove stop words
        tokens = [token for token in tokens if token not in stop_words]

        # Apply stemming or lemmatization (choose one or both)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        # lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Choose either stemmed or lemmatized tokens
        processed_tokens = stemmed_tokens  # Or use lemmatized_tokens

        # Combine processed tokens back into a string
        processed_review = " ".join(processed_tokens)

        # Store the processed review in the new column
        df.loc[i, "Processed_Review"] = str(processed_review)

    return df

# Load dataset
df = pd.read_csv("drugtrain.csv")


# Now, df contains only the columns you want

df = preprocess_data(df)
df=analyze_sentiment(df)
# Optionally, label sentiment based on the 'rating' column
# For example, you can consider ratings >= 7 as positive, <= 4 as negative, and the rest as neutral
# df['Sentiment'] = pd.cut(df['rating'], bins=[0, 4, 7, 10], labels=['negative', 'neutral', 'positive'])

columns_to_keep = ['drugName', 'Review', 'rating', 'Processed_Review', 'sentiment_score']
df = df[columns_to_keep]
print(df.head())

# Save the preprocessed data to a new CSV file
df.to_csv("preprocessed_drugtrain.csv", index=False)
