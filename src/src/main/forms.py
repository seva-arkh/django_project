from django import forms
from django.db import models


class CreateNewWallet(forms.Form):
    class CardType(models.TextChoices):
        VISA = "VISA"
        MASTERCARD = "MASTERCARD"

    class CurrencyType(models.TextChoices):
        RUB = "RUB"
        USD = "USD"
        EUR = "EUR"

    card_type = (("VISA", "VISA"), ("MASTERCARD", "MASTERCARD"))
    currency_type = (("RUB", "RUB"), ("USD", "USD"), ("EUR", "EUR"))
    type = forms.ChoiceField(required=True, choices=card_type)
    currency = forms.ChoiceField(required=True, choices=currency_type)
