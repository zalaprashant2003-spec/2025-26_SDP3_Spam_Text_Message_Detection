"Spam Text Message Detection "

This project is a Machine Learning-based system that detects whether a text message is *Spam* or *Not Spam (Ham)*

## Features
- Detects spam SMS messages
- Simple and clean user interface using Streamlit
- Email Detection for this use Telegram Bot.
      - If any spam message appears in an email ID, the
      Telegram bot notifies the user instantly.
      - Users can check spam messages directly via Telegram, without opening emails
- Professional responsive website interface for managing detections

## Tech Stack
- Python
- Scikit-learn
- NLTK
- Pandas
- NumPy
- Django & Bootstrap 5
- Streamlit
- Git & GitHub
- Telegram Bot API

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
5. Django server starts
6. User enters message in browser
7. Backend predicts result and sends response
8. Telegram Bot monitors emails and sends spam notifications to users automatically
9. Result is displayed on frontend

## Work
- Lab1-Study how to do this project, find dataset.
- Lab2&3
       - Implement the Naive Bayes model for spam detection.
       - Add a simple user interface to test message predictions.
- Lab4 - Add simple frontend and connect with model.
- Lab5 - Connect model with telegram bot for Email and balaced dataset.
- Lab6/7 - Modern UI Design & Django Integration
       - Designed responsive website using Bootstrap 5 with professional cyber-security theme
       - Updated spam.csv dataset and retrained Naive Bayes model for improved detection accuracy
       - Enabled instant email-based spam notifications via Telegram Bot