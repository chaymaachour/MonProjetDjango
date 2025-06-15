from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from airponFtth.models import Abonne, Panne, Technicien

# Formulaire d’inscription pour un technicien (avec création de compte utilisateur + modèle Technicien)
class TechnicienRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Champ email obligatoire
    first_name = forms.CharField(label="Prénom")  # Prénom
    last_name = forms.CharField(label="Nom")  # Nom
    telephone = forms.CharField(label="Téléphone")  # Téléphone du technicien
    adresse = forms.CharField(label="Adresse")  # Adresse du technicien

    class Meta:
        model = User  # Utilisation du modèle User de Django
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']  # Champs à afficher dans le formulaire

    def save(self, commit=True):
        # Sauvegarde du compte utilisateur et création de l'objet Technicien lié
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()  # Sauvegarde de l'utilisateur
            # Création du profil technicien lié à l'utilisateur
            technicien = Technicien.objects.create(
                user=user,
                telephone=self.cleaned_data['telephone'],
                adresse=self.cleaned_data['adresse']
            )
            # Ajout automatique du technicien au groupe 'Technicien'
            group, _ = Group.objects.get_or_create(name='Technicien')
            user.groups.add(group)

        return user

# Formulaire pour créer ou modifier un abonné
class AbonneForm(forms.ModelForm):
    class Meta:
        model = Abonne
        fields = ['nom', 'prenom', 'numtel', 'adresse']  # Champs visibles dans le formulaire

    def __init__(self, *args, **kwargs):
        # Récupération de l'objet Sub passé au formulaire
        self.sub = kwargs.pop('sub', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        # Validation personnalisée pour limiter le nombre d'abonnés à 8 par Sub
        cleaned_data = super().clean()
        if self.sub and self.sub.abonnes.count() >= 8:
            raise forms.ValidationError("Ce sous-niveau contient déjà 8 abonnés.")
        return cleaned_data

# Formulaire complet pour un technicien/admin qui gère les pannes
class PanneForm(forms.ModelForm):
    class Meta:
        model = Panne
        fields = ['abonne', 'type_panne', 'description', 'etat']  # Tous les champs nécessaires à la gestion complète

# Formulaire simplifié pour qu’un abonné signale une panne (sans choisir l'état ni l'abonné)
class PannePublicForm(forms.ModelForm):
    class Meta:
        model = Panne
        fields = ['description']  # Seule la description est demandée à l'utilisateur public
