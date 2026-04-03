import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

model = None
vectorizer = None

def load_model():
    global model, vectorizer

    if model is None:
        model_path = os.path.join(BASE_DIR, "model", "model.pkl")
        vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

        print("Loading model...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

def ml_predict(text):
    load_model()

    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = max(model.predict_proba(X)[0])

    return pred, prob