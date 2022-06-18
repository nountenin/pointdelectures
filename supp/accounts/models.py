from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from book.models import ReadPoint


class Account(AbstractUser):
    # phonenumber = models.CharField(max_length=18)
    # adresse = models.CharField(max_length=30)
    # password_changed = models.BooleanField(default=False)
    # readpoint = models.ForeignKey(ReadPoint, on_delete=models.CASCADE,default=1)
    #
    # USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = []
    print("hi")

# make_password()
