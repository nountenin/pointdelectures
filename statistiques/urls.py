from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[
path("statistics/", views.reader_statistics, name="statistics" ),
path("books_borrows/", views.books_borrows, name="books_borrows" )
]
