from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

def signup(request):
    if request.user.is_authenticated:
        return redirect("all_news")

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = False

        if User.objects.filter(username = username).exists():
            messages.error(request, "Username is already taken. Try with a new username")
            user_exists = True

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email is already taken. Try with a new email")
            user_exists = True

        if user_exists:
            return render(request, 'user/signup.html')
        
        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password= password
        )
        user.save()
        messages.success(request, "Account Created Successfully. Login to Continue")

    return render(request, 'user/signup.html')

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect("all_news")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return render(request, 'user/signin.html')
        else:
            login(request,user)
            return redirect("all_news")
        
    return render(request, 'user/signin.html')

def signout(request):
    logout(request)
    return render(request, 'user/signin.html')

@login_required(login_url="/user/signin")
def profile(request):
    return render(request, 'user/profile.html')