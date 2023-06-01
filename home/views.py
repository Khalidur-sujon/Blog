from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def login_view(request):
    return render(request, 'home/login.html')


def register_view(request):
    return render(request, 'home/register.html')
