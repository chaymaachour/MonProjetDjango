from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import logging
from django.contrib import messages
# Import des modèles
from airponFtth.models import Central, Hub, Chaine, Sub, Abonne, Panne

# Import des formulaires
from .forms import AbonneForm, PanneForm, TechnicienRegisterForm, PannePublicForm

# Page d'accueil
def accueil(request):
    # Affiche la liste de tous les centrals pour la page d’accueil
    centrals = Central.objects.all()
    return render(request, 'accueil.html', {'centrals': centrals})


def home(request):
    return render(request, 'app/home.html')

# Inscription technicien
def technicien_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirmation = request.POST.get('password_confirmation', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        # Validation simple
        if not all([username, first_name, last_name, email, password, password_confirmation, phone, address]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'registration/technicien_register.html')

        if password != password_confirmation:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'registration/technicien_register.html')

        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return render(request, 'registration/technicien_register.html')

        # Ici tu peux ajouter la création de l'utilisateur, etc.

        messages.success(request, "Compte créé avec succès !")
        return redirect('login')  # ou une autre page

    return render(request, 'registration/technicien_register.html')

@login_required
def dashboard_technicien(request):
    return render(request, 'dashboard/technicien_dashboard.html')


def pannes_non_resolues(request):
    seuil = timezone.now() - timedelta(days=5)
    pannes = Panne.objects.filter(
        etat='Non traité',
        date_signalement__lte=seuil
    )
    return render(request, 'airponFtth/pannes_non_resolues.html', {'pannes': pannes})
def notifier_pannes(request):
    seuil_date = timezone.now() - timedelta(days=5)
    pannes = Panne.objects.filter(etat='Non traité', date_signalement__lte=seuil_date)
    
    if pannes.exists():
        message = "Les pannes suivantes n'ont pas été traitées depuis plus de 5 jours:\n"
        for panne in pannes:
            message += f"- {panne.abonne.nom} {panne.abonne.prenom}: {panne.type_panne}\n"
        
        send_mail(
            subject="Alerte : Pannes non résolues",
            message=message,
            from_email="noreply@airponftth.com",
            recipient_list=["admin@airponftth.com"],  # à adapter
        )

    return render(request, 'airponFtth/alerte_envoyee.html', {'pannes': pannes})

    
def mettre_a_jour_panne(request, panne_id):
    panne = get_object_or_404(Panne, id=panne_id)
    if request.method == 'POST':
        panne.etat = 'résolue'
        panne.date_resolution = timezone.now()
        panne.save()
        return redirect('liste_pannes')
    return render(request, 'app/mettre_a_jour_panne.html', {'panne': panne})

# Navigation Hiérarchique Central → Hub → Chaine → Sub → Abonné
def central_list(request):
    centrals = Central.objects.all()
    return render(request, 'app/central_list.html', {'centrals': centrals})

def hub_list(request, central_id):
    central = get_object_or_404(Central, id=central_id)
    hubs = central.hubs.all()
    return render(request, 'app/hub_list.html', {'central': central, 'hubs': hubs})

def chaine_list(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    chaines = hub.chaines.all()
    return render(request, 'app/chaine_list.html', {'hub': hub, 'chaines': chaines})

def sub_list(request, chaine_id):
    chaine = get_object_or_404(Chaine, id=chaine_id)
    subs = chaine.subs.all()
    return render(request, 'app/sub_list.html', {'chaine': chaine, 'subs': subs})

def abonne_list(request, sub_id):
    sub = get_object_or_404(Sub, id=sub_id)
    abonnes = sub.abonnes.all()  # Utiliser 'abonnes' comme nom de la relation inverse
    return render(request, 'abonnes/abonne_list.html', {'abonnes': abonnes, 'sub': sub})

# CRUD Abonnés
def ajouter_abonne(request, central_id, sub_id):
    sub = get_object_or_404(Sub, id=sub_id)

    if request.method == 'POST':
        form = AbonneForm(request.POST)
        if form.is_valid():
            if sub.abonnes.count() >= 8:
                messages.error(request, "Ce sous-niveau contient déjà 8 abonnés.")
                return redirect('abonne_list', sub_id=sub_id)

            abonne = form.save(commit=False)
            abonne.sub = sub
            abonne.save()
            return redirect('abonne_list', sub_id=sub.id)
    else:
        form = AbonneForm()

    return render(request, 'app/ajouter_abonne.html', {'form': form, 'sub': sub})



def modifier_abonne(request, abonne_id):
    abonne = get_object_or_404(Abonne, id=abonne_id)

    if request.method == 'POST':
        form = AbonneForm(request.POST, instance=abonne)
        if form.is_valid():
            form.save()
            return redirect('abonne_list', sub_id=abonne.sub.id)
    else:
        form = AbonneForm(instance=abonne)

    return render(request, 'abonnes/modifier_abonne.html', {'form': form, 'abonne': abonne})

def supprimer_abonne(request, sub_id, abonne_id):
    # Récupérer l'objet Sub
    sub = get_object_or_404(Sub, id=sub_id)
    
    # Récupérer l'abonné spécifique
    abonne = get_object_or_404(Abonne, id=abonne_id, sub=sub)
    
    # Traitement du formulaire POST pour supprimer l'abonné
    if request.method == 'POST':
        abonne.delete()  # Suppression de l'abonné
        return redirect('abonne_list', sub_id=sub.id)
    
    # Si la requête est GET, afficher une confirmation avant suppression
    return render(request, 'app/supprimer_abonne.html', {
        'abonne': abonne,
        'sub': sub,
    })

# Liste globale des abonnés
def tous_abonnes(request):
    abonnes = Abonne.objects.select_related('sub').all()
    return render(request, 'app/tous_abonnes_list.html', {'abonnes': abonnes})



# Gestion des Pannes
def ajouter_panne(request, abonne_id):
    abonne = get_object_or_404(Abonne, id=abonne_id)
    if request.method == 'POST':
        form = PanneForm(request.POST)
        if form.is_valid():
            panne = form.save(commit=False)
            panne.abonne = abonne
            panne.save()
            return redirect('liste_pannes')
    else:
        form = PanneForm()
    return render(request, 'app/ajouter_panne.html', {'form': form, 'abonne': abonne})

def liste_pannes(request):
    pannes = Panne.objects.select_related('abonne').all()
    return render(request, 'airponFtth/liste_pannes.html', {'pannes': pannes})


# Liste des chaînes et abonnés par chaîne
def liste_chaines(request):
    chaines = Chaine.objects.all()
    return render(request, 'liste_chaines.html', {'chaines': chaines})

def abonnés_par_chaine(request, chaine_id):
    chaine = get_object_or_404(Chaine, id=chaine_id)
    abonnés = Abonne.objects.filter(sub__chaine=chaine)
    return render(request, 'abonnes_par_chaine.html', {'chaine': chaine, 'abonnés': abonnés})
