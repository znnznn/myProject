from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def login(request):
    return render(request, 'main/login.html')


def new_user(request):
    return render(request, 'main/new_user.html')


def profile_user(request):
    return render(request, 'main/profile_user.html')


def user(request):
    return render(request, 'main/profile_user.html')


def user_list(request):
    return render(request, 'main/profile_user.html')


def user_profit(request):
    return render(request, 'main/profile_user.html')