from django.db import models
from django.contrib.auth import get_user_model

from djmoney.models.fields import MoneyField

User = get_user_model()

TEXT_LIMIT = 15

class Portfolio(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE
    )
    # symbol
    # Code
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    purchase_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    purchase_date = models.DateField()# here i can make just date_field instead datetime field

    def __str__(self) -> str:
        return self.name


