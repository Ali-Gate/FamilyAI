from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'family_ai/home.html')

def register(request):  
    return render(request, 'family_ai/register.html')


def login(request):
    return render(request, 'family_ai/login.html')


def logout(request):
    return render(request, 'family_ai/logout.html')
