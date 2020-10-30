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
    open_price = models.DecimalField(max_digits=50, verbose_name='Ціна відкриття')
    high_price = models.DecimalField(max_digits=50, verbose_name='Найвища ціна')
    low_price = models.DecimalField(max_digits=50, verbose_name='Найнижча ціна')
    bid_price = models.DecimalField(max_digits=50, verbose_name='Ціна продажу')
    ask_price = models.DecimalField(max_digits=50, verbose_name='Ціна купівлі')
    change_percentage = models.DecimalField(max_digits=50, verbose_name='Зміна у відсотках')
    prevclose = models.DecimalField(max_digits=50, verbose_name='Попередня ціна закриття')
    week_52_high = models.DecimalField(max_digits=50, verbose_name='Найвижча ціна за рік')
    week_52_low = models.DecimalField(max_digits=50, verbose_name='Найнижча ціна за рік')
    trade_date = models.CharField(max_length=50, verbose_name='Дата купівлі')
