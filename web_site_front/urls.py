from django.urls import path

from formulairmail.views import vuemail
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('book_site', views.BookSite, name='book_site'),
    path('book_site/<str:name>', views.BookSites, name='book_site_sort'),
    path('book_site_search/', views.searchBy, name='book_site_search'),
    path('add_comment_site', views.addcoment, name='add_comment_site'),
    path('add_comment_site_eco', views.addcoment_eco, name='add_comment_site_eco'),
    path('event_site', views.EventSite, name='events_site'),
    path('home_site', views.HomeSite, name='home_site'),
    path('readpoint_site', views.ReadPointSite, name='readpoint_site'),
    path('ecocitoyennete_site', views.Ecocitoyennete, name='ecocitoyennete_site'),
    path('contacts_site', views.Contact, name='contacts_site'),
    path('about_site', views.About, name='about_site'),
    path('slide', views.slide, name='slide'),
    path('newletter', views.newletter, name='newletter'),
    path('slide_delete/<int:id>', views.deleteslide, name='slide_delete'),
    path('slide_edit/<int:id>', views.editslide, name='slide_edit'),
    path('detailsBook_site/<int:id>', views.detailsBook, name='detailsBook_site'),
    path('detailsCategorie/<str:name>', views.detailsCategorie, name='detailsCategorie'),
    path('point_livre/<int:id>', views.pointLivre, name='point_livre'),
    path('detailsEvent/<int:id>', views.detailsEvent, name='detailsEvent'),
    path('getbooks',views.getBooks,name='getbooks')
   ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
