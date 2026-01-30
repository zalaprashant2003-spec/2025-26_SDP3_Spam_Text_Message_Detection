import pickle
import numpy as np
from text_preprocessing import clean_text

with open("project/model_store/svm_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("project/model_store/svm_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict_message(message):
    message = clean_text(message)
    vector = vectorizer.transform([message])

    prediction = model.predict(vector)[0]
    score = model.decision_function(vector)[0]

    confidence = 1 / (1 + np.exp(-abs(score)))

    return ("Spam" if prediction == 1 else "Ham"), confidence


if __name__ == "__main__":
    while True:
        msg = input("Enter message (or 'exit'): ")
        if msg.lower() == "exit":
            break

        label, prob = predict_message(msg)
        print(f"Prediction: {label} | Confidence: {prob:.2f}")
