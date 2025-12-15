from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

from .models import Event, Participation

def calendar_view(request):
    """Vue principale du calendrier"""
    context = {
        'today': timezone.now(),
    }
    return render(request, 'calendar.html', context)


def events_json(request):
    """API pour récupérer les événements en JSON (pour FullCalendar)"""
    # Récupérer les paramètres de filtre
    start = request.GET.get('start')
    end = request.GET.get('end')
    filter_type = request.GET.get('filter', 'all')
    upcoming_only = request.GET.get('upcoming', False)
    
    # Construire la requête de base
    events = Event.objects.filter(status='published')
    
    # Filtrer par date si fourni
    if start and end:
        try:
            start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
            
            # Pour FullCalendar, on filtre les événements qui chevauchent la période
            events = events.filter(
                start_datetime__lt=end_date,
                end_datetime__gt=start_date
            )
        except (ValueError, TypeError):
            pass
    
    # Appliquer les filtres supplémentaires
    if filter_type == 'mine' and request.user.is_authenticated:
        events = events.filter(organizer=request.user)
    elif filter_type == 'participating' and request.user.is_authenticated:
        # Événements où l'utilisateur participe
        participating_ids = request.user.participations.filter(
            status='accepted'
        ).values_list('event_id', flat=True)
        events = events.filter(id__in=participating_ids)
    elif filter_type == 'upcoming':
        events = events.filter(start_datetime__gte=timezone.now())
    
    # Pour la vue mobile "à venir"
    if upcoming_only:
        events = events.filter(
            start_datetime__gte=timezone.now()
        ).order_by('start_datetime')[:10]
    
    # Préparer les données pour FullCalendar
    events_data = []
    for event in events:
        # Déterminer la couleur en fonction de l'utilisateur
        if request.user.is_authenticated:
            if event.organizer == request.user:
                color = '#10b981'  # Vert pour mes événements
            elif event.participations.filter(participant=request.user, status='accepted').exists():
                color = '#8b5cf6'  # Violet pour mes participations
            else:
                color = '#3b82f6'  # Bleu pour les autres
        else:
            color = '#3b82f6'  # Bleu par défaut
        
        # Événements passés en gris
        if event.is_past():
            color = '#9ca3af'
        
        events_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_datetime.isoformat(),
            'end': event.end_datetime.isoformat(),
            'location': event.location,
            'organizer': event.organizer.get_full_name() or event.organizer.username,
            'url': f'/core/events/{event.id}/',
            'backgroundColor': color,
            'borderColor': color,
            'textColor': '#ffffff',
            'extendedProps': {
                'location': event.location,
                'organizer': event.organizer.get_full_name() or event.organizer.username,
                'description': event.description[:100] + '...' if len(event.description) > 100 else event.description,
                'available_spots': event.max_participants - event.current_participants_count(),
            }
        })
    
    return JsonResponse(events_data, safe=False)


def event_detail(request, event_id):
    """Vue détaillée d'un événement"""
    event = get_object_or_404(Event, id=event_id, status='published')
    
    available_spots = event.max_participants - event.current_participants_count()
    participation_status = None
    if request.user.is_authenticated:
        participation = event.participations.filter(participant=request.user).first()
        participation_status = participation.status if participation else None
    
    context = {
        'event': event,
        'available_spots': available_spots,
        'is_organizer': request.user == event.organizer if request.user.is_authenticated else False,
        'is_participating': participation_status == 'accepted',
        'participation_status': participation_status,
    }
    
    return render(request, 'core/event_detail.html', context)


@login_required
def event_create(request):
    """Création d'un événement"""
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            location = request.POST.get('location', '')
            start_datetime_str = request.POST.get('start_datetime')
            end_datetime_str = request.POST.get('end_datetime')
            max_participants = int(request.POST.get('max_participants', 20))
            status = request.POST.get('status', 'published')
            
            # Validation des champs requis
            if not title or not start_datetime_str or not end_datetime_str:
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                return render(request, 'core/event_create.html')
            
            # Convertir les chaînes datetime en objets datetime
            # Le format datetime-local est "YYYY-MM-DDTHH:mm"
            try:
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
                # Rendre les dates timezone-aware
                start_datetime = timezone.make_aware(start_datetime)
                end_datetime = timezone.make_aware(end_datetime)
            except ValueError:
                messages.error(request, "Format de date invalide.")
                return render(request, 'core/event_create.html')
            
            # Validation: la date de fin doit être après la date de début
            if end_datetime <= start_datetime:
                messages.error(request, "La date de fin doit être après la date de début.")
                return render(request, 'core/event_create.html')
            
            # Créer l'événement
            event = Event.objects.create(
                title=title,
                description=description,
                location=location,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                max_participants=max_participants,
                organizer=request.user,
                status=status
            )
            
            messages.success(request, f"L'événement '{event.title}' a été créé avec succès!")
            return redirect('calendar')
            
        except ValueError as e:
            messages.error(request, f"Erreur dans les données saisies: {str(e)}")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la création de l'événement: {str(e)}")
    
    return render(request, 'core/event_create.html')


@login_required
def event_participate(request, event_id):
    """Permet à un utilisateur de demander/obtenir une participation à un événement"""
    event = get_object_or_404(Event, id=event_id, status='published')

    # Refuser si organisateur
    if event.organizer == request.user:
        messages.error(request, "Vous êtes l'organisateur de cet événement.")
        return redirect('event_detail', event_id=event.id)

    # Refuser si complet ou passé
    if not event.is_available():
        messages.error(request, "L'événement n'accepte plus de nouvelles participations.")
        return redirect('event_detail', event_id=event.id)

    participation, created = Participation.objects.get_or_create(
        event=event,
        participant=request.user,
        defaults={'status': 'accepted'}
    )

    if not created:
        if participation.status == 'accepted':
            messages.info(request, "Vous participez déjà à cet événement.")
        elif participation.status == 'pending':
            messages.info(request, "Votre demande de participation est déjà en attente.")
        elif participation.status == 'rejected':
            messages.warning(request, "Votre participation a été refusée par l'organisateur.")
        elif participation.status == 'cancelled':
            # Reactiver si de la place
            if event.is_available():
                participation.status = 'accepted'
                participation.save(update_fields=['status'])
                messages.success(request, "Votre participation a été réactivée.")
            else:
                messages.error(request, "Plus de places disponibles.")
        else:
            messages.info(request, "Statut de participation inchangé.")
    else:
        messages.success(request, "Votre participation a été enregistrée.")

    return redirect('event_detail', event_id=event.id)


def event_qrcode(request, event_id):
    """Génère un QR code pour l'événement"""
    if not QRCODE_AVAILABLE:
        messages.error(request, "La génération de QR code n'est pas disponible. Veuillez installer le package 'qrcode'.")
        return redirect('event_detail', event_id=event_id)
    
    event = get_object_or_404(Event, id=event_id, status='published')
    
    # Construire l'URL complète de l'événement
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    
    host = request.get_host()
    event_url = f"{protocol}://{host}/core/events/{event.id}/"
    
    # Créer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(event_url)
    qr.make(fit=True)
    
    # Créer l'image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir en réponse HTTP
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response