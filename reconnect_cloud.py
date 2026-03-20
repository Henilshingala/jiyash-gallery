import os, django, cloudinary, cloudinary.api

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediagallery.settings')
django.setup()

from gallery.models import MediaItem, Section

cloudinary.config(cloud_name='dwakrzkzj', api_key='557847486238377', api_secret='RbAh_LBSub4ZILJFymyfh6MeIx0')

print("Fetching all Cloudinary assets...")
assets = []
next_cursor = None
while True:
    res = cloudinary.api.resources(type='upload', max_results=500, next_cursor=next_cursor)
    assets.extend(res['resources'])
    next_cursor = res.get('next_cursor')
    if not next_cursor:
        break

print(f"Found {len(assets)} assets on Cloudinary.")

cloud_map = {}
for a in assets:
    pid = a['public_id']
    # The Cloudinary Web UI typically appends a 6-character random string preceded by an underscore.
    # We will map both the strict prefix and the exact ID to be safe.
    # Ex: a['public_id'] = "WhatsApp_Image_2026-03-19_at_10.56.33_AM_p2qz9k"
    original_name = pid.rsplit('_', 1)[0].lower() if '_' in pid else pid.lower()
    full_cloud_name = f"{pid}.{a['format']}"
    
    # Store strict prefix map
    cloud_map[original_name] = full_cloud_name
    # Also store full map just in case it wasn't modified
    cloud_map[pid.lower()] = full_cloud_name


# Update MediaItems
mapped_items = 0
unmapped_items = []
for item in MediaItem.objects.all():
    # item.file.name might be "uploads/WhatsApp_Image_2026-03-19.jpeg"
    base = os.path.basename(item.file.name).rsplit('.', 1)[0].lower()
    
    # Try to find a match
    match = None
    if base in cloud_map:
        match = cloud_map[base]
    else:
        # Fallback search - checking if any public_id starts with this
        for a in assets:
            if a['public_id'].lower().startswith(base):
                match = f"{a['public_id']}.{a['format']}"
                break
                
    if match:
        MediaItem.objects.filter(id=item.id).update(file=match)
        mapped_items += 1
    else:
        unmapped_items.append(base)

# Update Sections
mapped_sections = 0
for s in Section.objects.all():
    if not s.cover_image: continue
    base = os.path.basename(s.cover_image.name).rsplit('.', 1)[0].lower()
    match = None
    if base in cloud_map:
        match = cloud_map[base]
    else:
        for a in assets:
            if a['public_id'].lower().startswith(base):
                match = f"{a['public_id']}.{a['format']}"
                break
    if match:
        Section.objects.filter(id=s.id).update(cover_image=match)
        mapped_sections += 1

print(f"\nSuccessfully re-mapped {mapped_items} Media Items and {mapped_sections} Section Covers!")
if unmapped_items:
    print(f"Failed to find cloud matches for {len(unmapped_items)} items:")
    for m in unmapped_items[:5]: print(f" - {m}")
