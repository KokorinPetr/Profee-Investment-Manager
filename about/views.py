from django.views.generic.base import TemplateView

class ContactInformationView(TemplateView):
    template_name = 'about/contact_information.html'
