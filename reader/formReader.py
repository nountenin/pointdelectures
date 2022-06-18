from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class FormReader(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormReader, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Reader
        fields = [
            'first_name',
            'last_name',
            'nationality_reader',
            'phone1_reader',
            'phone2_reader',
            'email',
            'image_reader',
            'gender_reader',
            'address_reader',
            'type_piece_reader',
            'number_piece_reader',
            'image_piece_reader',
            'username',
        ]


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Reader
        fields = [
            'first_name',
            'last_name',
            'phone1_reader',
            'phone2_reader',
            'email',
            'image_reader',
            'gender_reader',
            'address_reader',
            'type_piece_reader',
            'number_piece_reader',
            'image_piece_reader',
            'username',
            'is_superuser',
            'user_permissions',
            'groups'
        ]
        readpoint = forms.ModelChoiceField(queryset=ReadPoint.objects.filter(status=1),
                                           empty_label="Sélectionnez un point de lecture")


class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=18,
                               widget=forms.TextInput(attrs={'placeholder': "Entez votre nom d'utilisateur"}))
    password = forms.CharField(label="", max_length=18,
                               widget=forms.PasswordInput(attrs={'placeholder': "Entez votre mot de passe"}))


class get_username_form(UserCreationForm):
    username = forms.CharField(label="", max_length=255)


class ConfirmationPassword(UserCreationForm):
    username = forms.CharField(label="", max_length=250,
                               widget=forms.TextInput(attrs={'placeholder': "Entez votre nom d'utilisateur"}))
