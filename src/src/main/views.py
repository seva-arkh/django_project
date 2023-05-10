from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.models import Wallet

from main.forms import CreateNewWallet

import decimal
import uuid


# Create your views here.
def index(response, id):
    ls = Wallet.objects.get(id=id)
    if response.user.wallet.all():
        if response.method == "POST":
            if response.POST.get("newItem"):
                val = response.POST.get("new")
                if val:
                    ls.balance = round(ls.balance + decimal.Decimal(val), 2)
                    ls.save()
                return render(response, "main/wallet.html", {"ls": ls})
            if response.POST.get("deleteWallet"):
                ls.delete()
                return render(response, "main/view.html", {"ls": ls})
            if response.POST.get("view_transactions"):
                return render(response, "main/view_transactions.html",
                              {"ls": ls})
    return render(response, "main/wallet.html", {"ls": ls})


def home(response):
    return render(response, "main/home.html", {})


def create(response):
    print(response.POST)
    if response.method == "POST":
        form = CreateNewWallet(response.POST)

        if form.is_valid():
            t = form.cleaned_data["type"]
            c = form.cleaned_data["currency"]
            n = uuid.uuid4().hex[:8].upper()
            if c == "RUB":
                b = 100
            else:
                b = 3
            t = Wallet(name=n, type=t, currency=c, balance=b)

            t.save()
            response.user.wallet.add(t)

        return HttpResponseRedirect("/%i" % t.id)

    else:
        form = CreateNewWallet()

    return render(response, "main/create.html", {"form": form})


def view(response):
    return render(response, "main/view.html", {})


def transfer(response):
    if response.method == "POST":
        if response.POST.get("internal"):
            return HttpResponseRedirect("/internal")
        elif response.POST.get("external"):
            return HttpResponseRedirect("/external")

    return render(response, "main/transfer_type.html", {})


def transfer_internal(response):
    if response.method == "POST":
        if response.POST.get("next"):
            print(12345)
            sender = Wallet.objects.get(name=response.POST.get("from"))
            receiver = Wallet.objects.get(name=response.POST.get("to"))
            amount = decimal.Decimal(response.POST.get("amount"))

            if amount <= sender.balance and \
                    sender.currency == receiver.currency:
                sender.balance = round(sender.balance -
                                       decimal.Decimal(amount), 2)
                receiver.balance = round(receiver.balance +
                                         decimal.Decimal(amount), 2)
                status = "PAID"

            else:
                status = "FAILED"

            sender.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=amount,
                commision=0,
                status=status,
            )
            receiver.transaction_set.create(
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=amount,
                commision=0,
                status=status,
            )
            print(sender.name, receiver.name)
            sender.save()
            receiver.save()
            return HttpResponseRedirect("/home")

    return render(response, "main/transfer_internal.html", {})


def transfer_external(response):
    wallets = Wallet.objects.all()
    other_wallets = []
    u_id = response.user
    for wallet in wallets:
        if wallet.user != u_id:
            other_wallets.append(wallet)
    if response.method == "POST":
        if response.POST.get("next"):
            sender = Wallet.objects.get(name=response.POST.get("from"))
            receiver = Wallet.objects.get(name=response.POST.get("to"))
            amount = decimal.Decimal(response.POST.get("amount"))

        commision = round(amount * decimal.Decimal(0.1), 2)

        if amount <= sender.balance and \
                sender.currency == receiver.currency:
            sender.balance = round(sender.balance -
                                   decimal.Decimal(amount), 2)
            receiver.balance = receiver.balance + round(
                amount * decimal.Decimal(0.9), 2
            )
            status = "PAID"
        else:
            status = "FAILED"
        sender.transaction_set.create(
            sender=sender.name,
            receiver=receiver.name,
            transfer_amount=amount,
            commision=commision,
            status=status,
        )
        print(sender.name, receiver.name)
        receiver.transaction_set.create(
            sender=sender.name,
            receiver=receiver.name,
            transfer_amount=amount,
            commision=commision,
            status=status,
        )

        sender.save()
        receiver.save()
        return HttpResponseRedirect("/home")
    return render(
        response, "main/transfer_external.html",
        {"other_wallets": other_wallets}
    )
