from django import forms
from .models import PantryItem

class PantryItemForm(forms.ModelForm):
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Expiration Date'
    )
    class Meta:
        model = PantryItem
        fields = ['name', 'quantity', 'expiration_date']
