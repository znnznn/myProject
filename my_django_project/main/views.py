from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.


def index(request):
    title = {'title': 'col'}
    return render(request, 'main/index.html', context=title)


def contacts(request):
    return render(request, 'main/contacts.html')


def login_page(request):
    if request.POST:
        data_user = dict(request.POST)
        user = authenticate(username=data_user['email'][0], password=data_user['password'][0])
        if user:
            login(request, user)
            message = f'{user["username"]} вітаємо!'
            return render(request, 'main/user.html', context={'user': user, 'message': message})
        else:
            message = f'Користувача з такими даними не існує.'
        return render(request, 'main/login.html', context={'user': user, 'message': message})
    return render(request, 'main/login.html')


def new_user(request):
    return render(request, 'main/new_user.html')


@login_required(login_url='/login')
def profile_user(request):
    return render(request, 'main/profile_user.html')


@login_required(login_url='/login')
def user(request):
    return render(request, 'main/user.html')


@login_required(login_url='/login')
def user_search(request):
    return render(request, 'main/user.html')


@login_required(login_url='/login')
def user_list(request):
    return render(request, 'main/user_list.html')


@login_required(login_url='/login')
def user_list_del(request):
    return render(request, 'main/user_list.html')


@login_required(login_url='/login')
def user_profit(request):
    return render(request, 'main/user_profit.html')


@login_required(login_url='/login')
def del_user(request):
    return render(request, 'main/delete_profile.html')


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return render(request, 'main/index.html')
