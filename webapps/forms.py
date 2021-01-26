from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data  


class RegistrationForm(forms.Form):
    
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_username'}))
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(
        attrs={'id': 'id_password'}))
    password2 = forms.CharField(max_length=200, label='Confirm', widget=forms.PasswordInput(
        attrs={'id': 'id_confirm_password'}))
    email = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'id': 'id_email'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username