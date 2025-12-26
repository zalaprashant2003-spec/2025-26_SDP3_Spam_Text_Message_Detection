import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "model_store")

model = pickle.load(
    open(os.path.join(MODEL_DIR, "nb_model.pkl"), "rb")
)

vectorizer = pickle.load(
    open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "rb")
)


def predict(message):
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)
    return prediction[0]
