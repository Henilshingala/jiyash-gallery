import os
import django
import cloudinary
import cloudinary.api
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')
django.setup()

cloudinary.config(
    cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key = settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret = settings.CLOUDINARY_STORAGE['API_SECRET']
)

print("--- Images ---")
res = cloudinary.api.resources(resource_type="image", max_results=20)
for r in res.get('resources', []):
    print(f"Public ID: {r['public_id']} | Type: {r['resource_type']}")

print("\n--- Videos ---")
res = cloudinary.api.resources(resource_type="video", max_results=20)
for r in res.get('resources', []):
    print(f"Public ID: {r['public_id']} | Type: {r['resource_type']}")
