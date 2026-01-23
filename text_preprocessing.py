# import re

# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
#     text = re.sub(r"\d+", "", text)             # remove numbers
#     text = re.sub(r"[^\w\s]", "", text)         # remove punctuation
#     text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
#     return text

import re

def clean_text(text):
    text = text.lower()

    # Normalize URLs
    text = re.sub(r'http\S+|www\S+', ' URL ', text)

    # Normalize numbers (phone, prize, otp)
    text = re.sub(r'\d+', ' NUMBER ', text)

    # Keep punctuation but normalize spacing
    text = re.sub(r'\s+', ' ', text).strip()

    return text
