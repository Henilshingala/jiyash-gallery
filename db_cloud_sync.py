import os
import django
import cloudinary
import cloudinary.api
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')
django.setup()

from gallery.models import MediaItem, Section

def sync_cloudinary():
    # Configure Cloudinary
    cloudinary.config(
        cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key = settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret = settings.CLOUDINARY_STORAGE['API_SECRET']
    )
    
    print("Checking Cloudinary for existing resources...")
    
    # Get all images
    images = cloudinary.api.resources(type="upload", resource_type="image", max_results=500)
    image_ids = {r['public_id'] for r in images.get('resources', [])}
    
    # Get all videos
    videos = cloudinary.api.resources(type="upload", resource_type="video", max_results=500)
    video_ids = {r['public_id'] for r in videos.get('resources', [])}
    
    all_cloud_ids = image_ids.union(video_ids)
    print(f"Found {len(all_cloud_ids)} resources on Cloudinary.")

    # Check database
    items = MediaItem.objects.all()
    deleted_count = 0
    
    for item in items:
        # Construct the expected public_id from item.file.name
        # item.file.name is usually "image/upload/v123/name.ext" or just "name.ext"
        # We need the base name without extension
        file_path = item.file.name
        # Remove any path prefix if it exists
        base_name = os.path.basename(file_path).split('.')[0]
        
        if base_name not in all_cloud_ids:
            print(f"Deleting orphaned record: {item.file.name} (ID: {item.id})")
            item.delete()
            deleted_count += 1
            
    # Also check Section covers
    sections = Section.objects.all()
    for s in sections:
        if s.cover_image:
            base_name = os.path.basename(s.cover_image.name).split('.')[0]
            if base_name not in all_cloud_ids:
                print(f"Removing missing cover from Section: {s.name}")
                s.cover_image = None
                s.save()

    print(f"Sync complete. Removed {deleted_count} orphaned records.")

if __name__ == "__main__":
    sync_cloudinary()
