
import datetime
import json

from OpenSSL import SSL
#context = SSL.Context()
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, request, redirect, g, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_talisman import Talisman
from flask_seasurf import SeaSurf

from lesson_29_flask.userLogin_flask import UserLogin
from lesson_29_flask.db_flask import DataBase
from lesson_29_flask.tradier_api import symbol_stocks

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
#Talisman(app)
#app.config['SESSION_COOKIE_SECURE'] = True
#app.config['SESSION_COOKIE_HTTPONLY'] = False

login_manager = LoginManager(app)
#login_manager.session_protection = "strong"
amount_stock = 10
PER_PAGE = 1

@app.route('/')
@app.route('/index')
def main_page():
    return render_template('index.html', title='Головна сторінка')


@login_manager.user_loader
def load_user(user_id):
    user = UserLogin(user_id).user_db(user_id)
    return user


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('user_page'))
    if request.method == 'POST':
        data_user = dict(request.form)
        data_user['refactor_email'] = str(data_user['EMAIL']).replace('@', '$').replace('.', '$')
        user = DataBase(data_user)
        user_id = user.take_user()
        if user_id and check_password_hash(user_id['PASSWORD'], data_user['PASSWORD']):
            remember_me = True if data_user.get('remember') else False
            userLogin = UserLogin(user_id).user_id(user_id)
            login_user(userLogin, remember=remember_me)
            return redirect('/user/1')
        else:
            flash('Невірно введений email або пароль')
            return redirect(url_for('login_page'))
    return render_template('login.html', title='Авторизація')


@app.route('/contacts',  methods=['POST', 'GET'])
def contacts_page():
    if request.method == 'POST':
        data_user = dict(request.form)
        for key, values in data_user.items():
            data_user[key] = values.strip()
        if "" in data_user.values():
            flash('Всі поля мають бути заповненими')
            return redirect(url_for('contacts_page'))
        data_user['date'] = str(datetime.datetime.today())[:16]
        user = DataBase(data_user)
        message = user.add_message()
        if message:
            flash('Повідомлення успішно відправлено')
            return render_template('contacts.html', title='Контакти')
        flash("Сталась помилка з\'єднання з базою даних")
        return redirect(redirect(url_for('contacts_page')))
    return render_template('contacts.html', title='Контакти')


@app.route('/user/<int:page>', methods=['GET', 'POST'])
@login_required
def user_page(page=1):
    count_page = 3
    user_id = current_user.user_data()
    with open('stocks.json', 'r') as file_stocks:
        list_stocks = json.load(file_stocks)
        my_stocks = list_stocks['securities']['security']
        my_stocks = sorted(my_stocks, key=lambda symbol: symbol['symbol'])
        pages = round(len(my_stocks) / amount_stock)
        print(len(my_stocks), pages)
    page = page if 1 <= page else 1
    page = page if page <= pages else pages
    start_pos = 0 if page == 1 else (page - 1) * amount_stock
    start_pos = start_pos if pages <= len(my_stocks) else len(my_stocks)
    end_pos = start_pos + amount_stock
    end_pos = end_pos if end_pos <= len(my_stocks) else len(my_stocks)
    my_stocks = my_stocks[start_pos:end_pos]
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    show_page = {
        'prev_page': page - 1,
        'page_1': page,
        'page_2': page + 1,
        'page_3': page + 2,
        'next_page': page + count_page,
        'pages': pages
    }
    i = 0
    while i != len(my_stocks):
        data_symbol = symbol_stocks(my_stocks[i]['symbol'])
        if None is not data_symbol['quotes']['quote']['change_percentage'] >= 0:
            my_stocks[i]['positive_change'] = True
        else:
            my_stocks[i]['positive_change'] = False
        my_stocks[i]['quote'] = data_symbol['quotes']['quote']
        i += 1
    #print(my_stocks[0])
    return render_template('user.html',  title=f'{user_name}', stocks=my_stocks, page=show_page)


