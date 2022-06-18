from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.shortcuts import redirect

from book.models import ReadPoint


# Create your models here.
class Reader(AbstractUser):
    gender = [
        ("f", "feminin"),
        ('m', 'masculin')
    ]
    tp = [
        ('Passport', 'Passport'),
        ('Carte d\'identité national', 'Carte d\'identité national'),
        ('Permis de conduire', 'Permis de conduire'),
        ('Carte d\'identité militaire', 'Carte d\'identité militaire'),
        ('Carte de séjour', 'Carte de séjour'),
        ('Carte Scolaire', 'Carte Scolaire'),
        ('Carte Etudiant', 'Carte Etudiant'),
    ]
    typ = [
        ('1', 'User'),
        ('2', 'Reader'),
    ]
    password_changed = models.BooleanField(default=False)
    nationality_reader = models.CharField(max_length=20, null=True, blank=True)
    phone1_reader = models.CharField(max_length=20)
    phone2_reader = models.CharField(max_length=20, null=True, blank=True)
    gender_reader = models.CharField(max_length=1, choices=gender)
    address_reader = models.CharField(max_length=30)
    image_reader = models.ImageField(upload_to='reader/images/', null=True, blank=True)
    type_piece_reader = models.CharField(max_length=30, choices=tp, null=True, blank=True)
    number_piece_reader = models.CharField(max_length=30, null=True, blank=True)
    image_piece_reader = models.FileField(upload_to='reader/fichiers', null=True, blank=True)
    readpoint = models.ForeignKey(ReadPoint, default=1, on_delete=models.CASCADE)
    type_Reader = models.CharField(choices=typ, max_length=1, null=True, blank=True)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f'ID: {self.pk}  Nom et Prenom: {self.last_name} {self.first_name}'

    def redirection(self):
        if self.type_Reader == '2':
            return redirect('home_site')


class Frequentation(models.Model):
    lecteur = models.ForeignKey(Reader, on_delete=models.CASCADE)
    date_frequentation = models.IntegerField(default=datetime.now().year)
    readpoint = models.ForeignKey(ReadPoint, on_delete=models.CASCADE)
    semaine = models.IntegerField(default=datetime.now().isocalendar()[1])
    mois  = models.IntegerField(default=datetime.now().month)



