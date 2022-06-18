

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Contact
from rest_framework import viewsets
from .serializers import ContactSerializer
from django.contrib import messages

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message envoyé avec succès")
        else:
            messages.error(request, "Votre message n'a pas été envoyé veuillez verifier le formulaire")
    return redirect('contacts_site')

# @login_required(login_url='login')
def listecontact(request):
    listecontact = Contact.objects.filter(status=1).filter(readpoint=request.user.readpoint) if not request.user.is_superuser else Contact.objects.filter(status=1)
    return render(request, 'siteweb/liste_contact.html', context={'listecontact': listecontact})


# @login_required(login_url='login')
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.status = 0
    contact.save()
    listecontact = Contact.objects.exclude(status=0)
    return render(request, 'siteweb/liste_contact.html', context={'listecontact': listecontact})


class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
