from django.contrib.admin.models import LogEntry
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from book.models import Rayon
from formulairmail.forms import Email_form
from formulairmail.models import Newsletter
from library_gn import settings
from reader.formReader import *


# Create your views here.
@login_required(login_url='login')
def readers(request):
    if request.user.has_perm('reader.view_reader'):
        add = request.user.has_perm('reader.add_reader')
        delete = request.user.has_perm('reader.delete_reader')
        change = request.user.has_perm('reader.change_reader')
        if request.user.is_superuser:
            context = Reader.objects.filter(status=1).filter(type_Reader=2)
        else:
            context = Reader.objects.filter(status=1).filter(readpoint_id=request.user.readpoint.pk ).filter(type_Reader=2)
        return render(request, 'reader/readers.html', {
            'context': context,
            'add': add,
            'delete': delete,
            'change': change
        })
    else:
        return redirect('home_site')


@login_required(login_url='login')
def add_reader(request):
    if request.user.has_perm('reader.add_reader'):
        if request.user.is_superuser:
            form_readpoint = ReadPoint.objects.filter(status=1)
        else:
            form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)

        if request.method == 'POST':
            readpoint_selected = int(request.POST['readpoint']) if request.POST['readpoint'] != '' else ''
            file = request.FILES.get('image_piece_reader')
            context = FormReader(request.POST, request.FILES)
            if file or not file:
                filename = file.name if file else None
                if filename:
                    if not filename.endswith('.pdf'):
                        messages.error(request, "Le type de la piece doit etre en pdf")
                        return render(request, 'reader/add_reader.html',
                                      {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                       'Form': context,
                                       'readpoint_selected': readpoint_selected
                                       })
                context = FormReader(request.POST, request.FILES)
                if context.is_valid():
                    reader = Reader.objects.filter(phone1_reader=context.cleaned_data['phone1_reader']).filter(
                        status=1)
                    reader2 = Reader.objects.filter(phone2_reader=context.cleaned_data['phone2_reader']).filter(
                        status=1)
                    noprobleme = True
                    email = Reader.objects.filter(email=context.cleaned_data['email']).filter(
                        status=1)
                    if readpoint_selected == '':
                        messages.error(request, "Le point de lecture est obligatoire")
                        noprobleme = False
                    if email:
                        messages.error(request, 'Cet email existe déjà')
                        noprobleme = False
                    if reader:
                        messages.error(request, 'Le telephone1 existe veillez lui changer')
                        noprobleme = False
                    if reader2:
                        messages.error(request, 'Le telephone2 existe veillez lui changer')
                        noprobleme = False
                    if not noprobleme:
                        return render(request, 'reader/add_reader.html',
                                      {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                       'Form': context,
                                       'readpoint_selected': readpoint_selected
                                       })
                    else:
                        reader = context.save(commit=False)
                        reader.type_Reader = 2
                        reader.readpoint_id = int(request.POST['readpoint'])
                        reader.created_by = request.user.id
                        if not reader.save():
                            if reader.type_Reader == 2:
                                ema = request.POST['email']
                                em = Newsletter(emails=ema)
                                em.save()
                                fre = Frequentation(lecteur=reader,readpoint=request.user.readpoint)
                                fre.save()
                            context = FormReader()
                            try:
                                if send_mail(
                                        subject='LVIA',
                                        message='hello word',
                                        from_email=settings.EMAIL_HOST_USER,
                                        recipient_list=[reader.email],
                                        html_message=f'<div class="envoie"><h1 class="h1">Confirmation de votre Email</h1>'
                                                     f'<p class="p">Votre Compte a été créé veuillez cliquer sur ce '
                                                     f'<a href="http://127.0.0.1:8000/readers/confirmation/{reader.pk}/{reader.email}/{reader.username}">'
                                                     f'lien</a> pour le confirmer!</p></div>'
                                        ,
                                        fail_silently=True
                                ):

                                    messages.success(request, "Lecteur ajouté avec succès")
                                    return render(request, 'reader/add_reader.html',
                                                  {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                                   'Form': context})
                                else:
                                    messages.success(request,
                                                     "Lecteur ajouté avec succès\nMessage de confirmation non envoyer veillez lui renvoyer ce "
                                                     "message de confirmation dans son affichage detailler")
                                    return render(request, 'reader/add_reader.html',
                                                  {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                                   'Form': context})

                            except:
                                messages.success(request, "Message de confirmation non envoyer veillez lui renvoyer ce "
                                                          "message de confirmation dans son affichage detaillé")
                                return render(request, 'reader/add_reader.html',
                                              {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                               'Form': context,
                                               'readpoint_selected': readpoint_selected})
                        else:
                            messages.error(request, "Echec d'ajout du lecteur")
                            return render(request, 'reader/add_reader.html',
                                          {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                                           'Form': context,
                                           'readpoint_selected': readpoint_selected})
                else:
                    messages.error(request, 'verifier bien le formulaire')
                    return render(request, 'reader/add_reader.html',
                                  {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint, 'Form': context,
                                   'readpoint_selected': readpoint_selected})
            else:
                messages.error(request, 'Il n\'ya pas de Fichiers')
                return render(request, 'reader/add_reader.html',
                              {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint,
                               'Form': context,
                               'readpoint_selected': readpoint_selected
                               })
        Form = FormReader()
        return render(request, 'reader/add_reader.html',
                      {'tooltip': 'Ajout d\'un Lecteur', 'form_readpoint': form_readpoint, 'Form': Form})
    else:
        return redirect('home_site')


