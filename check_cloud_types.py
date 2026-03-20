import cloudinary, cloudinary.api
cloudinary.config(cloud_name='dwakrzkzj', api_key='557847486238377', api_secret='RbAh_LBSub4ZILJFymyfh6MeIx0')

print("--- Images ---")
res_images = cloudinary.api.resources(resource_type='image', type='upload', max_results=20)
for r in res_images.get('resources', []):
    print(f"ID: {r['public_id']} | Format: {r['format']}")

print("\n--- Videos ---")
res_videos = cloudinary.api.resources(resource_type='video', type='upload', max_results=20)
for r in res_videos.get('resources', []):
    print(f"ID: {r['public_id']} | Format: {r['format']}")
