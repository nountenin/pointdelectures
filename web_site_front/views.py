import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from Events.models import Events
from book.models import *

# Create your views here.
from web_site_front.forms import SlideForm, NewLettersForm, Commentaires_form, Commentaires_form_eco
from web_site_front.models import Slide, Commentaires_eco


def BookSite(request):
    livre = Book.objects.filter(status=1).order_by('-notes')
    livre_pag = Paginator(livre, 20)
    curent_page = request.GET.get('page')
    page = livre_pag.get_page(curent_page)
    categorie = Category.objects.all().values('name_category').annotate(count=Count('id')).filter(status=1).order_by(
        'name_category')
    context = {
        'tooltip': 'Nos livres',
        'page': page,
        'curent_page': curent_page,
        'category': categorie,
        'nb': livre.count(),
        # 'book_meuilleur_choix': book_meuilleur_choix
        # 'note':note
    }
    return render(request, 'web_site_front/book_site.html', context)


def EventSite(request):
    categorie = Category.objects.filter(status=1)
    event = Events.objects.filter(status=1)
    event_page = Paginator(event, 2)
    curent_page = request.GET.get('page')
    page = event_page.get_page(curent_page)
    context = {
        'tooltip': 'Evenement',
        'category': categorie,
        'page': page,
        'curent_page': curent_page,
    }
    return render(request, 'web_site_front/events_site.html', context)


def HomeSite(request):
    categorie = Category.objects.all().values('name_category').annotate(count=Count('id')).filter(status=1).order_by(
        'name_category')
    eco = Events.objects.filter(type='ecocitoyenne').filter(status=1)
    livre = Book.objects.filter(status=1).order_by('-notes')
    redpoint = ReadPoint.objects.filter(status=1)
    event = Events.objects.filter(status=1)
    slides = Slide.objects.filter(status=1)
    commentaire = Commentaires.objects.filter(status=1).order_by('-created_at')
    context = {

        # 'tooltip': 'Evenement',
        'category': categorie,
        'ecocitoyenne': eco,
        'slides': slides,
        'book': livre,
        'plecture': redpoint,
        'evenement': event,
        'commentaire': commentaire
    }
    return render(request, 'web_site_front/home_site.html', context)


def ReadPointSite(request):
    redpoint = ReadPoint.objects.filter(status=1)
    categorie = Category.objects.filter(status=1)
    event_page = Paginator(redpoint, 4)
    curent_page = request.GET.get('page')
    page = event_page.get_page(curent_page)
    context = {
        'tooltip': 'Point de Lectures',
        'plecture': redpoint,
        'page': page,
        'curent_page': curent_page,
        'category': categorie
    }
    return render(request, 'web_site_front/readpoint_site.html', context)


def Ecocitoyennete(request):
    categorie = Category.objects.filter(status=1)
    event = Events.objects.filter(status=1)
    event_page = Paginator(event, 2)
    curent_page = request.GET.get('page')
    page = event_page.get_page(curent_page)

    comments = Commentaires_eco.objects.filter(status=1).order_by('created_at')
    event_page_eco = Paginator(comments, 2)
    curent_page_comment = request.GET.get('page_comment')
    page_comment = event_page_eco.get_page(curent_page_comment)

    context = {
        'tooltip': 'Ecocitoyenneté',
        'category': categorie,
        'page': page,
        'curent_page': curent_page,
        'page_comment': page_comment,
        'curent_page_comment': curent_page_comment,
    }
    return render(request, 'web_site_front/ecocitoyennete_site.html', context)


def Contact(request):
    categorie = Category.objects.filter(status=1)
    pointlecture = ReadPoint.objects.filter(status=1)
    context = {
        'tooltip': 'Contact',
        'category': categorie,
        'readpoint': pointlecture
    }
    return render(request, 'web_site_front/contacts_site.html', context)


def About(request):
    categorie = Category.objects.filter(status=1)
    context = {
        'tooltip': 'Apropos',
        'category': categorie
    }
    return render(request, 'web_site_front/about_site.html', context)


