from django import forms

from .models import Stock, Portfolio

class GetRatesForm(forms.Form):
    currency = forms.CharField()
    amount = forms.FloatField()


class DateInput(forms.DateInput):
    input_type = 'date'

class StockForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['portfolio'].queryset = Portfolio.objects.filter(user=user)


    class Meta:
        model = Stock
        fields = [
            'portfolio', 'name', 'quantity', 
            'purchase_price', 'purchase_date',
        ]
        widgets = {
            'purchase_date': DateInput(),
        }


class GetEmailForm(forms.Form):
    email = forms.CharField(max_length=100)
