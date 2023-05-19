from django.forms import ModelForm
from .models import Vehicle
from django import forms
class VehicleForm(ModelForm):
    
    class Meta:
        model = Vehicle
        fields = ('id', 'plate', 'title', 'color', 'owner', 'image')
        labels = {
            'id': 'ID',
            'plate': 'Plate Number',
            'title': 'Title',
            'color': 'Color',
            'owner': 'Vehicle Owner',
            'image': 'Image'
        }

class SearchingForm(forms.Form):
    search = forms.CharField(max_length=100, label='Plate numbers')