@login_required(login_url='login')
def delete(request, id):
    if request.user.has_perm('reader.delete_reader'):
        try:
            read = Reader.objects.get(pk=id)
        except:
            pass
        read.status = 0
        read.save()
        messages.info(request, "Suppression effectuée avec succés")
        return redirect('readers')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def charged(request, id):
    form_readpoint = None
    if request.user.has_perm('reader.change_reader'):
        if request.user.is_superuser:
            form_readpoint = ReadPoint.objects.filter(status=1)
        else:
            try:
                form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)
            except:
                pass
        instance = get_object_or_404(Reader, id=id)
        readpoint_selected = None
        try:
            readpoint_selected = ReadPoint.objects.get(pk=instance.readpoint.pk)
            readpoint_selected = readpoint_selected.pk
        except:
            pass

        if request.method == 'POST':
            readpoint_selected = int(request.POST['readpoint']) if request.POST['readpoint'] != '' else ''
            context = FormReader(request.POST or None, request.FILES, instance=instance)
            noproblem = True
            if context.is_valid():
                reader = Reader.objects.filter(phone1_reader=context.cleaned_data['phone1_reader']).exclude(
                    pk=id).filter(status=1)
                reader2 = Reader.objects.filter(phone2_reader=context.cleaned_data['phone2_reader']).exclude(
                    pk=id).filter(status=1)
                reader3 = Reader.objects.filter(email=context.cleaned_data['email']).exclude(pk=id).filter(status=1)
                if reader:
                    messages.error(request, 'Le telephone1 existe veillez lui changer')
                    noproblem = False
                if reader3:
                    messages.error(request, 'Cette adresse email existe veillez lui changer')
                    noproblem = False
                if reader2:
                    messages.error(request, 'Le telephone2 existe veillez lui changer')
                    noproblem = False
                if not noproblem:
                    return render(request, 'reader/update_reader.html',
                                  {'Form': context, 'readpoint_selected': readpoint_selected,
                                   'form_readpoint': form_readpoint})
                reader = context.save(commit=False)
                try:
                    reader.readpoint_id = int(request.POST['readpoint'])
                except:
                    pass
                reader.created_by = request.user.id
                reader.save()
                messages.info(request, "Modification effectuée avec succés")
                return redirect('readers')
            else:
                messages.error(request, "Erreur de Modification verifier bien le formulaire")
                return render(request, 'reader/update_reader.html',
                              {'tooltip': "Modification d'un lecteur", 'Form': context,
                               'readpoint_selected': readpoint_selected, 'form_readpoint': form_readpoint})
        read = Reader.objects.get(pk=id)
        context = FormReader(instance=read)
        return render(request, 'reader/update_reader.html',
                      {'Form': context, 'readpoint_selected': readpoint_selected, 'form_readpoint': form_readpoint})
    else:
       return redirect('home_site')


