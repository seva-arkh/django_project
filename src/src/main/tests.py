from django.test import TestCase
from main.models import Wallet, Transaction
import uuid


# Create your tests here.
class URLTests(TestCase):
    def test_testhomepage(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_createwallet(self):
        name_1 = uuid.uuid4().hex[:8].upper()
        wallet1 = Wallet(name=name_1, type="VISA", currency="USD", balance=3)
        self.assertEqual(wallet1.name, name_1)
        self.assertEqual(wallet1.type, "VISA")
        self.assertEqual(wallet1.currency, "USD")
        self.assertEqual(wallet1.balance, 3)

    def test_internaltransaction(self):
        name_1 = uuid.uuid4().hex[:8].upper()
        name_2 = uuid.uuid4().hex[:8].upper()
        sender = Wallet(name=name_1,
                        type="VISA",
                        currency="USD",
                        balance=3)
        receiver = Wallet(name=name_2,
                          type="MASTERCARD",
                          currency="USD",
                          balance=3)
        amount = 1
        sender.balance = sender.balance - amount
        receiver.balance = receiver.balance + amount
        Transaction(
                wallet=sender,
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=amount,
                commision=0,
                status="PAID",
            )
        Transaction(
                wallet=receiver,
                sender=sender.name,
                receiver=receiver.name,
                transfer_amount=amount,
                commision=0,
                status="PAID",
            )
        sender.save()
        receiver.save()
        self.assertEqual(sender.balance, 2)
        self.assertEqual(receiver.balance, 4)
        for i in sender.transaction_set.all():
            self.assertEqual(i.sender, sender.name)
            self.assertEqual(i.receiver, receiver.name)
            self.assertEqual(i.transfer_amount, amount)
            self.assertEqual(i.commision, 0)
            self.assertEqual(i.status, "PAID")
        for i in receiver.transaction_set.all():
            self.assertEqual(i.sender, receiver.name)
            self.assertEqual(i.receiver, receiver.name)
            self.assertEqual(i.transfer_amount, amount)
            self.assertEqual(i.commision, 0)
            self.assertEqual(i.status, "PAID")
