from reader.models import Reader
from subscription.models import Subscription
from django import forms


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        # fields = '__all__'
        fields = ['start_subscription', 'end_subscription']
    start_subscription = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Debut d'abonnement")
    end_subscription = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Fin d'abonnement")
