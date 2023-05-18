from django import forms

class SearchingForm(forms.Form):
    search = forms.CharField(max_length=100, label='Plate numbers')