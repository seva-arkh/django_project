## django_project
prototype of a bank app using django REST framework. It has such fuctions
URLS:
# "register_api/"
Creates an account. API request: {
    "username": "",
    "email": "",
    "password": ""
}
# "login_api/" - log in to an account
# "logout_api/" - log out from an account
# "wallets/" - view all wallets; create a wallet
# "wallets/wallet_name/"  - view one wallet_name
# "wallets/transactions/" - view all transactions
# "wallets/transactions/id/" - get a transactionby its id
# "wallets/transactions/wallet_name/" - get all transactions of one wallet using wallet_name
