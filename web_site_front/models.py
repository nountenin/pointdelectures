from django.db import models

from book.models import Book
from reader.models import Reader


class Slide(models.Model):
    text = models.CharField(max_length=50)
    image = models.ImageField(upload_to='slides')
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{} {}".format(
            self.text,
            self.image
        )



class Commentaires_eco(models.Model):
    lecteur = models.ForeignKey(Reader,on_delete=models.CASCADE)
    commentaire = models.TextField()
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{} {}".format(
            self.text,
            self.image
        )

# Create your models here.
