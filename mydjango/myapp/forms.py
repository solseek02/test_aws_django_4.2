from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'}),
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}),
        }