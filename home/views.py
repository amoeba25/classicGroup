# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def loginReq(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            print("Username Does Not Exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login in successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Username and Password is Incorrect")
            print("User and Password is incorrect")
    return render(request, 'home/home.html')


@login_required(login_url="homepage")
def logoutReq(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("homepage")


@login_required(login_url="homepage")
def notAuthorized(request):
    return render(request, "404.html")
