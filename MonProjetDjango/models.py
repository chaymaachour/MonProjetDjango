from django.contrib import admin
from .models import Panne, Abonne, Technicien, Central, Hub, Chaine, Sub

class PanneAdmin(admin.ModelAdmin):
    list_display = ('abonne', 'description', 'date_signalement', 'etat')  # Afficher les champs dans la liste
    list_filter = ('etat',)  # Ajouter un filtre par état dans l'admin
    search_fields = ('abonne__nom', 'description')  # Recherche par nom d'abonné ou description

admin.site.register(Panne, PanneAdmin)
admin.site.register(Abonne)
admin.site.register(Technicien)
admin.site.register(Central)
admin.site.register(Hub)
admin.site.register(Chaine)
admin.site.register(Sub)
