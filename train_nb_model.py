# os
# import pandas as pd
# import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# # 1. Load dataset
# data = pd.read_csv("spam.csv", encoding="latin-1")[['v1', 'v2']]
# data.columns = ['label', 'message']

# # 2. Convert labels: ham -> 0, spam -> 1
# data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# # 3. Split data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(
#     data['message'], data['label'], test_size=0.2, random_state=42
# )

# # 4. Vectorize text using TF-IDF
# vectorizer = TfidfVectorizer(stop_words='english')
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # 5. Train Naive Bayes model
# model = MultinomialNB()
# model.fit(X_train_vec, y_train)

# # 6. Make predictions on test set
# y_pred = model.predict(X_test_vec)

# # 7. Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy*100:.2f}%")

# cm = confusion_matrix(y_test, y_pred)
# print("Confusion Matrix:")
# print(cm)

# report = classification_report(y_test, y_pred, target_names=['Ham', 'Spam'])
# print("Classification Report:")
# print(report)

# # 8. Ensure model_store folder exists
# if not os.path.exists("project/model_store"):
#     os.makedirs("project/model_store")

# # 9. Save model & vectorizer safely
# with open("project/model_store/nb_model.pkl", "wb") as f:
#     pickle.dump(model, f)

# with open("project/model_store/vectorizer.pkl", "wb") as f:
#     pickle.dump(vectorizer, f)

# print("Naive Bayes model trained, evaluated, and saved in model_store")


import os
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from text_preprocessing import clean_text


# -----------------------------
# 1. Load dataset
# -----------------------------
data = pd.read_csv("spam.csv", encoding="latin-1")[['v1', 'v2']]
data.columns = ['label', 'message']

# Convert labels
data['label'] = data['label'].map({'ham': 0, 'spam': 1})


# -----------------------------
# 2. Apply preprocessing
# -----------------------------
data['message'] = data['message'].apply(clean_text)


# -----------------------------
# 3. Train-test split (STRATIFIED)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    data['message'],
    data['label'],
    test_size=0.2,
    random_state=42,
    stratify=data['label']
)


# -----------------------------
# 4. TF-IDF (CHAR N-GRAMS → precision boost)
# -----------------------------
vectorizer = TfidfVectorizer(
    analyzer='char_wb',     # character-level (best for SMS)
    ngram_range=(3, 5),
    min_df=2,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# -----------------------------
# 5. Train Naive Bayes (precision-friendly)
# -----------------------------
model = MultinomialNB(alpha=0.2)
model.fit(X_train_vec, y_train)


# -----------------------------
# 6. Predictions
# -----------------------------
y_pred = model.predict(X_test_vec)


# -----------------------------
# 7. Evaluation
# -----------------------------
print(f"\nAccuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))


# -----------------------------
# 8. Save model & vectorizer
# -----------------------------
model_dir = "project/model_store"
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "nb_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(model_dir, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel and vectorizer saved successfully in project/model_store")
    