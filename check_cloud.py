import cloudinary, cloudinary.api
cloudinary.config(cloud_name='dwakrzkzj', api_key='557847486238377', api_secret='RbAh_LBSub4ZILJFymyfh6MeIx0')
res = cloudinary.api.resources(type='upload', max_results=20, direction='desc')
print("Recent uploads from Cloudinary:")
for r in res.get('resources', []):
    print("ID:", r['public_id'], "| Format:", r.get('format', 'none'), "| Folder:", r.get('folder', 'Root'))
