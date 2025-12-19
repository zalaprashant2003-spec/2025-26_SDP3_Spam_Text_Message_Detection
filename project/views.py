from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def home(request):
#     # return HttpResponse("Hello Django")
#     return render(request, 'project/home.html')

def home(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("message")
        model = request.POST.get("model")
        result = "Spam"  # replace with ML prediction
    return render(request, "project/home.html", {"result": result})
