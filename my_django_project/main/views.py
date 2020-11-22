import json

import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

from .tradier_api import symbol_stocks
from .models import Message, TradeStock
# Create your views here.


amount_stock = 10


def check_user(request):
    if request.user.is_authenticated:
        title = request.user.username
    else:
        title = 'Біржовий аналітик'
    return title


def index(request):
    title = check_user(request)
    return render(request, 'main/index.html', context={'title': title})


def contacts(request):
    title = check_user(request)
    if request.POST:
        data_message = dict(request.POST)
        message_user = Message(user_name=data_message['username'][0], user_email=data_message['email'][0],
                               message=data_message['message'][0])
        message_user.save()
        message = f'{data_message["username"][0]} Ваше повідомлення відправлено.'
        return render(request, 'main/contacts.html', context={"message": message,
                                                              'title': title})
    return render(request, 'main/contacts.html', context={'title': title})


def login_page(request):
    title = check_user(request)
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='user')
    if request.POST:
        data_user = dict(request.POST)
        user = authenticate(username=data_user['email'][0], password=data_user['password'][0])
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect_to='user')
        else:
            message = f'Користувача з такими даними не існує.'
        return render(request, 'main/login.html', context={'user': user, 'message': message})
    return render(request, 'main/login.html', context={'title': title})


def new_user(request):
    title = check_user(request)
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
        user.first_name = data_user['firstName'][0]
        user.last_name = data_user['lastName'][0]
        user.save()
        if not user:
            message = "Сталась помлка з\'днання з базою даних"
        else:
            message = f'{data_user["firstName"][0]} Ви успішно зареєструвались.'
        return render(request, 'main/login.html', context={'message': message, 'title': title})
    return render(request, 'main/new_user.html', context={'title': title})


@login_required(login_url='/login')
def profile_user(request):
    return render(request, 'main/profile_user.html')


@login_required(login_url='/login')
def user_page(request):
    user = request.user
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
    return render(request, 'main/user.html', context={'user': user, 'title': user.username, 'stocks': my_stocks})


@login_required(login_url='/login')
def user_search(request):

    user = request.user
    if request.POST:
        stock_search = dict(request.POST)
        my_stocks = False
        with open('main/stocks_all.json', 'r') as file_stocks:
            list_stocks = json.load(file_stocks)
            stocks = list_stocks['securities']['security']
        for i in stocks:
            if i['symbol'] == str(stock_search['symbol'][0]).upper():
                my_stocks = [i]
        data_symbol = [symbol_stocks(my_stocks[0]['symbol']) if my_stocks else False]
        if data_symbol[0]:
            if True is data_symbol[0]['quotes']['quote']['change_percentage'] >= 0:
                my_stocks[0]['positive_change'] = True
            else:
                my_stocks[0]['positive_change'] = False
            my_stocks[0]['quote'] = data_symbol[0]['quotes']['quote']
            return render(request, 'main/user.html', context={'title': user.username, 'stocks': my_stocks})
        my_stocks = [{'Дані відсутні': f'Символ {stock_search["symbol"][0]} не знайдено'}]
        return render(request, 'main/user.html', context={'title': user.username, 'stocks': my_stocks, "btn": True})
    return HttpResponseRedirect(redirect_to='user')


@login_required(login_url='/login')
def user_list(request):
    """ exclude """

    user = request.user
    if request.POST:
        my_stock = dict(request.POST)
        my_stock = eval(my_stock['stock'][0])
        data_user = TradeStock(user=user)
        data_save = data_user.data_stock(my_stock)
        if data_save:
            message = 'Цінні папери додано в портфель'
        else:
            message = 'Сталась помилка спробуйте, ще раз'
    else:
        message = ''
    all_data = TradeStock.objects.filter(user_id=user.id).exclude(exch='profit').values()
    if all_data:
        all_data = list(all_data)
        for item in all_data:
            price = float(item['ask_price'])
            data_symbol = symbol_stocks(item['symbol'])
            price_new = data_symbol['quotes']['quote']['bid']
            delta = round((price_new - price) * 100, 2)
            item['profit'] = delta
            item['bid_price'] = price
            item['ask_price'] = price_new
            item['change_percentage'] = round((price_new - price) / price * 100, 2)
            if delta >= 0:
                item['positive_profit'] = True
            else:
                item['positive_profit'] = False
        print(all_data)
        all_data = sorted(all_data, key=lambda symbol: symbol['trade_date'], reverse=True)
        sum_profit = sum([+i['profit'] for i in all_data])
    else:
        all_data = [{'Дані відсутні': 'Список спостереження порожній'}]
        sum_profit = 0
    not_show = ['open_price', 'high_price', 'low_price', 'prevclose', 'positive_profit', 'user_id']
    context = {'stocks': all_data, 'title': user.username, 'message': message, 'sum_profit': sum_profit,
               'not_show': not_show}
    return render(request, 'main/user_list.html', context=context)


