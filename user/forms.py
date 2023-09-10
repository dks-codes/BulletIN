from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder':'Confirm New Password'}))
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class EditUserProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
