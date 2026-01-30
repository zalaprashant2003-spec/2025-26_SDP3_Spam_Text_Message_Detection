import pickle
from text_preprocessing import clean_text

# Load model and vectorizer
with open("project/model_store/nb_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("project/model_store/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("project/model_store/label_map.pkl", "rb") as f:
    label_map = pickle.load(f)

def predict_message(message):
    message = clean_text(message)
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector).max()
    return label_map[prediction], probability


# Manual test
if __name__ == "__main__":
    while True:
        msg = input("Enter message (or 'exit'): ")
        if msg.lower() == "exit":
            break
        label, prob = predict_message(msg)
        print(f"Prediction: {label} | Confidence: {prob:.2f}")

