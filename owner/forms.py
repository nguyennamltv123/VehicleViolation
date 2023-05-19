from django.forms import ModelForm
from .models import Owner
from django import forms
class OwnerForm(ModelForm):
    
    class Meta:
        model = Owner
        fields = ('id', 'firstname', 'lastname', 'id_card', 'phone', 'email', 'image')
        labels = {
            'id': 'ID',
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'id_card': 'ID Card',
            'phone': 'Phone',
            'email': 'Email',
            'image': "Image"
        }

class SearchingForm(forms.Form):
    search = forms.CharField(max_length=100, label='ID Numbers')