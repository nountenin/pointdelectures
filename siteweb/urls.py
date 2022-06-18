from django.urls import path
from .views import *
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('listecontact', views.ContactView)

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('listecontact/', listecontact, name='listecontact'),
    path('delete_contact/<int:id>/', delete_contact, name='delete_contact')
]
