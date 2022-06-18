from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib import messages


# Create your views here.


def login_user(request):

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # test si son mot de passe n'est pas changé
                # redirection vers un formulaire de changement de mot de passe qui
                # doit ressembler au formulaire d'authentification
                # si le mot de passe est changé
                # redirection vers le dashboard

                print("Authentification effectuée avec succès")
                login(request, user)
                print(request)
                return redirect('dashboard')
            else:
                messages.error(request, "les identifiants fournis sont incorrects")
                return render(request, "accounts/login.html", {'form': form})
        else:
            messages.error(request, "verifiez les champs")
            return render(request, "accounts/login.html", {'form': form})

    return render(request, "accounts/login.html", {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def add_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # envoie mail avec login et mot de passe et lien de connexion
            # redirection vers la liste des utilisateurs

    return render(request, 'accounts/addUser.html', {'form': form})
