from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Code
from django.utils import timezone
from .service import send_email_in_thread
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('users:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('users:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect('users:register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        messages.success(request, "Registration successful")
        return redirect('users:home')

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('users:home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('users:login')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('users:login')


@login_required
def home_view(request):
    #home view
    return redirect('noter:home')


def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            send_email_in_thread(email)
            messages.success(request, "Reset code sent to your email")
            return redirect('users:restore', user.email)
        else:
            messages.error(request, "Email not found")
            return redirect('users:forgot')

    return render(request, 'users/forgot.html')


def restore_view(request, email):
    if request.method == 'POST':
        code_value = request.POST.get('code')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('users:restore', email)

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "User not found")
            return redirect('users:forgot')

        code = Code.objects.filter(code=code_value, user=user).first()

        if not code:
            messages.error(request, "Invalid code")
            return redirect('users:restore', email)

        if code.is_expired():
            messages.error(request, "Code has expired")
            return redirect('users:forgot')

        user.set_password(password)
        user.save()
        messages.success(request, "Password changed successfully. Please log in.")
        return redirect('users:login')

    return render(request, 'users/restore.html')


def hello(request):
    pass