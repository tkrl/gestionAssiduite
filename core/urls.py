from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events/json/', views.events_json, name='events_json'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/participate/', views.event_participate, name='event_participate'),
    path('events/<int:event_id>/qrcode/', views.event_qrcode, name='event_qrcode'),
    path('events/create/', views.event_create, name='event_create'),
]