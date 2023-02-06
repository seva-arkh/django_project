from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Wallet, Transaction
from .forms import CreateNewWallet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from .serializer import TransactionSerializer, WalletSerializer

import decimal
import uuid



# Create your views here.

# @api_view(["POST"])
# def index(response, id):
# 	ls = Wallet.objects.get(id=id)
#
# 	if response.user.wallet.all():
# 		if response.method == "POST":
# 			print(response.POST)
# 			if response.POST.get("newItem"):
# 				val = response.POST.get("new")
# 				if val:
# 					ls.balance = round(ls.balance + decimal.Decimal(val), 2)
# 					ls.save()
# 				return render(response, "main/wallet.html", {"ls": ls})
# 			if response.POST.get("deleteWallet"):
# 				ls.delete()
# 				return render(response, "main/view.html", {"ls": ls})
# 			if response.POST.get("view_transactions"):
# 				transactions = []
# 				serializer = TransactionSerializer(ls.transaction_set.all(), many=True)
# 				return Response(serializer.data)  #render(response, "main/view_transactions.html", {"ls": ls})
#
# 	return render(response, "main/wallet.html", {"ls": ls})

# @api_view(["GET"])
# def home(response):
# 	return Response({"home": "Home"})#render(response, "main/home.html", {})

# def create(response):
#
# 	if response.method == "POST":
# 		form  = CreateNewWallet(response.POST)
#
# 		if form.is_valid():
# 			t = form.cleaned_data["type"]
# 			c = form.cleaned_data["currency"]
# 			n = uuid.uuid4().hex[:8].upper()
# 			if c=="RUB":
# 				b = 100
# 			else:
# 				b = 3
# 			t = Wallet(name=n, type=t, currency=c, balance=b)
#
# 			t.save()
# 			response.user.wallet.add(t)
#
# 		return HttpResponseRedirect("/%i" %t.id)
#
# 	else:
# 		form  = CreateNewWallet()
#
# 	return render(response, "main/create.html", {"form": form})

# @api_view(['POST'])
# def create(request):
# 	type = request.data["type"]
# 	currency = request.data["currency"]
# 	name = uuid.uuid4().hex[:8].upper()
# 	balance = 0
# 	if currency=="RUB":
# 		balance = 100
# 	else:
# 		balance = 3
#
# 	t = Wallet(name=name, type=type, currency=currency, balance=balance)
# 	t.save()
# 	request.user.wallet.add(t)
# 	serializer = WalletSerializer(t)
# 	return Response(serializer.data)
# 	# else:
# 	# 	return Response(serializer.errors)

@api_view(['GET', 'POST'])
def all_wallets(response):
	if response.method == 'GET':
		wallets = response.user.wallet.all()
		transactions = []
		for wallet in wallets:
			serializer = WalletSerializer(wallet)
			transactions.append(serializer.data)
		return Response(transactions)
	elif response.method == 'POST':
		wallets = response.user.wallet.all()
		if len(wallets) >= 5:
			return Response({"You cannot create more than 5 wallets"})
		type = response.data["type"]
		currency = response.data["currency"]
		name = uuid.uuid4().hex[:8].upper()
		balance = 0
		if currency=="RUB":
			balance = 100
		else:
			balance = 3
		t = Wallet(name=name, type=type, currency=currency, balance=balance)
		t.save()
		response.user.wallet.add(t)
		serializer = WalletSerializer(t)
		return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def wallet(response, name):
	wallet = Wallet.objects.get(name=name)
	if response.method == 'GET':
		serializer = WalletSerializer(wallet)
		return Response(serializer.data)
	elif response.method == 'DELETE':
		wallet.delete()
		return Response({"DELETED"})


