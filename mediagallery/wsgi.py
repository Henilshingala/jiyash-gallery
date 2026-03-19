import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')

application = get_wsgi_application()

try:
    application = WhiteNoise(application)
    application.add_files(str(MEDIA_ROOT), prefix='media/')
