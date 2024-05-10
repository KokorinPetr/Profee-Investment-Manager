from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),

    path('get_rates/', views.get_rates, name='get_rates'),

    path('stock/delete/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('stock/add/', views.add_to_portfolio, name='add_stock'),
    path('portfolio/<int:portfolio_id>/report/', views.generate_portfolio_report, name='portfolio_report'),
    path('portfolio/<int:portfolio_id>/report/on-mail/', views.get_email, name='email_portfolio_report'),
    path('', views.index, name='index')
]
