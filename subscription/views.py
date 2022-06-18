from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from reader.models import Reader
from subscription.forms import SubscriptionForm
from subscription.models import Subscription


# Create your views here.
@login_required(login_url='login')
def subscriptions(request):
    add = request.user.has_perm('subscription.add_subscription')
    delete = request.user.has_perm('subscription.delete_subscription')
    change = request.user.has_perm('subscription.change_subscription')
    voir = request.user.has_perm('subscription.view_subscription')
    customlist = []
    if request.user.is_superuser:
        reader = Reader.objects.filter(status=1).filter(type_Reader=2)
    else:
        reader = Reader.objects.filter(readpoint=request.user.readpoint.pk).filter(type_Reader=2)

    listes = Subscription.objects.filter(status=1).filter(reader__type_Reader=2)
    nb = 1
    for li in listes:
        dif = (li.end_subscription - li.start_subscription)
        ob = {
            'id': nb,
            'pk': li.pk,
            'reader': li.reader,
            'start_subscription': li.start_subscription,
            'end_subscription': li.end_subscription,
            'dif': li.end_subscription > li.start_subscription,
            'nb_jour': ((li.end_subscription - li.start_subscription) - (date.today() - li.start_subscription)).days
        }
        nb += 1
        customlist.append(ob)
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        reader_selected = int(request.POST['reader']) if request.POST['reader'] != '' else ''
        if add:
            # form['reader'].value(reader_selected)
            if form.is_valid():
                noproblem = True
                if form.cleaned_data['end_subscription'] <= date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date fin d'inscription doit être supérieur a la date "
                                   "d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False

                if form.cleaned_data['start_subscription'] > date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur ou egale a la "
                                   "date d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if form.cleaned_data['start_subscription'] > form.cleaned_data['end_subscription']:
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur a la date fin "
                                   "d'abonnement veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if not noproblem:
                    return render(request, 'subscription/subscriptions.html',
                                  {'form': form, 'listes': customlist, 'reader_selected': reader_selected,
                                   'reader': reader,
                                   'listes': customlist,
                                   'add': add,
                                   'delete': delete,
                                   'change': change,
                                   'voir': voir,
                                   'reader': reader

                                   })
                else:
                    sub = form.save(commit=False)
                    sub.created_by = request.user.id
                    sub.reader_id = int (request.POST['reader'])
                    sub.save()
                    messages.success(request, "Abonnement effectué avec succés")
                    return HttpResponseRedirect(reverse('subscriptions'))
            else:
                messages.error(request, "Erreur d'ajout veillez vérifier bien votre formulaire")
                return render(request, 'subscription/subscriptions.html',
                              {'form': form, 'listes': customlist, 'reader_selected': reader_selected,
                               'reader': reader,
                               'listes': customlist,
                               'add': add,
                               'delete': delete,
                               'change': change,
                               'voir': voir,
                               'reader': reader

                               })
        else:
            return render(request, 'permission.html')

    if add or voir:
        form = SubscriptionForm()
        return render(request, 'subscription/subscriptions.html', {
            'form': form,
            'listes': customlist,
            'add': add,
            'delete': delete,
            'change': change,
            'voir': voir,
            'reader': reader
        })
    else:
        return redirect('home_site')


@login_required(login_url='login')
def delete(request, id):
    if request.user.has_perm('subscription.delete_subscription'):
        liste = Subscription.objects.get(pk=id)
        liste.status = 0
        liste.save()
        messages.info(request, "Suppression effectuée avec succés")
        return HttpResponseRedirect(reverse('subscriptions'))
    else:
        return redirect('home_site')


@login_required(login_url='login')
def modifier(request, id):
    if request.user.has_perm('subscription.change_subscription'):
        abon = Subscription.objects.get(pk=id)
        if request.user.is_superuser:
            reader = Reader.objects.filter(status=1).filter(type_Reader=2)
        else:
            reader = Reader.objects.filter(readpoint_id=request.user.readpoint.pk).filter(type_Reader=2)
        reader_selected = Reader.objects.get(pk=abon.reader_id)
        reader_selected = reader_selected.pk
        if request.method == "POST":
            reader_selected = int(request.POST['reader']) if request.POST['reader'] != '' else ''
            form = SubscriptionForm(request.POST, instance=abon)
            noproblem = True
            if form.is_valid():
                if form.cleaned_data['end_subscription'] <= date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date fin d'inscription doit être supérieur a la date "
                                   "d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if form.cleaned_data['start_subscription'] > date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur ou egale a la "
                                   "date d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if form.cleaned_data['start_subscription'] > form.cleaned_data['end_subscription']:
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur a la date fin d'abonnement veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if request.POST['reader'] == '':
                    messages.error(request,"Veuillez selectionnez un lecteur")
                    noproblem = False
                if not noproblem:
                    return render(request, 'subscription/edit_subscription.html',
                                  {'form': form, 'reader_selected': reader_selected, 'reader': reader,
                                   'tooltip': "Modification"})
                else:
                    subscription = form.save(commit=False)
                    subscription.created_by = request.user.id
                    subscription.reader_id = int(request.POST['reader'])
                    print(subscription.reader)
                    if not subscription.save():
                        messages.info(request, "Modification effectué avec succés")
                    return HttpResponseRedirect(reverse('subscriptions'))
            else:
                return render(request, 'subscription/edit_subscription.html',
                              {'form': form, 'reader_selected': reader_selected, 'reader': reader,
                               'tooltip': "Modification"})
        else:
            abonform = SubscriptionForm(instance=abon)
            return render(request, 'subscription/edit_subscription.html',
                          {'form': abonform, 'reader_selected': reader_selected, 'reader': reader,
                           'tooltip': "Modification"})
    else:
        return redirect('home_site')


