from django import forms
from airponFtth.models import Abonne, Panne
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Technicien


class TechnicienRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    telephone = forms.CharField(label="Téléphone")
    adresse = forms.CharField(label="Adresse")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            technicien = Technicien.objects.create(
                user=user,
                telephone=self.cleaned_data['telephone'],
                adresse=self.cleaned_data['adresse']
            )
            from django.contrib.auth.models import Group
            group, created = Group.objects.get_or_create(name='Technicien')
            user.groups.add(group)
        return user



class AbonneForm(forms.ModelForm):
    class Meta:
        model = Abonne
        fields = ['nom', 'prenom', 'numtel', 'adresse']

class PanneForm(forms.ModelForm):
    class Meta:
        model = Panne
        fields = ['abonne', 'type_panne', 'description','etat']

class PannePublicForm(forms.ModelForm):  # <-- Cette classe manquait
    class Meta:
        model = Panne
        fields = ['description']


