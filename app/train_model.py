import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

data = [
    ("You won 5 lakh", "scam"),
    ("Instant loan offer", "scam"),
    ("Meeting at 5pm", "safe"),
    ("Flat 50% off", "marketing")
]

df = pd.DataFrame(data, columns=["text", "label"])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

model = LogisticRegression()
model.fit(X, df["label"])

joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")