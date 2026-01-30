import pickle
import os

# BASE_DIR → project/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model_store")

svm_model = pickle.load(
    open(os.path.join(MODEL_DIR, "svm_model.pkl"), "rb")
)

svm_vectorizer = pickle.load(
    open(os.path.join(MODEL_DIR, "svm_vectorizer.pkl"), "rb")
)

def predict(message):
    vector = svm_vectorizer.transform([message])
    prediction = svm_model.predict(vector)
    return prediction[0]
