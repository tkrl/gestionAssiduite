from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
from core.models import Event

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée des événements de test pour le calendrier'

    def handle(self, *args, **kwargs):
        # Créer un utilisateur de test s'il n'existe pas
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Jean',
                'last_name': 'Dupont'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Utilisateur de test créé'))

        # Noms d'événements de test
        event_titles = [
            "Formation Django Avancé",
            "Réunion d'équipe hebdomadaire",
            "Atelier de développement web",
            "Présentation du projet Q4",
            "Session de code review",
            "Formation sécurité informatique",
            "Brainstorming nouveaux produits",
            "Conférence sur l'IA",
            "Workshop Tailwind CSS",
            "Meetup développeurs locaux",
            "Séminaire gestion de projet",
            "Entraînement présentation",
            "Révision stratégique",
            "Planning sprint suivant",
            "Formation PostgreSQL",
        ]

        # Lieux de test
        locations = [
            "Salle de conférence A",
            "Bureau 201",
            "Espace coworking",
            "Amphithéâtre principal",
            "Salle de réunion virtuelle",
            "Cafétéria",
            "Lab informatique",
            "Salle de formation",
            "Online (Zoom)",
            "Google Meet",
        ]

        # Supprimer les anciens événements de test
        Event.objects.filter(organizer=user).delete()

        # Créer des événements pour les 30 prochains jours
        today = timezone.now()
        events_created = 0

        for i in range(15):  # Créer 15 événements
            # Date aléatoire dans les 30 prochains jours
            days_ahead = random.randint(0, 30)
            start_date = today + timedelta(days=days_ahead)
            
            # Heure de début entre 8h et 18h
            start_hour = random.randint(8, 18)
            start_datetime = start_date.replace(
                hour=start_hour,
                minute=random.choice([0, 15, 30, 45]),
                second=0,
                microsecond=0
            )
            
            # Durée entre 1 et 3 heures
            duration_hours = random.randint(1, 3)
            end_datetime = start_datetime + timedelta(hours=duration_hours)
            
            # Créer l'événement
            event = Event.objects.create(
                title=random.choice(event_titles),
                description=f"Description de l'événement {i+1}. Ceci est un événement de test créé automatiquement pour démontrer le fonctionnement du calendrier.",
                location=random.choice(locations),
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                max_participants=random.randint(10, 50),
                organizer=user,
                status='published'
            )
            
            events_created += 1
            self.stdout.write(f"✓ Événement créé: {event.title} le {start_datetime.strftime('%d/%m/%Y à %H:%M')}")

        self.stdout.write(self.style.SUCCESS(f'{events_created} événements de test créés avec succès!'))