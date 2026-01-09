import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
    text = re.sub(r"\d+", "", text)             # remove numbers
    text = re.sub(r"[^\w\s]", "", text)         # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text
