from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *


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
