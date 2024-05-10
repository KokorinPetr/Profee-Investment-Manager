from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail

import datetime as dt

from .models import Portfolio, Stock, User
from .forms import GetRatesForm, StockForm, GetEmailForm
from .utils.report_generator import report_generator


from google_sh_connection import GetCurrencyRate


def index(request):
    time_now = dt.datetime.now()
    context = {
        'time_now': time_now
    }
    return render(request, 'portfolio/index.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    portfolios = Portfolio.objects.filter(user=user).prefetch_related('stock_set')

    selected_portfolio_id = request.GET.get('portfolio_id')
    if selected_portfolio_id:
        selected_portfolio = portfolios.filter(id=selected_portfolio_id).first()
    else:
        selected_portfolio = portfolios.first() if portfolios.exists() else None

    context = {
        'user': user,
        'portfolios': portfolios,
        'selected_portfolio': selected_portfolio
    }
    return render(request, 'portfolio/profile.html', context)


def get_rates(request):
    context = {}
    in_base_flag = False
    if request.method == 'POST':
        form = GetRatesForm(request.POST)
        if form.is_valid():
            currency_name = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            exchange_rate = GetCurrencyRate().get_rate(currency_name)
            if isinstance(exchange_rate, (int, float)):
                sell_price = amount * exchange_rate
                context['currency_name'] = currency_name
                context['exchange_rate'] = exchange_rate
                context['sell_price'] = sell_price
                in_base_flag = True
            else:
                context['error_message'] = "We appologize, but we don't have that in our base."
    else:
        form = GetRatesForm()
    context['form'] = form
    context['in_base_flag'] = in_base_flag
    return render(request, 'portfolio/get_rates.html', context)


@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.user == stock.portfolio.user:
        stock.delete()
        return redirect('portfolio:profile', username=request.user.username)
    return redirect('portfolio:profile', username=request.user.username)


@login_required
def add_to_portfolio(request):
    form = StockForm(
        request.POST or None,
        user=request.user
    )
    if not form.is_valid():
        return render(request, 'portfolio/stock_add.html', {'form': form})
    stock = form.save(commit=False)
    stock.save()
    return redirect('portfolio:profile', request.user)


@login_required
def generate_portfolio_report(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.user != portfolio.user:
        return HttpResponse('Access denied', status=403)
    response_content = report_generator(portfolio)
    response = HttpResponse(response_content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="portfolio_report.txt"'
    return response


def get_email(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.user != portfolio.user:
        return HttpResponse('Access denied', status=403)
    response_content = report_generator(portfolio)
    to_email = portfolio.user.email
    send_mail(
        f'Hello {portfolio.user.first_name} {portfolio.user.last_name}, this is your report on {portfolio.name}.',
        response_content,
        'profeeinvest@mail.ru',
        [to_email],
        fail_silently=False,
    )
    return HttpResponse('Message was sucsesfuly sent!')
