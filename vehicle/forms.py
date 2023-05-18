from django.forms import ModelForm
from .models import Vehicle

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