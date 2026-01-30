import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, request, jsonify, render_template_string

df = pd.read_csv(r'C:\Spam_msg\dataset\spam.csv', encoding='latin-1')
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = "".join([c for c in text if c.isalpha() or c.isspace()])
    tokens = nltk.word_tokenize(text)
    tokens = [stemmer.stem(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

df['processed_message'] = df['message'].apply(preprocess_text)

tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['processed_message'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

def predict_message(text):
    processed = preprocess_text(text)
    vectorized = tfidf.transform([processed])
    return model.predict(vectorized)[0]

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Spam Detection</title>
<style>
body { font-family: Arial; background:#f2f2f2; }
.box { width:400px; margin:100px auto; padding:20px; background:white; border-radius:8px; }
</style>
</head>
<body>
<div class="box">
<h2>Spam SMS Detector</h2>
<textarea id="msg" rows="4" style="width:100%"></textarea><br><br>
<button onclick="send()">Check</button>
<p id="res"></p>
</div>
<script>
function send(){
 fetch('/predict',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({message:document.getElementById('msg').value})
 }).then(r=>r.json()).then(d=>{
  document.getElementById('res').innerHTML =
   "<b>Prediction:</b> " + d.prediction.toUpperCase();
 });
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/predict', methods=['POST'])
def predict():
    msg = request.json.get('message')
    return jsonify({'prediction': predict_message(msg)})

if __name__ == "__main__":
    print("Server starting...")
    app.run(debug=True)
