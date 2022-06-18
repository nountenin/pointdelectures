from django.urls import path

from formulairmail.views import vuemail
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import GeneratePdf, GenerateUserPdf

urlpatterns = [
    path('', views.readers, name="readers"),
    path('addreader/', views.add_reader, name="add-reader"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('update/<int:id>/', views.charged, name='update'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('details/<int:id>/', views.details, name='details'),
    path('details_user/<int:id>/', views.details_user, name='details_user'),
    path('mail/', vuemail, name="vuemail"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('add-user/', views.add_user, name="add-user"),
    path("users/", views.users, name="users"),
    path("envoimail/", views.envoimail, name="envoimail"),
    path("sendConfirmation/<str:username>/<int:pk>/<str:email>/", views.send_confirmation_mail, name="send_confirmation_mail"),
    path("username/", views.get_user, name="username"),
    path("change/<int:id>/<str:email>/<str:username>/", views.change_password, name="change"),
    path("confirmChange/", views.confirm_changePassword, name="confirm_changePassword"),
    path('confirmation/<int:id>/<str:email>/<str:username>/', views.checkUser, name="confirmationPassword"),
    path('pdf/', GeneratePdf.as_view(), name='pdfprintReader'),
    path('pdfs/', GenerateUserPdf.as_view(), name='pdfprintUser'),

    #     mail
    path('emails/',views.emails,name='newsletters'),
    path('delete_email/<int:id>', views.delete_email,name = 'delete_email'),

    # Profil
    path('profile/',views.profile,name="profile")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
