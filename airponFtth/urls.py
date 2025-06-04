from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accueil/', views.accueil, name='accueil'),

    # Navigation hiérarchique
    path('central/', views.central_list, name='central_list'),
    path('central/<int:central_id>/hubs/', views.hub_list, name='hub_list'),
    path('hub/<int:hub_id>/chaines/', views.chaine_list, name='chaine_list'),
    path('chaine/<int:chaine_id>/subs/', views.sub_list, name='sub_list'),
    path('sub/<int:sub_id>/abonnes/', views.abonne_list, name='abonne_list'),

    # CRUD abonnés
    path('sub/<int:central_id>/<int:sub_id>/abonnes/ajouter/', views.ajouter_abonne, name='ajouter_abonne'),
    path('abonnes/<int:abonne_id>/modifier/', views.modifier_abonne, name='modifier_abonne'),
    path('sub/<int:sub_id>/abonnes/<int:abonne_id>/supprimer/', views.supprimer_abonne, name='supprimer_abonne'),

    # Tous les abonnés
    path('abonnes/', views.tous_abonnes, name='tous_abonnes'),

    # Gestion des pannes
    path('abonnes/<int:abonne_id>/pannes/ajouter/', views.ajouter_panne, name='ajouter_panne'),
    path('pannes/', views.liste_pannes, name='liste_pannes'),
    path('pannes/<int:panne_id>/mettre_a_jour/', views.mettre_a_jour_panne, name='mettre_a_jour_panne'),
    path('pannes/plus5j/', views.pannes_non_resolues, name='pannes_plus5j'),

    # Authentification
    path('signup/', views.technicien_register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('dashboard/technicien/', views.dashboard_technicien, name='dashboard_technicien'),

    # Chaines et abonnés par chaîne
    path('chaines/', views.liste_chaines, name='liste_chaines'),
    path('abonnes/chaine/<int:chaine_id>/', views.abonnés_par_chaine, name='abonnes_par_chaine'),
]
