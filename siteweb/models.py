from django.db import models

from book.models import ReadPoint


class Contact(models.Model):
    nom_complet = models.CharField(max_length=20)
    mail_contact = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField()
    readpoint= models.ForeignKey(ReadPoint,on_delete=models.CASCADE)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{nom_complet} {mail_contact} {subject} {message} {status}".format(
            nom_complet = self.nom_complet,
            mail_contact= self.mail_contact,
            subject = self.subject,
            message = self.message,
            status = self.status
        )
