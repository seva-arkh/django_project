from rest_framework import serializers

# from .models import Wallet
# from django.db import models
# from django.contrib.auth.models import User
# import uuid


class TransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    sender = serializers.CharField()
    receiver = serializers.CharField()
    transfer_amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    commision = serializers.DecimalField(max_digits=20, decimal_places=2)
    status = serializers.CharField()
    timestamp = serializers.DateTimeField()


class WalletSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    type = serializers.CharField(max_length=20)
    currency = serializers.CharField(max_length=20)
    balance = serializers.DecimalField(max_digits=20, decimal_places=2,
                                       read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    modified_on = serializers.DateTimeField(read_only=True)
