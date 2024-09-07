from django import forms
from .models import Faculte, Facultaire, Departement

class FaculteForm(forms.ModelForm):
    class Meta:
        model = Faculte
        fields = '__all__'

class FacultaireForm(forms.ModelForm):
    class Meta:
        model = Facultaire
        fields = '__all__'
        
class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = '__all__'