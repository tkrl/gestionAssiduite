import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamProject.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Vérifie si admin existe
if not User.objects.filter(username='admin').exists():
    # Crée le superuser
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPassword123!'
    )
    print("✅ Superuser 'admin' créé avec succès!")
    print("🔑 Identifiants : admin / AdminPassword123!")
else:
    print("ℹ️ Superuser 'admin' existe déjà.")
