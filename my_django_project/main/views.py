import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

from .tradier_api import symbol_stocks
# Create your views here.


amount_stock = 10


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

            print(User.objects.get(username=user))
            message = f'{user.username} вітаємо!'
            return HttpResponseRedirect(redirect_to='user')
        else:
            message = f'Користувача з такими даними не існує.'
        return render(request, 'main/login.html', context={'user': user, 'message': message})
    return render(request, 'main/login.html')


def new_user(request):
    if request.POST:
        data_user = dict(request.POST)
        if data_user['email'][0] != data_user['username'][0]:
            message = 'Username повинен дорівнювати Email'
            return render(request, 'main/new_user.html', context={'message': message})
        elif data_user['password'][0] != data_user['password2'][0]:
            message = 'Паролі мають бути однаковими'
            return render(request, 'main/new_user.html', context={'message': message})
        user = User.objects.create_user(username=data_user['email'][0], email=data_user['email'][0],
                                        password=data_user['password'][0])
        user.last_name = data_user['firstName'][0]
        user.last_name = data_user['lastName'][0]
        user.save()
        if not user:
            message = "Сталась помлка з\'днання з базою даних"
        else:
            message = f'{data_user["firstName"][0]} Ви успішно зареєструвались.'
        return render(request, 'main/login.html', context={'message': message, 'user': user})
    return render(request, 'main/new_user.html')


@login_required(login_url='/login')
def profile_user(request):
    return render(request, 'main/profile_user.html')


@login_required(login_url='/login')
def user_page(request):
    user = request.user
    print(user)
    with open('main/stocks_all.json', 'r') as file_stocks:
        list_stocks = json.load(file_stocks)
        my_stocks = list_stocks['securities']['security']
        my_stocks = sorted(my_stocks, key=lambda symbol: symbol['symbol'])
    i = 0
    while i != amount_stock:
        data_symbol = symbol_stocks(my_stocks[i]['symbol'])

        if True is data_symbol['quotes']['quote']['change_percentage'] >= 0:
            my_stocks[i]['positive_change'] = True
        else:
            my_stocks[i]['positive_change'] = False
        my_stocks[i]['quote'] = data_symbol['quotes']['quote']
        i += 1
    print(my_stocks[0])
    print(my_stocks[0].keys())
    return render(request, 'main/user.html', context={'user': user, 'title': user.username, 'stocks': my_stocks})


@login_required(login_url='/login')
def user_search(request):
    return render(request, 'main/user.html')


@login_required(login_url='/login')
def user_list(request):
    return render(request, 'main/user_list.html')





def user_search_list(request):
    pass


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
