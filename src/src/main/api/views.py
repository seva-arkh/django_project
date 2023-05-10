# from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseRedirect
from main.models import Wallet, Transaction

# from .forms import CreateNewWallet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.api.serializer import TransactionSerializer, WalletSerializer

import decimal
import uuid


@api_view(["GET", "POST"])
def all_wallets(response):
    if response.method == "GET":
        wallets = response.user.wallet.all()
        transactions = []
        for wallet in wallets:
            serializer = WalletSerializer(wallet)
            transactions.append(serializer.data)
        return Response(transactions)
    elif response.method == "POST":
        wallets = response.user.wallet.all()
        if len(wallets) >= 5:
            return Response({"You cannot create more than 5 wallets"})
        type = response.data["type"]
        currency = response.data["currency"]
        name = uuid.uuid4().hex[:8].upper()
        balance = 0
        if currency == "RUB":
            balance = 100
        else:
            balance = 3
        t = Wallet(name=name, type=type, currency=currency, balance=balance)
        t.save()
        response.user.wallet.add(t)
        serializer = WalletSerializer(t)
        return Response(serializer.data)


@api_view(["GET", "DELETE"])
def wallet(response, name):
    wallet = Wallet.objects.get(name=name)
    if response.method == "GET":
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    elif response.method == "DELETE":
        wallet.delete()
        return Response({"DELETED"})


@api_view(["GET", "POST"])
def all_transactions(response):

    if response.method == "GET":
        wallets = response.user.wallet.all()
        transactions = []
        for wallet in wallets:
            serializer = TransactionSerializer(wallet.transaction_set.all(),
                                               many=True)
            if serializer.data:
                print(serializer.data)
                transactions.append(serializer.data)
        return Response(transactions)

    else:
        sender = Wallet.objects.get(name=response.data["sender"])
        receiver = Wallet.objects.get(name=response.data["receiver"])

        transfer_amount = decimal.Decimal(response.data["transfer_amount"])
        commision = decimal.Decimal(0)

        if sender.user != receiver.user:
            commision = round(transfer_amount * decimal.Decimal(0.1), 2)

        if (
            sender.currency == receiver.currency
            and sender.balance > transfer_amount
            and transfer_amount > 0
        ):
            sender.balance -= transfer_amount
            receiver.balance += transfer_amount - commision
            sender.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=transfer_amount,
                commision=commision,
            )
            receiver.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=transfer_amount,
                commision=commision,
            )
            return Response({"PAID"})
        else:
            status = "FAILED"
            sender.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=transfer_amount,
                commision=commision,
                status=status,
            )
            receiver.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=transfer_amount,
                commision=commision,
                status=status,
            )
            sender.save()
            receiver.save()
            return Response({"FAILED"})


@api_view(["GET"])
def transaction(response, id):
    transaction = Transaction.objects.get(id=id)
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)


@api_view(["GET"])
def wallet_transactions(response, name):
    wallet = Wallet.objects.get(name=name)
    serializer = TransactionSerializer(wallet.transaction_set.all(), many=True)
    return Response(serializer.data)
