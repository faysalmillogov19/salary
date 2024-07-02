from django import forms
from .models import Employe, Contrat,SituationMatrimoniale,Diplome, Dossiers
from .models import (Categorie,Specialite,Structure,TypeContrat, 
    ModeCalcule)
from elementSal.models import Elementsalaire
from django.forms import ClearableFileInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.exceptions import ValidationError

# Utilisez tous les champs du modèle Employe

class DateInput(forms.DateInput):
    input_type = 'date'

#Formulaire de l'employe
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'  

    def valide_date_naissance(value):
        if value.year > 2006 or (value.year == 2006 and value.month >=12):
            raise forms.ValidationError("La date est invalide")

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if any(char.isdigit() for char in nom):
            raise ValidationError("Le nom ne peut pas contenir des chiffres.")
        return nom

    def clean_prenoms(self):
        prenoms = self.cleaned_data['prenoms']
        if any(char.isdigit() for char in prenoms):
            raise ValidationError("Les prénoms ne peuvent pas contenir des chiffres.")
        return prenoms

    def clean_lieu_naissance(self):
        lieu_naissance = self.cleaned_data['lieu_naissance']
        if any(char.isdigit() for char in lieu_naissance):
            raise ValidationError("Le lieu de naissance ne peut pas contenir des chiffres.")
        return lieu_naissance

    def clean_nom_pere(self):
        nom_pere = self.cleaned_data['nom_pere']
        if any(char.isdigit() for char in nom_pere):
            raise ValidationError("Le nom du pere ne peuvent pas contenir des chiffres.")
        return nom_pere

    def clean_nom_mere(self):
        nom_mere = self.cleaned_data['nom_mere']
        if any(char.isdigit() for char in nom_mere):
            raise ValidationError("Le nom de la mère ne peuvent pas contenir des chiffres.")
        return nom_mere


    def clean_personne_prevenir(self):
        personne_prevenir = self.cleaned_data['personne_prevenir']
        if any(char.isdigit() for char in personne_prevenir):
            raise ValidationError("Le nom ne peuvent pas contenir des chiffres.")
        return personne_prevenir

    def clean_sous_couvert(self):
        sous_couvert = self.cleaned_data['sous_couvert']
        if any(char.isdigit() for char in sous_couvert):
            raise ValidationError("Le nom ne peuvent pas contenir des chiffres.")
        return sous_couvert

    # Ajoutez des classes Bootstrap aux champs du formulaire
    nom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    prenoms = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    lieu_naissance = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    date_naissance = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control'}), 
        input_formats=['%Y-%m-%d'], 
        validators=[valide_date_naissance],
        required=False,
        )
    sexe = forms.ChoiceField(  
        choices=[('M', 'Masculin'), 
        ('F', 'Féminin')], 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        )
    situation_matrimoniale = forms.ModelChoiceField(
        queryset=SituationMatrimoniale.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        )
    nombre_enfant = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        )
    telephone = PhoneNumberField(
        region='BF', 
        widget=PhoneNumberPrefixWidget(initial="BF", attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
        required=False,
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False,
        )
    adresse = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    numero_cnib = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    profession = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    dernier_diplome = forms.ModelChoiceField(
        queryset=Diplome.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        )
    specialite = forms.ModelChoiceField(
        queryset=Specialite.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        )
    option = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False,
        )
    numero_cnss = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    numero_matricule = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    nom_pere = forms.CharField(label='Nom du père',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    nom_mere= forms.CharField(label='Nom de la mère',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    personne_prevenir = forms.CharField(label='Personne à prévenir',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    telephone_prevenir = PhoneNumberField(label='Contact de la personne à prévenir ',
        region='BF', 
        widget=PhoneNumberPrefixWidget(initial="BF", attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
        required=False,
        )
    photo_cnib = forms.ImageField(label="Ajouter la photo de votre CNIB" ,
        widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file'}),
        required=False,
        )
    photo_identite = forms.ImageField(label="Ajouter votre photo d'identité",
        widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file'}),
        required=False,
        )
    sous_couvert= forms.CharField(label='Sous couvert',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        )
    
    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance and (date_naissance.year > 2006 or (date_naissance.year == 2006 and date_naissance.month >= 12)):
            raise forms.ValidationError("La date de naissance doit être antérieure à décembre 2006.")

        return date_naissance

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            return cv.name  
        return None

    def clean_lettre_motivation(self):
        lettre_motivation = self.cleaned_data.get('lettre_motivation')
        if lettre_motivation:
            return lettre_motivation.name  
        return None

    def clean_diplome(self):
        diplome = self.cleaned_data.get('diplome')
        if diplome:
            return diplome.name  
        return None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajoutez des identifiants aux champs du formulaire
        self.fields['nom'].widget.attrs['id'] = 'id_nom'
        self.fields['prenoms'].widget.attrs['id'] = 'id_prenom'
        self.fields['lieu_naissance'].widget.attrs['id'] = 'id_lieu_naissance'
        self.fields['date_naissance'].widget.attrs['id'] = 'id_date_naissance'
        self.fields['sexe'].widget.attrs['id'] = 'id_sexe'
        self.fields['situation_matrimoniale'].widget.attrs['id'] = 'id_situation_matrimoniale'
        self.fields['nombre_enfant'].widget.attrs['id'] = 'id_nombre_enfant'
        self.fields['telephone'].widget.attrs['id'] = 'id_telephone'
        self.fields['email'].widget.attrs['id'] = 'id_email'
        self.fields['adresse'].widget.attrs['id'] = 'id_nom'
        self.fields['nom'].widget.attrs['id'] = 'id_adresse'
        self.fields['dernier_diplome'].widget.attrs['id'] = 'id_dernier_diplome'
        self.fields['categorie'].widget.attrs['id'] = 'id_categorie'
        self.fields['specialite'].widget.attrs['id'] = 'id_specialite'
        self.fields['option'].widget.attrs['id'] = 'id_option'        
        self.fields['numero_cnss'].widget.attrs['id'] = 'id_numero_cnss'
        self.fields['numero_matricule'].widget.attrs['id'] = 'idnumero_matricule'

#formulaire du dossier des employe
class DossiersFrom(forms.ModelForm):
    class Meta:
        model = Dossiers
        fields = ('libelle', 'file')


    libelle = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    file = forms.FileField(
        widget=ClearableFileInput(attrs={'class': 'form-control-file'}), 
        required=False
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['libelle'].widget.attrs['id'] = 'id_libelle'
        self.fields['file'].widget.attrs['id'] = 'id_file'

#formulaire des contrat
class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'
        widget = {
            'type_contrat': forms.Select(attrs={'class':'contrat-type'})
        }


    # Ajoutez des classes Bootstrap aux champs du formulaire
    structure = forms.ModelChoiceField(
        queryset=Structure.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        )
    employe = forms.ModelChoiceField(
        queryset=Employe.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True,
        )
    poste = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=True,
        )
    description_poste = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}),
        required=True,
        )
    description_profil = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}),
        required=True,
        )
    lieu_affectation = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=True,
        )
    diplome_requis = forms.ModelChoiceField(
        queryset=Diplome.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True,
        )
    type_contrat = forms.ModelChoiceField(
        queryset=TypeContrat.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True,
        )
    cadre = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        required=False,  # Facultatif selon vos besoins
    )
    mode_calcul = forms.ModelChoiceField(
        queryset=ModeCalcule.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True)
    date_debut = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control'}), 
        input_formats=['%Y-%m-%d'],
        required=True,
        )
    date_fin = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control'}), 
        input_formats=['%Y-%m-%d'],
        required=True,
        )
    salaire_base = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    indemnite_logement = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    indemnite_transport = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    indemnite_fonction = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    indemnite_risque = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    prime_nourriture = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    prime_lait = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    prime_salissure = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    prime_astreinte = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    nombre_annee_travail = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    augmentation_octobre_2019 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    augementation_special_pourcentage = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    sursalaire = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,  # Facultatif selon vos besoins
    )
    prime_anciennete = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        required=False,  # Facultatif selon vos besoins
    )
    prime_quart = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        required=False,  # Facultatif selon vos besoins
    )
    prime_panier = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        required=False,  # Facultatif selon vos besoins
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #     if 'instance' in kwargs and kwargs['instance'] is not None:
    #         employe = kwargs['instance'].employe
    #         self.fields['employe'].initial = employe
    #         self.fields['employe'].widget.attrs['readonly'] = True

        # Ajoutez des identifiants aux champs du formulaire
        self.fields['structure'].widget.attrs['id'] = 'id_structure'
        self.fields['employe'].widget.attrs['id'] = 'id_employe'
        self.fields['description_poste'].widget.attrs['id'] = 'id_description_poste'
        self.fields['description_profil'].widget.attrs['id'] = 'id_description_profil'
        self.fields['lieu_affectation'].widget.attrs['id'] = 'id_lieu_affectation'
        self.fields['diplome_requis'].widget.attrs['id'] = 'id_diplome_requis'
        self.fields['type_contrat'].widget.attrs['id'] = 'id_type_contrat'
        self.fields['date_debut'].widget.attrs['id'] = 'id_date_debut'
        self.fields['date_fin'].widget.attrs['id'] = 'id_date_fin'
        self.fields['salaire_base'].widget.attrs['id'] = 'id_salaire_base'
        self.fields['indemnite_logement'].widget.attrs['id'] = 'id_indemnite_logement'
        self.fields['indemnite_transport'].widget.attrs['id'] = 'id_indemnite_transport'
        self.fields['indemnite_fonction'].widget.attrs['id'] = 'id_indemnite_fonction'
        self.fields['prime_nourriture'].widget.attrs['id'] = 'id_prime_nourriture'
        self.fields['prime_lait'].widget.attrs['id'] = 'id_prime_lait'
        self.fields['prime_anciennete'].widget.attrs['id'] = 'id_prime_anciennete'
        self.fields['prime_salissure'].widget.attrs['id'] = 'id_prime_salissure'
        self.fields['prime_astreinte'].widget.attrs['id'] = 'id_prime_astreinte'
        self.fields['nombre_annee_travail'].widget.attrs['id'] = 'id_nombre_annee_travail'
        self.fields['prime_quart'].widget.attrs['id'] = 'id_prime_quart'
        self.fields['prime_panier'].widget.attrs['id'] = 'id_prime_panier'
        # Exécutez la fonction updateDateFields lors de l'initialisation du formulaire
        self.fields['type_contrat'].widget.attrs['onchange'] = 'updateDateFields();'

class StructureForum(forms.ModelForm):
    class Meta:
        model = Structure
        fields = '__all__'

    # Ajoutez des classes Bootstrap aux champs du formulaire
    denomination = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=True,
        )
    description_structure = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}),
        required=True,
        )
    telephone = PhoneNumberField(
        region='BF', 
        widget=PhoneNumberPrefixWidget(initial="BF", attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'})
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    adresse = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
class DossiersFrom(forms.ModelForm):
    class Meta:
        model = Dossiers
        fields = ['libelle', 'file']


    libelle = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    file = forms.FileField(
        widget=ClearableFileInput(attrs={'class': 'form-control-file'}), 
        required=False
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['libelle'].widget.attrs['id'] = 'id_libelle'
        self.fields['file'].widget.attrs['id'] = 'id_file'
        
#Formulaire des type decontrat
class TypeContratForm(forms.ModelForm):
    libelle = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}),
        required=True,
        )
    class Meta(object):
        model=TypeContrat
        fields=['libelle', 'file']