@login_required(login_url='login')
def details(request, id):
    if request.user.has_perm('reader.view_reader'):
        read = Reader.objects.exclude(status=0).filter(pk=id).filter(type_Reader=2)
        if read:
            return render(request, 'reader/details.html', {'context': read})
        else:
            messages.error(request, "Cet utilisateur n'existe pas")
            context = Reader.objects.exclude(status=0)
            return render(request, 'reader/readers.html', {'context': context})
    else:
        return redirect('home_site')


@login_required(login_url='login')
def details_user(request, id):
    if request.user.is_superuser:
        read = Reader.objects.exclude(status=0).filter(pk=id).filter(type_Reader=1)
        if read:
            return render(request, 'reader/detaille_user.html', {'context': read})
        else:
            messages.error(request, "Cet utilisateur n'existe pas")
            context = Reader.objects.exclude(status=0)
            return render(request, 'reader/users.html', {'context': context})
    else:
        return redirect('home_site')


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
                login(request, user)
                if user.type_Reader == '1':
                    return redirect('dashboard')
                elif user.type_Reader == '2':
                    return redirect('home_site')
            else:
                messages.error(request, "les identifiants fournis sont incorrects oubien compte non confirmer")
                return render(request, "reader/login.html", {'form': form})
        else:
            messages.error(request, "verifiez les champs")
            return render(request, "reader/login.html", {'form': form})

    return render(request, "reader/login.html", {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


# ok
def confirm_changePassword(request):
    if request.method == 'POST':
        if request.POST['username'] != '':
            try:
                reader = Reader.objects.get(username=request.POST['username'])
            except:
                messages.error(request, 'Cet utilisateur n\'existe pas')
                return redirect('confirm_changePassword')
            if reader:
                try:
                    if send_mail(
                            subject='LVIA',
                            message='hello word',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[reader.email],
                            html_message=f'div class="envoie"><h1 class="h1">Confirmation de votre Email</h1>'
                                         f'<p class="p">Votre Compte a été créé veuillez cliquer sur ce '
                                         f'<a href="http://127.0.0.1:8000/readers/confirmation/{reader.pk}/{reader.email}/{reader.username}"> '
                                         f'lien</a> pour le confirmer!</p></div>'
                            ,
                            fail_silently=True):
                        messages.success(request, f"Un message de confirmation à été envoyer à {reader.email} ")
                except:
                    messages.error(request, f'impossible d\'envoyer l\'email de confirmation\nVeuillez réessayer')

    return render(request, 'reader/get_username.html', {'form': ConfirmationPassword()})


# @login_required(login_url='login')
def change_password(request, id, email, username):
    reader = Reader.objects.filter(pk=id).filter(status=1).filter(email=email).filter(username=username)
    if request.method == 'POST':
        form = ConfirmationPassword(request.POST, instance=reader[0])
        if form.is_valid():
            user = form.save(commit=False)
            user.password_changed = True
            user.save()
            messages.success(request, "Le mot de passe changé avec succès")
            return redirect('login')
        else:
            messages.error(request, 'Erreur de modification de mot de passe  veillez ressayer')
        return render(request, 'reader/confirme_password.html', {'form': form})
    if reader:
        if not reader[0]:
            return redirect('login')
        else:
            form = ConfirmationPassword(instance=reader[0])
            return render(request, 'reader/confirme_password.html', {'form': form})
    else:
        return redirect('login')


def get_user(request):
    if request.method == 'POST':
        if request.POST['username'] == '':
            return render(request, 'reader/get_username.html', {'form': get_username_form()})
        try:
            reader = Reader.objects.get(username=request.POST['username'])
        except:
            messages.error(request, "Cet utilisateur n'existe pas")
            return render(request, 'reader/get_username.html', {'form': get_username_form()})
        if not reader:
            messages.error(request, "Cet utilisateur n'existe pas")
            return render(request, 'reader/get_username.html', {'form': get_username_form()})
        try:
            if send_mail(
                    subject='LVIA',
                    message='hello word',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[reader.email],
                    html_message=f'div class="envoie"><h1 class="h1">Confirmation de votre Email</h1>'
                                 f'<p class="p">Votre Compte a été créé veuillez cliquer sur ce '
                                 f'<a href="http://127.0.0.1:8000/readers/change/{reader.pk}/{reader.email}/{reader.username}">'
                                 f'lien</a> pour le confirmer!</p></div>'
                    ,
                    fail_silently=True):
                messages.success(request, "message envoyé  avec succès")

        except:
            messages.error(request, f'impossible d\'envoyer l\'email de confirmation\nVeuillez réessayer')
    return render(request, 'reader/get_username.html', {'form': get_username_form()})


def confirm_password(request):
    pass


@login_required(login_url='login')
def add_user(request):
    if request.user.is_superuser:
        if request.user.is_superuser:
            form_readpoint = ReadPoint.objects.filter(status=1)
        else:
            form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)

        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST)
            readpoint_selected = int(request.POST['readpoint']) if request.POST['readpoint'] != '' else ''
            if form.is_valid():
                noproblem = True
                reader = Reader.objects.filter(phone1_reader=form.cleaned_data['phone1_reader']).filter(status=1)
                reader2 = Reader.objects.filter(phone2_reader=form.cleaned_data['phone2_reader']).filter(status=1)
                reader3 = Reader.objects.filter(email=form.cleaned_data['email']).filter(status=1)
                if readpoint_selected == '':
                    messages.error(request, "Veiullez selectionner un point de lecture")
                    noproblem = False
                if reader:
                    messages.error(request, 'Le telephone1 existe veillez lui changer')
                    noproblem = False
                if reader3:
                    messages.error(request, 'Cette adresse email existe veillez lui changer')
                    noproblem = False
                if reader2:
                    messages.error(request, 'Le telephone2 existe veillez lui changer')
                    noproblem = False
                if not noproblem:
                    return render(request, 'reader/addUser.html',
                                  {'Form': form, 'readpoint_selected': readpoint_selected,
                                   'form_readpoint': form_readpoint})
                user = form.save(commit=False)
                user.type_Reader = 1
                user.created_by = request.user.id
                user.save()
                fre = Frequentation(lecteur=user, readpoint=request.user.readpoint)
                fre.save()
                try:
                    if send_mail(
                            subject='LVIA',
                            message='hello word',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[user.email],
                            html_message=f'div class="envoie"><h1 class="h1">Confirmation de votre Email</h1>'
                                         f'<p class="p">Votre Compte a été créé veuillez cliquer sur ce '
                                         f'<a href="http://127.0.0.1:8000/readers/confirmation/{user.pk}/{user.email}/{user.username}">'
                                         f'lien</a> pour le confirmer!</p></div>'
                            ,
                            fail_silently=True):
                        messages.success(request, "Utilisateur ajouté avec succès")
                        return redirect('add-user')
                    else:
                        messages.success(request,
                                         "Utilisateur ajouté avec succès Mais le Message de confirmation non envoyer veillez lui renvoyer ce "
                                         "message de confirmation dans son affichage detailler")
                        return render(request, 'reader/addUser.html',
                                      {'tooltip': "Ajout d'un utilisateur d'un lecteur", 'Form': FormReader(),
                                       'form_readpoint': form_readpoint})
                except:
                    messages.success(request, "Message de confirmation non envoyer veillez lui renvoyer ce "
                                              "message de confirmation dans son affichage detailler")
            else:
                messages.error(request, "Erreur d'ajout verifier bien le formulaire")
                return render(request, 'reader/addUser.html',
                              {'tooltip': "Ajout d'un utilisateur d'un lecteur", 'Form': form,
                               'readpoint_selected': readpoint_selected, 'form_readpoint': form_readpoint})

        return render(request, 'reader/addUser.html',
                      {'Form': form, 'form_readpoint': form_readpoint, 'tooltip': 'Ajout d\'un Utilisateur'})
    else:
        return redirect('home_site')

