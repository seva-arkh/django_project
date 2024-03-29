from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
from register_login_logout.forms import RegisterForm


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {'form': form})
