from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'carLogoDetection/home.html')


def search(request):
    return render(request, 'carLogoDetection/search.html')

def upload(request):
    return render(request, 'carLogoDetection/upload.html')