@api_view(['GET', 'POST'])
def all_transactions(response):

	if response.method == 'GET':
		wallets = response.user.wallet.all()
		transactions = []
		for wallet in wallets:
			serializer = TransactionSerializer(wallet.transaction_set.all(), many=True)
			if serializer.data:
				print(serializer.data)
				transactions.append(serializer.data)
		return Response(transactions)

	else:
		sender = Wallet.objects.get(name=response.data["sender"])
		receiver = Wallet.objects.get(name=response.data["receiver"])

		transfer_amount = decimal.Decimal(response.data["transfer_amount"])
		commision = decimal.Decimal(0)

		if 	sender.user != receiver.user:
			commision = round(transfer_amount*decimal.Decimal(0.1), 2)

		if sender.currency == receiver.currency and sender.balance > transfer_amount and transfer_amount > 0:
			sender.balance -= transfer_amount
			receiver.balance += transfer_amount - commision
			sender.transaction_set.create(sender=sender.name, receiver=receiver.name, transfer_amount=transfer_amount, commision=commision)
			receiver.transaction_set.create(sender=sender.name, receiver=receiver.name, transfer_amount=transfer_amount, commision=commision)
			return Response({"PAID"})
		else:
			status = "FAILED"
			sender.transaction_set.create(sender=sender.name, receiver=receiver.name, transfer_amount=transfer_amount, commision=commision, status = status)
			receiver.transaction_set.create(sender=sender.name, receiver=receiver.name, transfer_amount=transfer_amount, commision=commision, status = status)
			sender.save()
			receiver.save()
			return Response({"FAILED"})



@api_view(['GET'])
def transaction(response, id):
	transaction = Transaction.objects.get(id=id)
	serializer = TransactionSerializer(transaction)
	return Response(serializer.data)

@api_view(['GET'])
def wallet_transactions(response, name):
	wallet = Wallet.objects.get(name=name)
	serializer = TransactionSerializer(wallet.transaction_set.all(), many=True)
	return Response(serializer.data)


# def view(response):
# 	return render(response, "main/view.html", {})
#
# def transfer(response):
# 	if response.method == "POST":
# 		if response.POST.get("internal"):
# 			 return  HttpResponseRedirect('/internal')
# 		if response.POST.get("external"):
# 			return  HttpResponseRedirect('/external')
#
# 	return render(response, "main/transfer_type.html", {})
#
# def transfer_internal(response):
# 	if response.method == "POST":
# 		if response.POST.get("next"):
# 			wallet_1 = Wallet.objects.get(name=response.POST.get("from"))
# 			wallet_2 = Wallet.objects.get(name=response.POST.get("to"))
# 			amount = decimal.Decimal(response.POST.get("amount"))
#
# 			if amount <= wallet_1.balance and wallet_1.currency == wallet_2.currency:
# 				wallet_1.balance = round(wallet_1.balance - decimal.Decimal(amount), 2)
# 				wallet_2.balance = round(wallet_2.balance - decimal.Decimal(amount), 2)
#
# 				wallet_1.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=0)
# 				wallet_2.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=0)
# 				wallet_1.save()
# 				wallet_2.save()
# 			else:
# 				wallet_1.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=0, status="FAILED")
# 				wallet_2.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=0, status="FAILED")
# 				wallet_1.save()
# 				wallet_2.save()
# 			return  HttpResponseRedirect('/home')
#
# 	return render(response, "main/transfer_internal.html", {})
#
# def transfer_external(response):
# 	wallets = Wallet.objects.all()
# 	other_wallets = []
# 	u_id = response.user
# 	for wallet in wallets:
# 		if wallet.user != u_id:
# 			other_wallets.append(wallet)
# 	if response.method == "POST":
# 		if response.POST.get("next"):
# 			wallet_1 = Wallet.objects.get(name=response.POST.get("from"))
# 			wallet_2 = Wallet.objects.get(name=response.POST.get("to"))
# 			amount = decimal.Decimal(response.POST.get("amount"))
#
# 		commision = round(amount*decimal.Decimal(0.1), 2)
#
# 		if amount <= wallet_1.balance and wallet_1.currency == wallet_2.currency:
# 			wallet_1.balance = round(wallet_1.balance - decimal.Decimal(amount), 2)
# 			wallet_2.balance = wallet_2.balance + round(amount*decimal.Decimal(0.9), 2)
#
# 			wallet_1.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=commision)
# 			wallet_2.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=commision)
# 			wallet_1.save()
# 			wallet_2.save()
#
# 		else:
# 			wallet_1.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=commision, status="FAILED")
# 			wallet_2.transaction_set.create(sender=wallet_1.name, receiver=wallet_2.name, transfer_amount=amount, commision=commision, status="FAILED")
# 			wallet_1.save()
# 			wallet_2.save()
# 		return  HttpResponseRedirect('/home')
# 	return render(response, "main/transfer_external.html", {"other_wallets": other_wallets})
