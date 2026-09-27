from django import forms
from .models import Inventory


class InventoryModelForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['medicinename', 'availablestock']
        label = {'medicinename': 'Medicine Name',
                 'availablestock': 'Available Stock'}
