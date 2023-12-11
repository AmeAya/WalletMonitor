from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
import requests


def homeView(request):
    return render(request, 'home.html')


def signInView(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('home_url')
        else:
            return redirect('sign_in_url')


def signOutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_url')


def signUpView(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if AccountHolder.objects.filter(email=email):
            return render(request, 'sign_up.html', {'msg': 'Email is not valid'})
        else:
            user = AccountHolder(email=email)
            user.set_password(password)
            user.save()
            return redirect('sign_in_url')


def profileView(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('sign_in_url')


def changeProfileView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'change_profile.html')
        elif request.method == 'POST':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            if request.user.name != name:
                request.user.name = name
            if request.user.surname != surname:
                request.user.surname = surname
            request.user.save()
            return redirect('profile_url')
    else:
        return redirect('sign_in_url')


def addFundsView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            currencies = [elem[0] for elem in CURRENCY_CHOICES]
            return render(request, 'add_funds.html', {'currencies': currencies})
        elif request.method == 'POST':
            funds = int(request.POST.get('funds'))
            currency = request.POST.get('currency')
            if request.user.currency == currency:
                request.user.wallet += funds
            else:
                url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/'
                url += str(currency).lower() + '.json'
                response = requests.get(url)
                data = response.json()[str(currency).lower()]
                request.user.wallet += funds * data[str(request.user.currency).lower()]
            request.user.save()
            return redirect('profile_url')
    else:
        return redirect('sign_in_url')
