from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import SignUp

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        f'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
]
