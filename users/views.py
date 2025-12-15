from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render

User = get_user_model()

def SignUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/singup.html')

def Logout_user(request):
    logout(request)
    return redirect('home')

def Login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')