@app.route('/user/stocks/search/all', methods=['GET', 'POST'])
@login_required
def user_search():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    if request.method == 'POST':
        stock = dict(request.form)
        symbol = stock['symbol']
        data_symbol = symbol_stocks(symbol)
        if data_symbol:
            with open('stocks.json', 'r') as file_stocks:
                list_stocks = json.load(file_stocks)
                my_stocks = [i for i in list_stocks['securities']['security'] if i['symbol'] == symbol]
            if data_symbol['quotes']['quote']['change_percentage'] >= 0:
                my_stocks[0]['positive_change'] = True
            else:
                my_stocks[0]['positive_change'] = False
            my_stocks[0]['quote'] = data_symbol['quotes']['quote']
            return render_template('user.html', title=f'{user_name}', stocks=my_stocks)
        my_stocks = [{'Дані відсутні': f'Символ {stock["symbol"]} не знайдено'}]
        return render_template('user.html', title=f'{user_name}', stocks=my_stocks)
    return redirect(url_for('user_page'))


@app.route('/user/stocks/search', methods=['GET', 'POST'])
@login_required
def user_list_search():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    if request.method == 'POST':
        my_stocks = dict(request.form)
        my_stocks['symbol'] = str(my_stocks['symbol']).upper()
        user_id['stock'] = my_stocks
        user_stocks = DataBase(user_id).take_user_views_symbol()
        if user_stocks:
            i = 0
            while i != len(user_stocks):
                price = user_stocks[i]['ask']
                data_symbol = symbol_stocks(user_stocks[i]['symbol'])
                price_new = data_symbol['quotes']['quote']['bid']
                if not price_new:
                    price_new = 0
                delta = round((price_new - price) * 100, 2)
                user_stocks[i]['profit'] = delta
                user_stocks[i]['bid'] = price
                user_stocks[i]['ask'] = price_new
                user_stocks[i]['change_percentage'] = round((price_new - price) / price * 100, 2)
                if delta >= 0:
                    user_stocks[i]['positive_profit'] = True
                else:
                    user_stocks[i]['positive_profit'] = False
                i += 1
                sum_profit = sum([+i['profit'] for i in user_stocks])
                return render_template('user_list.html', title=f'{user_name}', stocks=user_stocks, sum_profit=sum_profit)
        user_stocks = [{'Дані відсутні': f'Символ {my_stocks["symbol"]} не знайдено'}]
        sum_profit = 0
        return render_template('user_list.html', title=f'{user_name}', stocks=user_stocks, sum_profit=sum_profit)

    return user_list()


@app.route('/user/stocks', methods=['GET', 'POST'])
@login_required
def user_list():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
        text_flash = 'Вітаємо.'
    else:
        user_name = str(user_id)
        text_flash = ''
    if request.method == 'POST':
        my_stocks = dict(request.form)
        my_stocks = eval(my_stocks['stock'])
        if not my_stocks.get('quote'):
            data_symbol = symbol_stocks(my_stocks['symbol'])
            if True is data_symbol['quotes']['quote']['change_percentage'] >= 0:
                my_stocks['positive_change'] = True
            else:
                my_stocks['positive_change'] = False
            my_stocks['quote'] = data_symbol['quotes']['quote']
            return render_template('user.html', title=f'{user_name}', stocks=[my_stocks])
        my_stocks = my_stocks['quote']
        my_stocks['trade_date'] = str(datetime.datetime.today())[:16]
        user_id['stock'] = my_stocks
        user_stocks = DataBase(user_id)
        user_stocks = user_stocks.add_user_views()
        if user_stocks:
            text_flash = 'Дані збережено'
        else:
            text_flash = f"Символ паперу {my_stocks['symbol']}: {my_stocks['description']} вже відслідковується"
    user_stocks = DataBase(user_id)
    user_stocks = user_stocks.take_user_views()
    if not user_stocks:
        sum_profit = 0
        user_stocks = [{'Дані відсутні': 'Список спостереження порожній'}]
        return render_template('user_list.html', title=f'{user_name}', stocks=user_stocks, sum_profit=sum_profit)
    i = 0
    while i != len(user_stocks):
        price = user_stocks[i]['ask']
        data_symbol = symbol_stocks(user_stocks[i]['symbol'])
        price_new = data_symbol['quotes']['quote']['bid']
        if not price_new:
            price_new = 0
        delta = round((price_new - price) * 100, 2)
        user_stocks[i]['profit'] = delta
        user_stocks[i]['bid'] = price
        user_stocks[i]['ask'] = price_new
        user_stocks[i]['change_percentage'] = round((price_new - price) / price * 100, 2)
        if delta >= 0:
            user_stocks[i]['positive_profit'] = True
        else:
            user_stocks[i]['positive_profit'] = False
        i += 1
    user_stocks = sorted(user_stocks, key=lambda symbol: symbol['trade_date'], reverse=True)
    sum_profit = sum([+i['profit'] for i in user_stocks])
    flash(f'{text_flash}')
    return render_template('user_list.html', title=f'{user_name}', stocks=user_stocks, sum_profit=sum_profit)


