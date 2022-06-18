from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from reader.models import Reader
from subscription.models import Subscription
from book.models import ReadPoint, Book, Rayon, Category
from borrow.models import Borrow


# Create your views here.
@login_required(login_url='login')
def reader_statistics(request):
    if request.user.type_Reader=='1':
        count_reader = Reader.objects.exclude(status=0).count()
        count_reader_girls = Reader.objects.filter(gender_reader__exact='f').exclude(status=0).count()
        count_reader_men = count_reader - count_reader_girls
        count_reader_men_percentage = ((count_reader_men / count_reader) * 100)
        count_reader_girls_percentage = 100.00 - count_reader_men_percentage
        count_subscribed = Subscription.objects.filter(status__exact=1).count()
        subscribeds = Subscription.objects.filter(status__exact=1)
        count_subscribed_percentage = (count_subscribed / count_reader) * 100
        count_subscribed_men = 0
        for subscribed in subscribeds:
            if subscribed.reader.gender_reader == 'm':
                count_subscribed_men += 1
        count_subscribed_men_percentage = 0
        if count_subscribed != 0:
            count_subscribed_men_percentage = (count_subscribed_men / count_subscribed) * 100

        count_subscribed_girls = count_subscribed - count_subscribed_men
        count_subscribed_girls_percentage = 0
        if count_subscribed != 0:
            count_subscribed_girls_percentage = (count_subscribed_girls / count_subscribed) * 100


        readpoints = ReadPoint.objects.exclude(status=0)
        data = []
        labels = []
        readpoint_subscribed_data = []
        subscribed_labels = []
        for rp in readpoints:
            readerCount = Reader.objects.filter(status=1).filter(readpoint=rp).count()
            if readerCount:
                data.append(readerCount)
                labels.append(rp.name_readpoint)
                readpoint_readers = Reader.objects.filter(status=1).filter(readpoint=rp)
                count_rs = 0
                for readpoint_reader in readpoint_readers:
                    rprs = Subscription.objects.filter(status=1).filter(reader=readpoint_reader).count()
                    if(rprs):
                        count_rs += rprs

                if count_rs > 0 :
                    readpoint_subscribed_data.append(count_rs)
                    subscribed_labels.append(rp.name_readpoint)

        context = {
            'count_reader': count_reader,
            'count_reader_girls': count_reader_girls,
            'count_reader_men': count_reader_men,
            'count_reader_men_percentage': round(count_reader_men_percentage, 2),
            'count_reader_girls_percentage': round(count_reader_girls_percentage, 2),
            'count_subscribed': count_subscribed,
            'count_subscribed_percentage': round(count_subscribed_percentage, 2),
            'count_subscribed_men': count_subscribed_men,
            'count_subscribed_men_percentage': round(count_subscribed_men_percentage, 2),
            'count_subscribed_girls': count_subscribed_girls,
            'count_subscribed_girls_percentage': round(count_subscribed_girls_percentage, 2),
            'data': data,
            'labels': labels,
            'readpoint_subscribed_data':readpoint_subscribed_data,
            'subscribed_labels':subscribed_labels,
        }
        return render(request, 'statistiques/reader_statistics.html', context)
    elif request.user.type_Reader=='2':
        return redirect('home_site')
@login_required(login_url='login')
def books_borrows(request):
    count_books = Book.objects.filter(status=1).aggregate(Sum('number_copy_book'))
    count_borrows = Borrow.objects.filter(status=1).count()

    book_quantities = []
    readpoint_names = []
    readpoints = ReadPoint.objects.exclude(status=0)
    for rp in readpoints:
        count_books_readpoint = 0
        rayons = Rayon.objects.exclude(status=0).filter(readpoint=rp)
        for ray in rayons:
            categories = Category.objects.exclude(status=0).filter(rayon=ray)
            count_books_rayon = 0
            for cat in categories:
                print(categories, cat)
                count_books_category = Book.objects.exclude(status=0).filter(category=cat).aggregate(
                    Sum('number_copy_book'))
                temp = count_books_category.get('number_copy_book__sum')
                if (temp):
                    count_books_rayon += temp
            count_books_readpoint += count_books_rayon
        if count_books_readpoint:
            book_quantities.append(count_books_readpoint)
            readpoint_names.append(rp.name_readpoint)

    emprunt_quatity = []
    readpoints_labels = []

    for rp in readpoints:
        rayons = Rayon.objects.exclude(status=0).filter(readpoint=rp)
        count_books_readpoint = 0
        for ray in rayons:
            categories = Category.objects.exclude(status=0).filter(rayon=ray)
            count_books_rayon = 0
            for cat in categories:
                count_books_category = 0
                books_category = Book.objects.exclude(status=0).filter(category=cat)
                for bk in books_category:
                    count_books_borrow = Borrow.objects.exclude(status=0).exclude(status=2).filter(book=bk).count()
                    count_books_category += count_books_borrow
                count_books_rayon += count_books_category
            count_books_readpoint += count_books_rayon
        if count_books_readpoint:
            emprunt_quatity.append(count_books_readpoint)
            readpoints_labels.append(rp.name_readpoint)



    context = {
        'count_books': count_books.get('number_copy_book__sum'),
        'count_borrows': count_borrows,
        'count_borrows_percentage': round((count_borrows / count_books.get('number_copy_book__sum')) * 100, 2),
        'data': book_quantities,
        'labels': readpoint_names,
        'emprunt_quatity': emprunt_quatity,
        'readpoints_labels': readpoints_labels
    }

    return render(request, 'statistiques/books_borrows.html', context)
