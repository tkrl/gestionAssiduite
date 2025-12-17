from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render
from core.models import Event, Participation
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

User = get_user_model()

def SignUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/singup.html')

@login_required
def Logout_user(request):
    logout(request)
    return redirect('home')

def Login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    """Page de profil principal"""
    user = request.user
    

    
    # Événements à venir organisés
    upcoming_organized = Event.objects.filter(
        organizer=user,
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')[:5]
    
    # Participations à venir
    upcoming_participations = Participation.objects.filter(
        participant=user,
        event__start_datetime__gte=timezone.now(),
        status='accepted'
    ).select_related('event').order_by('event__start_datetime')[:5]
    
    # Activité récente
    recent_activity = {
        'last_login': user.last_login,
        'events_created': Event.objects.filter(organizer=user).count(),
        'total_participations': Participation.objects.filter(participant=user).count(),
    }
    
    context = {
        'user_profile': user,
        'upcoming_organized': upcoming_organized,
        'upcoming_participations': upcoming_participations,
        'recent_activity': recent_activity,
        'is_own_profile': True,
    }
    
    return render(request, 'accounts/profil.html', context)

