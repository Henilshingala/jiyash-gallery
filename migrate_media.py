import os
import django
from django.core.files import File

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')
django.setup()

from gallery.models import MediaItem, Section
from django.conf import settings

def run_migration():
    print("==================================================")
    print(" JIYA & SHAILESH GALLERY: Cloudinary Auto-Migration Tool ")
    print("==================================================\n")

    # 1. Migrate Section Covers
    sections = Section.objects.all()
    for s in sections:
        if s.cover_image and not s.cover_image.name.startswith(('http', 'cloudinary')):
            local_path = os.path.join(str(settings.BASE_DIR), 'media', s.cover_image.name)
            if os.path.exists(local_path):
                print(f"Uploading Cover: {s.cover_image.name}...")
                with open(local_path, 'rb') as f:
                    # Pass only the filename, Django will auto-prepend upload_to ('covers/')
                    s.cover_image.save(os.path.basename(local_path), File(f), save=True)

    # 2. Migrate Media Items
    items = MediaItem.objects.all()
    total = items.count()
    for i, item in enumerate(items, 1):
        if item.file.name.startswith(('http', 'cloudinary')):
            continue
            
        local_path = os.path.join(str(settings.BASE_DIR), 'media', item.file.name)
        if not os.path.exists(local_path):
            continue
            
        size_mb = os.path.getsize(local_path) / (1024 * 1024)
        if size_mb > 99:
            print(f"[{i}/{total}] Skipping {os.path.basename(local_path)} - over 100MB limit")
            item.delete()
            continue
            
        print(f"[{i}/{total}] Uploading {os.path.basename(local_path)}...")
        with open(local_path, 'rb') as f:
            item.file.save(os.path.basename(local_path), File(f), save=True)

    print("\nMigration Complete! 🎉")

if __name__ == "__main__":
    run_migration()
