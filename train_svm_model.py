import os
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from text_preprocessing import clean_text


# -----------------------------
# 1. Load dataset
# -----------------------------
data = pd.read_csv("spam.csv", encoding="latin-1")[['v1', 'v2']]
data.columns = ['label', 'message']

data['label'] = data['label'].map({'ham': 0, 'spam': 1})


# -----------------------------
# 2. Preprocessing
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
# 4. TF-IDF (CHAR N-GRAMS)
# -----------------------------
vectorizer = TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(3, 5),
    min_df=2,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# -----------------------------
# 5. Train SVM (FIXED)
# -----------------------------
model = LinearSVC(
    C=3.0,                 # stronger margin
    class_weight='balanced',  # 🔥 CRITICAL FIX
    max_iter=5000
)

model.fit(X_train_vec, y_train)


# -----------------------------
# 6. Evaluation
# -----------------------------
y_pred = model.predict(X_test_vec)

print(f"\nAccuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))


# -----------------------------
# 7. Save model
# -----------------------------
model_dir = "project/model_store"
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "svm_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(model_dir, "svm_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("\n✅ SVM model saved successfully")
