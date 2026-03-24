"Spam Text Message Detection "

This project is a Machine Learning-based system that detects whether a text message is *Spam* or *Not Spam (Ham)*

## Features
- Detects spam SMS messages
- Simple and clean user interface using Streamlit
- Email Detection for this use Telegram Bot.
      - If any spam message appears in an email ID, the Telegram bot notifies the user instantly.
      - Users can check spam messages directly via Telegram, without opening emails
- Professional responsive website interface for managing detections
- Supports multiple ML algorithms like Naive Bayes and Support Vector Machine (SVM)
- Real-time message analysis and prediction
- User authentication system for secure access

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
- Gmail API

## Dataset
Dataset used: *SMS Spam Collection Dataset*
Source: Kaggle Learning Repository  
Contains 5169 labeled messages (spam & ham).

## How the System Works
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

## How to Run the Project

Step 1: Train the Model
First, train the Naive Bayes model using below command (use correct path):
- python train_nb_model.py (for Naive Bayes)

Step 2: Apply Migrations
Run these commands in terminal:
- python manage.py makemigrations
- python manage.py migrate

Step 3: Run the Server
Start the Django server:
- python manage.py runserver 8080

Now open browser and go to:
http://127.0.0.1:8080

You will see the home page and can start using the project.

Email Connection & Telegram Notification

1. First, register and login with your account.
2. Go to Email Detection page and connect your Gmail.
   (You can also read Guidelines page for help)

3. Now open another terminal (so total 2 terminals will be running):

   Terminal 1 (Already running):
   - python manage.py runserver 8080

   Terminal 2 (go inside project directory):
   - python spam_notifier.py

4. Now system will start monitoring your emails.

If any spam email is detected, you will receive message on Telegram.

## How to Add Users (Gmail Access Setup)
1. Go to Google Cloud Console  
2. Open your project (Default / Gemini Project)  
3. Go to **API & Services**  
4. Click on **OAuth Consent Screen**  
5. Open **Audience / Test Users** section  
6. Add user email IDs who can access the system  

## Project Purpose
This system helps users to detect spam messages easily and protect from fraud, phishing links, and unwanted messages.
It provides both manual message checking and automatic email monitoring with instant alerts.

## Work
- Lab1-Study how to do this project, find dataset.
- Lab2&3
       - Implement the Naive Bayes model for spam detection.
       - Add a simple user interface to test message predictions.
- Lab4 - Add simple frontend and connect with model.
- Lab5 - Connect model with telegram bot for Email and balaced dataset.
- Lab6/7
       - Modern UI Design & Django Integration
       - Designed responsive website using Bootstrap 5 with professional cyber-security theme
       - Updated spam.csv dataset and retrained Naive Bayes model for improved detection accuracy
       - Enabled instant email-based spam notifications via Telegram Bot
- Lab8 
       - Add Support Vector Machine Algo for train the model.
- Lab9
        - Connecting Google Authetication with our system
- Lab10 to Lab12
        - Testing
        - Bug Solving
        - UI imorovement
        - Project Report
