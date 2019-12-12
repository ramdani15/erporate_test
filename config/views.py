from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import render, redirect

from core.models import Role


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['password'] = password
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Login Failed")
    else:
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    if request.user.role == Role.PELAYAN:
        return render(request, 'pelayan/home.html')
    elif request.user.role == Role.KASIR:
        return render(request, 'kasir/home.html')
    else:
        return render(request, 'manager/home.html')
    return redirect('/')


@login_required
def detail(request, id):
    if request.user.role == Role.PELAYAN:
        return render(request, 'pelayan/detail.html', {'pesanan_id': id})
    return render(request, 'kasir/detail.html', {'pesanan_id': id})
