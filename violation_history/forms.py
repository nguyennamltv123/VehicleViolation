from django import forms
from django.forms import ModelForm
from .models import Violation, ViolationHistory

class ViolationForm(ModelForm):
    
    class Meta:
        model = Violation
        fields = ('id', 'description', 'fee')
        labels = {
            'id': 'ID',
            'description': 'Description',
            'fee': 'Fee'
        }

class SearchingForm(forms.Form):
    search = forms.CharField(max_length=100, label='Plate numbers')