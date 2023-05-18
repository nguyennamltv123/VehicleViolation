from django.forms import ModelForm
from .models import Owner

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