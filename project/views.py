from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .ml.naive_bayes import predict


def home(request):
    """Render the home page with hero section and info cards"""
    return render(request, "project/home.html")


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
