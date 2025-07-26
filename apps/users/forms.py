from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django_countries.widgets import CountrySelectWidget

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname...'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username...'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address...'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CountryForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country']
        widgets = {
            # 'country': CountrySelectWidget(  # still using the widget, but clean
            #     attrs={'class': 'form-select'}  # Bootstrap styling
            # )
            CountrySelectWidget(layout="{name}", attrs={'class': 'form-select'})
        }

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email...'})
        }