def checkUser(request, id, email, username):
    reader = Reader.objects.filter(pk=id).filter(status=1).filter(password_changed=False).filter(email=email).filter(
        username=username)
    if request.method == 'POST':
        form = ConfirmationPassword(request.POST, instance=reader[0])
        if form.is_valid():
            user = form.save(commit=False)
            user.password_changed = True
            user.save()
            messages.success(request, "Le mot de passe changé avec succès")
            return redirect('login')
        else:
            messages.error(request, 'Erreur de confirmation de mot de passe  veillez ressayer')
        return render(request, 'reader/change_password.html', {'form': form})
    if reader:
        if not reader[0]:
            return redirect('login')
        else:
            form = ConfirmationPassword(instance=reader[0])
            return render(request, 'reader/change_password.html', {'form': form})
    else:
        return redirect('login')


@login_required(login_url='login')
def users(request):
    if request.user.is_superuser:
        add = request.user.has_perm('reader.add_reader')
        delete = request.user.has_perm('reader.delete_reader')
        change = request.user.has_perm('reader.change_reader')
        context = Reader.objects.filter(status=1).filter(type_Reader=1)
        return render(request, 'reader/users.html', {
            'context': context,
            'add': add,
            'delete': delete,
            'change': change
        })
    else:
        return redirect('home_site')


