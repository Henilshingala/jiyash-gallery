import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')
application = get_wsgi_application()

# Serve media files via WhiteNoise in production
# This makes uploaded images/videos accessible at /media/uploads/... and /media/covers/...
from whitenoise import WhiteNoise

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'

if MEDIA_ROOT.exists():
    application = WhiteNoise(application)
    application.add_files(str(MEDIA_ROOT), prefix='media/')
