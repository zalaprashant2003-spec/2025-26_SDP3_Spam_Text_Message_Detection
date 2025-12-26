from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .ml.naive_bayes import predict


# def home(request):
#     # return HttpResponse("Hello Django")
#     return render(request, 'project/home.html')

def home(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("message")
        prediction = predict(text)  # call ML function
        result = "Spam" if prediction == 1 else "Not Spam"
    return render(request, "project/home.html", {"result": result})