# envoi un mail de confirmation a un utilisateru
def send_confirmation_mail(request, username, pk, email):
    try:
        if send_mail(
                subject='LVIA',
                message='hello word',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=f'div class="envoie"><h1 class="h1">Confirmation de votre Email</h1>'
                             f'<p class="p">Votre Compte a été créé veuillez cliquer sur ce '
                             f'<a href="http://127.0.0.1:8000/readers/confirmation/{pk}/{email}/{username}">'
                             f'lien</a> pour le confirmer!</p></div>'
                ,
                fail_silently=True):
            messages.success(request, "message envoyé  avec succès")
        else:
            messages.error(request, f'impossible d\'envoyer l\'email de confirmation\nVeuillez réessayer')
    except:
        messages.error(request, f'impossible d\'envoyer l\'email de confirmation\nVeuillez réessayer')
    return redirect(f'/readers/details/{pk}')
    # envoie mail avec login et mot de passe et lien de connexion
    #


def envoimail(request):
    if request.method == 'POST':
        form = Email_form(request.POST)
        emailDestinateur = request.POST['email_exp']
        emailDestinateur = emailDestinateur.split(",")
        message = request.POST['message']
        objet = request.POST['object']
        if form.is_valid():
            try:
                if send_mail(subject=objet, message=message, from_email=settings.EMAIL_HOST_USER,
                             recipient_list=[emailDestinateur],
                             fail_silently=False, html_message=message):
                    form.save()
                    messages.success(request, "Evoi effectué avec succès")
                    return redirect(f"readers/details/{request.POST['pk']}")
                else:
                    messages.error(request, "Erreur d'envoi")
                    return redirect(f"readers/details/{request.POST['pk']}")
            except:
                messages.error(request, f'impossible d\'envoyer veuillez ressayer.')
                return redirect(f"readers/details/{request.POST['pk']}")

        else:
            messages.error(request, "Erreur d'envoi")
    return redirect(f"readers/")


def emails(request):
    em = Newsletter.objects.all().exclude(status=0)
    context = {
        'email': em,
        'tooltip': 'Liste des Emails des Newsletters'
    }
    return render(request, 'reader/email.html', context)