@login_required(login_url='login')
def resubscriptions(request, id):
    if request.user.has_perm('subscription.add_subscription'):
        abon = Subscription.objects.get(pk=id)
        if request.user.is_superuser:
            reader = Reader.objects.filter(status=1).filter(type_Reader=2)
        else:
            reader = Reader.objects.filter(readpoint_id=request.user.readpoint.pk).filter(type_Reader=2)
        lecteur = Reader.objects.get(pk=abon.reader_id)
        if request.method == "POST":
            lecteur = int(request.POST['reader']) if request.POST['reader'] != '' else ''
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                noproblem = True
                if request.POST['reader'] == '':
                    messages.error(request,
                                   "viuellez selectionnez un lecteur.",
                                   fail_silently=True
                                   )
                    noproblem = False


                if form.cleaned_data['end_subscription'] <= date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date fin d'inscription doit être supérieur a la date "
                                   "d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if form.cleaned_data['start_subscription'] > date.today():
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur ou egale a la "
                                   "date d'aujourd'hui veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if form.cleaned_data['start_subscription'] > form.cleaned_data['end_subscription']:
                    messages.error(request,
                                   "Erreur d'abonnement la date debut d'inscription doit être inferieur a la date fin d'abonnement veillez ressayer.",
                                   fail_silently=True
                                   )
                    noproblem = False
                if not noproblem:

                    return render(request, 'subscription/resubscriptions.html',
                                  {'form': form,'reader': reader, 'tooltip': "Ajout d'un lecteur", 'lecteur': lecteur})
                else:
                    subscription = form.save(commit=False)
                    subscription.created_by = request.user.id
                    subscription.reader_id = lecteur
                    subscription.save()
                    messages.info(request, "Ajout effectué avec succés")
                    return HttpResponseRedirect(reverse('subscriptions'))
            else:
                messages.error(request, "Erreur d'ajout veillez vérifier bien votre formulaire")
                return render(request, 'subscription/resubscriptions.html',
                              {'form': form, 'reader': reader, 'tooltip': "Réabonnement", 'lecteur': lecteur})
        else:
            form = SubscriptionForm(instance=abon)
            return render(request, 'subscription/resubscriptions.html',
                          {'form': form, 'reader': reader, 'tooltip': "Réabonnement", 'lecteur': lecteur})
    else:
        return redirect('home_site')


@login_required(login_url='login')
def listexpirer(request):
    if request.user.has_perm('subscription.view_subscription'):
        form = SubscriptionForm()
        customlist = []
        listes = Subscription.objects.filter(status=1)
        for li in listes:
            ob = {
                'pk': li.pk,
                'reader': li.reader,
                'start_subscription': li.start_subscription,
                'end_subscription': li.end_subscription,
                'dif': li.end_subscription > date.today(),
                'nb_jour': (li.end_subscription - date.today()).days
            }
            customlist.append(ob)
        context = {
            'tooltip': 'Réabonnement',
            'form': form,
            'listes': customlist
        }
        return render(request, 'subscription/listexpirer.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def profile_reader(request, id):
    if request.user.has_perm('subscription.view_subscription'):
        abonnem = Subscription.objects.filter(pk=id).filter(status=1)
        customlist2 = []
        for ab in abonnem:
            ob2 = {
                'pk': ab.pk,
                'status': ab.status,
                'firstname': ab.reader.first_name,
                'lastname': ab.reader.last_name,
                'nationalite': ab.reader.nationality_reader,
                'adress': ab.reader.address_reader,
                'email': ab.reader.email,
                'sexe': ab.reader.gender_reader,
                'photo': ab.reader.image_reader,
                'finSubs': ab.end_subscription,
                'type_piece': ab.reader.type_piece_reader,
                'number_type_piece': ab.reader.number_piece_reader,
                'telephone': ab.reader.phone1_reader,
                'telephone2': ab.reader.phone2_reader,
                'readpoint': ab.reader.readpoint.name_readpoint,
                'communeRP': ab.reader.readpoint.commune_readpoint,
                'contactRP': ab.reader.readpoint.contact1_readpoint,
                'emailRP': ab.reader.readpoint.email_readpoint,
            }
            customlist2.append(ob2)
            listesAbonnement = Subscription.objects.filter(reader=ab.reader)
            customl = []
            for li in listesAbonnement:
                tab = {
                    'pk': li.pk,
                    'reader': li.reader,
                    'start_subscription': li.start_subscription,
                    'end_subscription': li.end_subscription,
                    'dif': li.end_subscription > date.today(),
                    'nb_jour': (li.end_subscription - date.today()).days
                }
                customl.append(tab)

        return render(request, 'subscription/profile_reader.html', {'abonnem': customlist2, 'l': listesAbonnement})
    else:
        return redirect('home_site')


# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        if request.user.is_superuser:
            subscription = Subscription.objects.filter(status=1)
        else:
            reader = Subscription.objects.filter(reader__readpoint=request.user.readpoint.pk).filter(status=1)
        print(subscription)
        # changer le chemin du temble
        pdf = html_to_pdf('subscription/printSubscription.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "subscription": subscription,
            # le tooltip
            "title":'Liste Des Abonnéments'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
