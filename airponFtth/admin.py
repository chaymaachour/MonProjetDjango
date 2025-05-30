from django.contrib import admin
from .models import Abonne, Panne, Central, Hub, Chaine, Sub

# Admin personnalisé pour Abonné
class AbonneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'numtel', 'adresse']
    search_fields = ['nom', 'prenom', 'numtel', ]
    list_filter = ['sub']

# Admin personnalisé pour Panne
class PanneAdmin(admin.ModelAdmin):
    list_display = ['abonne', 'description', 'date_signalement', 'etat']  # Affiche les champs dans la liste
    list_filter = ['etat', 'abonne']  # Filtrage par état de la panne et abonné
    search_fields = ['abonne__nom', 'description']  # Recherche par nom d'abonné et description
    # Rendre l'état lisible sous forme de texte (Non traité, en cours, résolue)
    def etat_display(self, obj):
        return obj.get_etat_display()  # Utilise la méthode get_etat_display()
    etat_display.short_description = 'État'  # Titre de la colonne 'État' dans la liste

# Enregistrer les modèles dans l'admin
admin.site.register(Abonne, AbonneAdmin)
admin.site.register(Panne, PanneAdmin)
admin.site.register(Central)
admin.site.register(Hub)
admin.site.register(Chaine)
admin.site.register(Sub)
