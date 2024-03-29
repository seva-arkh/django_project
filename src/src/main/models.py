from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
# card_type = ((1, "VISA"), (2, "MASTERCARD"))
# currency_type = ((1, "RUB"), (2, "USD"), (3, "EUR"))


class Wallet(models.Model):
    class CardType(models.TextChoices):
        VISA = "VISA"
        MASTERCARD = "MASTERCARD"

    class CurrencyType(models.TextChoices):
        RUB = "RUB"
        USD = "USD"
        EUR = "EUR"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wallet", null=True
    )
    name = models.CharField(
        max_length=8, unique=True, default=uuid.uuid4().hex[:8].upper()
    )
    type = models.CharField(max_length=20, choices=CardType.choices)
    currency = models.CharField(max_length=20, choices=CurrencyType.choices)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    transfer_amount = models.DecimalField(max_digits=20, decimal_places=2)
    commision = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=300, default="PAID")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender
