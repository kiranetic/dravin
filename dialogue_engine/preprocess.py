from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_text(texts):
    vectorizer = TfidfVectorizer(max_features=1000)  # Limit for 4 GB RAM
    features = vectorizer.fit_transform(texts)
    return features, vectorizer
