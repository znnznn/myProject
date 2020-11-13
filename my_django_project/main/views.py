from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    title = {'title': 'col'}
    return render(request, 'main/index.html', context=title)


def contacts(request):
    return render(request, 'main/contacts.html')


def login(request):
    return render(request, 'main/login.html')


def new_user(request):
    return render(request, 'main/new_user.html')


def profile_user(request):
    return render(request, 'main/profile_user.html')


def user(request):
    return render(request, 'main/user.html')


def user_search(request):
    return render(request, 'main/user.html')


def user_list(request):
    return render(request, 'main/user_list.html')

def user_list_del(request):
    return render(request, 'main/user_list.html')




def user_profit(request):
    return render(request, 'main/user_profit.html')


def del_user(request):
    return render(request, 'main/delete_profile.html')