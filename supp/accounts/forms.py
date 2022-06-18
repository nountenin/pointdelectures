from django import forms
from django.contrib.auth.forms import UserCreationForm

from book.models import ReadPoint
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=18,
                               widget=forms.TextInput(attrs={'placeholder': "Entez votre nom d'utilisateur"}))
    password = forms.CharField(label="", max_length=18,
                               widget=forms.PasswordInput(attrs={'placeholder': "Entez votre mot de passe"}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'phonenumber', 'adresse', 'groups', 'readpoint']
        readpoint = forms.ModelChoiceField(queryset=ReadPoint.objects.filter(status=1),
                                           empty_label="Sélectionnez un point de lecture")
