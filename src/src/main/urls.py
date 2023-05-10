from django.urls import path
from register_login_logout.api.views import RegisterAPI
from main.api import views as api_views
from main import views

urlpatterns = [
    # api
    path(
        "wallets/transactions/",
        api_views.all_transactions,
        name="all transactions / transaction",
    ),
    path("wallets/transactions/<int:id>/",
         api_views.transaction,
         name="transaction"),
    path(
        "wallets/transactions/<str:name>/",
        api_views.wallet_transactions,
        name="wallet transactions",
    ),
    path("wallets/", api_views.all_wallets, name="all wallets"),
    path("wallets/<str:name>/", api_views.wallet, name="wallet"),
    # django views
    path("register_1/", RegisterAPI.as_view(), name="register"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view"),
    path("transfer/", views.transfer, name="transfer"),
    path("internal/", views.transfer_internal, name="internal"),
    path("external/", views.transfer_external, name="external"),
    path("<int:id>", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
]
