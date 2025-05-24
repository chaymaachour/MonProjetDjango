from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from pannes.models import Panne

class Command(BaseCommand):
    help = "Envoie des notifications aux abonnés avec pannes non résolues depuis plus de 5 jours."

    def handle(self, *args, **kwargs):
        cinq_jours = timezone.now() - timedelta(days=5)

        pannes_en_retard = Panne.objects.filter(etat__in=["en attente", "en cours"], date_signalement__lte=cinq_jours)

        if not pannes_en_retard.exists():
            self.stdout.write("✅ Aucun abonné avec une panne non résolue depuis plus de 5 jours.")
            return

        for panne in pannes_en_retard:
            abonne = panne.abonne
            if abonne and abonne.email:
                sujet = "📢 Rappel : Panne non résolue depuis plus de 5 jours"
                message = (
                    f"Bonjour {abonne.prenom},\n\n"
                    f"Nous vous informons que votre panne signalée le {panne.date_signalement.strftime('%d-%m-%Y')} "
                    f"est toujours en cours ou en attente de résolution.\n\n"
                    f"Type de panne : {panne.get_type_panne_display()}\n"
                    f"Description : {panne.description}\n\n"
                    f"Nous nous excusons pour le délai et vous assurons que notre équipe travaille à la résoudre au plus vite.\n\n"
                    f"Merci pour votre patience."
                )

                send_mail(
                    sujet,
                    message,
                    'achourchayma321@gmail.com',  # EMAIL_HOST_USER
                    [abonne.email],
                    fail_silently=False,
                )
                self.stdout.write(f"✅ Email envoyé à {abonne.email}")

        self.stdout.write("📬 Tous les emails ont été envoyés.")
