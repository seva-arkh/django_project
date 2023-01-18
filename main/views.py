from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Wallet, Transaction
from .forms import CreateNewWallet
import decimal
import uuid

# Create your views here.

def index(response, id):
	ls = Wallet.objects.get(id=id)

	if response.user.wallet.all():
		if response.method == "POST":
			print(response.POST)
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
				return render(response, "main/view_transactions.html", {"ls": ls})

	return render(response, "main/wallet.html", {"ls": ls})


def home(response):
	return render(response, "main/home.html", {})

def create(response):

	if response.method == "POST":
		form  = CreateNewWallet(response.POST)

		if form.is_valid():
			t = form.cleaned_data["type"]
			c = form.cleaned_data["currency"]
			n = uuid.uuid4().hex[:8].upper()
			if c=="RUB":
				b = 100
			else:
				b = 3
			t = Wallet(name=n, type=t, currency=c, balance=b)

			t.save()
			response.user.wallet.add(t)

		return HttpResponseRedirect("/%i" %t.id)

	else:
		form  = CreateNewWallet()

	return render(response, "main/create.html", {"form": form})

def view(response):
	return render(response, "main/view.html", {})

def transfer(response):
	if response.method == "POST":
		if response.POST.get("internal"):
			 return  HttpResponseRedirect('/internal')
		if response.POST.get("external"):
			return  HttpResponseRedirect('/external')

	return render(response, "main/transfer_type.html", {})

def transfer_internal(response):
	if response.method == "POST":
		if response.POST.get("next"):
			wallet_1 = Wallet.objects.get(name=response.POST.get("from"))
			wallet_2 = Wallet.objects.get(name=response.POST.get("to"))
			amount = decimal.Decimal(response.POST.get("amount"))

			if amount <= wallet_1.balance and wallet_1.currency == wallet_2.currency:
				wallet_1.balance = round(wallet_1.balance - decimal.Decimal(amount), 2)
				wallet_2.balance = round(wallet_2.balance - decimal.Decimal(amount), 2)

				wallet_1.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=0)
				wallet_2.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=0)
				wallet_1.save()
				wallet_2.save()
			else:
				wallet_1.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=0, status="FAILED")
				wallet_2.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=0, status="FAILED")
				wallet_1.save()
				wallet_2.save()
			return  HttpResponseRedirect('/home')

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
			wallet_1 = Wallet.objects.get(name=response.POST.get("from"))
			wallet_2 = Wallet.objects.get(name=response.POST.get("to"))
			amount = decimal.Decimal(response.POST.get("amount"))

		commision = round(amount*decimal.Decimal(0.1), 2)

		if amount <= wallet_1.balance and wallet_1.currency == wallet_2.currency:
			wallet_1.balance = round(wallet_1.balance - decimal.Decimal(amount), 2)
			wallet_2.balance = wallet_2.balance + round(amount*decimal.Decimal(0.9), 2)

			wallet_1.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=commision)
			wallet_2.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=commision)
			wallet_1.save()
			wallet_2.save()

		else:
			wallet_1.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=commision, status="FAILED")
			wallet_2.transaction_set.create(sendler=wallet_1.name, reciever=wallet_2.name, transfer_amount=amount, commision=commision, status="FAILED")
			wallet_1.save()
			wallet_2.save()
		return  HttpResponseRedirect('/home')
	return render(response, "main/transfer_external.html", {"other_wallets": other_wallets})