@app.route('/user/stocks/sel', methods=['GET', 'POST'])
@login_required
def user_list_del():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    if request.method == 'POST':
        my_stocks = dict(request.form)
        my_stocks = eval(my_stocks['stock'])
        my_stocks['trade_date'] = str(datetime.datetime.today())[:16]
        user_id['stock'] = my_stocks
        user_stocks = DataBase(user_id).del_user_views()
        if user_stocks:
            if my_stocks['profit'] >= 0:
                flash_text = f'100 шт {my_stocks["symbol"]} продано з прибутком {my_stocks["profit"]}'
            else:
                flash_text = f'100 шт {my_stocks["symbol"]} продано з збитком {my_stocks["profit"]}'
        else:
            flash_text = f"Сталась помилка з\'єдання з базою даних."
        flash(flash_text)
        return redirect(url_for('user_list'))
    return render_template('index.html', title=f'{user_name}')


@app.route('/user/stocks/profit')
@login_required
def user_profit_page():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    user_profit = DataBase(user_id).take_user_profit()
    if user_profit:
        sum_profit = sum([+i['prevclose'] for i in user_profit])
        if sum_profit < 0:
            flash(f'Отриманий збиток за період з {user_id["oper_date"]} по {str(datetime.datetime.today())[:16]}')
        else:
            flash(f'Отриманий прибуток за період з {user_id["oper_date"]} по {str(datetime.datetime.today())[:16]}')
        for i in user_profit:
            if i['prevclose'] > 0:
                i['positive_profit'] = True
            else:
                i['positive_profit'] = False
    else:
        flash(f"Ви не здійнили, ще жодної операції.")
        sum_profit = 0
        user_profit = [{'Дані відсутні': 'Список операцій порожній'}]
    return render_template('user_profit.html', title=f'{user_name}', stocks=user_profit, sum_profit=sum_profit)


@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user_id = current_user.user_data()
    if request.method == 'POST':
        user = dict(request.form)
        if '' in user.values() or ' ' in user.values():
            flash('Поля мають бути заповненими')
            return redirect(url_for('profile_page'))
        elif not user['firstName'].isalpha() or not user['lastName'].isalpha():
            flash("Поле ім\'я або фамілія має містити лише букви")
            return redirect(url_for('profile_page'))
        elif '@' not in user['EMAIL'] or '.' not in user['EMAIL']:
            flash('Невірно введений формат електронної пошти')
            return redirect(url_for('profile_page'))
        elif user['PASSWORD'] != user['PASSWORD2']:
            flash('Введені паролі не рівні')
            return redirect(url_for('profile_page'))
        for key, values in user.items():
            user[key] = values.strip()
        user['id'] = user_id['id']
        user['PASSWORD'] = generate_password_hash(user['PASSWORD'])
        user.pop('PASSWORD2')
        user['date'] = str(datetime.datetime.today())[:16]
        user_edit = DataBase(user)
        db_user = user_edit.edit_user()
        if db_user:
            flash(f"{user['USERNAME']}, Ви успішно змінили особисті дані")
            return redirect(url_for('user_page'))
        flash(f"Користувач з {user['EMAIL']} вже існує")
        return redirect(url_for('new_user_page'))
    return render_template('profile_user.html', title='Профіль', username=user_id)


