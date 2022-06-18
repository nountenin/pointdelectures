from django import forms
from .models import *


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['nom_complet'].label = "Nom Complet"
        self.fields['mail_contact'].label = "Email"
        self.fields['subject'].label = "Subject"
        self.fields['message'].label = "Message"
        self.fields['readpoint'].label = "Point de Lecture"

    class Meta:
        model = Contact
        fields = [
            'nom_complet',
            'mail_contact',
            'subject',
            'message',
            'readpoint'
        ]
