from django.urls import path
from . import views
from .views import GeneratePdf

urlpatterns = [
    path('', views.subscriptions, name="subscriptions"),
    path('resubscription/', views.listexpirer, name="resubscriptions"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('modifier/<int:id>/', views.modifier, name="modifier"),
    path('carte/<int:id>/', views.profile_reader, name="carte"),
    path('resubscriptions/<int:id>/', views.resubscriptions, name="resubscriptions"),
    path('pdf/', GeneratePdf.as_view(),name='printSubscription'),

]
