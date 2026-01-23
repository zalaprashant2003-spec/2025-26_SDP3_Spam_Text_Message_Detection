from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .ml.naive_bayes import predict


<<<<<<< HEAD
# def home(request):
#     # return HttpResponse("Hello Django")
#     return render(request, 'project/home.html')

def home(request):
=======
def home(request):
    """Render the home page with hero section and info cards"""
    return render(request, "project/home.html")


def message_detection(request):
    """Render the message spam detection page with form and results"""
>>>>>>> cfef04c (Add complete project with updated README and frontend code)
    result = None
    if request.method == "POST":
        text = request.POST.get("message")
        prediction = predict(text)  # call ML function
        result = "Spam" if prediction == 1 else "Not Spam"
<<<<<<< HEAD
    return render(request, "project/home.html", {"result": result})
=======
    return render(request, "project/message_detection.html", {"result": result})


def email_detection(request):
    """Render the email spam detection 'Coming Soon' page"""
    return render(request, "project/email_detection.html")
>>>>>>> cfef04c (Add complete project with updated README and frontend code)
