from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .ml.naive_bayes import predict

import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# def home(request):
#     """Render the home page with hero section and info cards"""
#     return render(request, "project/home.html")


def message_detection(request):
    """Render the message spam detection page with form and results"""
    result = None
    if request.method == "POST":
        text = request.POST.get("message")
        prediction = predict(text)  # call ML function
        result = "Spam" if prediction == 1 else "Not Spam"
    return render(request, "project/message_detection.html", {"result": result})


def email_detection(request):
    """Render the email spam detection 'Coming Soon' page"""
    return render(request, "project/email_detection.html")

from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import EmailAccount
from django.contrib import messages

# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # saves email and password
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'project/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                account = EmailAccount.objects.get(email=email, password=password)
                request.session['user_email'] = account.email  # simple session
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            except EmailAccount.DoesNotExist:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'project/login.html', {'form': form})

def logout_view(request):
    request.session.flush()  # removes all session data
    return redirect('login')

# 
# 
# 

import os
import pickle
from google_auth_oauthlib.flow import Flow
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Gmail API Scope
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly"
]


# File paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(APP_DIR, "credentials.json")
TOKEN_DIR = os.path.join(APP_DIR, "tokens")


# ---------------- HOME PAGE ----------------
def home(request):
    user_email = request.session.get("user_email")
    gmail_connected = False

    # ✅ Only check token if user logged in
    if user_email:
        token_file = os.path.join(TOKEN_DIR, f"token_{user_email.replace('@','_')}.json")
        gmail_connected = os.path.exists(token_file)

    return render(request, "project/home.html", {
        "gmail_connected": gmail_connected,
        "is_logged_in": bool(user_email)
    })


# ---------------- GOOGLE LOGIN REDIRECT ----------------
def gmail_auth(request):
    # 🔐 Force login first
    if "user_email" not in request.session:
        return redirect("login")

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        include_granted_scopes=False,
        redirect_uri="http://127.0.0.1:8080/gmail/callback/"
    )

    auth_url, state = flow.authorization_url(
    access_type="offline",
    include_granted_scopes="true",
    prompt="consent"
)


    # ✅ Save only state (string)
    request.session["gmail_state"] = state

    return redirect(auth_url)


# ---------------- GOOGLE CALLBACK ----------------
def gmail_callback(request):
    state = request.session.get("gmail_state")
    if not state:
        return redirect("/")

    # ✅ Re-create flow
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri="http://127.0.0.1:8080/gmail/callback/"
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials


    # Get logged-in user email
    user_email = request.session.get("user_email", "unknown_user")

    # Save token
    os.makedirs(TOKEN_DIR, exist_ok=True)
    token_path = os.path.join(TOKEN_DIR, f"token_{user_email.replace('@','_')}.json")

    with open(token_path, "w") as f:
        f.write(creds.to_json())


    # ✅ Go back to HOME
    return redirect("/")