@login_required(login_url='/login')
def user_search_list(request):
    user = request.user
    btn = False
    if request.POST:
        stock_search = dict(request.POST)
        symbol = str(stock_search['symbol'][0]).upper()
        stocks = TradeStock.objects.filter(user=user, symbol=symbol).exclude(exch='profit').values()
        if stocks:
            all_data = list(stocks)
            print(all_data)
            for item in all_data:
                price = float(item['ask_price'])
                data_symbol = symbol_stocks(item['symbol'])
                price_new = data_symbol['quotes']['quote']['bid']
                delta = round((price_new - price) * 100, 2)
                item['profit'] = delta
                item['bid_price'] = price
                item['ask_price'] = price_new
                item['change_percentage'] = round((price_new - price) / price * 100, 2)
                if delta >= 0:
                    item['positive_profit'] = True
                else:
                    item['positive_profit'] = False
            all_data = sorted(all_data, key=lambda symbol: symbol['trade_date'], reverse=True)
            sum_profit = sum([+i['profit'] for i in all_data])
        else:
            all_data = [{'Дані відсутні': f'Символ {stock_search["symbol"][0]} не знайдено'}]
            btn = True
            sum_profit = 0
        not_show = ['open_price', 'high_price', 'low_price', 'prevclose', 'positive_profit', 'user_id']
        context = {'stocks': all_data, 'title': user.username, 'sum_profit': sum_profit,
                   'not_show': not_show, 'btn': btn}
        return render(request, 'main/user_list.html', context=context)
    return HttpResponseRedirect(redirect_to='user/list')


@login_required(login_url='/login')
def user_list_sel(request):
    user = request.user
    if request.POST:
        sel_stock = dict(request.POST)

        sel_stock = str(sel_stock['stock'][0]).replace('<', '').replace('>', '').replace('Decimal', 'float').replace(
            'UTC', '').replace('=', '').replace('tzinfo', '')
        print('replace    ', sel_stock)
        sel_stock = eval(sel_stock)
        sel = TradeStock.objects.filter(id=sel_stock['id']).update(prevclose=float(sel_stock['profit']), exch='profit')
        return HttpResponseRedirect(redirect_to='/user/list')
    return render(request, 'main/user_list.html')


@login_required(login_url='/login')
def user_profit(request):
    user = request.user
    user_profit = TradeStock.objects.filter(user=user, exch='profit').values()
    if user_profit:
        sum_profit = sum([+i['prevclose'] for i in user_profit])
        if sum_profit < 0:
            message = f'Отриманий збиток за період з {user.date_joined} по {str(datetime.datetime.today())[:16]}'
        else:
            message = f'Отриманий прибуток за період з {user.date_joined} по {str(datetime.datetime.today())[:16]}'
        for i in user_profit:
            if i['prevclose'] > 0:
                i['positive_profit'] = True
            else:
                i['positive_profit'] = False
    else:
        message = f"Ви не здійнили, ще жодної операції."
        sum_profit = 0
        user_profit = [{'Дані відсутні': 'Список операцій порожній'}]
    not_show = ['open_price', 'high_price', 'low_price', 'prevclose', 'positive_profit',
                'user_id', 'week_52_high', 'week_52_low', 'exch']
    context = {'stocks': user_profit, 'title': user.username,
               'sum_profit': sum_profit, 'not_show': not_show, 'message': message}
    return render(request, 'main/user_profit.html', context=context)


@login_required(login_url='/login')
def del_user(request):
    return render(request, 'main/delete_profile.html')


@login_required(login_url='/login')
def logout_user(request):
    title = check_user(request)
    message = f'До зустрічі {title}'
    logout(request)
    title = check_user(request)
    return render(request, 'main/index.html', context={'title': title, 'message': message})