def delete_email(request, id):
    if request.user.has_perm('formulairmail'):
        em = Newsletter.objects.get(pk=id)
        em.status = 0
        if em.save():
            messages.success(request, 'Suppression éffectuée avec succès')
        return redirect('email')
    else:
        return redirect('home_site')


# Update User


# @login_required(login_url='login')
def edit_user(request, id):
    if request.user.has_perm('reader.change_reader'):
        form_readpoint = None
        if request.user.is_superuser:
            form_readpoint = ReadPoint.objects.filter(status=1)
        else:
            try:
                form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)
            except:
                pass
        instance = get_object_or_404(Reader, id=id)
        readpoint_selected = None
        try:
            readpoint_selected = ReadPoint.objects.get(pk=instance.readpoint.pk)
            readpoint_selected = readpoint_selected.pk
        except:
            pass

        if request.method == 'POST':
            readpoint_selected = int(request.POST['readpoint']) if request.POST['readpoint'] != '' else ''
            context = RegisterForm(request.POST or None, request.FILES, instance=instance)
            noproblem = True
            if context.is_valid():
                reader = Reader.objects.filter(phone1_reader=context.cleaned_data['phone1_reader']).exclude(
                    pk=id).filter(status=1)
                reader2 = Reader.objects.filter(phone2_reader=context.cleaned_data['phone2_reader']).exclude(
                    pk=id).filter(status=1)
                reader3 = Reader.objects.filter(email=context.cleaned_data['email']).exclude(pk=id).filter(status=1)
                if reader:
                    messages.error(request, 'Le telephone1 existe veillez lui changer')
                    noproblem = False
                if reader3:
                    messages.error(request, 'Cette adresse email existe veillez lui changer')
                    noproblem = False
                if reader2:
                    messages.error(request, 'Le telephone2 existe veillez lui changer')
                    noproblem = False
                if request.POST['readpoint'] == '':
                    messages.error(request, 'Veiullez selectionnez un point de lecture')
                    noproblem = False
                if not noproblem:
                    return render(request, 'reader/edit_user.html',
                                  {'Form': context, 'readpoint_selected': readpoint_selected,
                                   'form_readpoint': form_readpoint})
                reader = context.save(commit=False)
                reader.readpoint_id = int(request.POST['readpoint'])
                reader.created_by = request.user.id
                reader.save()
                messages.info(request, "Modification effectuée avec succés")
                return redirect('users')
            else:
                messages.error(request, "Erreur de Modification verifier bien le formulaire")
                return render(request, 'reader/edit_user.html',
                              {'tooltip': "Modification d'un lecteur", 'Form': context,
                               'readpoint_selected': readpoint_selected, 'form_readpoint': form_readpoint})
        read = Reader.objects.get(pk=id)
        context = RegisterForm(instance=read)
        return render(request, 'reader/edit_user.html',
                      {'Form': context, 'readpoint_selected': readpoint_selected, 'form_readpoint': form_readpoint})
    else:
       return redirect('home_site')


def profile(request):
    print("user connected", request.user.last_name)
    user_log = LogEntry.objects.filter(user=request.user.id)
    return render(request, 'reader/profile.html', context={'user': request.user,
                                                           'user_log': user_log})


# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        lecteur = Reader.objects.filter(status=1).filter(type_Reader='2')
        # changer le chemin du temble
        pdf = html_to_pdf('reader/printReader.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "reader": lecteur,
            # le tooltip
            "title":'Liste Des Lecteurs'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
    #PPRES TOUS ON CREE L'UREL POUR CETTE VIEW
# Creating a class based view
class GenerateUserPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        user = Reader.objects.filter(status=1).filter(type_Reader=1)
        # changer le chemin du temble
        pdf = html_to_pdf('reader/printUser.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "users": user,
            # le tooltip
            "title":'Liste Des utilisateurs'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
    #PPRES TOUS ON CREE L'UREL POUR CETTE VIEW