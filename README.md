"Spam Text Message Detection "

This project is a Machine Learning-based system that detects whether a text message is *Spam* or *Not Spam (Ham)*

## Features
- Detects spam SMS messages
- Simple and clean user interface using Streamlit

## Tech Stack
- Python
- Scikit-learn
- NLTK
- Pandas
- NumPy
- Streamlit
- Git & GitHub

## Dataset
Dataset used: *SMS Spam Collection Dataset*
Source: Kaggle Learning Repository  
Contains 5169 labeled messages (spam & ham).

##How the System Works
1. Load and clean the dataset
2. Preprocess text:
   -Lowercasing
   -Removing punctuation and numbers
   -Tokenization
   -Stopword removal
   -Stemming
3. Convert text into numerical features using TF-IDF
4. Train model using Multinomial Naive Bayes
5. Flask server starts
6. User enters message in browser
7. Backend predicts result and sends response
8. Result is displayed on frontend

## Work
Lab1-Study how to do this project, find dataset.
Lab2&3 - Implement the Naive Bayes model for spam detection.
       - Add a simple user interface to test message predictions.
