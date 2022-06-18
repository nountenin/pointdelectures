from crispy_forms.helper import FormHelper
from django import forms

from book.models import Commentaires
from formulairmail.models import Newsletter
from web_site_front.models import Slide,  Commentaires_eco


class SlideForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SlideForm, self).__init__(*args, **kwargs)

        self.fields['text'].label = "Entrer le text du slide "
        self.fields['image'].label = "Entrer l'image du slide "

    class Meta:
        model = Slide
        fields = [
            'text',
            'image'

        ]


class Commentaires_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Commentaires_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Commentaires
        fields = [
           'commentaire',
           'note',
           'book',
        ]

class Commentaires_form_eco(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Commentaires_form_eco, self).__init__(*args, **kwargs)

    class Meta:
        model = Commentaires_eco
        fields = [
           'commentaire',
        ]


class NewLettersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewLettersForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Newsletter
        fields = ['emails']

