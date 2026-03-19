import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')

application = get_wsgi_application()

try:
    application = WhiteNoise(application)
except Exception as e:
    print(f"WhiteNoise warning: {e}")
