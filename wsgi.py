import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamProject.settings')

application = get_wsgi_application()

# Pour WhiteNoise
from whitenoise import WhiteNoise
application = WhiteNoise(application, root='staticfiles')