@login_required(login_url='login')
def slide(request):
    slides = Slide.objects.filter(status=1)
    form = SlideForm()
    context = {
        'form': form,
        'slides': slides
    }
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "succes")
            return render(request, 'web_site_front/slide_site.html', context)

        else:
            messages.error(request, "Les données ne sont pas valide")
            return render(request, 'web_site_front/slide_site.html', context)

    return render(request, 'web_site_front/slide_site.html', context)


@login_required(login_url='login')
def deleteslide(request, id):
    if request.user.has_perm('delete_slide'):
        em = Slide.objects.get(pk=id)
        em.status = 0
        em.save()
        return redirect('slide')


@login_required(login_url='login')
def editslide(request, id):
    if request.user.has_perm('change_slide'):
        rp = Slide.objects.get(id=id)
        slides = Slide.objects.filter(status=1)
        form = SlideForm(instance=rp)
        if request.method == "POST":
            form = SlideForm(request.POST, request.FILES, instance=rp)
            if form.is_valid():
                form.save()
                messages.success(request, "Modification effectuée avec succés")
                return redirect('slide')
            else:
                messages.error(request, 'Erreur de modification')
                return render(request, 'web_site_front/slide_site.html', {'slides': slides, 'form': form})
        return render(request, 'web_site_front/slide_site.html', {'slides': slides, 'form': form})
    else:
        messages.error(request, "Vous n'avez pas le droit de modifier un point de lecture")
        return render(request, 'permission.html')


def detailsBook(request, id):
    categorie = Category.objects.filter(status=1)

    if id is not None:
        book = Book.objects.filter(status=1).filter(pk=id)
        book = book[0]
        commentaire = Commentaires.objects.filter(book=book).order_by('-created_at')
        books = Book.objects.filter(status=1).filter(category=book.category).exclude(pk = book.pk)
        return render(request, 'web_site_front/detailsBook_site.html',
                      {'commentaire': commentaire, 'book': book, 'books': books, 'category': categorie,
                       'tooltip': 'Détails sur le livre'})
    return redirect('home_site')


def detailsCategorie(request, name):
    categorie = Category.objects.filter(status=1)
    if name is not None:
        livre = Book.objects.filter(status=1).filter(category__name_category=name)
        livre_pag = Paginator(livre, 20)
        curent_page = request.GET.get('page')
        page = livre_pag.get_page(curent_page)
        categorie = Category.objects.all().values('name_category').annotate(count=Count('id')).filter(
            status=1).order_by(
            'name_category')
        context = {
            'tooltip': 'Nos livres',
            'page': page,
            'curent_page': curent_page,
            'category': categorie,
            'nb': livre.count(),
            'tooltip': 'Détails sur la catégorie',
            'id':name
                    }

        return render(request, 'web_site_front/detailsCategorie.html',context)

    return redirect('home_site')


def detailsEvent(request, id):
    categorie = Category.objects.filter(status=1)
    if id is not None:
        event = Events.objects.filter(status=1).filter(pk=id)
        return render(request, 'web_site_front/detailsEvents.html',
                      {'events': event, 'category': categorie, 'tooltip': 'Détails sur l\'événément'})
    return redirect('home_site')


def newletter(request):
    if request.method == 'POST':
        form = NewLettersForm(request.POST)
        if form.is_valid():
            messages.success(request, 'votre Email a été enregistré avec succès')
            form.save()
            return redirect('home_site')
        else:
            messages.error(request, 'veillez saisir un email valide')
            return redirect('home_site')


def pointLivre(request, id):
    if id is not None:
        livre = Book.objects.filter(status=1).order_by('-notes').filter(category__rayon__readpoint_id=id)
        livre_pag = Paginator(livre, 20)
        curent_page = request.GET.get('page')
        page = livre_pag.get_page(curent_page)
        categorie = Category.objects.filter(status=1)
        context = {
            'tooltip': 'Nos livres',
            'page': page,
            'id':id,
            'curent_page': curent_page,
            'category': categorie,
            'nb': livre.count(),
            # 'book_meuilleur_choix': book_meuilleur_choix
            # 'note':note
        }
        return render(request, 'web_site_front/point_livre.html', context)

    return redirect('home_site')



