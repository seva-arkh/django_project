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
log in to an account. API request: {  
    "username": "",  
    "password": ""  
}
### "logout_api/" - log out from an account

### "wallets/"
* view all user's wallets. Returns in a such form: {  
        "id": "16",  
        "name": "E3FCB82E",  
        "type": "VISA",  
        "currency": "RUB",  
        "balance": "145.00",  
        "created_on": "2023-05-09T14:26:05.756975Z",  
        "modified_on": "2023-05-09T14:53:38.385735Z"  
    }. 
    * id: id of a wallet
    * name: unique name of an each wallet. It is an 8 characters long name that is genereted randomly 
    * type: type of a wallet out of 2 options: VISA, MASTERCARD:
    * currency: cyrrency type of a wallet out of 3 options: USD, EUR, RUB
    * balance: balance of a wallet
    * created_on: time when a wallet was created
    * modified_on: time when the balance was updated
* create a wallet. API request: {  
        "type": "VISA",  
        "currency": "RUB",  
    }.  
    This request creates a wallet with balance depending on currency tyoe. If currency is USD or EUR the balance will be 3. If currency is RUB the balance will be 100. I is possible to have up to 5 wallets
* delete a wallet.

### "wallets/wallet_name/"
* view a wallet with wallet_name
* delete this wallet

### "wallets/transactions/"
* view all urser's transactions in a such form:{  
            "id": "31",  
            "sender": "7A758158",  
            "receiver": "E3FCB82E",  
            "transfer_amount": "25.00",  
            "commision": "0.00",  
            "status": "PAID",  
            "timestamp": "2023-05-09T14:42:53.685596Z". 
        }   
    * id: id of a transation.
    * sender: name of a sendler's wallet. Type of currency of reciever's wallet should be the same
    * receiver: name of a receiver's wallet.
    * transfer_amount: the amount of money that is transfered from one wallet to anouther. 
    * commision: comission is 0 if sender and reciever wallets belong to one user. Otherwise comision is 5%.
    * status: it can be PAID or FAILED depending on whether or not a transaction was completed successfull.
    * timestamp: time when transaction was made.

### "wallets/transactions/id/"
get a transaction by its id

### "wallets/transactions/wallet_name/" 
get all transactions of one wallet using wallet_name
