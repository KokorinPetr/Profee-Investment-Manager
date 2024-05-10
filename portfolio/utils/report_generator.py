from django.shortcuts import get_object_or_404

from decimal import Decimal, ROUND_HALF_UP
import datetime as dt

# will change file name below
from google_sh_connection import GetCurrencyRate

from ..models import Stock


def report_generator(portfolio):
    stocks = Stock.objects.filter(portfolio=portfolio)
    response_content = f'Report about portfolio: {portfolio.name}\n'
    response_content += f'Portfolio owner: {portfolio.user}\n'
    response_content += f'Date: {dt.date.today()}\n'
    response_content += 'Stock list:\n'
    total_value = Decimal('0.00')

    for i, stock in enumerate(stocks):
        current_price = GetCurrencyRate().get_rate(stock.name)
        if isinstance(current_price, str):
            response_content += f"  {i+1}. {stock.name} - Quantity: {stock.quantity}, purchase price: ${stock.purchase_price.amount} USD, we don't have current price yet.\n"
            continue
        
        current_price = Decimal(current_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        purchase_price = stock.purchase_price.amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        current_value = Decimal(stock.quantity) * current_price
        difference = (purchase_price - current_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        
        response_content += f'  {i+1}. {stock.name} - Quantity: {stock.quantity}, purchase price: ${purchase_price} USD, current price: ${current_price} USD, difference: ${difference} USD\n'
        total_value += current_value

    total_value = total_value.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    response_content += f'Total value: ${total_value}\n'
    return response_content