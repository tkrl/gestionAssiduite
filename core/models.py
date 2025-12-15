
# Create your models here.
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta

class Event(models.Model):
    """Modèle pour les événements du calendrier"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]
    
    # Informations de base
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description", blank=True)
    location = models.CharField(max_length=200, verbose_name="Lieu", blank=True)
    
    # Dates et heures
    start_datetime = models.DateTimeField(verbose_name="Date et heure de début")
    end_datetime = models.DateTimeField(verbose_name="Date et heure de fin")
    
    # Capacité
    max_participants = models.PositiveIntegerField(
        verbose_name="Nombre maximum de participants",
        default=20,
        validators=[MinValueValidator(1)]
    )
    
    # Organisation
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
        verbose_name="Organisateur"
    )
    
    # Statut
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published',
        verbose_name="Statut"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['start_datetime']
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['organizer']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%d/%m/%Y %H:%M')}"
    
    # Méthodes utilitaires
    def is_past(self):
        """Vérifie si l'événement est passé"""
        return self.end_datetime < timezone.now()
    
    def is_ongoing(self):
        """Vérifie si l'événement est en cours"""
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime
    
    def is_upcoming(self):
        """Vérifie si l'événement est à venir"""
        return self.start_datetime > timezone.now()
    
    def duration(self):
        """Calcule la durée de l'événement"""
        return self.end_datetime - self.start_datetime
    
    def is_available(self):
        """Vérifie si l'événement accepte encore des inscriptions"""
        return (
            self.status == 'published' 
            and not self.is_past()
            and self.current_participants_count() < self.max_participants
        )
    
    def current_participants_count(self):
        """Compte le nombre de participants acceptés"""
        return self.participations.filter(status='accepted').count()
    
    def save(self, *args, **kwargs):
        # Validation de cohérence des dates
        if self.end_datetime <= self.start_datetime:
            from django.core.exceptions import ValidationError
            raise ValidationError("La date de fin doit être après la date de début")
        super().save(*args, **kwargs)


class Participation(models.Model):
    """Modèle pour les participations aux événements"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
        ('cancelled', 'Annulé'),
    ]
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name="Événement"
    )
    
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name="Participant"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    
    comments = models.TextField(blank=True, verbose_name="Commentaires")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = ['event', 'participant']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.participant} - {self.event}"