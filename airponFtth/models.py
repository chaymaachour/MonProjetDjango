from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Technicien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - Technicien"

TYPE_PANNE_CHOICES = [
    ('connexion', 'Perte de connexion'),
    ('debit', 'Débit faible'),
    ('fibre', 'Coupure fibre'),
    ('voip', 'Problème VoIP'),
    ('deco', 'Déconnexions fréquentes'),
    ('fixe', 'Problème de ligne fixe'),
    ('routeur', 'Erreur routeur/modem'),
    ('sync', 'Perte de synchronisation'),
    ('ip', 'Adresse IP erronée'),
    ('reseau', 'Panne générale réseau'),
]

ETAT_CHOICES = [
    ('non_traite', 'Non traité'),
    ('en_cours', 'En cours'),
    ('resolu', 'Résolu'),
]

class Central(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Modèle représentant un Hub rattaché à un Central
class Hub(models.Model):
    central = models.ForeignKey(Central, on_delete=models.CASCADE, related_name='hubs')
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200) 
    date_creation = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.nom

class Chaine(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='chaines')
    nom = models.CharField(max_length=100)

    def clean(self):
        if not self.pk and self.hub.chaines.count() >= 8:
            raise ValidationError("Ce Hub contient déjà 8 chaînes.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Sub(models.Model):
    chaine = models.ForeignKey(Chaine, on_delete=models.CASCADE, related_name='subs')
    nom = models.CharField(max_length=100)

    def clean(self):
        if not self.pk and self.chaine.subs.count() >= 4:
            raise ValidationError("Cette chaîne contient déjà 4 Subs.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Abonne(models.Model):
    sub = models.ForeignKey(Sub, related_name='abonnes', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numtel = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
  
  #Assure la validation des données du modèle avant l’enregistrement en base.
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Panne(models.Model):
    abonne = models.ForeignKey(Abonne, on_delete=models.CASCADE, related_name='pannes')
    type_panne = models.CharField(max_length=50, choices=TYPE_PANNE_CHOICES)
    description = models.TextField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='non_traite')
    date_signalement = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
