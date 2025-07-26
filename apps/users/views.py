import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Code, UserProfile
from .service import send_registration_code_async, send_change_email_code_async
from django.contrib import messages
from .forms import UserForm, UserProfileForm, CountryForm
from django.contrib.auth.hashers import check_password
from core.settings import base
from django.http import HttpResponse

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
    user = request.user
    return render(request, 'home.html')

@login_required
def account_view(request):
    user = request.user
    user_profile = user.profile
    return render(request, 'account.html', {'user': user, 'user_profile': user_profile})

@login_required
def settings_view(request):
    user = request.user
    return render(request, 'settings.html', {'user': user})

@login_required
def change_email(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if User.objects.filter(email = email).exists():
            messages.error(request, "Invalid credentials")
            return redirect('users:change_email')
        send_change_email_code_async(email, request.user)
        return redirect('users:verify_change_email',  email)
    return render(request, 'settings/change-email.html', {'user': user})

@login_required
def verify_change_email(request, email):
    user = request.user

    if request.method == 'POST':
        code_value = request.POST.get('code')

        code = Code.objects.filter(code=code_value, user=user).first()

        if not code:
            messages.error(request, "Invalid code")
            return redirect('users:change_email')

        if code.is_expired():
            messages.error(request, "Code has expired")
            return redirect('users:change_email')

        if code.user != user:
            messages.error(request, "Invalid code")
            return redirect('users:change_email')

        user = request.user
        user.email = email
        user.save()
        messages.success(request, "Email change successful")
        return redirect('users:change_email')
    return render(request, 'settings/verify-change-email.html')



@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "Confirm passwords are not same!")
            return redirect('users:change_password')
        password = request.POST.get('password')
        if not check_password(password, user.password):
            messages.error(request, "Current password is incorrect")
            return redirect('users:change_password')

        user.set_password(new_password)
        user.save()
        messages.success(request, "Password changed successfully")
        return redirect('users:login')
    return render(request, 'settings/change-password.html', {'user': user})

@login_required
def read_profile(request):
    user = request.user
    user_profile = user.profile
    return render(request, 'settings/read_profile.html', {'user': user, 'user_profile': user_profile})




@login_required
def country(request):
    user = request.user
    user_profile = user.profile
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('users:read_country')
    else:
        form = CountryForm(instance=user_profile)
    return render(request, 'settings/country.html', {'user_profile': user_profile, 'form': form})

@login_required
def read_country(request):
    user = request.user
    user_profile = user.profile
    return render(request, 'settings/read_country.html', {'user_profile': user_profile})






@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.profile  # adjust this if you're using OneToOneField differently

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:read_profile')  # or wherever you want to redirect
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'settings/edit-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def upload_photo(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user = user).first()
    if request.method == "POST" and request.FILES.get("image"):
        user_profile.photo = request.FILES["image"]
        user_profile.save()
        return redirect('users:upload_photo')
    return render(request, 'settings/upload-photo.html', {'user_profile': user_profile ,'user_profile_photo': user_profile.photo})

@login_required
def delete_photo(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user = user).first()
    user_profile.photo.delete()
    return redirect('users:upload_photo')


def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            send_registration_code_async(email)
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














def google_loging(request):
    auth_url = (
        f"{base.GOOGLE_AUTH_URL}"
        f"?client_id={base.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={base.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return redirect(auth_url)


# def google_callback(request):
#     code = request.GET.get('code')
#     token_data = {
#         "code": code,
#         "client_id": base.GOOGLE_CLIENT_ID,
#         "client_secret": base.GOOGLE_CLIENT_SECRET,
#         "redirect_uri": base.GOOGLE_REDIRECT_URI,
#         "grant_type": "authorization_code",
#     }
#     token_response = requests.post(base.GOOGLE_TOKEN_URL, data=token_data)
#     token_json = token_response.json()
#     access_token = token_json.get("access_token")
#     user_info_response = requests.get(base.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})
#     user_info = user_info_response.json()
#
#     email = user_info.get('email')
#     google_id = user_info.get('id')
#
#     try:
#         user = User.objects.get(email=email)
#         if not user.google_id:
#             user.google_id = google_id
#             user.save()
#     except User.DoesNotExist:
#         user = User.objects.create(
#             email = email,
#             google_id = google_id,
#             first_name=user_info.get('given_name'),
#             last_name=user_info.get('family_name'),
#         )
#         user_profile = UserProfile.objects.create(
#             user = user
#         )
#     login(request, user)
#     return redirect('users:home')




def google_callback(request):
    code = request.GET.get('code')

    token_data = {
        "code": code,
        "client_id": base.GOOGLE_CLIENT_ID,
        "client_secret": base.GOOGLE_CLIENT_SECRET,
        "redirect_uri": base.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(base.GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    user_info_response = requests.get(
        base.GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    email = user_info.get('email')
    google_id = user_info.get('id')

    try:
        user = User.objects.get(google_id=google_id)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=email)
            if user.google_id is None:
                user.google_id = google_id
                user.save()
            elif user.google_id != google_id:
                # Security case: someone is trying to log in with different google ID
                return HttpResponse("Authentication error: conflicting Google ID.", status=403)
        except User.DoesNotExist:
            user = User.objects.create(
                email=email,
                google_id=google_id,
                first_name=user_info.get('given_name'),
                last_name=user_info.get('family_name'),
            )
            # UserProfile.objects.create(user=user)

    login(request, user)
    return redirect('users:home')