@app.route('/user/profile/delete', methods=['GET', 'POST'])
@login_required
def del_profile_page():
    user_id = current_user.user_data()
    if user_id:
        user_name = user_id.get('USERNAME')
        user_id['refactor_email'] = str(user_id['EMAIL']).replace('@', '$').replace('.', '$')
    else:
        user_name = str(user_id)
    if request.method == 'POST':
        logout_user()
        del_user = DataBase(user_id).del_user()
        flash(f'Нажаль {user_name} вас видалено.')
        return redirect(url_for('main_page'))
    flash(f'Ви впевненні {user_name}, що хочете себе видалити')
    return render_template('delete_profile.html', title='Видалення профілю !!!', username=user_id)


@app.route('/new_user', methods=['POST', 'GET'])
def new_user_page():
    if current_user.is_authenticated:
        return redirect(url_for('user_page'))
    if request.method == 'POST':
        data_new_user = dict(request.form)
        data_new_user['refactor_email'] = str(data_new_user['EMAIL']).replace('@', '$').replace('.', '$')
        if '' in data_new_user.values() or ' ' in data_new_user.values():
            flash('Поля мають бути заповненими')
            return redirect(url_for('new_user_page'))
        elif not data_new_user['firstName'].isalpha() or not data_new_user['lastName'].isalpha():
            flash("Поле ім\'я або фамілія має містити лише букви")
            return redirect(url_for('new_user_page'))
        elif '@' not in data_new_user['EMAIL'] or '.' not in data_new_user['EMAIL']:
            flash('Невірно введений формат електронної пошти')
            return redirect(url_for('new_user_page'))
        elif data_new_user['PASSWORD'] != data_new_user['PASSWORD2']:
            flash('Введені паролі не рівні')
            return redirect(url_for('new_user_page'))
        for key, values in data_new_user.items():  # треба дізнатись чи треба паролі стріпати
            data_new_user[key] = values.strip()
        data_new_user['PASSWORD'] = generate_password_hash(data_new_user['PASSWORD'])
        data_new_user.pop('PASSWORD2')
        data_new_user['date'] = str(datetime.datetime.today())[:16]
        new_user = DataBase(data_new_user)
        db_user = new_user.add_user()
        if db_user:
            flash(f"{data_new_user['USERNAME']}, Ви успішно зареєструвались.")
            return redirect(url_for('login_page'))
        flash(f"Користувач з {data_new_user['EMAIL']} вже існує.")
        return redirect(url_for('new_user_page'))
    return render_template('new_user.html', title='Реєстрація')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_page():
    user_id = current_user.user_data()
    if user_id:
        username = user_id.get('USERNAME')
        flash(f'{username}, Ви вийшли з кабінету.')
    logout_user()
    return redirect(url_for('main_page'))


@app.teardown_appcontext
def close(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.errorhandler(401)
def error_page(error):
    flash('Авторизуйтесь будь ласка')
    return redirect(url_for('login_page')), 401


@app.errorhandler(403)
def error_page1(error):
    flash(error)
    return render_template('login.html', title='Авторизація'), 403



@app.errorhandler(404)
def error_page1(error):
    flash('Авторизуйтесь будь ласка')
    return render_template('login.html', title='Авторизація'), 404

@app.errorhandler(500)
def error_page1(error):
    flash(error)
    return render_template('login.html', title='Авторизація'), 500


app.run(host='localhost', port='8888', debug=True)


"""@app.after_request
@app.before_request
@app.before_first_request
@app.teardown_request"""