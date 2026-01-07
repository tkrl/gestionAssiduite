#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamProject.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Vérifie si l'admin existe déjà
if not User.objects.filter(username='admin').exists():
    # Crée le superuser
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPassword123!'
    )
    print("✅ Superuser 'admin' créé avec succès !")
else:
    print("ℹ️ Superuser 'admin' existe déjà.")
