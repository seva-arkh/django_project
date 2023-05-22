# django_project
prototype of a bank app using django REST framework. It has such fuctions
URLS:
### "register_api/"
Create an account. API request: {  
    "username": "",  
    "email": "",  
    "password": ""  
}
### "login_api/"
login to an account. API request: {  
    "username": "",  
    "password": ""  
}
### "logout_api/"
logout from an account

### "wallets/"
* view all user's wallets. Returns in such form: {  
        "id": "16",  
        "name": "E3FCB82E",  
        "type": "VISA",  
        "currency": "RUB",  
        "balance": "145.00",  
        "created_on": "2023-05-09T14:26:05.756975Z",  
        "modified_on": "2023-05-09T14:53:38.385735Z"  
    }. 
    * id: id of a wallet
    * name: unique name of each wallet. It is an 8 character long name that is generated randomly  
    * type: type of a wallet out of 2 options: VISA, MASTERCARD:
    * currency: currency type of a wallet out of 3 options: USD, EUR, RUB
    * balance: balance of a wallet
    * created_on: time when a wallet was created
    * modified_on: time when the balance was updated
* create a wallet. API request: {  
        "type": "VISA",  
        "currency": "RUB",  
    }.  
    This request creates a wallet with a balance depending on currency type. If currency is USD or EUR the balance will be 3. If currency is RUB the balance will be 100. It is possible to have up to 5 wallets.

### "wallets/wallet_name/"
* view wallet information by its wallet_name
* delete this wallet

### "wallets/transactions/"
* view all user's transactions in such form:{  
            "id": "31",  
            "sender": "7A758158",  
            "receiver": "E3FCB82E",  
            "transfer_amount": "25.00",  
            "commission": "0.00",  
            "status": "PAID",  
            "timestamp": "2023-05-09T14:42:53.685596Z". 
        }   
    * id: id of a transaction.
    * sender: name of a sender's wallet. The type of currency of the receiver's and sender's wallet should be the same.
    * receiver: name of a receiver's wallet.
    * transfer_amount: the amount of money transferred from one wallet to another.  
    * commission: commission: commission is 0 if the sender and receiver wallets belong to one user. Otherwise, the commission is 5%.
    * status: it can be PAID or FAILED depending on whether or not a transaction was completed successfully.
    * timestamp: the time when a transaction was made.

### "wallets/transactions/id/"
get a transaction by its id

### "wallets/transactions/wallet_name/" 
get all transactions of one wallet using wallet_name
