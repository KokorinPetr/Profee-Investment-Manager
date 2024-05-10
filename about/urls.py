from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path(
        'contact-infomation/',
        views.ContactInformationView.as_view(),
        name='contact_infomation'
    ),
]
