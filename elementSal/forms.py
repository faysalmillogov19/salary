from django import forms
from elementSal.models import Elementsalaire

class ElementsalaireForm (forms.ModelForm):
    class Meta:
        model=Elementsalaire
        fields="__all__"

    

class ElementsacontratForm(forms.ModelForm):
    class Meta:
        model = Elementsalaire
        fields = "intitule_element"
    element_salaire = forms.ModelChoiceField(
        queryset=Elementsalaire.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        )