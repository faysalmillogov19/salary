from django import forms
from .models import TarifHeureSup

class TarifHeureSupForm(forms.ModelForm):
    class Meta:
        model = TarifHeureSup
        fields = ['taux', 'jourFerie', 'nuit']
      
