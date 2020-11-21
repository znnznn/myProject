from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.

user = get_user_model()


class TradeStock(models.Model):
    """ database model for analysis of selected stocks """

    user = models.ForeignKey(user, verbose_name='Біржовий аналітик', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50, verbose_name='Символ')
    description = models.TextField(max_length=500, verbose_name='Емітент цінних паперів')
    exch = models.CharField(max_length=50, verbose_name='Біржа')
    stock_type = models.CharField(max_length=50, verbose_name='Тип цінних паперів')
    open_price = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Ціна відкриття')
    high_price = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Найвища ціна')
    low_price = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Найнижча ціна')
    bid_price = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Ціна продажу')
    ask_price = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Ціна купівлі')
    change_percentage = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Зміна у відсотках')
    prevclose = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Попередня ціна закриття')
    week_52_high = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Найвижча ціна за рік')
    week_52_low = models.DecimalField(max_digits=50, decimal_places=5, verbose_name='Найнижча ціна за рік')
    trade_date = models.DateTimeField(auto_now=True, verbose_name='Дата купівлі')

    def data_stock(self, stock: dict):
        self.symbol = stock['symbol']
        self.description = stock['description']
        self.exch = stock['exch']
        self.stock_type = stock['type']
        self.open_price = stock['open']
        self.high_price = stock['high']
        self.low_price = stock['low']
        self.bid_price = stock['bid']
        self.ask_price = stock['ask']
        self.change_percentage = stock['change_percentage']
        self.prevclose = stock['prevclose']
        self.week_52_high = stock['week_52_high']
        self.week_52_low = stock['week_52_low']
        try:
            self.save()
            return True
        except:
            return False




class Message(models.Model):
    """ database model for sent message """

    user_name = models.CharField(max_length=50, verbose_name='Name')
    user_email = models.CharField(max_length=50, verbose_name='Email')
    message = models.TextField(max_length=500, verbose_name='message')
    msg_date = models.DateTimeField(auto_now=True, verbose_name='message_date')