def addcoment(request):
    if request.POST:
        form = Commentaires_form(request.POST)
        if form.is_valid():
            comentaire = form.save(commit=False)
            comentaire.lecteur = request.user.id
            if not comentaire.save():
                book = Book.objects.get(pk=comentaire.book.pk)
                coment = book.note()
                book.notes = coment['note__avg']
                book.save()

                messages.success(request, "Votre commentaire a été ajouté avec succès")
            else:
                messages.error(request, "Votre commentaire n'a pas été ajouté")

        else:
            messages.error(request,'Veuillez renseigner les messages')
        return redirect(f'detailsBook_site/{request.POST["book"]}')


def addcoment_eco(request):
    if request.user.is_authenticated:
        if request.POST:
            form = Commentaires_form_eco(request.POST)
            if form.is_valid():
                comentaire = form.save(commit=False)
                comentaire.lecteur = request.user
                if not comentaire.save():
                    messages.success(request, "Votre commentaire a été ajouté avec succès")
                else:
                    messages.error(request, "Votre commentaire n'a pas été ajouté")
        return redirect('ecocitoyennete_site')
    else:

        messages.error(request, "Veuillez vous authentifier pour poster une question ou commentaire")
        return redirect('ecocitoyennete_site')


def getBooks(request):
    if request.method == 'GET':
        ca = Category.objects.filter(name_category=request.GET['name'])
        books = Book.objects.filter(status=1).filter(category__in=ca).select_related('category')
        ser = serializers.serialize('json', books)
        return HttpResponse(ser)


def BookSites(request, name):
    name = name[1:]
    categorie = Category.objects.filter(name_category=name).filter(status=1)
    livre = Book.objects.filter(status=1).filter(category__in=categorie).select_related('category')

    if not livre.exists():
        messages.error(request, 'Aucun Livre dans cette categorie')
        return redirect('book_site')
    livre_pag = Paginator(livre, 12)
    curent_page = request.GET.get('page')
    page = livre_pag.get_page(curent_page)
    context = {
        'tooltip': 'Nos livres',
        'page': page,
        'curent_page': curent_page,
        'category': Category.objects.all().values('name_category').annotate(count=Count('id')).filter(
            status=1).order_by(
            'name_category'),
        'nb': livre.count(),
        'trie': True,
        'cat': '1' + name
    }
    return render(request, 'web_site_front/book_site.html', context)


def searchBy(request):
    if request.method == 'POST':
        attr = request.POST['search']
        livre = Book.objects.filter(isbn_book="akounamatata")
        book_by_isbn = Book.objects.filter(isbn_book__contains=attr).filter(status=1)
        # if book_by_isbn.exists():
        #     livre=book_by_isbn
        book_by_nom = Book.objects.filter(title_book__contains=attr).filter(status=1)
        # if book_by_nom.exists():
        #     livre+=book_by_nom
        book_by_date = Book.objects.filter(publication_date_book__contains=attr).filter(status=1)
        # if book_by_date.exists():
        #     livre+=book_by_date
        book_by_resume = Book.objects.filter(resume_book__contains=attr).filter(status=1)
        book_by_house = Book.objects.filter(edition_house__contains=attr).filter(status=1)
        book_by_author = Book.objects.filter(author__first_name_author__contains=attr).filter(status=1)
        if not book_by_author.exists():
            book_by_author = Book.objects.filter(author__last_name_author__contains=attr).filter(status=1)
        if book_by_nom.exists():
            livre = book_by_nom
        else:
            if book_by_isbn.exists():
                livre = book_by_isbn
            else:
                if book_by_date.exists():
                    livre = book_by_date
                else:
                    livre = book_by_resume if book_by_resume.exists() else book_by_house if book_by_house.exists() else book_by_author if book_by_author.exists() else livre

        if not livre.exists():
            messages.error(request, 'Aucun Resultat')
            return redirect('book_site')
        livre_pag = Paginator(livre, 12)
        curent_page = request.GET.get('page')
        page = livre_pag.get_page(curent_page)
        context = {
            'tooltip': 'Nos livres',
            'page': page,
            'curent_page': curent_page,
            'category': Category.objects.all().values('name_category').annotate(count=Count('id')).filter(
                status=1).order_by(
                'name_category'),
            'nb': livre.count(),
            'trie': True,
        }
        return render(request, 'web_site_front/book_site.html', context)
