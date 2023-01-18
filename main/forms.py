from django import forms


class CreateNewWallet(forms.Form):
    card_type = (("VISA","VISA"), ("MASTERCARD","MASTERCARD"))
    currency_type = (("RUB", "RUB"), ("USD", "USD"), ("EUR", "EUR"))
    type = forms.ChoiceField(required=True, choices=card_type)
    currency = forms.ChoiceField(required=True, choices=currency_type)
