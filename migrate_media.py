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
    print(" LUMINARY GALLERY: Cloudinary Auto-Migration Tool ")
    print("==================================================\n")
    print("Please keep this window open until everything finishes.\n")

    # 1. Migrate Section Covers
    sections = Section.objects.all()
    print(f"Checking {sections.count()} sections for covers...")
    for s in sections:
        if s.cover_image and not s.cover_image.name.startswith(('http', 'cloudinary')):
            local_path = os.path.join(str(settings.BASE_DIR), 'media', s.cover_image.name)
            if os.path.exists(local_path):
                print(f"  Uploading Cover: {s.cover_image.name}")
                try:
                    with open(local_path, 'rb') as f:
                        s.cover_image.save(s.cover_image.name, File(f), save=True)
                except Exception as e:
                    print(f"  ! Error uploading {s.cover_image.name}: {e}")

    # 2. Migrate Media Items
    items = MediaItem.objects.all()
    total = items.count()
    print(f"\nChecking {total} Media Items for migration...")
    
    skipped_videos = []
    
    for i, item in enumerate(items, 1):
        # If it's already a cloud link, skip
        if item.file.name.startswith(('http', 'cloudinary')):
            continue
            
        local_path = os.path.join(str(settings.BASE_DIR), 'media', item.file.name)
        if not os.path.exists(local_path):
            print(f"[{i}/{total}] SKIP: File missing locally: {item.file.name}")
            continue
            
        # Check size limit for free Cloudinary tier (Max 100MB)
        size_mb = os.path.getsize(local_path) / (1024 * 1024)
        if size_mb > 99:
            print(f"[{i}/{total}] SKIP & DELETE: {item.file.name} is {size_mb:.1f}MB (over 100MB limit)")
            skipped_videos.append(item.file.name)
            item.delete()
            continue
            
        print(f"[{i}/{total}] Uploading {item.file.name} ({size_mb:.1f}MB)...")
        try:
            with open(local_path, 'rb') as f:
                # This uploads securely to Cloudinary and saves the URL in the database natively!
                item.file.save(item.file.name, File(f), save=True)
        except Exception as e:
            print(f"  ! Error uploading: {e}")

    print("\n==================================================")
    print(" Migration Complete! 🎉")
    print("==================================================")
    if skipped_videos:
        print(f"Deleted {len(skipped_videos)} videos because they were too large (>100MB):")
        for v in skipped_videos:
            print(f" - {v}")
    print("\nNext steps:")
    print("1. Delete the local 'media' folder completely.")
    print("2. Commit and push everything to GitHub.")
    print("3. Render will deploy successfully!")

if __name__ == "__main__":
    run_migration()
