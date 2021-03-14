import requests
import json
import time

#  url = 'https://sandbox.tradier.com/v1/markets/etb'   /beta/markets/fundamentals/corporate_actions


def all_stocks():

    url = 'https://sandbox.tradier.com/v1/markets/etb'
    headers = {"Accept":"application/json",
           "Authorization":"Bearer 6ieiYLJ6rJGbWJWHXOivBDFYi7kR"}

    response = requests.request("GET", url, headers=headers)
    resp = response.json()
    stocks = open('stocks_all.json', 'w')
    json.dump(resp, stocks, indent=4)


def symbol_stocks(symbol: str):

    #url = f"https://api.tradier.com/v1/markets/quotes?symbols=aapl"
    url = f'https://sandbox.tradier.com/v1/markets/quotes?symbols={symbol.upper()}'
    headers = {"Accept": "application/json",
               "Authorization": "Bearer 6ieiYLJ6rJGbWJWHXOivBDFYi7kR"}
    response = requests.request("GET", url, headers=headers)
    resp = response.json()
    if resp['quotes'].get('quote') is None:
        return False
    return resp


def symbol_stocks_historical(symbol: str, start_date: str, end_date: str, interval: str) -> dict:
    date = "year, month, day, daily, weekly, monthly"
    #url = f"https://api.tradier.com/v1/markets/quotes?symbols=aapl"
    url = f'https://sandbox.tradier.com/v1/markets/history'
    params = {'symbol': symbol, 'interval': interval, 'start': start_date, 'end': end_date}
    headers = {"Accept": "application/json",
               "Authorization": "Bearer 6ieiYLJ6rJGbWJWHXOivBDFYi7kR"}
    response = requests.get(url, params=params, headers=headers)
    resp = response.json()
    print(response.status_code)
    return resp['history']['day']


if __name__ == '__main__':
    print(symbol_stocks_historical(symbol='AAPL', start_date='2021-03-01', end_date='2021-03-05', interval='daily'))


""" A	NYSE MKT
B	NASDAQ OMX BX
C.	Національна фондова біржа
D	FINRA ADF
Е	Незалежний від ринку (Створено Nasdaq SIP)
F	Взаємні фонди / грошові ринки (NASDAQ)
Я	Міжнародна біржа цінних паперів
J	Прямий край A
К	Direct Edge X
М	Чиказька фондова біржа
N	NYSE
P	NYSE Arca
Питання	NASDAQ OMX
S	NASDAQ Маленька кришка
Т	NASDAQ Int
U	OTCBB
V	Позабіржове інше
W	CBOE
X	NASDAQ OMX PSX
G	GLOBEX
Y	BATS Y-обмін
Z	ЛУПИЦИ
Потоки OPRA (опції)
A	Параметри NYSE Amex
B	Біржа опцій BOX
C.	Чиказька біржа опціонів (CBOE)
H	ISE Близнюки
Я	Міжнародна біржа цінних паперів (ISE)
М	Обмін опціонами MIAX
N	Параметри NYSE Arca
О	Орган, що звітує за опціонами (OPRA)
P	МІАКС ПЕРЛИНА
Питання	Ринок опціонів NASDAQ
Т	NASDAQ OMX BX
W	C2 Обмін опціями
X	NASDAQ OMX PHLX
Z	Ринок опціонів BATS

© Tradier Inc. Всі права захищені.

 """