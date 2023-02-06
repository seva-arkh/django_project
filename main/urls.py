from django.urls import path

from . import views

urlpatterns = [
# path("<int:id>", views.index, name="index"),
# path("home/", views.home, name="home"),
# path("", views.home, name="home"),
path("wallets/transactions/", views.all_transactions, name="all transactions / transaction"),
path("wallets/transactions/<int:id>/", views.transaction, name="transaction"),
path("wallets/transactions/<str:name>/", views.wallet_transactions, name="wallet transactions"),
path("wallets/", views.all_wallets, name="all wallets"),
path("wallets/<str:name>/", views.wallet, name="wallet"),
#path('register_1/', RegisterAPI.as_view(), name='register'),
# path("create/", views.create, name="create"),
# path("view/", views.view, name="view"),
# path("transfer/", views.transfer, name="transfer"),
# path("internal/", views.transfer_internal, name="internal"),
# path("external/", views.transfer_external, name="external"),
]
